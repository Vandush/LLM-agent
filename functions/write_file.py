import sys
import os
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    
    absWorkingDirectory = os.path.abspath(working_directory)

    if file_path.startswith('/'):
        absFilePath = os.path.abspath(file_path)
    else:
        absFilePath = os.path.abspath(os.path.join(absWorkingDirectory, file_path))

    if absWorkingDirectory not in absFilePath:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        if os.path.exists(absFilePath) is True:
            with open(absFilePath, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        else:
            os.makedirs(os.path.dirname(absFilePath), exist_ok=True)
            with open(absFilePath, "w") as f:
                f.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Either creates a file and filepath with the desired content, or overwrites an existing file with the desired content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file we wish to create or overwrite the contents of. Can be an absolute or relative path, but it must be within the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The string that will be used to make up the contents of the file we are writing to.",
            ),
        },
    ),
)
