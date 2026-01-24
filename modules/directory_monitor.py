import os
import csv
import time
import grp  # Required for Group Name
import pwd  # Required for Owner Name
from pathlib import Path
from datetime import datetime

class DirectoryMonitor:
    def __init__(self, watch_dir, log_file):
        self.watch_dir = Path(watch_dir)
        self.log_file = log_file
        self.previous_state = self._scan_directory()
        
        # Initialize Log File with Assignment-Required Headers
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "Event", "Filename", "Type", 
                    "Size", "Perms", "Owner", "Group", 
                    "Created_Time", "Modified_Time", "Accessed_Time"
                ])

    def _get_file_info(self, filepath):
        try:
            stats = filepath.stat()
            
            # File Type Logic
            if filepath.is_dir(): ftype = "Directory"
            elif filepath.is_symlink(): ftype = "Symlink"
            else: ftype = "File"
            
            # Get Owner & Group Names
            try:
                owner_name = pwd.getpwuid(stats.st_uid).pw_name
                group_name = grp.getgrgid(stats.st_gid).gr_name
            except KeyError:
                owner_name = str(stats.st_uid)
                group_name = str(stats.st_gid)

            return {
                "size": stats.st_size,
                "type": ftype,
                "perm": oct(stats.st_mode)[-3:],
                "owner": owner_name,
                "group": group_name,
                "ctime": time.ctime(stats.st_ctime),
                "mtime": time.ctime(stats.st_mtime),
                "atime": time.ctime(stats.st_atime),
                "raw_mtime": stats.st_mtime # for comparison
            }
        except FileNotFoundError:
            return None

    def _scan_directory(self):
        current_state = {}
        if not self.watch_dir.exists():
            return current_state
        for entry in self.watch_dir.iterdir():
            info = self._get_file_info(entry)
            if info:
                current_state[entry.name] = info
        return current_state

    def log_event(self, event_type, filename, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, event_type, filename, 
                details.get("type"), details.get("size"), details.get("perm"),
                details.get("owner"), details.get("group"),
                details.get("ctime"), details.get("mtime"), details.get("atime")
            ])
        print(f"[DIR MONITOR] {event_type}: {filename}")

    def check_changes(self):
        current_state = self._scan_directory()
        
        # Check Created/Modified
        for filename, info in current_state.items():
            if filename not in self.previous_state:
                self.log_event("CREATED", filename, info)
            elif info['raw_mtime'] != self.previous_state[filename]['raw_mtime']:
                self.log_event("MODIFIED", filename, info)
                
        # Check Deleted
        for filename in list(self.previous_state.keys()):
            if filename not in current_state:
                self.log_event("DELETED", filename, self.previous_state[filename])

        self.previous_state = current_state