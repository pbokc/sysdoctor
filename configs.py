API_BASE = "https://api.openai.com/v1/chat/completions"  # or your provider
MODEL = "gpt-4.1-mini"  # pick your cost/latency target
API_KEY_ENV = "OPENAI_API_KEY"

SAMPLE_HZ = 1.0
WINDOW_SECS = 120
MAX_PROCS = 25
COOLDOWN_SECS = 900

# Incident thresholds
CPU_HOT_AVG = 0.85          # 15s moving avg
MEM_AVAIL_FRAC = 0.10
SWAP_DELTA_BYTES = 256*1024*1024
LEAK_DRSS_PER_MIN = 200*1024*1024
IO_HOT_RW_BPS = 150*1024*1024  # tune per machine
