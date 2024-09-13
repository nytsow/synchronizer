# Intro
This module permits to synchronize a replica directory with a source directory, including all files and subdirectories.
The user specifies the duration between each verification.

# Dependencies
This module only depends on the schedule module to be installed:
```
pip install schedule
```

# Details
This module repeatedly synchronizes a replica directory with a source directory, including all files and subdirectories.

It implements a class _synchronizer_ that needs 4 arguments:
-   src_path: the source directory path, must already exist
-   rep_path: the replica directory path, must already exist
-   delay: the amount of seconds between two updates
-   log_path: the log file path, created in the given directory at first run if not existing

# Usage
Can be used as a standalone script:
```
python synchronizer.py src_path rep_path delay_sec log_path
```
Or by Python code:
```
try:
    sync = synchronizer(src_path, rep_path, delay, log_path)
except Exception as exception:
    print(str(exception))  # Handle exception here
    exit()
sync.start()
```
