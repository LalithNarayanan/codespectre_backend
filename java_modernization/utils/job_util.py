import streamlit as st
from datetime import datetime
import os

STORAGE_FILE = "job_run_state.txt"
def load_job_run_state():
    """Loads the last run date and counter from the storage file."""
    # current_path = os.getcwd()
    # print(f"current_path:{current_path}")
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, "r") as f:
            try:
                last_run_date, counter_str = f.readline().strip().split(",")
                return last_run_date, int(counter_str)
            except ValueError:
                return None, 0
    return None, 0

def save_job_run_state(last_run_date, run_counter):
    """Saves the last run date and counter to the storage file."""
    with open(STORAGE_FILE, "w") as f:
        f.write(f"{last_run_date},{run_counter}\n")

def get_job_run_id_persistent():
    """Generates a persistent job run ID."""
    today = datetime.now().strftime("%d%m%Y")
    last_run, counter = load_job_run_state()

    if last_run == today:
        counter += 1
    else:
        counter = 1

    save_job_run_state(today, counter)
    return f"{today}_{counter}"

if __name__ == "__main__":
    print("job_util..")
