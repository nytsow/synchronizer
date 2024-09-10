import sys, os, shutil, filecmp, time, schedule
from datetime import datetime

# source path: C:\Users\alexa\OneDrive\Documents\Dev\Tests\python\synchronizer\testDir1
# replica path: C:\Users\alexa\OneDrive\Documents\Dev\Tests\python\synchronizer\testDir2
# log path: C:\Users\alexa\OneDrive\Documents\Dev\Tests\python\synchronizer\synchronizer.log
# python synchronizer.py C:\Users\alexa\OneDrive\Documents\Dev\Tests\python\synchronizer\testDir1 C:\Users\alexa\OneDrive\Documents\Dev\Tests\python\synchronizer\testDir2 10 C:\Users\alexa\OneDrive\Documents\Dev\Tests\python\synchronizer\synchronizer.log

class synchronizer():
    """This module repeatedly synchronizes a replica directory with a source directory, including all files and subdirectories.

It needs 4 arguments:
-   src_path: the source directory path, must already exist
-   rep_path: the replica directory path, must already exist
-   delay: the amount of seconds between two updates
-   log_path: the log file path, created in the given directory at first run if not existing
"""

    def __init__(self, src_path, rep_path, delay, log_path):
        # Sanitization.
        if os.path.exists(src_path):
            self.src_path = src_path
        else:
            raise Exception("src_path does not exist")
        if os.path.exists(rep_path):
            self.rep_path = rep_path
        else:
            raise Exception("rep_path does not exist")
        if rep_path == src_path:
            raise Exception("src_path and rep_path must be different")
        if delay.isnumeric():
            self.delay = int(delay)
        else:
            raise Exception("delay must be an integer")
        if os.path.isdir(os.path.dirname(log_path)):
            self.log_path = log_path
        else:
            raise Exception("log_path directory does not exist")
        
        self.log_file = None

    def start(self):
        self.start_log()
        schedule.every(sync.delay).seconds.do(sync.explore_top_dir)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def explore_top_dir(self):
        # Open the log file.
        self.log_file = open(self.log_path, "a")
        self.start_update_log("Start update")
        # We already know both directories are existing. No more checks on this level. Start exploration.
        self.explore_dir(self.src_path, self.rep_path, os.path.basename(self.src_path), os.path.basename(self.rep_path))
        # Close the log file.
        self.log_file.close()

    def explore_dir(self, src_path, rep_path, src_dir, rep_dir):
        # List source directory content (files and subdirectories).
        src_content_list = os.listdir(src_path)
        # List replica directory content (files and subdirectories), as we know at this step it exists.
        # We will use it only for checking if content in replica is no more in source as has to be deleted.
        rep_content_list = os.listdir(rep_path)
        
        for src_content in src_content_list:
            src_content_path = os.path.join(src_path, src_content)
            rep_content_path = os.path.join(rep_path, src_content)
            # Manage subdirectory.
            if os.path.isdir(src_content_path):
                # Check if it already is in replica.
                if os.path.exists(rep_content_path):
                    # Explore the subdirectory.
                    self.explore_dir(src_content_path, rep_content_path, os.path.join(src_dir, src_content), os.path.join(rep_dir, src_content))
                else:
                    # Copy the subdirectory, with all subdirectories and files with metadata (use shutil.copy2 by default).
                    shutil.copytree(src_content_path, rep_content_path)
                    self.insert_log(f"Copy of directory {os.path.join(src_dir, src_content)}")
            # Manage file.
            else:
                # Check if it already is in replica, through metadata comparison.
                # Note: filecmp.cmp with shallow=True by default, must be enough for basic usage.
                if (not os.path.exists(rep_content_path)
                    or not filecmp.cmp(rep_content_path, src_content_path)):
                    # Copy the file, with metadata, overwriting file if existing.
                    shutil.copy2(src_content_path, rep_path)
                    self.insert_log(f"Copy of file {os.path.join(src_dir, src_content)}")
            # Mark as treated by removing from replica content list.
            if src_content in rep_content_list:
                rep_content_list.remove(src_content)

        # Check if remaining content in replica is listed, meaning it is no more in source.
        for rep_content in rep_content_list:
            rep_content_path = os.path.join(rep_path, rep_content)
            # Manage subdirectory.
            if os.path.isdir(rep_content_path):
                shutil.rmtree(rep_content_path)
                self.insert_log(f"Removal of directory {os.path.join(rep_dir, rep_content)}")
            # Manage file.
            else:
                self.insert_log(f"Removal of file {os.path.join(rep_dir, rep_content)}")
                os.remove(rep_content_path)

    def start_log(self):
        print(f"- The synchronizer starts from now, updating replica directory at each {sync.delay} seconds. Press CTRL+C to stop.")
        self.log_file = open(self.log_path, "a")
        self.log_file.write("- Synchronizer start\n")
        self.log_file.close()

    def start_update_log(self, msg):
        msg = "-- " + datetime.now().strftime('%d/%m/%Y, %H:%M:%S') + ": " + msg
        print(msg)
        self.log_file.write(msg + "\n")

    def insert_log(self, msg):
        msg = "--- " + msg
        print(msg)
        self.log_file.write(msg + "\n")

if __name__ == "__main__":
    if len(sys.argv) == 5:
        try:
            sync = synchronizer(*sys.argv[1:])
        except Exception as exception:
            print("\n" + str(exception) + ", please check the doc:\n\n" + synchronizer.__doc__)
            exit()
        sync.start()
    else:
        print("\n4 arguments are required, please check the doc:\n\n" + synchronizer.__doc__)