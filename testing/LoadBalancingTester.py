import requests
from random_word import RandomWords
import threading
import time

URL = "http://192.168.49.2:32723/shorten"
thread_count = 50
interval = 0.1
rand = RandomWords()
running = True
dict = {}
lock = threading.Lock()

def send_req():
    while running:
        long_url = f"www.{rand.get_random_word()}.com"
        try:
            r = requests.post(URL ,data={"long_url":long_url})
            pod = r.json()['handled_by_pod']
            with lock:
                if pod in dict:
                    dict[pod] += 1
                else:
                    dict[pod] = 1
        except Exception as e:
            print(f"failed {e}")
        time.sleep(interval)

threads = []

for i in range(thread_count):
    t = threading.Thread(target=send_req)
    t.start()
    threads.append(t)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    running = False
    print("\nStopping threads...")

    for t in threads:
        t.join()

    print("\n📊 Final summary:")
    print(dict)
