import json
import re
from typing import TypedDict, Optional, List, Dict, Any
import os 
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import json, re, time, random
from typing import Annotated, Sequence
from langgraph.graph.message import add_messages

from langchain_core.messages import (
    AIMessage,
    ToolMessage,
    BaseMessage,
    SystemMessage,

)
from langchain.chat_models import init_chat_model
import app.tools as tools
import app.prompts as prompts

load_dotenv()



def _get_role(m: Any) -> Optional[str]:
    if isinstance(m, dict):
        return m.get("role") or m.get("type")
    try:
        return getattr(m, "type", None) or getattr(m, "role", None)
    except Exception:
        return None


def trim_by_turns(msgs: List[Any], keep_last_turns: int = 10) -> List[Any]:
    """
    Обрезает историю по ходам, где ход начинается с human/user.
    Сохраняет типы элементов как есть (dict или BaseMessage).
    """
    if not msgs:
        return msgs

    prefix = []
    i = 0
    while i < len(msgs) and _get_role(msgs[i]) in ("system",):
        prefix.append(msgs[i])
        i += 1
    tail = msgs[i:]

    turns, current = [], []
    for m in tail:
        role = _get_role(m)
        if role in ("human", "user") and current:
            turns.append(current)
            current = [m]
        else:
            current.append(m)
    if current:
        turns.append(current)

    trimmed = turns[-keep_last_turns:]
    flat = [m for turn in trimmed for m in turn]

    while flat and _get_role(flat[0]) == "tool":
        flat.pop(0)

    return prefix + flat


class TruncatingInMemorySaver(InMemorySaver):
    def __init__(self, keep_last: int = 12):
        super().__init__()
        self.keep_last = int(keep_last)

    def put(self, *args, **kwargs):
        # попытаться достать checkpoint из kwargs или позиционно
        checkpoint = kwargs.get("checkpoint", None)
        if checkpoint is None and len(args) >= 2:
            checkpoint = args[1]  # обычно: (config, checkpoint, ...)

        if isinstance(checkpoint, dict):
            self._truncate_checkpoint(checkpoint)

        # передаём дальше без изменений сигнатуры
        return super().put(*args, **kwargs)

    def _truncate_checkpoint(self, checkpoint: Dict[str, Any]) -> None:
        """
        Обрезает историю сообщений до self.keep_last.
        Разные версии LangGraph складывают их по-разному, поэтому пробуем несколько путей.
        """
        # 1) writes.messages
        writes = checkpoint.get("writes")
        if isinstance(writes, dict):
            msgs = writes.get("messages")
            if isinstance(msgs, list):
                msgs = trim_by_turns(msgs, keep_last_turns=self.keep_last)
                writes["messages"] = msgs
                checkpoint["writes"] = writes

        # 2) channel_values.messages
        ch_vals = checkpoint.get("channel_values")
        if isinstance(ch_vals, dict):
            msgs = ch_vals.get("messages")
            if isinstance(msgs, list):
                msgs = trim_by_turns(msgs, keep_last_turns=self.keep_last)
                ch_vals["messages"] = msgs
                checkpoint["channel_values"] = ch_vals

        # 3) values.messages (встречается в старых/альтернативных путях)
        values = checkpoint.get("values")
        if isinstance(values, dict):
            msgs = values.get("messages")
            if isinstance(msgs, list):
                msgs = trim_by_turns(msgs, keep_last_turns=self.keep_last)
                values["messages"] = msgs
                checkpoint["values"] = values

# ----------------------------------------------------------

AGENT_MODEL = os.getenv("AGENT_MODEL", "openai:llama4scout")

class AgentState(TypedDict):
    # messages: List[BaseMessage] # List of messages
    messages: Annotated[Sequence[BaseMessage], add_messages]
    next_tool: Optional[str]
    tool_args: Optional[dict]
    final_answer_ready: bool

LLM_ROUTER_PROMPT = prompts.LLM_ROUTER_PROMPT
FINAL_ANSWER_PROMPT = prompts.FINAL_ANSWER_PROMPT


# ---- РЕЕСТР ТУЛОВ (важно: ключ = имя в JSON от роутера)
TOOL_REGISTRY = prompts.TOOL_REGISTRY

