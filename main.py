import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    """
    Main entry point for the AI Code Assistant application.
    
    This function loads environment variables, parses command-line arguments,
    initializes the Gemini API client, and processes the user's prompt.
    
    It prints usage instructions if no prompt is provided, and optionally
    prints verbose output. The function then constructs the message payload
    and calls the content generation function.
    
    Raises:
        SystemExit: If no user prompt is provided via command-line arguments.
    """
    
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
    """
    Handles the content generation loop using the Gemini API client.

    This function sends the current message history to the model, processes the response,
    and handles any function calls by invoking the appropriate functions. It continues
    the loop until the model produces a final response without further function calls.

    Args:
        client: The Gemini API client instance.
        messages (list): The conversation history as a list of message objects.
        verbose (bool): If True, prints detailed information about token usage and function responses.

    Raises:
        Exception: If a function call result is empty or if no function responses are generated.
    """
    
    for i in range(20):  # Loop up to 20 times
        print(f"Iteration {i + 1}")
        # Generate content with current messages
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
        )
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)
        for candidate in response.candidates:
            messages.append(candidate.content)


    
        # Check if there are function calls
        if response.function_calls:
            function_responses = []
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                if (
                    not function_call_result.parts
                    or not function_call_result.parts[0].function_response
                ):
                    raise Exception("empty function call result")
                if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_responses.append(function_call_result.parts[0])
            messages.append(types.Content(role="tool", parts=function_responses))
            if not function_responses:
                raise Exception("no function responses generated, exiting.")
        else:
            # No function calls = agent is done
            # Print final response and break
            print(f"\nFinal response:\n{response.text}")
            break


if __name__ == "__main__":
    main()
