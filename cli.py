# from import answer_question
# from sampler import RING

HELP = """
Commands:
  status                 Show quick system status from latest window
  incidents              List recent incidents (not implemented)
  show <id>              Show incident JSON summary (compact) (not implemented)
  ask "...question..."   Ask about the current 2-min window (not implemented)
  ask <id> "...q..."     Ask about a specific incident window (not implemented)
  help                   Show this help
  quit/exit/q            Exit
"""

def _latest_summary():
    # win = list(RING)
    # if len(win) < 5: return None
    # compute drss/min like sampler does
    # from sampler import _compute_drss_per_min, _summarize_window  # reuse
    # _compute_drss_per_min(win[0], win[-1])
    # return _summarize_window(win)
    # Placeholder summary mimicking the expected structure
    return {
        "cpu_total_med": 12.5,
        "mem_avail_med": 4 * 1024**3,  # 4 GiB
        "swap_used_now": 512 * 1024**2,  # 512 MiB
        "disk_rw_bps_now": {"r": 10 * 1024**2, "w": 5 * 1024**2},  # 10/5 MiB/s
        "top_procs": [
            {"name": "python", "pid": 1234, "cpu": 5.2, "rss": 300 * 1024**2, "drss_per_min": 10 * 1024**2},
            {"name": "chrome", "pid": 2345, "cpu": 2.1, "rss": 500 * 1024**2, "drss_per_min": 5 * 1024**2},
            {"name": "code", "pid": 3456, "cpu": 1.8, "rss": 400 * 1024**2, "drss_per_min": 2 * 1024**2},
            {"name": "zsh", "pid": 4567, "cpu": 0.5, "rss": 50 * 1024**2, "drss_per_min": 1 * 1024**2},
            {"name": "docker", "pid": 5678, "cpu": 0.3, "rss": 200 * 1024**2, "drss_per_min": 0},
        ]
    }

def qa_loop():
    print("Welcome to sysdoctor! Type 'help' for help.")
    print("-" * 60)
    
    while True:
        # Get question from user
        try:
            question = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print(); break
        
        # Skip empty questions
        if not question:
            print("Please enter a question.")
            continue

        # Check for exit conditions
        if question.lower() in ['quit', 'exit', 'q']:
            print("Exiting sysdoctor")
            break

        # Show help
        if question.lower() == 'help':
            print(HELP)
            continue

        if question.lower() == "status":
            s = _latest_summary()
            if not s: print("Collecting data…"); continue
            print(f"CPU~{s['cpu_total_med']:.2f}, avail_mem={s['mem_avail_med']//(1024**2)}MB, "
                  f"swap={s['swap_used_now']//(1024**2)}MB, disk r/w={s['disk_rw_bps_now']['r']//(1024**2)}/{s['disk_rw_bps_now']['w']//(1024**2)} MiB/s")
            top = s["top_procs"][:5]
            for p in top:
                print(f"  {p['name'][:20]:20} pid={p['pid']:>6} cpu={p['cpu']:.2f} rss={p['rss']//(1024**2)}MB Δrss/min={p.get('drss_per_min',0)//(1024**2)}MB")
            continue

        # Call the function to get the answer
        # answer = answer_question(question)
        answer = "This is a placeholder answer."  # Replace with actual function call
        
        # Display the Q&A pair
        print(f"A: {answer}")

# Run the loop
if __name__ == "__main__":
    qa_loop()