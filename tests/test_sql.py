import sys
from typing import List, Any
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)
import tests.evaluation_obs_sql as e_sql

sys.path.append("/Users/aziz/Documents/repos/shai-hackathon")
import app.agent as agent
import app.prompts as prompts


def format_messages_string(messages: List[Any]) -> str:
    """Format messages into a single string for analysis."""
    return "\n".join(message.pretty_repr() for message in messages)

evaluator_model = os.getenv("EVALUATOR_MODEL")
evaluator_api_base = os.getenv("EVALUATOR_API_BASE")
evaluator_api_key = os.getenv("EVALUATOR_API_KEY")


class SQLEvaluation(BaseModel):
    """Evaluation of candidate SQL against golden SQL across two criteria: execution accuracy and exact match."""

    exec_accuracy: bool = Field(
        description="Does the candidate SQL produce the same result as the golden SQL (ignoring syntax/formatting differences)?"
    )
    exec_accuracy_justification: str = Field(
        description="Explain why the candidate SQL does or does not produce the same result."
    )

    exact_match: bool = Field(
        description="Is the candidate SQL textually identical to the golden SQL (ignoring whitespace and capitalization)?"
    )
    exact_match_justification: str = Field(
        description="Explain why the candidate SQL matches or differs from the golden SQL text."
    )



if __name__ == "__main__":
    
    test_cases = []
    for req, criteria in zip(e_sql.sql_reqsuests, e_sql.sql_answers):
        test_cases.append((req, criteria))

    graph = agent.build_agent_with_router()
    
    criteria_eval_llm = init_chat_model(
        evaluator_model,
        openai_api_base=evaluator_api_base,
        openai_api_key=evaluator_api_key,
    )
    criteria_eval_structured_llm = criteria_eval_llm.with_structured_output(SQLEvaluation)

    eval_results = []


    for test_case in test_cases:
        req = test_case[0]
        golden_sql = test_case[1]

        msg = {"messages": [{"role": "user", "content": req}]}
        config = {"configurable": {"thread_id": str(req)}}

        result = graph.invoke(msg, config)
        all_messages_str = format_messages_string(result["messages"])

        eval_result = criteria_eval_structured_llm.invoke(
            [
                {"role": "system", "content": prompts.RESPONSE_CRITERIA_SYSTEM_PROMPT_SQL},
                {
                    "role": "user",
                    "content": f"""\n\n Request: {req}
                                Tool calls: \n\n {all_messages_str} 
                                \n\n Golden SQL: {golden_sql} \n\n 
                    Evaluate whether the assistant's response meets the criteria and provide justification for your evaluation.""",
                },
            ]
        )
        eval_results.append(eval_result)

        print([e.exec_accuracy for e in eval_results])
        print([e.exact_match for e in eval_results])