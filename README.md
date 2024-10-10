# File Tree Scanner Script for Large-Scale Data
This Python script efficiently generates a file tree and outputs a CSV manifest of all files, including their paths, sizes, last modified timestamps, and last accessed timestamps. The script uses multi-threading and the `scandir` function to handle very large datasets across potentially millions of files.

## Features
- **Efficient Directory Scanning**: Utilizes `os.scandir` for faster directory traversal.
- **Multi-threading**: Uses `concurrent.futures.ThreadPoolExecutor` to parallelize directory scanning and maximize CPU usage.
- **Organized Output**: Outputs a CSV file with the following columns:
  - `path`: Full path of the file.
  - `size`: Size of the file in bytes.
  - `last_modified`: Last modification time in `YYYY-MM-DD HH:MM:SS` format.
  - `last_accessed`: Last access time in `YYYY-MM-DD HH:MM:SS` format.
- **Error Handling**: Gracefully handles permission errors and skips inaccessible files or directories.
- **Scalable**: Designed for large-scale data environments, capable of handling PB-scale data efficiently.

## Requirements
- Python 3.6+
- No external dependencies (standard library only)

## Usage

### 1. Clone or copy the script
Save the script to your local machine with a `.py` extension.

### 2. Run the script
```bash
python file_tree_scanner.py
