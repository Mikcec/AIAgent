import os
from google.genai import types

def get_files_info(working_directory, directory=None):
    """
    Retrieves information about the contents of a specified directory within a working directory.
    Args:
        working_directory (str): The base directory within which directory listings are permitted.
        directory (str, optional): The relative path to the directory whose contents are to be listed. If None, the working_directory itself is used.
    Returns:
        str: A formatted string listing each entry in the directory with its file size (in bytes) and whether it is a directory.
             If the specified directory is outside the working directory or is not a directory, returns an error message.
             If an error occurs while reading the directory, returns an error message.
    """
    if directory is None:
        directory = "."  # Default to current directory
    abs_path = os.path.abspath(os.path.join(working_directory, directory))
    
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(abs_path):
        return (f'Error: "{directory}" is not a directory')
    contents = []
    try:

        for entry in os.listdir(abs_path):
            full_path = os.path.join(abs_path, entry)
            is_dir = os.path.isdir(full_path)
            file_size = os.path.getsize(full_path) 
            contents.append(f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}")
    except Exception as e:
        return f"Error: Error reading directory contents: {e}"

    return "\n".join(contents)


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
