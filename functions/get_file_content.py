import sys
import os

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
        #print(f'TROUBLESHOOTING: {os.path.dirname(absFilePath)}')
        if len(open(absFilePath, "r").read(10001)) > MAX_CHARS:
            return f'{open(absFilePath, "r").read(MAX_CHARS)}' + '\n' + f'[...File "{file_path}" truncated at 10000 characters]'
        else:
            return f'{open(absFilePath, "r").read()}'
    except Exception as e:
        return f'Error: {e}'
