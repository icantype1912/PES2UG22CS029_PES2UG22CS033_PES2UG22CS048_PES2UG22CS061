from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import subprocess
import threading
import time

from Monitoring import log_queue, start_monitor, stop_monitor
from LoadBalancingTester import stat_queue, start_stress_test, stop_stress_test, get_results

app = FastAPI()

# Cluster

@app.post("/start-cluster")
def start_cluster():
    def run():
        subprocess.call(["bash", "k8s-start.sh"])
    threading.Thread(target=run).start()
    return {"status": "Cluster startup script initiated"}

@app.post("/stop-cluster")
def stop_cluster():
    def run():
        subprocess.call(["bash", "k8s-stop.sh"])
    threading.Thread(target=run).start()
    return {"status": "Cluster stop script initiated"}

#Logs

@app.post("/start-logs")
def api_start_logs():
    threading.Thread(target=start_monitor).start()
    return {"status": "Log monitoring started"}

@app.post("/stop-logs")
def api_stop_logs():
    stop_monitor()
    return {"status": "Log monitoring stopped"}

@app.get("/stream-logs")
def stream_logs():
    def event_stream():
        while True:
            log = log_queue.get()
            if log == "STOP":
                break
            yield f"data: {log}\n\n"
            time.sleep(0.1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

#Stress Test

@app.post("/start-stress-test")
def api_start_stress_test():
    threading.Thread(target=start_stress_test).start()
    return {"status": "Stress test started"}

@app.post("/stop-stress-test")
def api_stop_stress_test():
    stop_stress_test()
    return {"status": "Stress test stopped"}

@app.get("/stream-stats")
def stream_stats():
    def event_stream():
        while True:
            stat = stat_queue.get()
            if stat == "STOP":
                break
            yield f"data: {stat}\n\n"
            time.sleep(0.1)

    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.get("/stress-results")
def stress_results():
    return get_results()
