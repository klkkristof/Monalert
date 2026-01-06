import psutil
import json
import os
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("/home/kristof/Documents/Monalert/logs")
METRICS_FILE = LOG_DIR / "metrics.json"

LOG_DIR.mkdir(parents=True, exist_ok=True)
if not METRICS_FILE.exists():
    METRICS_FILE.touch()

def collect_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    network = psutil.net_io_counters()
    
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'cpu_percent': cpu_usage,
        'memory': {
            'total': memory.total,
            'used': memory.used,
            'percent': memory.percent
        },
        'disk': {
            'total': disk.total,
            'used': disk.used,
            'percent': disk.percent
        },
        'network': {
            'bytes_sent': network.bytes_sent,
            'bytes_recv': network.bytes_recv
        }
    }
    
    
    with open('/home/kristof/Documents/Monalert/logs/metrics.json', 'a') as f:
        f.write(json.dumps(metrics) + '\n')
    
    return metrics

if __name__ == "__main__":
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=2))