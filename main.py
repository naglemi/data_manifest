import os
import csv
import concurrent.futures
from pathlib import Path
import time

# Function to scan a single directory
def scan_directory(directory):
    entries = []
    try:
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_file(follow_symlinks=False):
                    try:
                        stats = entry.stat(follow_symlinks=False)
                        entries.append({
                            'path': entry.path,
                            'size': stats.st_size,
                            'last_modified': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(stats.st_mtime)),
                            'last_accessed': time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(stats.st_atime))
                        })
                    except Exception as e:
                        # Log error if needed (e.g. permission denied)
                        continue
    except Exception as e:
        # Log permission denied or other issues
        pass
    return entries

# Function to get all subdirectories
def get_subdirs(directory):
    subdirs = []
    try:
        with os.scandir(directory) as it:
            for entry in it:
                if entry.is_dir(follow_symlinks=False):
                    subdirs.append(entry.path)
    except Exception as e:
        pass
    return subdirs

# Multi-threaded function to scan all directories
def scan_all_directories(root_dir, output_file):
    # Open CSV file for output
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['path', 'size', 'last_modified', 'last_accessed'])
        writer.writeheader()

        # Use a thread pool for efficient directory scanning
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            future_to_dir = {executor.submit(scan_directory, root_dir): root_dir}
            
            while future_to_dir:
                done, _ = concurrent.futures.wait(future_to_dir, return_when=concurrent.futures.FIRST_COMPLETED)

                for future in done:
                    directory = future_to_dir[future]
                    del future_to_dir[future]
                    
                    # Write file entries to CSV
                    try:
                        entries = future.result()
                        for entry in entries:
                            writer.writerow(entry)
                    except Exception as e:
                        # Handle errors, e.g. permission issues
                        pass
                    
                    # Add subdirectories to scan
                    subdirs = get_subdirs(directory)
                    for subdir in subdirs:
                        future_to_dir[executor.submit(scan_directory, subdir)] = subdir

if __name__ == "__main__":
    # Define the root directory and output CSV file
    root_directory = '/'  # Start from the root directory; change as needed
    output_csv = 'file_manifest.csv'

    # Start the scan
    scan_all_directories(root_directory, output_csv)
