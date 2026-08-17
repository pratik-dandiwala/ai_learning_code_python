"""
Business logic layer — maps each task to its prompt template.
Separated from routing (main.py) and LLM transport (llm_client.py).
"""

# Relative import (using .): get the generate() function from llm_client.py in this same package.
# Alternatively we can also use from lab2b_app.llm_client import generate. However, since we are in the same package (directory/folder), the exisitng method works
from .llm_client import generate

PROMPTS = {
    "summarize": "Summarize the following text concisely in 3-5 bullet points.",
    "rewrite": "Rewrite the following text in a clear, professional tone.",
    "keypoints": "Extract the key points from the following text as a numbered list.",
    "explain": "Explain the following concept in simple terms that anyone can understand.",
}

# Processes the requested AI task.
# It selects the appropriate prompt from PROMPTS,
# sends the prompt and user's text to the LLM,
# and returns the AI result as a dictionary.
def process_task(task: str, text: str) -> dict: # Accept arguments as string type and return output as dictionary
    # Check whether the requested task exists in the PROMPTS dictionary.
    if task not in PROMPTS: 
        # manually raise exception "ValueError" - stops normal execution because the task value is invalid.
        # Consider if the input task is "translate" which is not present in PROMPT dictionary.
        # Example output > "Unknown task: translate. Available tasks ["summarize", "rewrite", "keypoints", "explain"]"
        raise ValueError(f"Unknown task: {task}. Available tasks: {list(PROMPTS.keys())}")

    # Calling a generate function we imported in line 8 and passing PROMPTS[task] and text as an arguments.
    # return the output it receives from generate() in llm_client.py and store it under a variable result
    result = generate(PROMPTS[task], text) 
    return {
        "task": task,
        "content": result["content"],
        "tokens_used": result["tokens_used"],
    }
