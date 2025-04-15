from kubernetes import client, config, watch
from colorama import Fore, Style, init

init(autoreset=True)

config.load_kube_config()

v1 = client.CoreV1Api()
w = watch.Watch()

print("👀 Watching for pod events...\n")

try:
    for event in w.stream(v1.list_namespaced_pod, namespace="default"):
        pod = event['object']
        event_type = event['type']  # ADDED, MODIFIED, DELETED
        name = pod.metadata.name
        status = pod.status.phase

        if event_type == "ADDED":
            color = Fore.GREEN
        elif event_type == "DELETED":
            color = Fore.RED
        elif event_type == "MODIFIED":
            color = Fore.YELLOW
        else:
            color = Fore.WHITE

        if event_type != "MODIFIED":
            print(f"{color}{event_type}: {name} - Status: {status}{Style.RESET_ALL}")
except KeyboardInterrupt:
    print(Fore.CYAN + "\n🛑 Stopped watching.")
