import threading
import time
import psutil
from modules.directory_monitor import DirectoryMonitor
from modules.system_metrics import SystemMonitor
from modules.visualizer import generate_report

def run_dir_monitor(stop_event):
    monitor = DirectoryMonitor("./monitored_folder")
    print("--- Directory Monitor Running ---")
    while not stop_event.is_set():
        monitor.scan()
        time.sleep(1) # Check every second

def run_sys_monitor(stop_event):
    monitor = SystemMonitor("system_log.csv")
    # Prime CPU counter
    psutil.cpu_percent()
    print("--- System Monitor Running ---")
    while not stop_event.is_set():
        monitor.log_data()
        monitor.show_top_processes()
        generate_report("system_log.csv") # Update chart
        time.sleep(5) # Check every 5 seconds

if __name__ == "__main__":
    # Create a stop event to kill threads safely
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
        print("\nStopping...")
        stop_event.set()
        t1.join()
        t2.join()
        print("Goodbye.")
