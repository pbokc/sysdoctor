#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import threading
import time

from colorama import Fore, Style
import colorama
from dotenv import load_dotenv
from llm_api_client import create_prompt_and_get_response
from daemon import start_daemon, launch_daemon, stop_daemon, is_daemon_running, get_recent_snapshots

def main():
    colorama.init()
    
    parser = argparse.ArgumentParser(description="sysdoctor - diagnose your computer")
    parser.add_argument("--daemon", action="store_true", help="Start daemon")
    parser.add_argument("--stop-daemon", action="store_true", help="Stop daemon")
    parser.add_argument("--daemon-status", action="store_true", help="Check daemon status")
    args = parser.parse_args()
    
    logging.basicConfig(
        level=logging.DEBUG,
        filename="sysdoctor.log",
        format="%(asctime)s %(levelname)s %(message)s"
    )
    
    # Handle daemon management commands
    if args.daemon:
        return start_daemon()
    elif args.stop_daemon:
        return stop_daemon()
    elif args.daemon_status:
        if is_daemon_running():
            print("Daemon is running")
        else:
            print("Daemon is not running")
        return
    
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

    # Ensure daemon is running
    if not is_daemon_running():
        print("Starting daemon...")
        # Launch daemon without the CLI becoming the daemon
        if launch_daemon():
            print("Daemon started successfully.")
        else:
            print("Failed to start daemon.")
            return 1
    else:
        logging.info("Daemon already running")
    
    print("sysdoctor daemon is running. Starting chat interface...")

    while True:
        try:
            print()
            prompt = input(f"{Fore.BLUE}you>{Style.RESET_ALL} ")
            if prompt.lower() in ['exit', 'quit']:
                if is_daemon_running():
                    keep_daemon = input("Keep daemon running? (y/n): ").strip().lower()
                    if keep_daemon != 'y':
                        print("Stopping daemon...")
                        stop_daemon()
                        print("Daemon stopped.")
                    else:
                        print("Daemon will continue running in background.")
                print("Exiting sysdoctor.")
                break
            elif prompt.strip() == "":
                continue
            else:
                logging.info(f"Executing command: {prompt}")
                response = create_prompt_and_get_response(prompt)
                print(f"\n{Fore.GREEN}sysdoctor>{Style.RESET_ALL} {response}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting sysdoctor.")
            break

if __name__ == "__main__":
    sys.exit(main())
