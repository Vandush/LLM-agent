import subprocess
import os

def run_python_file(working_directory, file_path):
    
    absWorkingDirectory = os.path.abspath(working_directory)

    if file_path.startswith('/'):
        absFilePath = os.path.abspath(file_path)
    else:
        absFilePath = os.path.abspath(os.path.join(absWorkingDirectory, file_path))

    if absWorkingDirectory not in absFilePath:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.exists(absFilePath) is False:
        return f'Error: File "{file_path}" not found.'
    if absFilePath.split('.')[-1] != "py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        fileRun = subprocess.run([absFilePath], cwd=os.path.dirname(absFilePath), capture_output=True, timeout=30)
        output = f'STDOUT: {fileRun.stdout}' + '\n' + f'STDERR: {fileRun.stderr}'
        if fileRun.returncode != 0:
            output = output + '\n' + f'Process exited with code {fileRun.returncode}'
        if len(fileRun.stdout) == 0:
            return f'No output produced.'
        return f'{output}'
    except Exception as e:
        return f"Error: executing Python file: {e}"


'''
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
'''
'''
Tips

    os.path.exists: Check if a path exists
    os.makedirs: Create a directory and all its parents
    os.path.dirname: Return the directory name

Example of writing to a file:

with open(file_path, "w") as f:
    f.write(content)

'''


'''
    MAX_CHARS = 10000

    try:
        if len(open(absFilePath, "r").read(10001)) > MAX_CHARS:
            return f'{open(absFilePath, "r").read(MAX_CHARS)}' + '\n' + f'[...File "{file_path}" truncated at 10000 characters]'
        else:
            return f'{open(absFilePath, "r").read()}'
    except Exception as e:
        return f'Error: {e}'
'''
