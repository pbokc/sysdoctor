import logging
from openai import OpenAI

SYSTEM_PROMPT = (
    """
    You are SysCopilot, a debugging advisor running on a developer’s Mac (Darwin).
    Your job is to form hypotheses quickly, request minimal machine evidence via tools, 
    and produce concise, actionable next steps. You are read-only—you must not execute 
    or recommend destructive actions.
    """   
)

def create_prompt_and_get_response(question: str) -> str:
    """
    Creates a prompt, sends it to the OpenAI API, and returns the response.
    """
    try:
        client = OpenAI()

        response = client.responses.create(
            model="gpt-5-nano", # TODO: replace with 4o-mini after testing
            instructions=SYSTEM_PROMPT,
            input=question,
        )
        logging.debug(f"Response: {response}")

        return response.output_text
    except Exception as e:
        logging.error(f"Error communicating with OpenAI API: {e}")
        return "Error: Unable to get response from the language model."
