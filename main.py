import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

try:
    args = sys.argv[1:]
    textInput = args[0]
except Exception as e:
    print("ERROR BIG BOY")
    sys.exit(1)

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
            types.Content(role="user", parts=[types.Part(text=textInput)]),
            ]

    response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages
            )
    
    userPrompt = args[0]
    promptTokens = response.usage_metadata.prompt_token_count
    responseTokens = response.usage_metadata.candidates_token_count


    if "--verbose" in args:
        print(f"User prompt: {textInput}")
        print(f"Prompt tokens: {promptTokens}")
        print(f"Response tokens: {responseTokens}")
#        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
#        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    print(response.text)

if __name__ == '__main__':
    main()
