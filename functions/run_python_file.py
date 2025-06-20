import os
import subprocess
from google.genai import types


def run_python_file(working_directory, file_path):
    """
    Executes a Python file located within a specified working directory.
    Args:
        working_directory (str): The base directory within which the Python file must reside.
        file_path (str): The relative or absolute path to the Python file to execute.
    Returns:
        str: The combined standard output and standard error from the executed Python file,
             or an error message if the file is not found, is outside the working directory,
             is not a Python file, or if execution fails.
    Notes:
        - Only files with a ".py" extension are allowed.
        - The file must exist and be located within the specified working directory.
        - Execution is limited to 30 seconds.
        - The function returns both stdout and stderr output, as well as the process exit code if non-zero.
    """
    current_wd = os.path.abspath(working_directory)
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.' 
    try:
        commands=["python3", abs_path]
        result = subprocess.run(
            commands, 
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
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
            name="run_python_file",
            description="Executes the contents of the given file, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path of the file that needs to be run, relative to the working directory. If not provided, returns an error message.",
                    ),
                },
            ),
        )