from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

client = OpenAI(
    api_key=openai_api_key
)

def get_completion(
    messages,
    temperature=0.0,
    model="gpt-3.5-turbo",
    max_tokens=4095,
    response_format="text"
):
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        timeout=10,
        max_tokens=max_tokens,
        top_p=0.95,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        response_format={"type": response_format}
    )
    return (
        completion.choices[0].message.content,
        completion.usage.prompt_tokens,
        completion.usage.completion_tokens
    )


current_model = 'gpt-3.5-turbo'

current_messages = [
    {
        'role': 'system', 
        'content': 'You will be given a task, a function implementation and a series of unit tests. First, write a few sentences to explain why the previous implementation is wrong as indicated by the tests. Then, create a new implementation that passes all the tests. Add the full function signature to your implementation and imports if necessary. Write your answer in json format: {"reflection": "", "implementation": ""}'
    }, 
    {
        'role': 'user', 
        'content': 'from typing import List\n\n\ndef separate_paren_groups(paren_string: str) -> List[str]:\n    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to\n    separate those group into separate strings and return the list of those.\n    Separate groups are balanced (each open brace is properly closed) and not nested within each other\n    Ignore any spaces in the input string.\n    >>> separate_paren_groups(\'( ) (( )) (( )( ))\')\n    [\'()\', \'(())\', \'(()())\']\n    """'
    }
]

print(get_completion(current_messages, model=current_model, response_format="json_object"))