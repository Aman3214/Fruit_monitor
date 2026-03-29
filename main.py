import subprocess
import time
import sys
import os
import signal

# --- CONFIGURATION ---
# Change these paths to match your actual file names/locations
CONDA_ENV = "fruit_monitor"
PATH_TO_AI = "fruit_monitor/ai_engine/ai_processor.py"
PATH_TO_NODE = "fruit_monitor/dashboard/server.js"  # Assuming your dashboard is here

processes = []

def start_processes():
    print("Initializing Fruit Monitoring System for Presentation...")
    
    try:
        # 1. Start the Node.js Dashboard Server
        print("[1/2] Starting Node.js Dashboard...")
        node_proc = subprocess.Popen(["node", PATH_TO_NODE], 
                                    stdout=subprocess.PIPE, 
                                    stderr=subprocess.STDOUT,
                                    text=True)
        processes.append(node_proc)
        time.sleep(2) # Give the server a moment to bind to the port

        # 2. Start the AI Processor via Conda
        print("[2/2] Starting Python AI Processor (Conda)...")
        # Use 'conda run' to ensure the correct environment and dependencies are used
        ai_cmd = ["conda", "run", "-n", CONDA_ENV, "--no-capture-output", "python", PATH_TO_AI]
        ai_proc = subprocess.Popen(ai_cmd, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT, 
                                  text=True)
        processes.append(ai_proc)

        print("\nALL SYSTEMS ONLINE.")
        print("Dashboard: http://localhost:3000")
        print("Press Ctrl+C to shut down all services safely.\n")

        # Stream outputs to the console
        while True:
            # Check if processes are still running
            for p in processes:
                if p.poll() is not None:
                    print(f"\nWarning: A process has stopped (Code: {p.returncode})")
                    return
            
            time.sleep(1)

    except KeyboardInterrupt:
        shutdown()

def shutdown():
    print("\n\nShutting down services...")
    for p in processes:
        p.terminate()
        # On Windows, you might need p.kill() if terminate() is ignored
    print("All processes stopped. Ready for next run.")
    sys.exit(0)

if __name__ == "__main__":
    start_processes()