from openai import OpenAI
import os
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

client = OpenAI(
    api_key=openai_api_key
)

@retry(wait=wait_random_exponential(min=1, max=180), stop=stop_after_attempt(6))
def get_completion(messages, temperature=0.0, model="gpt-3.5-turbo", max_tokens=1024):
    print("Attempting to get completion...")
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        timeout=45,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    return completion.choices[0].message.content

def create_system_message(template, **kwargs):
    return {"role": "system", "content": template.format(**kwargs)}

def create_user_message(template, **kwargs):
    return {"role": "user", "content": template.format(**kwargs)}

def create_ai_message(template, **kwargs):
    return {"role": "assistant", "content": template.format(**kwargs)}

    