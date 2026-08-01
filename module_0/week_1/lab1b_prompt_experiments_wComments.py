"""
Lab 1B: Prompt Engineering Experiment
A structured scientific experiment testing 4 variables that affect LLM output.
Demonstrates: how prompts shape responses, temperature effects, output formatting.

Run individual experiments:
  python prompt_experiment.py 1    # Specificity only
  python prompt_experiment.py 2    # Persona only
  python prompt_experiment.py 3    # Format only
  python prompt_experiment.py 4    # Temperature only
  python prompt_experiment.py      # All experiments
"""

import os # import python internal module os
import sys # import python internal module sys
import time # import python internal module time
from dotenv import load_dotenv # load .env file
from openai import OpenAI # import OpenAI module from openai library

load_dotenv() # load .env file, so a program can ready the variable values later

# Create an OpenAI client using the API key from the .env file.
# The OpenAI SDK automatically uses the default BASE_URL (https://api.openai.com/v1)
# for all future API requests made through this client.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini") # get model name from .env, if not return use default "gpt-4.1-mini"

SAMPLE_TEXT = """
Artificial intelligence has transformed how businesses operate. Companies now use
machine learning for everything from customer service chatbots to predictive
maintenance in manufacturing. However, the rapid adoption of AI has also raised
concerns about job displacement, algorithmic bias, and data privacy. Experts argue
that responsible AI development requires transparency, fairness, and accountability
at every stage of the development lifecycle.
""".strip() # .strip() will remove additional space from the string

total_tokens = 0 # set value of total_tokens to 0
total_calls = 0 # set value of total_calls to 0

# Define a function named call_llm. 
# It expects a prompt (a string) and optionally a temperature (a decimal number, defaulting to 0.7). 
# When it finishes, it returns two values: a string and an integer.
def call_llm(prompt: str, temperature: float = 0.7) -> tuple[str, int]: 
    """Call the LLM and return (response_text, tokens_used)."""
    global total_tokens, total_calls # keep these variables as global and not unique within function
    start = time.time() # get the current time from time module and assign it to variable start

    # Make an API request to OpenAI by sending the prompt and model settings,
    # then receive and store the AI's response in the 'response' object.
    response = client.chat.completions.create( #It actually becomes POST https://api.openai.com/v1/chat/completions - Request sent via Internet
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=300,
    )

    elapsed = time.time() - start # elapsed = current time from time module minus the value of variable start
    tokens = response.usage.total_tokens # get value from response object: response > usage > total_tokens
    total_tokens += tokens # total_tokens = current value of total_tokens + value of tokens
    total_calls += 1 # total_calls = current value of total_calls + 1

    text = response.choices[0].message.content # response > choices[0] > first choice/answer > message > content
    print(f"  [{tokens} tokens, {elapsed:.1f}s]") # .1f means > Show only 1 digit after the decimal point. 2.5, 3.6 etc. but not 2.56, 3.69
    return text, tokens # return the value of text and tokens upon calling this function


def experiment_specificity():
    """Variable 1: Instruction specificity (vague → precise)"""
    print("\n" + "=" * 60) # output > add one line space after previous pring and then print '=' 60 times like =========
    print("EXPERIMENT 1: Instruction Specificity")
    print("Question: How does prompt precision affect output quality?")
    print("=" * 60) # output > print '=' 60 times like =========

    levels = [
        ("Vague", f"Summarize this:\n{SAMPLE_TEXT}"),
        ("Specific", f"Summarize this text in exactly 3 bullet points:\n{SAMPLE_TEXT}"),
        ("Highly specific", f"Summarize this text in 3 bullet points, each under 15 words, focusing only on business impact:\n{SAMPLE_TEXT}"),
    ]

    for label, prompt in levels: # this is similar to, student = ("Pratik", 95), name, marks = student, where name becomes "Pratik" and marks becomes 95 
        # lets consider first loop levels[0] , here "Vague" becomes "label" and f"Summarize this:\n{SAMPLE_TEXT}" becomes "prompt"
        # label = "Vague"
        # prompt = "Summarize this: ......"
        # similarly for second loop levels[1], label = "Specific" and prompt = "Summarize this text in exactly 3 bullet points: ....."
        print(f"\n--- Level: {label} ---") # For first loop levels[0] outout > --- Level: Vague ---
        print(f"  Prompt: '{prompt.split(chr(10))[0]}'")
        # above line is similar to print(f"  Prompt: '{prompt.split("\n")[0]}'")
        # every keyboard character has a number, a = 65, b = 66, similarly \n = 10.
        # using index [0] this will only print first line of the prompt which is ""Summarize this:" for label "Vague" and so on
        result, _ = call_llm(prompt)
        # Remember call_llm function returns text, tokens. 
        # Hence if you write result, tokenNumber = call_llm(prompt) > here result = text and tokenNumber = tokens
        # But we only want text to be print against variable result and do not want token in this line
        # Here _ means > Yes, I know there's a second value, but I'm intentionally ignoring it.
        print(f"  Output:\n{result}") # print Output: and then in next line "result"

    # Beolow are just normal string print
    print("\n  OBSERVATION: Notice how specificity controls length, format, and focus.")
    print("  → More specific instructions = more predictable, useful outputs.")


