"""
A utility script for resetting test directories to a known state.

This script provides functionality to reset a test directory by copying files from a cleanup
(source) directory. It's particularly useful in testing scenarios where you need to ensure
a consistent starting state for your tests.

The script:
- Removes all existing content in the test directory
- Creates the test directory if it doesn't exist
- Copies all files and directories from the cleanup directory to the test directory
- Preserves the directory structure during copying

Example:
    To use this script directly:
    
    ```python
    python cleanup-copy.py
    ```
    
    The script uses predefined TEST_DIR and CLEANUP_DIR paths when run directly.
    
    To use as a module:
    
    ```python
    from cleanup_copy import reset_test_directory
    
    reset_test_directory('/path/to/test', '/path/to/cleanup')
    ```
"""

import os
import shutil



def reset_test_directory(test_dir, cleanup_dir):
    """
    Reset the test directory by copying files from the cleanup directory.
    
    This function performs a complete reset of the test directory:
    1. Removes all existing content in the test directory
    2. Creates the test directory if it doesn't exist
    3. Copies all files and directories from the cleanup directory
    
    Args:
        test_dir (str): Path to the test directory to reset. Will be created
            if it doesn't exist.
        cleanup_dir (str): Path to the cleanup directory containing the original
            files to copy from.
            
    Raises:
        FileNotFoundError: If the cleanup directory doesn't exist.
        
    Example:
        >>> reset_test_directory('/path/to/test', '/path/to/cleanup')
        Test directory '/path/to/test' has been reset from '/path/to/cleanup'.
    """
    # Ensure cleanup directory exists
    if not os.path.exists(cleanup_dir):
        raise FileNotFoundError(f"Cleanup directory '{cleanup_dir}' does not exist.")

    # Remove all contents of the test directory
    if os.path.exists(test_dir):
        for item in os.listdir(test_dir):
            item_path = os.path.join(test_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        os.makedirs(test_dir)  # Create test directory if it doesn't exist

    # Copy files from cleanup directory to test directory
    for item in os.listdir(cleanup_dir):
        src_path = os.path.join(cleanup_dir, item)
        dest_path = os.path.join(test_dir, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            shutil.copy(src_path, dest_path)

    print(f"Test directory '{test_dir}' has been reset from '{cleanup_dir}'.")

# Example Usage
if __name__ == "__main__":
    # Example paths - modify these according to your setup
    TEST_DIR = './test'  # Directory to be reset
    CLEANUP_DIR = './test-cleanup'  # Source directory with original files
    reset_test_directory(TEST_DIR, CLEANUP_DIR)