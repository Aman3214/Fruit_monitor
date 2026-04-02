import subprocess
import time
import sys

# --- CONFIGURATION ---
# We only use the filename here because 'cwd' will put us in the right folder
AI_SCRIPT = "ai_processor.py"
NODE_SCRIPT = "server.js"
MOCK_SCRIPT = "test_output.py"

processes = []

def start_processes():
    try:
        # 1. Start Node.js - This mimics: cd dashboard && node server.js
        print("[1/3] Starting Dashboard...")
        node_proc = subprocess.Popen(["node", NODE_SCRIPT], 
                                    cwd="dashboard") 
        processes.append(node_proc)
        time.sleep(2)

        # 2. Start AI - This mimics: cd ai_engine && python ai_processor.py
        print("[2/3] Starting AI Processor...")
        ai_proc = subprocess.Popen(["python", AI_SCRIPT], 
                                  cwd="ai_engine")
        processes.append(ai_proc)
        time.sleep(2)

        # 3. Start Mock - This mimics: cd test && python test_output.py
        print("[3/3] Starting Mock Data...")
        mock_proc = subprocess.Popen(["python", MOCK_SCRIPT], 
                                    cwd="test")
        processes.append(mock_proc)

        print("\nALL SYSTEMS ONLINE. Press Ctrl+C to exit.")

        while True:
            for p in processes:
                if p.poll() is not None:
                    # If mock finishes (Code 0), keep others running
                    if p == mock_proc and p.returncode == 0:
                        continue
                    print(f"Process stopped (Code: {p.returncode})")
                    shutdown()
            time.sleep(1)

    except KeyboardInterrupt:
        shutdown()

def shutdown():
    print("\nShutting down...")
    for p in processes:
        p.terminate()
    sys.exit(0)

if __name__ == "__main__":
    start_processes()