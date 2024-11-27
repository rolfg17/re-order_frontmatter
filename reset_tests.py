#!/usr/bin/env python3
"""
Reset Test Files

This script restores test Markdown files to their original state from a backup directory.
It's used in conjunction with the frontmatter reordering script to facilitate testing.

The script:
1. Removes all .md files from the test directory
2. Copies fresh versions from the backup directory
3. Reports which files were restored

Directory Structure:
    test_files/      - Directory containing active test files
    test_files-copy/ - Backup directory with original versions

Usage:
    ./reset_tests.py
"""

import os
import shutil
from pathlib import Path

# Get the absolute path of the script's directory
SCRIPT_DIR = Path(__file__).parent.absolute()
TEST_DIR = SCRIPT_DIR / "test_files"
BACKUP_DIR = SCRIPT_DIR / "test_files-copy"

def reset_test_files():
    """
    Reset test files to their original state from backup.
    
    This function:
    1. Checks if the backup directory exists
    2. Creates the test directory if needed
    3. Removes existing test files
    4. Copies fresh versions from backup
    
    Returns:
        bool: True if reset was successful, False otherwise
    """
    # Ensure directories exist
    if not BACKUP_DIR.exists():
        print(f"Error: Backup directory {BACKUP_DIR} does not exist!")
        return False
    
    # Create test directory if it doesn't exist
    TEST_DIR.mkdir(exist_ok=True)
    
    # Remove all files in test directory
    for file in TEST_DIR.glob("*.md"):
        file.unlink()
    
    # Copy all markdown files from backup to test directory
    copied = 0
    for src in BACKUP_DIR.glob("*.md"):
        dst = TEST_DIR / src.name
        shutil.copy2(src, dst)
        copied += 1
        print(f"Restored: {src.name}")
    
    print(f"\nReset complete: {copied} files restored")
    return True

if __name__ == "__main__":
    reset_test_files()
