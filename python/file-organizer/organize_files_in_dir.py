#!/usr/bin/python3

"""
Python script which uses tkinter and os functions to organize files 
in separate directories by their creation date.
"""

import os
import stat
from datetime import datetime
import shutil
from tkinter import filedialog, messagebox
from typing import Optional, Tuple


def get_files_src_dir() -> Optional[str]:
    """
    Select and return the selected directory.
    
    Returns:
        str: Path to selected directory, or None if cancelled
    """
    directory = filedialog.askdirectory(title="Select a directory to organize")
    if not directory:
        print("No directory selected. Exiting...")
        return None
    return directory


def get_file_creation_date(file_path: str) -> datetime:
    """
    Get the actual creation date of the file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        datetime: Creation date of the file
    """
    try:
        # Try to get creation time (works on Windows and some Unix systems)
        if hasattr(os.stat(file_path), 'st_birthtime'):
            creation_time = os.stat(file_path).st_birthtime
        else:
            # Fallback to modification time if creation time not available
            creation_time = os.path.getmtime(file_path)
        return datetime.fromtimestamp(creation_time)
    except (OSError, IOError) as e:
        print(f"Warning: Could not get creation date for {file_path}: {e}")
        # Fallback to current time
        return datetime.now()


def get_file_preview(src_dir: str) -> Tuple[list, int]:
    """
    Get a preview of files that will be organized.
    
    Args:
        src_dir (str): Source directory path
        
    Returns:
        Tuple[list, int]: List of file info tuples and total file count
    """
    try:
        directory_contents = os.listdir(src_dir)
        files_to_organize = []
        
        for item in directory_contents:
            item_path = os.path.join(src_dir, item)
            if os.path.isfile(item_path):
                try:
                    creation_date = get_file_creation_date(item_path)
                    date_folder = creation_date.strftime("%Y%m")
                    files_to_organize.append((item, date_folder, creation_date.strftime("%Y-%m-%d")))
                except Exception as e:
                    print(f"Warning: Could not process {item}: {e}")
        
        return files_to_organize, len(files_to_organize)
    except OSError as e:
        print(f"Error reading directory {src_dir}: {e}")
        return [], 0


def confirm_operation(files_info: list, total_files: int) -> bool:
    """
    Show confirmation dialog with file preview.
    
    Args:
        files_info (list): List of file information tuples
        total_files (int): Total number of files
        
    Returns:
        bool: True if user confirms, False otherwise
    """
    if total_files == 0:
        messagebox.showinfo("No Files", "No files found to organize in the selected directory.")
        return False
    
    # Create preview message
    preview_lines = [f"Found {total_files} files to organize:"]
    preview_lines.append("")
    
    # Group files by destination folder
    folder_groups = {}
    for filename, folder, date in files_info:
        if folder not in folder_groups:
            folder_groups[folder] = []
        folder_groups[folder].append((filename, date))
    
    for folder in sorted(folder_groups.keys()):
        preview_lines.append(f"📁 {folder}/ ({len(folder_groups[folder])} files)")
        for filename, date in folder_groups[folder][:3]:  # Show first 3 files
            preview_lines.append(f"   • {filename} (created: {date})")
        if len(folder_groups[folder]) > 3:
            preview_lines.append(f"   ... and {len(folder_groups[folder]) - 3} more files")
        preview_lines.append("")
    
    preview_text = "\n".join(preview_lines)
    
    # Show confirmation dialog
    result = messagebox.askyesno(
        "Confirm File Organization",
        f"{preview_text}\n\nDo you want to proceed with organizing these files?",
        icon='question'
    )
    
    return result


