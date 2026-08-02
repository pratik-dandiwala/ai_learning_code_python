"""
Lab 1C: AI Workbench CLI v1
A menu-driven CLI application with 4 AI tasks.
Demonstrates: separation of prompts from logic, function reuse, user interaction loop.

Architecture:
  User input → Task selection → Prompt template → LLM API → Formatted response

This same architecture becomes a REST API in Week 2.
"""

import os
import sys
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, RateLimitError, APIConnectionError

# Ensure box-drawing characters render on Windows terminals (cp1252 default).
# Harmless on macOS/Linux, which are already UTF-8. Guarded for older Pythons.

# Configure terminal output to use UTF-8 so Unicode characters display correctly.
# hasattr() is a built-in Python function.
# Think of stdout as a pipe that carries text from your Python program to your terminal.
if hasattr(sys.stdout, "reconfigure"): # This line checks, (type, method of type) - Does stdout support reconfigure() method? 
    # For example (str, "upper") > TRUE, where (str, "drive") > FALSE, since string doesn't support drive() method
    sys.stdout.reconfigure(encoding="utf-8") # encode the data in sys.stdout to utf-8

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-nano")


"''''''''''''''''''''''''"
"--- PROMPT TEMPLATES ---"
"''''''''''''''''''''''''"

# Store all AI task definitions in one place for easy maintenance and extension.
# Each task = a different system prompt. Adding a new AI capability = adding an entry here.
TASKS = {
    "1": {
        "name": "Summarize",
        "prompt": "You are a concise summarizer. Summarize the user's text in 3-5 clear bullet points. Focus on the most important information.",
    },
    "2": {
        "name": "Rewrite",
        "prompt": "You are a professional editor. Rewrite the user's text in a clear, professional tone. Maintain the original meaning but improve clarity and readability.",
    },
    "3": {
        "name": "Key Points",
        "prompt": "You are an analyst. Extract the key points from the user's text as a numbered list. Each point should be one clear sentence.",
    },
    "4": {
        "name": "Explain",
        "prompt": "You are a patient teacher. Explain the user's text in simple terms that a non-expert can understand. Use analogies where helpful.",
    },
}



"'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"
" Reusable function for sending prompts to the LLM and returning the response."
"'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''"


def call_llm(system_prompt: str, user_text: str) -> dict: 
    # type hints - accept arguments system_prompt & user_text as string. 
    # -> dict: - Another type hint. This function is expected to return a dictionary.
    """
    Call the LLM with a system prompt and user text.
    Returns dict with 'content', 'tokens', and 'model' keys.
    Handles errors gracefully with specific messages.
    """
    # Attempt the API request and handle any errors gracefully.
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        return {
            "content": response.choices[0].message.content, # [0] gets the first AI response from the list of generated choices.
            "tokens": response.usage.total_tokens, # Nested object attribute - get the total number of tokens used for this API call.
            "model": response.model, # Object attribute - access the model name returned by the OpenAI response.
        }
    except AuthenticationError:
        return {"content": "Error: Invalid API key. Check your .env file.", "tokens": 0, "model": "N/A"}
    except RateLimitError:
        return {"content": "Error: Rate limit hit. Wait a moment and try again.", "tokens": 0, "model": "N/A"}
    except APIConnectionError:
        return {"content": "Error: Cannot connect to OpenAI. Check your internet.", "tokens": 0, "model": "N/A"}
    except Exception as e: # Catch any unexpected error and store it in variable 'e' so we can display it.
        return {"content": f"Error: {e}", "tokens": 0, "model": "N/A"}


"''''''''''''''''''''''''''''''''''''''''''''"
" Display the main menu for the AI Workbench."
"''''''''''''''''''''''''''''''''''''''''''''"


def display_menu():
    print("\n┌──────────────────────────────────────┐")
    print("│        AI WORKBENCH CLI v1           │")
    print("├──────────────────────────────────────┤")

    # .items() returns both the key and value from each dictionary entry.
    # Unpack each (key, value) pair into two variables: key and task.
    for key, task in TASKS.items():

        # Left-align the task name within 32 spaces to keep the menu neatly formatted.
        print(f"│  {key}. {task['name']:<32}│")

    print("├──────────────────────────────────────┤")
    print("│  q. Quit                             │")
    print("└──────────────────────────────────────┘")


"''''''''''''''''''''''''''"
" Collects multi-line input"
"''''''''''''''''''''''''''"


