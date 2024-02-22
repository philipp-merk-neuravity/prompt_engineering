import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential, wait_random_exponential, stop_after_attempt, wait_fixed, before_sleep_log
import time
import logging

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

client = AsyncOpenAI(
    api_key=openai_api_key
)

@retry(wait=wait_random_exponential(min=1, max=180), stop=stop_after_attempt(6))
async def get_completion(
    messages,
    temperature=0.0,
    model="gpt-3.5-turbo",
    max_tokens=4095,
    response_format="text"
):
    start_time = time.time()  # Start time measurement
    completion = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        timeout=45,
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        response_format={"type": response_format}
    )
    duration = time.time() - start_time  # Calculate duration
    return (
        completion.choices[0].message.content,
        completion.usage.prompt_tokens,
        completion.usage.completion_tokens,
        duration
    )


def create_system_message(template, **kwargs):
    return {"role": "system", "content": template.format(**kwargs)}

def create_user_message(template, **kwargs):
    return {"role": "user", "content": template.format(**kwargs)}

def create_ai_message(template, **kwargs):
    return {"role": "assistant", "content": template.format(**kwargs)}
    