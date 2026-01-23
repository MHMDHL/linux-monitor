
import psutil
import csv
import time
import os
from datetime import datetime

class SystemMonitor:
    def __init__(self, log_file="system_log.csv"):
        self.log_file = log_file
        # Create CSV header if file doesn't exist
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow()

    def log_data(self):
        # CPU (interval=None is non-blocking)
        cpu = psutil.cpu_percent(interval=None)    

        # RAM
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024**3), 2) # GB
        ram_used = round(ram.used / (1024**3), 2)   # GB  

        # Disk
        disk = psutil.disk_usage('/')
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write to CSV
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, cpu, ram_total, ram_used, disk.percent])
        
        print(f" CPU: {cpu}% | RAM: {ram_used}/{ram_total}GB")

    def show_top_processes(self):
        # Get top 3 processes by CPU
        procs = 3
        for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                procs.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        # Sort and pick top 3
        top_3 = sorted(procs, key=lambda p: p['cpu_percent'], reverse=True)[:3]
        print(f" Top 3: {[p['name'] for p in top_3]}")      