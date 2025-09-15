from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env from current directory

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print("OPENAI_API_KEY loaded successfully:", api_key[:6] + "...")
else:
    print("OPENAI_API_KEY not found. Check your .env file and working directory.")