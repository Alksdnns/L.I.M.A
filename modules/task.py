# tasks.py
import time

def example_task(stop_flag, duration=10):
    print("Task started.")
    for i in range(duration):
        if stop_flag.is_set():
            print("Task received stop signal. Exiting early.")
            return
        print(f"Working... {i+1}")
        time.sleep(1)
    print("Task completed.")
