import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file_path):
    """
    Reads the content of a file located at the given file_path within the specified working_directory.
    This function ensures that the file to be read is within the permitted working directory and is a regular file.
    It attempts to read up to MAX_CHARS characters from the file. If the file content exceeds MAX_CHARS,
    the returned string is truncated and a message is appended to indicate truncation.
    Args:
        working_directory (str): The base directory within which file access is permitted.
        file_path (str): The relative path to the file from the working_directory.
    Returns:
        str: The content of the file as a string, truncated if necessary.
             Returns an error message string if the file is outside the working directory,
             does not exist, is not a regular file, or if an error occurs during reading.
    """


    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:

        with open(abs_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

    except Exception as e:
        return f"Error: Error reading file contents: {e}" 

    if len(file_content_string)>= MAX_CHARS:
        return f"{file_content_string}\n\n...File {file_path} truncated at 10000 characters"
    return file_content_string


schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Returns the contents of a file as a string, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path of the file that needs to be read, relative to the working directory. If not provided, returns an error message.",
                    ),
                },
            ),
        )

"""
This is the solution given by Boot
"""
# def get_file_content(working_directory, file_path):
#     abs_working_dir = os.path.abspath(working_directory)
#     abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
#     if not abs_file_path.startswith(abs_working_dir):
#         return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
#     if not os.path.isfile(abs_file_path):
#         return f'Error: File not found or is not a regular file: "{file_path}"'
#     try:
#         with open(abs_file_path, "r") as f:
#             content = f.read(MAX_CHARS)
#             if len(content) == MAX_CHARS:
#                 content += (
#                     f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
#                 )
#         return content
#     except Exception as e:
#         return f'Error reading file "{file_path}": {e}'