import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file


try:
    args = sys.argv[1:]
    textInput = args[0]
except Exception as e:
    print("ERROR BIG BOY")
    sys.exit(1)


systemPrompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [
            types.Content(role="user", parts=[types.Part(text=textInput)]),
            ]

    response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=systemPrompt
                ),
            )
    
    userPrompt = args[0]
    promptTokens = response.usage_metadata.prompt_token_count
    responseTokens = response.usage_metadata.candidates_token_count


    if "--verbose" in args:
        print(f"User prompt: {textInput}")
        print(f"Prompt tokens: {promptTokens}")
        print(f"Response tokens: {responseTokens}")
    
    if response.function_calls is None:
        print(response.text)
    else:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")

if __name__ == '__main__':
    main()
