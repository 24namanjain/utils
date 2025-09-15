# File Organizer

A robust Python script that organizes files in a directory by their creation date using a GUI interface with comprehensive error handling and user confirmation.

## ✨ Features

- **GUI File Selection**: Uses tkinter to select source directory
- **Smart Date Detection**: Uses actual file creation time when available, falls back to modification time
- **File Preview**: Shows what files will be organized before proceeding
- **User Confirmation**: Asks for confirmation before moving any files
- **Duplicate Handling**: Automatically handles duplicate filenames with numbering
- **Progress Tracking**: Real-time progress display with 1-based indexing
- **Comprehensive Error Handling**: Graceful handling of permission errors, missing files, etc.
- **Operation Summary**: Detailed report of successful and failed operations
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Setup

1. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies** (none required - uses standard library only):
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Usage

Run the script:
```bash
python organize_files_in_dir.py
```

### What happens:
1. **Directory Selection**: A file dialog opens to select the directory you want to organize
2. **File Preview**: The script scans the directory and shows you:
   - How many files will be organized
   - Which files will go into which date folders
   - Sample of files with their creation dates
3. **Confirmation**: You can review the preview and confirm or cancel the operation
4. **Organization**: Files are moved into subdirectories named by their creation date (e.g., "202401" for January 2024)
5. **Summary**: A detailed report shows successful moves, failures, and any errors

### Example Output:
```
File Organizer - Organize files by creation date
==================================================
Source Directory: /Users/username/Downloads
Total items found: 15
--------------------------------------------------
[  1/ 15] ✅ Moved: photo1.jpg → 202401/
[  2/ 15] ✅ Moved: document.pdf → 202402/
[  3/ 15] ✅ Moved: video.mp4 → 202401/
...

==================================================
ORGANIZATION SUMMARY
==================================================
✅ Successfully moved: 12 files
❌ Failed to move: 0 files
```

## 🛡️ Safety Features

- **No Data Loss**: Files are moved (not copied) but with duplicate handling
- **User Confirmation**: Always asks before making changes
- **Error Recovery**: Continues processing even if some files fail
- **Detailed Logging**: Shows exactly what happened to each file
- **Permission Handling**: Gracefully handles files that can't be moved

## 📁 File Organization

Files are organized into folders named by their creation date:
- Format: `YYYYMM` (e.g., `202401` for January 2024)
- Based on actual file creation time when available
- Falls back to modification time if creation time unavailable
- Duplicate filenames are automatically renamed (e.g., `file_1.txt`, `file_2.txt`)

## 🔧 Requirements

- **Python 3.6+**
- **tkinter** (included with Python)
- **Standard library modules**: os, stat, datetime, shutil, typing

## 🐛 Troubleshooting

### Common Issues:
- **"No files found"**: The directory might be empty or contain only folders
- **Permission errors**: Some files might be in use or protected
- **GUI not working**: Make sure you're running in an environment that supports tkinter

### Error Messages:
The script provides detailed error messages for any issues encountered, including:
- File access permissions
- Directory not found
- File in use by another program
- Disk space issues

## 📝 License

This script is provided as-is for educational and personal use.