# sysdoctor
A command line AI assistant that figures out why your computer is being weird

## How it works

sysdoctor provides LLMs real-time system data from your machine:

- Runs a background daemon that continuously collects system metrics (CPU, memory, disk, processes)
- Maintains a history of system snapshots in `~/.sysdoctor/snapshots.json` to track performance trends
- Provides a chat interface that automatically includes current system state as context for every user question
- Daemon persists across chat sessions, so you always have fresh data ready

The goal is to get specific action items based on your machine's state rather than generic advice.

## Example
![Demo of sysdoctor in action](sysdoctor_demo.png)

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Create a `.env` file in the `sysdoctor` directory:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

### Basic Usage
```bash
# Start chat interface (auto-starts daemon if needed)
sysdoctor

# Check if daemon is running
sysdoctor --daemon-status

# Manually start daemon in background
sysdoctor --daemon

# Stop daemon
sysdoctor --stop-daemon
```

### Run as a CLI command (recommended)
```bash
sysdoctor
```

#### One-time setup for CLI usage
1. Make the script executable:
   ```bash
   chmod +x sysdoctor.py
   ```
2. Create a symlink to `/usr/local/bin`:
   ```bash
   ln -sf "$PWD/sysdoctor.py" /usr/local/bin/sysdoctor
   ```
3. Now you can run `sysdoctor` from anywhere in your terminal.

### Run as a Python script
```bash
python sysdoctor.py
```

**Arguments:**
- `--daemon`: Start daemon in background and exit
- `--stop-daemon`: Stop running daemon and exit  
- `--daemon-status`: Check if daemon is running and exit## Data Storage

sysdoctor stores data in `~/.sysdoctor/`:
- `snapshots.json`: System snapshots collected by daemon
- `daemon.pid`: Process ID of running daemon
- `daemon.log`: Daemon operation logs

## Chat Interface

Type your questions about system performance and sysdoctor will analyze current and recent system state to provide specific recommendations.

Type `exit` or `quit` to exit. You'll be asked whether to keep the daemon running for future sessions.