# ---- МОДЕЛИ
llm = init_chat_model(AGENT_MODEL, temperature=0, model_kwargs={"response_format": {"type": "json_object"}})
llm_final_answer = init_chat_model(AGENT_MODEL, temperature=0)


system_msg_router = SystemMessage(content=LLM_ROUTER_PROMPT)
system_msg_final = SystemMessage(content=FINAL_ANSWER_PROMPT)


def llm_router(state: AgentState) -> AgentState:
    msgs = [m for m in state["messages"] if not isinstance(m, SystemMessage)]
    msgs.insert(0, system_msg_router)

    response: AIMessage = llm.invoke(msgs)
    content = (response.content or "").strip()

    m = re.search(r"\{.*\}", content, flags=re.DOTALL)
    json_str = m.group(0) if m else content

    try:
        parsed = json.loads(json_str)
    except Exception as e:
        raise ValueError(f"Router must return strict JSON. Parse error: {e}\nRaw:\n{content}")

    decision = parsed.get("decision", "").strip().lower()
    if decision == "final":
        return {
            "messages": state["messages"],
            "next_tool": None,
            "tool_args": None,
            "final_answer_ready": True,
        }

    if decision != "tool":
        raise ValueError(f"Router returned unknown decision: {parsed!r}")

    next_tool: str = parsed["next_tool"]
    tool_args: dict = parsed.get("tool_args", {}) or {}
    tool_call_id = str(parsed.get("tool_call_id") or f"call_{int(time.time()*1000)}_{random.randint(1000,9999)}")

    ai_with_tool_call = AIMessage(
        content="",
        tool_calls=[{
            "id": tool_call_id,
            "name": next_tool,
            "args": tool_args
        }]
    )

    return {
        "messages": [ai_with_tool_call],
        "next_tool": next_tool,
        "tool_args": tool_args,
        "final_answer_ready": False,
    }



def tool_executor(state: AgentState) -> AgentState:
    last_msg = state["messages"][-1]
    if not isinstance(last_msg, AIMessage) or not getattr(last_msg, "tool_calls", None):
        # Это логическая ошибка в графе: tool_executor должен вызываться
        # только после решения роутера "decision: tool".
        raise ValueError("tool_executor: expected AIMessage with tool_calls from router")

    tool_outputs: List[ToolMessage] = []
    # Переход в финал теперь РЕШАЕТСЯ ТОЛЬКО роутером, поэтому всегда False
    final_answer_ready = False

    for call in last_msg.tool_calls:
        tool_name = (call.get("name") or "").strip()
        tool_args = call.get("args") or {}
        call_id = call.get("id")

        if not call_id:
            raise ValueError(f"tool_executor: tool call missing id: {call}")

        tool_obj = TOOL_REGISTRY.get(tool_name)
        if not tool_obj:
            result = f"[ERROR] Tool `{tool_name}` not found."
        else:
            try:
                result = tool_obj(**tool_args)
            except Exception as e:
                result = f"[ERROR] Tool execution failed: {str(e)}"

        tool_outputs.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call_id,
                name=tool_name,
            )
        )

    return {
        "messages": tool_outputs,
        "next_tool": None,
        "tool_args": None,
        "final_answer_ready": final_answer_ready, 
    }


def route(state: AgentState) -> str:
    return "final_answer" if state["final_answer_ready"] else "tool_executor"


def final_answer_node(state: AgentState) -> AgentState:
    msgs = [m for m in state["messages"] if not isinstance(m, SystemMessage)]
    msgs.insert(0, system_msg_final)

    response: AIMessage = llm_final_answer.invoke(msgs)
    return {
        **state,
        "messages": [response]
    }


def build_agent_with_router():
    workflow = StateGraph(AgentState)

    workflow.add_node("llm_router", llm_router)
    workflow.add_node("tool_executor", tool_executor)
    workflow.add_node("final_answer", final_answer_node)

    workflow.add_edge(START, "llm_router")
    workflow.add_conditional_edges("llm_router", route, {
        "tool_executor": "tool_executor",
        "final_answer": "final_answer",
    })
    workflow.add_edge("tool_executor", "llm_router")
    workflow.add_edge("final_answer", END)

    checkpointer = InMemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    return app
