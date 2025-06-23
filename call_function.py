from google.genai import types
from config import MAX_CHARS, WORKING_DIRECTORY
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

def call_function(function_call_part, verbose=False):
    """
    Calls a specified function from a predefined function map with provided arguments.
    Args:
        function_call_part: An object containing the function name (`name`) and arguments (`args`) to be called.
        verbose (bool, optional): If True, prints detailed information about the function call. Defaults to False.
    Returns:
        types.Content: An object representing the result of the function call, or an error message if the function name is unknown.
    Raises:
        None
    Notes:
        - The function expects `function_call_part` to have `name` and `args` attributes.
        - Adds a `working_directory` argument to the function call.
        - Supported functions are: get_files_info, get_file_content, run_python_file, write_file.
    """

    
    function_name = function_call_part.name
    function_result={}
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if verbose:
        print(f"Calling function: {function_name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_name}") 
    
    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIRECTORY
    function_result = function_map[function_name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

