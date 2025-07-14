import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file

from functions.call_function import call_function

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

    messages = []
    active = True

    print('''
A simple AI agent using Gemini.

Use "--help" for a little more information.
    ''')

    while active is True:
        userInput = input("AI Agent:")
        verbose = "--verbose" in userInput
        help = "--help" in userInput
        conclude = userInput == "--exit" or userInput == "exit"
        concludeFailsafe = "--exit" in userInput and userInput != "--exit"
        words = [word for word in userInput.split() if not word.startswith('--')]
        textInput = " ".join(words)
        if conclude:
            textInput = "exit"


        messages.append(
            types.Content(role="user", parts=[types.Part(text=textInput)]),
        )

        for i in range(20):
            if help:
                print('''
The AI agent utilizes 'gemini-2.0-flash-001' and is able to:

- Read directories
- Read file contents
- Create files and directories
- Rewrite existing files
- Run Python files

It's working directory can be set in the "config" file. Be mindful this isn't the best model out 
there, so maybe dont give it access to something important.

--help      Displays this message.
--exit      Must be used on it's own, exit's the program.
--verbose   Displays additional information.
                ''')
                break

            if conclude:
                print('''
Exiting Agent.
                ''')
                sys.exit(0)

            if concludeFailsafe:
                print('''
Use just "--exit". Helps to avoid accidentally exiting if we didn't wish to
                      ''')
                break

            try:
                response = client.models.generate_content(
                    model='gemini-2.0-flash-001',
                    contents=messages,
                    config=types.GenerateContentConfig(
                        tools=[available_functions],
                        system_instruction=systemPrompt
                    ),
                )
                
                promptTokens = response.usage_metadata.prompt_token_count
                responseTokens = response.usage_metadata.candidates_token_count

                for i in response.candidates:
                    messages.append(i.content)

                if verbose:
                    print(f"User prompt: {textInput}")
                    print(f"Prompt tokens: {promptTokens}")
                    print(f"Response tokens: {responseTokens}")

                if response.function_calls is None:
                    print(response.text)
                    break
                else:
                    if verbose:
                        try:
                            function_call_result = call_function(response.function_calls[0], True)
                            print(f"-> {function_call_result.parts[0].function_response.response}")
                            messages.append(
                                types.Content(
                                    role="user",
                                    parts=[
                                        types.Part(
                                            text=function_call_result.parts[0].function_response.response['result']
                                        )
                                    ]
                                ),
                            )
                        except Exception as e:
                           return f'Error: {e}'
                    else:
                        try:
                            function_call_result = call_function(response.function_calls[0])
                            messages.append(
                                types.Content(
                                    role="user",
                                    parts=[
                                        types.Part(
                                            text=function_call_result.parts[0].function_response.response['result']
                                        )
                                    ]
                                ),
                            )
                        except Exception as e:
                            return f'Error: {e}'
            except Exception as e:
                return f'Error: {e}'

if __name__ == '__main__':
    main()
