import threading
import os 
import time
import psutil
from modules.directory_monitor import DirectoryMonitor
from modules.system_metrics import SystemMonitor
from modules.visualizer import generate_summary

# Configuration Paths
WATCH_DIR = "./monitored_folder"
LOG_DIR = "./logs"
DIR_LOG = os.path.join(LOG_DIR, "dir_log.csv")
SYS_LOG = os.path.join(LOG_DIR, "sys_log.csv")
REPORT_FILE = os.path.join(LOG_DIR, "final_report.txt")

# Ensure directories exist
os.makedirs(WATCH_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def run_dir_monitor(stop_event):
    monitor = DirectoryMonitor(WATCH_DIR, DIR_LOG)
    print("--- Directory Monitor Running (1s Check) ---")
    while not stop_event.is_set():
        monitor.check_changes()
        time.sleep(1) 

def run_sys_monitor(stop_event):
    monitor = SystemMonitor(SYS_LOG)
    # Prime CPU counter
    psutil.cpu_percent(interval=None)
    print("--- System Monitor Running (5s Check) ---")
    while not stop_event.is_set():
        monitor.log_metrics()
        generate_summary(DIR_LOG, SYS_LOG, REPORT_FILE)
        time.sleep(5) 

if __name__ == "__main__":
    stop_event = threading.Event()

    t1 = threading.Thread(target=run_dir_monitor, args=(stop_event,))
    t2 = threading.Thread(target=run_sys_monitor, args=(stop_event,))

    try:
        t1.start()
        t2.start()
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping Monitors...")
        stop_event.set()
        t1.join()
        t2.join()
        print("System Stopped. Check ./logs for report.")