def organize_files(src_dir: str) -> Tuple[int, int, list]:
    """
    Organize files in the source directory by creation date.
    
    Args:
        src_dir (str): Source directory path
        
    Returns:
        Tuple[int, int, list]: (successful_moves, failed_moves, error_messages)
    """
    try:
        directory_contents = os.listdir(src_dir)
        successful_moves = 0
        failed_moves = 0
        error_messages = []
        
        print(f"Source Directory: {src_dir}")
        print(f"Total items found: {len(directory_contents)}")
        print("-" * 50)
        
        for i, item in enumerate(directory_contents, 1):
            src_file_path = os.path.join(src_dir, item)
            
            # Skip if not a file
            if not os.path.isfile(src_file_path):
                print(f"[{i:3d}/{len(directory_contents)}] Skipping (not a file): {item}")
                continue
            
            try:
                # Get creation date and create destination folder
                creation_date = get_file_creation_date(src_file_path)
                destination_folder = creation_date.strftime("%Y%m")
                destination_directory = os.path.join(src_dir, destination_folder)
                
                # Create destination directory if it doesn't exist
                os.makedirs(destination_directory, exist_ok=True)
                
                # Create destination file path
                dest_file_path = os.path.join(destination_directory, item)
                
                # Check if destination file already exists
                if os.path.exists(dest_file_path):
                    # Handle duplicate files
                    base_name, ext = os.path.splitext(item)
                    counter = 1
                    while os.path.exists(dest_file_path):
                        new_name = f"{base_name}_{counter}{ext}"
                        dest_file_path = os.path.join(destination_directory, new_name)
                        counter += 1
                
                # Move the file
                shutil.move(src_file_path, dest_file_path)
                successful_moves += 1
                print(f"[{i:3d}/{len(directory_contents)}] ✅ Moved: {item} → {destination_folder}/")
                
            except Exception as e:
                failed_moves += 1
                error_msg = f"Failed to move {item}: {str(e)}"
                error_messages.append(error_msg)
                print(f"[{i:3d}/{len(directory_contents)}] ❌ {error_msg}")
        
        return successful_moves, failed_moves, error_messages
        
    except OSError as e:
        error_msg = f"Error accessing directory {src_dir}: {str(e)}"
        print(error_msg)
        return 0, 0, [error_msg]


def show_summary(successful_moves: int, failed_moves: int, error_messages: list):
    """
    Show operation summary.
    
    Args:
        successful_moves (int): Number of successful file moves
        failed_moves (int): Number of failed file moves
        error_messages (list): List of error messages
    """
    print("\n" + "=" * 50)
    print("ORGANIZATION SUMMARY")
    print("=" * 50)
    print(f"✅ Successfully moved: {successful_moves} files")
    print(f"❌ Failed to move: {failed_moves} files")
    
    if error_messages:
        print("\nError Details:")
        for error in error_messages:
            print(f"  • {error}")
    
    # Show GUI summary
    if successful_moves > 0 and failed_moves == 0:
        messagebox.showinfo("Success", f"Successfully organized {successful_moves} files!")
    elif successful_moves > 0 and failed_moves > 0:
        messagebox.showwarning(
            "Partial Success", 
            f"Organized {successful_moves} files successfully.\n{failed_moves} files failed to move."
        )
    else:
        messagebox.showerror("Error", "No files were organized successfully.")


def main():
    """
    Main function to organize files by creation date.
    """
    print("File Organizer - Organize files by creation date")
    print("=" * 50)
    
    # Get source directory
    src_dir = get_files_src_dir()
    if not src_dir:
        return
    
    # Validate directory exists
    if not os.path.exists(src_dir):
        messagebox.showerror("Error", f"Directory does not exist: {src_dir}")
        return
    
    if not os.path.isdir(src_dir):
        messagebox.showerror("Error", f"Path is not a directory: {src_dir}")
        return
    
    # Get file preview and confirm operation
    files_info, total_files = get_file_preview(src_dir)
    
    if not confirm_operation(files_info, total_files):
        print("Operation cancelled by user.")
        return
    
    # Organize files
    print("\nStarting file organization...")
    successful_moves, failed_moves, error_messages = organize_files(src_dir)
    
    # Show summary
    show_summary(successful_moves, failed_moves, error_messages)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
