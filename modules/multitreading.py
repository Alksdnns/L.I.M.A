import threading
import time

class MultithreadingModule:
    def __init__(self):
        self.threads = []
        self.stop_flags = {}

    def start_task(self, task_func, task_name=None, *args, **kwargs):
        """
        Start a function `task_func` in a separate thread.
        task_name: unique name to identify the task/thread.
        Args and kwargs are passed to task_func.
        """
        stop_flag = threading.Event()
        self.stop_flags[task_name] = stop_flag

        def task_wrapper(*args, **kwargs):
            try:
                task_func(stop_flag, *args, **kwargs)
            except Exception as e:
                print(f"Error in task '{task_name}': {e}")
            finally:
                # Clean up stop flag and thread reference when done
                self.stop_flags.pop(task_name, None)
                self.threads = [t for t in self.threads if t.name != task_name]

        thread = threading.Thread(target=task_wrapper, args=args, kwargs=kwargs, name=task_name)
        thread.daemon = True
        thread.start()
        self.threads.append(thread)
        print(f"Started task '{task_name}' in thread.")
        return thread

    def stop_task(self, task_name):
        """
        Signal the task to stop using the stop_flag.
        The task function must periodically check stop_flag.is_set()
        """
        stop_flag = self.stop_flags.get(task_name)
        if stop_flag:
            stop_flag.set()
            print(f"Stop signal sent to task '{task_name}'.")
        else:
            print(f"No running task found with name '{task_name}'.")

    def stop_all_tasks(self):
        """
        Stop all running tasks.
        """
        for task_name in list(self.stop_flags.keys()):
            self.stop_task(task_name)
        print("All stop signals sent.")

    def wait_for_all(self):
        """
        Join all threads (wait for them to finish).
        """
        for t in self.threads:
            t.join()
        print("All tasks completed.")
