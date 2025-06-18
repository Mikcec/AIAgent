import os

def get_files_info(working_directory, directory=None):

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


