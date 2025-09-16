#!/usr/bin/env python

import uuid
import importlib
import sys
from httpx import request
import pytest
from typing import Dict, List, Any, Tuple
from pydantic import BaseModel, Field
from langchain.chat_models import init_chat_model

from langsmith import testing as t

from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command
import os
from dotenv import load_dotenv

load_dotenv(".env", override=True)


sys.path.append("/Users/aziz/Documents/repos/shai-hackathon")
import evaluation_obs as e
import app.agent as agent
import app.prompts as prompts


graph = agent.build_agent_with_router()

def format_messages_string(messages: List[Any]) -> str:
    """Format messages into a single string for analysis."""
    return "\n".join(message.pretty_repr() for message in messages)


class CriteriaGrade(BaseModel):
    """Score the response against specific criteria."""

    grade: bool = Field(description="Does the response meet the provided criteria?")
    justification: str = Field(description="The justification for the grade and score")


def create_response_test_cases():
    """Create test cases for parametrized criteria evaluation with LangSmith.
    Only includes emails that require a response (triage_output == "respond").
    These are more relevant / interesting for testing tool calling / response quality.
    """

    test_cases = []
    for req, criteria in zip(e.reqsuests, e.criterias):
        test_cases.append((req, criteria))
    print(f"Created {len(test_cases)} test cases")
    return test_cases

# Агент
# agent_model = os.getenv("AGENT_MODEL")
# agent_api_base = os.getenv("AGENT_API_BASE")
# agent_api_key = os.getenv("AGENT_API_KEY")
# agent_llm = init_chat_model(
#     agent_model,
#     openai_api_base=agent_api_base,
#     openai_api_key=agent_api_key,
# )

# Оценщик
evaluator_model = os.getenv("EVALUATOR_MODEL")
evaluator_api_base = os.getenv("EVALUATOR_API_BASE")
evaluator_api_key = os.getenv("EVALUATOR_API_KEY")
criteria_eval_llm = init_chat_model(
    evaluator_model,
    openai_api_base=evaluator_api_base,
    openai_api_key=evaluator_api_key,
)
criteria_eval_structured_llm = criteria_eval_llm.with_structured_output(CriteriaGrade)

@pytest.mark.langsmith(output_keys=["criteria"])
@pytest.mark.parametrize("req, success_criteria", create_response_test_cases())
def test_response_criteria_evaluation(req, success_criteria):
    """Test if a response meets the specified criteria."""
    t.log_inputs({"module": "agent e2e", "test": "test_response_criteria_evaluation"})


    # Run the agent
    msg = {"messages": [{"role": "user", "content": req}]}
    config = {"configurable": {"thread_id": str(req)}}
    result = graph.invoke(msg, config)
    all_messages_str = format_messages_string(result["messages"])

    eval_result = criteria_eval_structured_llm.invoke(
        [
            {"role": "system", "content": prompts.RESPONSE_CRITERIA_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""\n\n Response criteria: {success_criteria} \n\n Assistant's response: \n\n {all_messages_str} \n\n Evaluate whether the assistant's response meets the criteria and provide justification for your evaluation.""",
            },
        ]
    )

    t.log_outputs(
        {
            "justification": eval_result.justification,
            "response": all_messages_str,
        }
    )

    assert eval_result.grade


# LANGSMITH_TEST_SUITE='SHAI / DSK assistant: Test e2e' pytest tests/test_e2e.py
