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

from dotenv import load_dotenv
load_dotenv(".env", override=True)


import sys



sys.path.append('/Users/aziz/Documents/repos/restaurant-bot/src/restaurant_agent')
import evaluation_obs as e
import agent
import prompts
import config
import pytest
from typing import List, Any
from langsmith import testing as t



def format_messages_string(messages: List[Any]) -> str:
    """Format messages into a single string for analysis."""
    return '\n'.join(message.pretty_repr() for message in messages)


class CriteriaGrade(BaseModel):
    """Score the response against specific criteria."""

    grade: bool = Field(description="Does the response meet the provided criteria?")
    justification: str = Field(description="The justification for the grade and score")

criteria_eval_llm = init_chat_model(config.EVALUATOR_MODEL)
criteria_eval_structured_llm = criteria_eval_llm.with_structured_output(CriteriaGrade)

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


@pytest.mark.langsmith(output_keys=["criteria"])
# Variable names and a list of tuples with the test cases
# Each test case is (req, success_criteria)
@pytest.mark.parametrize("req, success_criteria",create_response_test_cases())
def test_response_criteria_evaluation(req, success_criteria):
    """Test if a response meets the specified criteria.
    """
    # Log minimal inputs for LangSmith
    t.log_inputs({"module": "agent e2e", "test": "test_response_criteria_evaluation"})
    
    # Set up the assistant
    email_assistant = agent.app
    
    # Run the agent        
    msg = {"messages": [{"role": "user", "content": req}]}
    config = {"configurable": {"thread_id": str(req)}}
    result = agent.app.invoke(msg, config)
    all_messages_str = format_messages_string(result['messages'])
    
    # Evaluate against criteria
    eval_result = criteria_eval_structured_llm.invoke([
        {"role": "system",
            "content": prompts.RESPONSE_CRITERIA_SYSTEM_PROMPT},
        {"role": "user",
            "content": f"""\n\n Response criteria: {success_criteria} \n\n Assistant's response: \n\n {all_messages_str} \n\n Evaluate whether the assistant's response meets the criteria and provide justification for your evaluation."""}
    ])

    # Log feedback response
    t.log_outputs({
        "justification": eval_result.justification,
        "response": all_messages_str,
    })
        
    # Pass feedback key
    assert eval_result.grade

# LANGSMITH_TEST_SUITE='Kese assistant: Test e2e' pytest tests/test_e2e.py
