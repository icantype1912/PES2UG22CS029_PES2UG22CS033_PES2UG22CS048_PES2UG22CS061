import requests
from random_word import RandomWords
import threading
import time
from queue import Queue

URL = "http://192.168.49.2:30966/shorten"
thread_count = 50
interval = 0.1

running_event = threading.Event()
threads = []
lock = threading.Lock()
results = {}
stat_queue = Queue()
rand = RandomWords()

def send_request():
    while running_event.is_set():
        long_url = f"http://www.{rand.get_random_word()}.com"
        try:
            r = requests.post(URL, data={"long_url": long_url})
            pod = r.json().get("handled_by_pod", "unknown")
            with lock:
                results[pod] = results.get(pod, 0) + 1
                stat_queue.put(f"{pod}: {results[pod]}")
        except Exception as e:
            stat_queue.put(f"Request failed: {e}")
        time.sleep(interval)

def start_stress_test():
    if running_event.is_set():
        return "Already running"
    
    running_event.set()
    threads.clear()

    for _ in range(thread_count):
        t = threading.Thread(target=send_request)
        t.start()
        threads.append(t)
    
    return "Stress test started"

def stop_stress_test():
    if not running_event.is_set():
        return "Not running"
    
    running_event.clear()

    for t in threads:
        t.join()
    
    return "Stress test stopped"

def get_results():
    return results

def get_logs():
    logs = []
    while not stat_queue.empty():
        logs.append(stat_queue.get())
    return logs
