import psutil
import csv
import time
import os
from datetime import datetime

class SystemMonitor:
    def __init__(self, log_file):
        self.log_file = log_file
        
        # Initialize Log File with ALL Assignment Requirements
        if not os.path.exists(self.log_file):
             with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", 
                    "CPU_Usage", "Load_1m", "Load_5m", "Load_15m",
                    "Mem_Total", "Mem_Available", "Mem_Used", "Mem_Percent",
                    "Disk_Total", "Disk_Free", "Disk_Percent",
                    "Uptime_Sec", "Idle_Sec",
                    "Procs_Total", "Procs_Running", "Procs_Sleeping",
                    "Top3_CPU", "Top3_Memory"
                ])

    def get_metrics(self):
        # 1. CPU
        cpu_usage = psutil.cpu_percent(interval=None)
        load_avg = psutil.getloadavg()
        
        # 2. Memory
        mem = psutil.virtual_memory()
        
        # 3. Disk
        disk = psutil.disk_usage('/')
        
        # 4. Uptime & Idle
        boot_time = psutil.boot_time()
        uptime_sec = time.time() - boot_time
        try:
            idle_sec = psutil.cpu_times().idle
        except:
            idle_sec = 0 # Fallback
        
        # 5. Processes & Top 3
        procs_total = 0
        procs_running = 0
        procs_sleeping = 0
        
        proc_list = []
        for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
            try:
                procs_total += 1
                if p.info['status'] == psutil.STATUS_RUNNING: procs_running += 1
                elif p.info['status'] == psutil.STATUS_SLEEPING: procs_sleeping += 1
                proc_list.append(p.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort Top 3 CPU
        top_cpu = sorted(proc_list, key=lambda p: p['cpu_percent'] or 0, reverse=True)[:3]
        top_cpu_str = " | ".join([f"{p['name']}({p['cpu_percent']}%)" for p in top_cpu])

        # Sort Top 3 Memory
        top_mem = sorted(proc_list, key=lambda p: p['memory_percent'] or 0, reverse=True)[:3]
        top_mem_str = " | ".join([f"{p['name']}({round(p['memory_percent'],1)}%)" for p in top_mem])

        return [
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            cpu_usage,
            round(load_avg[0], 2), round(load_avg[1], 2), round(load_avg[2], 2),
            round(mem.total/1e9, 2), round(mem.available/1e9, 2), round(mem.used/1e9, 2), mem.percent,
            round(disk.total/1e9, 2), round(disk.free/1e9, 2), disk.percent,
            round(uptime_sec, 2), round(idle_sec, 2),
            procs_total, procs_running, procs_sleeping,
            top_cpu_str, top_mem_str
        ]

    def log_metrics(self):
        metrics = self.get_metrics()
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(metrics)
        print(f"[SYS MONITOR] CPU: {metrics[1]}% | Mem: {metrics[8]}% | Procs: {metrics[14]}")
        return metrics