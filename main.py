import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv

# def main():
#     load_dotenv()
#     api_key = os.environ.get("GEMINI_API_KEY")
#     client = genai.Client(api_key=api_key)
    

#     if len(sys.argv) <2:
#         print('Prompt error, no string provided.\nie: main.py "Your query"')
#         sys.exit(1)
#     else:
#         user_prompt= sys.argv[1:]
#         messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
#         response = client.models.generate_content(
#             model="gemini-2.0-flash-001",
#             contents=messages,
#         )
#         print("Prompt tokens:", response.usage_metadata.prompt_token_count)
#         print("Response tokens:", response.usage_metadata.candidates_token_count)
#         print("Response:")
#         print(response.text)

# def main():
#     load_dotenv()

#     args = sys.argv[1:]

#     if not args:
#         print("AI Code Assistant")
#         print('\nUsage: python main.py "your prompt here"')
#         print('Example: python main.py "How do I build a calculator app?"')
#         sys.exit(1)
#     user_prompt = " ".join(args)

#     api_key = os.environ.get("GEMINI_API_KEY")
#     client = genai.Client(api_key=api_key)

#     user_prompt = " ".join(args)

#     if "--verbose" in sys.argv:
#         user_prompt = user_prompt.replace("--verbose", "").strip()
        
#         messages = [
#         types.Content(role="user", parts=[types.Part(text=user_prompt)]),
#         ]
#         print(f"User prompt: {user_prompt}")
#         generate_content_v(client, messages)
        
#     else:
#         messages = [
#             types.Content(role="user", parts=[types.Part(text=user_prompt)]),
#         ]
#         generate_content(client, messages)

# def generate_content(client, messages):
#     response = client.models.generate_content(
#         model="gemini-2.0-flash-001",
#         contents=messages,
#     )
#     print("Response:")
#     print(response.text)

# def generate_content_v(client, messages):
#     response = client.models.generate_content(
#         model="gemini-2.0-flash-001",
#         contents=messages,
#     )
#     print("Prompt tokens:", response.usage_metadata.prompt_token_count)
#     print("Response tokens:", response.usage_metadata.candidates_token_count)

# if __name__ == "__main__":
#     main()
   

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
    )
    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
