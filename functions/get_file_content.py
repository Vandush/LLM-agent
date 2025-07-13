import os
from google import genai
from google.genai import types


def get_file_content(working_directory, file_path):
    
    absWorkingDirectory = os.path.abspath(working_directory)

    if file_path.startswith('/'):
        absFilePath = os.path.abspath(file_path)
    else:
        absFilePath = os.path.abspath(os.path.join(absWorkingDirectory, file_path))

    if absWorkingDirectory not in absFilePath:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if os.path.isfile(absFilePath) is False:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    try:
        if len(open(absFilePath, "r").read(10001)) > MAX_CHARS:
            return f'{open(absFilePath, "r").read(MAX_CHARS)}' + '\n' + f'[...File "{file_path}" truncated at 10000 characters]'
        else:
            return f'{open(absFilePath, "r").read()}'
    except Exception as e:
        return f'Error: {e}'

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Displays the conent of a file, up to 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file we wish to view the contents of. Can be an absolute or relative path, but it must be within the working directory.",
            ),
        },
    ),
)
