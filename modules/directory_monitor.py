import os
import time
from pathlib import Path
from datetime import datetime

class DirectoryMonitor:
    def __init__(self, directory_path):
        self.path = Path(directory_path)
        if not self.path.exists():
            self.path.mkdir(parents=True)
        self.files_snapshot = self.take_snapshot()

    def take_snapshot(self):
        """Creates a dictionary {filename: modification_time}"""
        snapshot = {}
        # rglob('*') scans subdirectories too
        for file in self.path.rglob('*'):
            if file.is_file():
                snapshot[str(file)] = file.stat().st_mtime
        return snapshot

    def scan(self):
        current_snapshot = self.take_snapshot()
        
        # Set logic to find differences
        old_set = set(self.files_snapshot.keys())
        new_set = set(current_snapshot.keys())

        # 1. Created
        created = new_set - old_set
        for f in created:
            self.log_event("CREATED", f)

        # 2. Deleted
        deleted = old_set - new_set
        for f in deleted:
            print(f" File Deleted: {f}")

        # 3. Modified (Same file, different time)
        common = old_set.intersection(new_set)
        for f in common:
            if self.files_snapshot[f]!= current_snapshot[f]:
                self.log_event("MODIFIED", f)

        # Update snapshot for next loop
        self.files_snapshot = current_snapshot

    def log_event(self, event_type, filepath):
        # Extract Metadata as required
        path_obj = Path(filepath)
        stats = path_obj.stat()
        print(f" {event_type}: {filepath}")
        print(f"   -> Size: {stats.st_size} bytes")
        print(f"   -> Owner ID: {stats.st_uid}")
