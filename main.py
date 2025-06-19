import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import system_prompt

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
schema_write_file = types.FunctionDeclaration(
            name="write_file",
            description="Updates the contents of the given file, constrained to the working directory.",
            parameters=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "file_path": types.Schema(
                        type=types.Type.STRING,
                        description="The path of the file that needs to be written, relative to the working directory. If not provided, returns an error message. If it does not exist, it will create it.",
                    ),
                    "content": types.Schema(
                        type=types.Type.STRING,
                        description="These are the contents that will be written to the file, relative to the working directory. If not provided, returns an error message. If it does not exist, it will create it.",
                    ),
                },
            ),
        )

available_functions = types.Tool(
            function_declarations=[
                schema_get_files_info,
                
            ]
        )
    

def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)


def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )

    # Check if the response contains a function call
    function_call_part = None
    for part in response.candidates[0].content.parts:
        if hasattr(part, "function_call") and part.function_call is not None:
            function_call_part = part.function_call
            break

    if function_call_part:
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        print("Response:")
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print("Response:")
        print(response.text)

    

if __name__ == "__main__":
    main()
