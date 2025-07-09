import os
from google import genai
from google.genai import types

def get_files_info(working_directory, directory=None):
    
    absWorkingDirectory = os.path.abspath(working_directory)

    if directory.startswith('/'):
        absDirectory = os.path.abspath(directory)
    else:
        absDirectory = os.path.abspath(os.path.join(absWorkingDirectory, directory))

    if absWorkingDirectory not in absDirectory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(absDirectory) is False:
        return f'Error: "{directory}" is not a directory'

    infoList = []

    try:
        for i in os.listdir(absDirectory):
            path = absDirectory + '/' + i
            info = f"- {i}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}"
            infoList.append(info)
        return '\n'.join(infoList)
    except Exception as e:
        return f'Error: {e}'


#From BootDev Course
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)
