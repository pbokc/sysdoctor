import multiprocessing
import time

def cpu_spam():
    while True:
        pass  # Busy loop

if __name__ == "__main__":
    duration = 300  # seconds
    print(f"Spamming CPU for {duration} seconds. Press Ctrl+C to stop early.")
    procs = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=cpu_spam)
        p.start()
        procs.append(p)
    try:
        time.sleep(duration)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        for p in procs:
            p.terminate()
        for p in procs:
            p.join()
    print("CPU spam finished.")