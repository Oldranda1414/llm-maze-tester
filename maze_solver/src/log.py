from datetime import datetime
import os

def log(message: str):
    os.makedirs("results/logs", exist_ok=True)
    
    log_path = f"results/logs/{datetime.now():%Y-%m-%d}.log"
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(log_path, "a") as f:
        f.write(f"[{timestamp}] {message.rstrip()}\n")
