import argparse
import logging
import sys

from dotenv import load_dotenv
from llm_api_client import create_prompt_and_get_response

def main():
    parser = argparse.ArgumentParser(description="sysdoctor - diagnose your computer")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level, filename="sysdoctor.log")

    load_dotenv()  # Load environment variables from .env file
    
    while True:
        try:
            prompt = input("you> ")
            if prompt.lower() in ['exit', 'quit']:
                print("Exiting sysdoctor.")
                break
            elif prompt.strip() == "":
                continue
            else:
                logging.info(f"Executing command: {prompt}")
                response = create_prompt_and_get_response(prompt)
                print(f"sysdoctor> {response}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting sysdoctor.")
            break

if __name__ == "__main__":
    sys.exit(main())
