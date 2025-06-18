import os

def write_file(working_directory, file_path, content):
    abs_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not abs_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(os.path.dirname(abs_path)):
        try:
            os.makedirs(os.path.dirname(abs_path))
        except Exception as e:
            return f"Error: creating directory: {e}"
    
    if os.path.isdir(abs_path):
        return f'Error: The specified path {file_path} is a directory"'  
    try:
        with open(abs_path, "w") as afp:
            afp.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    except Exception as e:
        return f"Error: writing to file: {e}"

