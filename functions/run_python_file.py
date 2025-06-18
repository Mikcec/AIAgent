import os
import subprocess

def run_python_file(working_directory, file_path):
    current_wd = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.' 
    try:
        result = subprocess.run(
            ["python3", abs_path], 
            stdin=None,
            input=None,
            stdout=None,
            stderr=None,
            capture_output=True,
            shell=False,
            cwd=current_wd,
            timeout=30,
            check=False,
            encoding=None,
            errors=None,
            text=True,
            env=None,
            universal_newlines=None
            )
        stdout = result.stdout
        stderr = result.stderr
        returncode = result.returncode

        if stdout == "" and stderr == "":
            return "No output produced"
        if returncode == 0:
            final= f"STDOUT: {stdout}\nSTDERR: {stderr}"
        else:
            final= f"STDOUT: {stdout}\nSTDERR: {stderr}, Process exited with code {returncode}"
        return final
    except Exception as e:
        return f"Error: executing Python file: {e}"



