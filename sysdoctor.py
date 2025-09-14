#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import threading
import time

from collections import deque
from dotenv import load_dotenv
from llm_api_client import create_prompt_and_get_response
from sys_tools import get_snapshot

# Ring buffer to store recent snapshots
snapshot_store = deque(maxlen=100)  # Store last 100 snapshots

def snapshot_collector(sample_interval_s: int = 10):
    """Background thread to collect snapshots periodically"""
    while True:
        snapshot = get_snapshot()
        snapshot_store.append(snapshot)
        time.sleep(sample_interval_s)

def main():
    parser = argparse.ArgumentParser(description="sysdoctor - diagnose your computer")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
    
    # Load environment variables from .env file in script directory
    script_dir = os.path.dirname(os.path.realpath(__file__))
    env_path = os.path.join(script_dir, ".env")
    logging.info(f"Looking for .env at: {env_path}")
    logging.info(f".env exists: {os.path.exists(env_path)}")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logging.info(f"Loaded .env from: {env_path}")
    else:
        print("Exiting sysdoctor. No .env file found, please create one with your OPENAI_API_KEY.")
        return
    
    logging.basicConfig(
        level=args.log_level,
        filename="sysdoctor.log",
        format="%(asctime)s %(levelname)s %(message)s"
    )

    snapshot_thread = threading.Thread(target=snapshot_collector, daemon=True)
    snapshot_thread.start()

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
