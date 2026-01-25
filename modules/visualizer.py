import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_summary(dir_log, sys_log, output_report):
    if not os.path.exists(sys_log):
        return

    try:
        # Load System Data
        sys_df = pd.read_csv(sys_log)
        
        # Load Directory Data (Handle empty/missing file safely)
        file_changes = 0
        if os.path.exists(dir_log) and os.path.getsize(dir_log) > 0:
            try:
                dir_df = pd.read_csv(dir_log)
                file_changes = len(dir_df)
            except: pass

        # Fix Dates
        if 'Timestamp' in sys_df.columns:
            sys_df['Timestamp'] = pd.to_datetime(sys_df['Timestamp'])

        # --- CALCULATE STATISTICS (Required for Assignment) ---
        # We use 'if' checks so it doesn't crash if a column is missing
        avg_cpu = sys_df["CPU_Usage"].mean() if "CPU_Usage" in sys_df.columns else 0
        max_mem = sys_df["Mem_Percent"].max() if "Mem_Percent" in sys_df.columns else 0
        
        # Get Uptime from the last row
        uptime = 0
        if "Uptime_Sec" in sys_df.columns and not sys_df.empty:
            uptime = sys_df["Uptime_Sec"].iloc[-1] / 3600 # Convert seconds to hours

        # --- GENERATE GRAPH ---
        plt.figure(figsize=(10, 5))
        if "CPU_Usage" in sys_df.columns:
            plt.plot(sys_df['Timestamp'], sys_df['CPU_Usage'], label='CPU %', color='blue')
        if "Mem_Percent" in sys_df.columns:
            plt.plot(sys_df['Timestamp'], sys_df['Mem_Percent'], label='Memory %', color='green')
            
        plt.title('System Resource Usage')
        plt.xlabel('Time')
        plt.ylabel('Percent (%)')
        plt.legend()
        plt.grid(True)
        plt.gcf().autofmt_xdate()
        
        plot_path = os.path.join(os.path.dirname(output_report), 'performance_plot.png')
        plt.savefig(plot_path)
        plt.close()

        # --- WRITE DETAILED REPORT ---
        with open(output_report, 'w') as f:
            f.write("=== LINUX MONITORING GROUP REPORT ===\n")
            f.write(f"Total Log Entries: {len(sys_df)}\n")
            f.write(f"System Uptime: {uptime:.2f} Hours\n")
            f.write("-------------------------------------\n")
            f.write(f"Avg CPU Usage: {avg_cpu:.2f}%\n")
            f.write(f"Max Memory Usage: {max_mem:.2f}%\n")
            f.write(f"Total File Changes Detected: {file_changes}\n")
            f.write("-------------------------------------\n")
            f.write("Visualisation saved to 'logs/performance_plot.png'\n")

        print(f"Report updated: {output_report}")

    except Exception as e:
        print(f"Error generating report: {e}")