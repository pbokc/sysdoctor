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
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))  # Load environment variables from .env file
    
    parser = argparse.ArgumentParser(description="sysdoctor - diagnose your computer")
    parser.add_argument("--log-level", default="INFO", help="Logging level")
    args = parser.parse_args()
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
