import openai
import json
from core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from models.canonical import CanonicalAlert
from core.tools import search_knowledge_base

client = openai.OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Searches the knowledge base for a given query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query to search for in the knowledge base."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

def get_plan(alert: CanonicalAlert) -> list:
    prompt = f"""
    Alert Details:
    - Service: {alert.service}
    - Severity: {alert.severity}
    - Title: {alert.title}

    Based on this, generate an investigation plan. You can use the available tools to gather more information.
    """

    messages = [
        {"role": "system", "content": """
            You are a senior on-call engineer. You have received the following alert.
            Your task is to analyze the alert and create a concise, step-by-step plan for investigation.
            The plan should guide another engineer on what to check to diagnose the problem.
            Focus on concrete actions, like which logs to check, which metrics to look at, or which systems to inspect.
            You can use the available tools to gather more information.
            """},
        {"role": "user", "content": prompt}
    ]

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.2,
    )

    response_message = response.choices[0].message
    messages.append(response_message)

    tool_calls = response_message.tool_calls
    if tool_calls:
        available_functions = {
            "search_knowledge_base": search_knowledge_base,
        }
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(function_response),
                }
            )
        second_response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=messages,
        )
        messages.append(second_response.choices[0].message)

    return messages

def generate_response(alert: CanonicalAlert, context_documents: list = None, plan: list = None) -> str:
    prompt = f"""
    Here is the information gathered:

    **Alert Data:**
    - Service: {alert.service}
    - Severity: {alert.severity}
    - Title: {alert.title}

    **Investigation Plan and Execution:**
    {plan if plan else "No plan was generated."}

    **Knowledge Base Context:**
    {context_documents if context_documents else "No context was found."}

    Now, please generate the final report.
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": """
                You are a senior on-call engineering assistant. Your role is to provide a comprehensive report based on a monitoring alert and subsequent investigation.
                You have been given an alert, an investigation plan, and some context from a knowledge base.
                Synthesize all this information into a clear, structured report for an engineer.

                The final report should include:
                1. A summary of the alert.
                2. The investigation plan that was followed and the results of any tool calls.
                3. Key findings from the knowledge base context.
                4. A concluding summary of the situation.
                """},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content