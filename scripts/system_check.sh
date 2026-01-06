#!/bin/bash

LOGDIR="/home/kristof/Documents/Monalert/logs"
LOGFILE="$LOGDIR/system.log"
CPU_THRESHOLD=80
MEM_THRESHOLD=85
DISK_THRESHOLD=90

mkdir -p $LOGDIR

touch "$LOGFILE"

# Logolas
log_message() {
    echo "[$(date  '+%Y-%m-%d %H-%M-%S') $1]" >> $LOGFILE
}


# CPU Check
cpu_usage=$(top -bn1 | awk '/Cpu\(s\)/ {
    gsub(",", ".", $2);
    printf("%.0f\n", $2);
}')
log_message "CPU Usage: ${cpu_usage}%"

if [ "$cpu_usage" -gt "$CPU_THRESHOLD" ]; then
    log_message "ALERT: High CPU usage detected!"
fi

# Memory Check
mem_usage=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100)}')
log_message "Memory Usage: ${mem_usage}%"

if [ $mem_usage -gt $MEM_THRESHOLD ]; then
    log_message "ALERT: High memory usage detected"
fi

# Disk Check
disk_usage=$(df -h | tail -1 | awk '{print $5}' | cut -d'%' -f1)
log_message "Disk usage: ${disk_usage}%"

if [ $disk_usage -gt $DISK_THRESHOLD ]; then
    log_message "ALERT: High disk usage detected"
fi
