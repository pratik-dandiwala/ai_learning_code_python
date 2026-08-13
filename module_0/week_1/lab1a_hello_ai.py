import os # import python internal module os
import sys # import python internal module sys
from dotenv import load_dotenv # load .env file
from openai import OpenAI, AuthenticationError, APIConnectionError # import given data/values from openai library

load_dotenv() # load .env file, so a program can ready the variable values later

api_key = os.getenv("OPENAI_API_KEY") # Get API key from .env file
if not api_key:
    print("ERROR: OPENAI_API_KEY not found")
    print("Copy .env.example to .env and add your key.")
    sys.exit(1)

# Create an OpenAI client using the API key from the .env file.
# The OpenAI SDK automatically uses the default BASE_URL (https://api.openai.com/v1)
# for all future API requests made through this client.
client = OpenAI(api_key=api_key)
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano") # get model name from .env, if not return use default "gpt-4.1-nano"

# API Call Block

try:
    # Make an API request to OpenAI by sending the prompt and model settings,
    # then receive and store the AI's response in the 'response' object.
    response = client.chat.completions.create( #It actually becomes POST https://api.openai.com/v1/chat/completions - Request sent via Internet
        model=MODEL,
        messages=[
            {"role":"system", "content": "You are a helpful assistance, Be concise."},
            {"role":"user", "content": "What is generative AI in one sentence."},
        ],
        temperature=0.7,
        max_tokens=60,
    )
    # response + error
    print(f"Response: {response.choices[0].message.content}") # [0] gets the first AI response from the list of generated choices.
    print(f"Tokens used: {response.usage.total_tokens}")  # Nested object attribute - get the total number of tokens used for this API call.

except AuthenticationError:
    print("Error: Invalid API key. Check your .env file")
except APIConnectionError:
    print("Error: Cannot connect. Check your internet")
except Exception as e:
    print(f"Unexpected error: {e}")
