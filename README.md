This module repeatedly synchronizes a replica directory with a source directory, including all files and subdirectories.

It needs 4 arguments:
-   src_path: the source directory path, must already exist
-   rep_path: the replica directory path, must already exist
-   delay: the amount of seconds between two updates
-   log_path: the log file path, created in the given directory at first run if not existing

Can be used as a standalone script:
```
python synchronizer.py src_path rep_path delay_sec log_path
```
