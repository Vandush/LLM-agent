import subprocess
import os
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path):
    
    absWorkingDirectory = os.path.abspath(working_directory)

    if file_path.startswith('/'):
        absFilePath = os.path.abspath(file_path)
    else:
        absFilePath = os.path.abspath(os.path.join(absWorkingDirectory, file_path))

    if absWorkingDirectory not in absFilePath:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(absFilePath) is False:
        return f'Error: File "{file_path}" not found.'
    if absFilePath.split('.')[-1] != "py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        fileRun = subprocess.run(['python3', absFilePath], cwd=os.path.dirname(absFilePath), capture_output=True, timeout=30)
        output = f'STDOUT: {fileRun.stdout}' + '\n' + f'STDERR: {fileRun.stderr}'
        if fileRun.returncode != 0:
            output = output + '\n' + f'Process exited with code {fileRun.returncode}'
        #if len(fileRun.stdout) == 0:
        if len(output) == 0:
            return f'No output produced.'
        return f'{output}'
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description='Will attempt to run the python file as a subprocess using the "python3" command. STDOUT and STDERR are captured, and the process will timeout after 30 seconds.',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path of the file we wish to run. Can be an absolute or relative path, but it must be within the working directory.",
            ),
        },
    ),
)
