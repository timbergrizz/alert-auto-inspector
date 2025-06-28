import openai
from core.config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL
from models.canonical import CanonicalAlert

client = openai.OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)

def get_explanation(alert: CanonicalAlert) -> str:
    prompt = f"""
    You are an on-call engineering assistant with senior experience. Your job is to explain a technical monitoring alert for a notification channel.
    give a detailed report of the alert as possible by given data for user to understand as fast as possible. inspect and investigate the circumstances with given tools.
    You MUST given what you have investigated and what you have found.

    Here is the alert data in a structured format:
    - Service: {alert.service_name}
    - Severity: {alert.severity}
    - Title: {alert.title}
    - Description: {alert.description}
    - Affected Entity: {alert.entity}

    Based on this information, provide a structured report of what is happening.
    """

    response = client.chat.completions.create(
        model=LLM_MODEL, # or "gpt-4"
        messages=[
            {"role": "system", "content": "You are an on-call engineering assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
