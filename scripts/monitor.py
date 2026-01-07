import psutil
import time
import prometheus_client
from prometheus_client import start_http_server, Gauge
from datetime import datetime


cpu_gauge = Gauge('system_cpu_usage_percent', 'CPU usage %')
mem_gauge = Gauge('system_memory_usage_percent', 'Memory usage %')
disk_gauge = Gauge('system_disk_usage_percent', 'Disk usage %')
net_sent_gauge = Gauge('system_network_bytes_sent_total', 'Network bytes sent total')
net_recv_gauge = Gauge('system_network_bytes_recv_total', 'Network bytes received total')


def collect_metrics():
    
    cpu_usage = psutil.cpu_percent(interval=1)
    
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    network = psutil.net_io_counters()
    
    cpu_gauge.set(cpu_usage)
    mem_gauge.set(memory.percent)
    disk_gauge.set(disk.percent)
    net_sent_gauge.set(network.bytes_sent)
    net_recv_gauge.set(network.bytes_recv)
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] CPU: {cpu_usage:.1f}% | RAM: {memory.percent:.1f}% | Disk: {disk.percent:.1f}%")


if __name__ == "__main__":
    
    start_http_server(8000)
    print("Monalert Prometheus exporter: http://localhost:8000/metrics")
    
    try:
        while True:
            collect_metrics()
            time.sleep(15)
            
    except KeyboardInterrupt:
        print("\nLeallitas...")
    except Exception as e:
        print(f"Error: {e}")
