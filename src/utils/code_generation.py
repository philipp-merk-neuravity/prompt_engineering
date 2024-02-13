import re
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from utils.data_conversion import convert_tests_to_list, parse_code_solution

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
model = ChatOpenAI(model="gpt-3.5-turbo", api_key=openai_api_key)

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

output_parser = StrOutputParser()

def gen_function(prompt_template_for_code_generation: str, function_signature: str) -> str:
    formatted_function_signature = {"function_signature": function_signature}
    chain = prompt_template_for_code_generation | model | output_parser | parse_code_solution
    return chain.invoke({"function_signature": formatted_function_signature})

def gen_tests(prompt_template_for_test_generation: str, function_signature: str) -> str:
    formatted_function_signature = {"function_signature": function_signature}
    chain = prompt_template_for_test_generation | model | output_parser | convert_tests_to_list
    return chain.invoke({"function_signature": formatted_function_signature})