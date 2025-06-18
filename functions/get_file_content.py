import os
from config import MAX_CHARS


def get_file_content(working_directory, file_path):


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