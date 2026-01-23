import pandas as pd
import matplotlib.pyplot as plt
import os

def generate_report(csv_file):
    if not os.path.exists(csv_file):
        print("Waiting for data...")
        return

        try:
            # Load data
            df = pd.read_csv(csv_file)

            # Fix Dates
            df = pd.to_datetime(df)

            # Setup Plot
            plt.figure(figsize=(10, 5))

            # Draw Lines
            plt.plot(df, df['CPU_Usage'], label='CPU %', color='blue')
            plt.plot(df, df, label='Disk %', color='red')

            # Formatting
            plt.title('System Health')
            plt.xlabel('Time')
            plt.ylabel('Usage %')
            plt.legend()
            plt.grid(True)
            plt.gcf().autofmt_xdate()

            # Save Plot
            plt.savefig('system_health_report.png')
            print("Report generated: system_health_report.png")
            plt.close()

        except Exception as e:
            print(f"Error generating report: {e}")