# -> str: This function is expected to return the user's input as a string.
def get_user_text() -> str:
    print("\n  Paste your text below.")
    print("  (Press Enter on an empty line to submit)")
    print("  " + "─" * 36)

    # 1. Create an empty list.
    # 2. Keep asking the user for input.
    # 3. If the user signals EOF, stop.
    # 4. If the user presses Enter:
    #   • If we already have some text → stop.
    #   • Otherwise → keep asking.
    # 5. If the user typed something:
    #   • Save it.
    #   • Continue asking for more lines.

    # Create an empty list to store multiple lines entered by the user.
    lines = []

    # Infinite loop - keep accepting user input until we explicitly stop using 'break'.
    while True:
        try:
            line = input("  │ ")
        # If the user signals End Of File (EOF) (by doing ctrl + z on terminal), stop collecting input.
        except EOFError:
            break # Exit the loop

        # Check if the user pressed Enter without typing anything.
        if line == "": # Did the user press Enter without typing anything?

            # A non-empty list is treated as True.    
            # If we already collected some lines, the user has finished entering text.    
            if lines: # Does the list contain at least one line?
                break # Exit the loop
        else:
            # Add the newly entered line to the list "lines".
            lines.append(line)

    # Join all values(strings) from the list "lines" into multi-line string and return it.
    return "\n".join(lines)


"''''''''''''''''''''''''''''''''"
"Coordinates the overall program."
"''''''''''''''''''''''''''''''''"

# Main function of the program.
# It controls the overall workflow of the application.
# Main menu loop:
# 1. Display the list of available AI tasks.
# 2. Read the user's choice.
# 3. If the user chooses 'q', show the session summary and exit.
# 4. If the choice is invalid, display an error and show the menu again.
# 5. If the choice is valid, continue with the selected AI task.

def main():

    # Checking if API Key is not empty - note: creating client doesn't specifically check if API key is empty, hence putting this check mark here
    if not os.getenv("OPENAI_API_KEY"): 
        print("┌──────────────────────────────────────┐")
        print("│  ERROR: OPENAI_API_KEY not set        │")
        print("│                                       │")
        print("│  1. Copy .env.example → .env          │")
        print("│  2. Add your API key                  │")
        print("│  3. Run again                         │")
        print("└──────────────────────────────────────┘")

        # Stop the program because it cannot work without an API key.
        sys.exit(1)

    print("\n  Welcome to AI Workbench!")
    print(f"  Model: {MODEL}")
    # print how many keys (AI tasks) are there under "TASKS" dictionary
    print(f"  Tasks available: {len(TASKS)}")

    # Keep track of the total tokens used during this program session.
    session_tokens = 0

    # Infinite loop - Keep showing the menu until the user chooses to quit.
    while True:
        # print initial introductory menu from the funciton display_menu()
        display_menu()
        # Read the user's menu choice and remove any extra spaces before and after the input.
        choice = input("\n  Select a task (1-4 or q): ").strip()

        # If user choose to "Q" or "q" exit the loop - note: .lower() will convert Q to q
        if choice.lower() == "q":
            print(f"\n  Session total: {session_tokens} tokens used")
            print("  Goodbye!\n")
            break

        # Check whether the entered option exists in the TASKS dictionary.
        if choice not in TASKS:
            print("  Invalid choice. Enter 1-4 or q.")
            continue # Continue to get the user's valid input

        # Retrieve the selected task (name and prompt) from the TASKS dictionary.
        task = TASKS[choice]
        print(f"\n  → Task: {task['name']}")
        # call function get_user_text() to get the text inout from an user
        user_text = get_user_text()

        # this will become TRUE if user does not provide any character as an input
        if not user_text.strip():
            print("  No text provided. Try again.")
            continue

        print(f"\n  Processing ({task['name']})...")
        # call_llm with by passing value of "prompt" from the selected TASKS, and entered text by user under user_text
        result = call_llm(task["prompt"], user_text)

        print(f"\n  {'━' * 38}")
        print(f"  Result ({task['name']}):")
        print(f"  {'━' * 38}")
        print()
        # using for loop to print each line seperately from the response (content) - to keep the response within CLI interface
        for line in result["content"].split("\n"):
            print(f"  {line}")
        print()
        print(f"  {'━' * 38}")
        print(f"  Tokens: {result['tokens']} | Model: {result['model']}")
        print(f"  {'━' * 38}")

        # add value of tokens from the response to the value of "Session_tokens"
        session_tokens += result["tokens"]

# Run the main() function only when this file is executed directly.
# Do not run it if this file is imported into another Python program.
if __name__ == "__main__":
    main() # Start the AI Workbench application, by calling function main().

