from kubernetes import client, config, watch
from kubernetes.config.config_exception import ConfigException
from queue import Queue
import threading
import time

log_queue = Queue()
running = False
thread = None
v1 = None
w = None

def load_kubernetes_config():
    global v1, w
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        w = watch.Watch()
        log_queue.put("✅ Kubernetes config loaded.")
        return True
    except ConfigException as e:
        log_queue.put(f"⚠️ Kubernetes config not loaded: {e}")
        return False

def monitor_loop():
    global running
    while running and v1 and w:
        try:
            for event in w.stream(v1.list_namespaced_pod, namespace="default", timeout_seconds=10):
                if not running:
                    break
                pod = event['object']
                event_type = event['type']
                name = pod.metadata.name
                status = pod.status.phase

                if event_type == "ADDED":
                    color = "GREEN"
                elif event_type == "DELETED":
                    color = "RED"
                elif event_type == "MODIFIED":
                    color = "YELLOW"
                else:
                    color = "WHITE"

                log_queue.put(f"{color}: {name} - Status: {status}")
        except Exception as e:
            log_queue.put(f"ERROR: {e}")
            time.sleep(1)

def start_monitor():
    global running, thread
    if not running:
        if not load_kubernetes_config():
            return False  # Don't start if config fails
        running = True
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        return True
    return False

def stop_monitor():
    global running
    running = False
    log_queue.put("🛑 Monitoring stopped.")

def get_logs():
    logs = []
    while not log_queue.empty():
        logs.append(log_queue.get())
    return logs
