import os
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

functionDict = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'run_python_file': run_python_file,
    'write_file': write_file
}

def call_function(function_call_part, verbose=False):
    
    # Error if the function is invalid.
    if function_call_part.name not in functionDict:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


    # Hard code the working directory.
    functionArgs = function_call_part.args.copy()
    functionArgs["working_directory"] = './calculator'

    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": functionDict[function_call_part.name](**functionArgs)},
                )
            ],
        )
    else:
        print(f" - Calling function: {function_call_part.name}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": functionDict[function_call_part.name](**functionArgs)},
                )
            ],
        )
