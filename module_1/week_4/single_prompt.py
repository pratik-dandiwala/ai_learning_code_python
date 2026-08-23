import os
import sys
from dotenv import load_dotenv, find_dotenv 
from openai import OpenAI, AuthenticationError, APIConnectionError

# If you have copied these project/module files from different source, 
# its possible that it may load API key from origin rather than your project .env file
# If so, from pwoersheel execute > $env:OPENAI_API_KEY (notice which API key you see)
# If not your API key, execute > Remove-Item Env:OPENAI_API_KEY (It will clear the wrong API key)
# Now when you run $env:OPENAI_API_KEY again, you will see blank outout and it will only get an API ke when you load it again from .env
# Alternatively, you can also write > load_dotenv(override=True) 
# to override the exsiting API key with the one availabel in your project .env

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY not found in environment variables.")
    sys.exit(1)

client = OpenAI(api_key=api_key)
MODEL = os.getenv("OPENAI_MODEL","gpt-4.1-nano")

print("Sending prompt: ")

try:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Can you summarise, extract keywords and give a headline to following text: Generative AI is a branch of artificial intelligence that can create new content such as text, images, audio, video, and computer code. It uses large machine learning models trained on vast amounts of data to understand patterns and generate human-like outputs. Tools such as ChatGPT, Gemini, and Claude demonstrate how generative AI can support writing, research, programming, education, and creative work. However, generated content may contain errors, bias, or unsupported claims, so human review remains important. Organizations are increasingly using generative AI to automate tasks, improve productivity, personalize experiences, and build intelligent applications. Responsible use requires attention to privacy, security, accuracy, and ethics."}
        ],
        temperature=0.1,
        max_tokens=100
    )
    print("Response:", response.choices[0].message.content)
    print("Tokens used:", response.usage.total_tokens)

except AuthenticationError as e:
    print("Authentication Error: Please check your OPENAI_API_KEY.")
except APIConnectionError as e:
    print("API Connection Error: Please check your internet connection.")
except Exception as e:
    print("An error occurred:", str(e))