# Now when we have understood two functions in details, 
# all other functions have similar logic, which we can understand considering what we have learned
# Still we may see comments against the logic which differs from what we have learned till now 
def experiment_persona():
    """Variable 2: Persona / audience targeting"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 2: Persona / Audience Targeting")
    print("Question: How does the target audience change the response?")
    print("=" * 60)

    personas = [
        ("CEO", f"You are briefing a CEO who has 30 seconds. Summarize the key business decision from this text:\n{SAMPLE_TEXT}"),
        ("10-year-old", f"Explain this to a curious 10-year-old using simple words and an analogy:\n{SAMPLE_TEXT}"),
        ("Software Engineer", f"Summarize this for a software engineer evaluating AI tools for their team. Focus on technical implications:\n{SAMPLE_TEXT}"),
    ]

    for persona, prompt in personas:
        print(f"\n--- Audience: {persona} ---")
        result, _ = call_llm(prompt)
        print(f"  Output:\n{result}")

    print("\n  OBSERVATION: Same source text, completely different outputs.")
    print("  → The audience instruction reshapes vocabulary, depth, and framing.")


def experiment_format():
    """Variable 3: Output format (free text vs structured)"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 3: Output Format Control")
    print("Question: Can you control the structure of AI output?")
    print("=" * 60)

    formats = [
        ("Free text", f"Summarize this:\n{SAMPLE_TEXT}"),
        ("JSON", f"Summarize this as valid JSON with keys: \"main_point\", \"risks\", \"opportunities\". Output ONLY the JSON:\n{SAMPLE_TEXT}"),
        ("Markdown table", f"Summarize this as a markdown table with columns: Theme | Key Point | Implication. Include 3 rows:\n{SAMPLE_TEXT}"),
    ]

    for fmt, prompt in formats:
        print(f"\n--- Format: {fmt} ---")
        result, _ = call_llm(prompt)
        print(f"  Output:\n{result}")

    print("\n  OBSERVATION: LLMs can output structured data (JSON, tables, lists).")
    print("  → This is how AI integrates with software systems — structured output.")


def experiment_temperature():
    """Variable 4: Temperature effect on same prompt"""
    print("\n" + "=" * 60)
    print("EXPERIMENT 4: Temperature Effect")
    print("Question: How does temperature change output variability?")
    print("=" * 60)

    prompt = f"Write a one-sentence creative tagline for this technology:\n{SAMPLE_TEXT}"
    temperatures = [0.0, 0.7, 1.5]

    for temp in temperatures:
        print(f"\n--- Temperature: {temp} ---")
        print(f"  Running same prompt twice to compare consistency:")
        results = []
        for run in range(2): # run this loop 2 times - because for experiment we want to call LLM twice for same temperature - hence total 6 times
            result, _ = call_llm(prompt, temperature=temp)
            results.append(result) # append the list [] named results in line #162 with the value of result in line 164
            print(f"    Run {run + 1}: {result}")

        if results[0] == results[1]:
            print("  → Outputs are IDENTICAL (deterministic)")
        else:
            print("  → Outputs DIFFER (probabilistic sampling)")

    print("\n  OBSERVATION:")
    print("  → temp=0: Same output every time. Use for factual/consistent tasks.")
    print("  → temp=0.7: Balanced. Good default for most applications.")
    print("  → temp=1.5: High variance. Use for creative/brainstorming tasks.")


def print_summary():
    """Print experiment summary with total usage."""
    print("\n" + "=" * 60)
    print("EXPERIMENT COMPLETE — Summary")
    print("=" * 60)
    print(f"  Total API calls made: {total_calls}")
    print(f"  Total tokens used:    {total_tokens}")
    print(f"  Estimated cost:       ${total_tokens * 0.00000015:.4f} (approx)")
    print()
    print("  Key Findings:")
    print("  1. SPECIFICITY: More precise prompts → more useful outputs")
    print("  2. PERSONA: Audience framing changes vocabulary and depth")
    print("  3. FORMAT: LLMs can output structured data (JSON, tables)")
    print("  4. TEMPERATURE: Controls randomness vs consistency")
    print()
    print("  → The prompt IS the program. Master prompts = master AI.")
    print("=" * 60)

# __name__ is one of Python's built-in variables. Python automatically creates it. You don't have to define it.
# when you run python lab1bprompt_experiment.py, python automatically sets __name__ = "__main__". Hence this condition becomes TRUE
# However, if another file imports lab1bprompt_experiment.py, to use any one function from this file
# for example, you define import lab1bprompt_experiment.py in lab1ahello_ai.py, 
# __name__ becomes lab1bprompt_experiment.py hence the condition becomes FALSE
# and the whole program won't execute in lab1a_hello_ai.py, rather only a required functions can be used
if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not set. See .env.example")
        sys.exit(1) # stops the program if API key doesn't exist

    print("=" * 60)
    print("Lab 1B: Prompt Engineering Experiment")
    print(f"Model: {MODEL}")
    print(f"Sample text: {len(SAMPLE_TEXT)} chars")
    print("=" * 60)

    experiments = {
        "1": experiment_specificity, # key:value > key is number, and value is a function name
        "2": experiment_persona, # if you tell python experiments["2"]() > It will execute function experiment_persona()
        "3": experiment_format,
        "4": experiment_temperature,
    }

    # sys.argv is a command-line argument. For example, when we run "python lab1b_prompt_experiments.py 3"
    # Python creates sys.argv,
    # [
    #   lab1b_prompt_experiments.py
    #   3
    # ]
    # here sys.argv[0] is file name "lab1b_prompt_experiments.py"
    # and sys.argv[1] is 3
    # Below condition checks, if length of sys.argv is > 1 and if sys.argv[1] present in experiments dictionary
    if len(sys.argv) > 1:
        if sys.argv[1] in experiments:
            experiments[sys.argv[1]]() # run the function at place sys.argv[1] from an experiment dictionary
        else:
            print("Invalid experiment number.")
            print("Use: 1, 2, 3 or 4")
            sys.exit(1)
    else:
        for exp in experiments.values(): # If we do not specify argument, this loop will run app functions.
            exp()

    print_summary() # execute the function print_summary() and print print multiple given lines
