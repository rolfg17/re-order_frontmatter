#!/usr/bin/env python3
"""
Markdown Frontmatter Reorderer

This script reorders YAML frontmatter in Markdown files according to configurable rules.
It allows specifying which keys should appear at the top and bottom of the frontmatter,
with support for wildcard patterns. The script only processes markdown files in the 
specified directory (not in subdirectories).

Configuration is read from a JSON file (default: frontmatter_config.json) with format:
{
    "top_keys": ["key1", "key2"],
    "bottom_keys": ["pattern.*"]
}

Usage:
    ./reorder_frontmatter.py directory_path [--config config_file.json]

Example:
    ./reorder_frontmatter.py ./my_markdown_files --config custom_config.json

Note:
    Only processes .md files directly in the specified directory.
    Does not traverse into subdirectories.
"""

import argparse
import json
import os
import re
import yaml
import fnmatch
from typing import Dict, List, Tuple

def load_config(config_path: str) -> Tuple[List[str], List[str]]:
    """
    Load the configuration file containing top and bottom keys.
    If the config file doesn't exist, return empty lists for both top and bottom keys.
    
    Args:
        config_path: Path to the JSON configuration file
        
    Returns:
        Tuple of (top_keys, bottom_keys) lists
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get('top_keys', []), config.get('bottom_keys', [])
    except FileNotFoundError:
        print(f"Warning: Configuration file '{config_path}' not found.")
        print("Using default configuration (no reordering will occur).")
        return [], []
    except json.JSONDecodeError:
        print(f"Warning: Configuration file '{config_path}' is not valid JSON.")
        print("Using default configuration (no reordering will occur).")
        return [], []
    except Exception as e:
        print(f"Warning: Error reading configuration file: {str(e)}")
        print("Using default configuration (no reordering will occur).")
        return [], []

def extract_frontmatter(content: str) -> Tuple[Dict, str, bool]:
    """
    Extract YAML frontmatter from markdown content.
    
    Args:
        content: Complete markdown file content
        
    Returns:
        Tuple of (frontmatter_dict, remaining_content, has_frontmatter)
        where has_frontmatter indicates if valid frontmatter was found
    """
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content, False
    
    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return {}, content, False
        return frontmatter, match.group(2), True
    except yaml.YAMLError:
        return {}, content, False

def matches_pattern(key: str, patterns: List[str]) -> bool:
    """
    Check if a key matches any of the given patterns (with wildcards).
    
    Args:
        key: The frontmatter key to check
        patterns: List of patterns (supporting wildcards) to match against
        
    Returns:
        True if the key matches any pattern, False otherwise
    """
    return any(fnmatch.fnmatch(key, pattern) for pattern in patterns)

def reorder_frontmatter(frontmatter: Dict, top_keys: List[str], bottom_keys: List[str]) -> Dict:
    """
    Reorder frontmatter according to specified top and bottom keys, supporting wildcards.
    
    Args:
        frontmatter: Original frontmatter dictionary
        top_keys: List of keys to appear at the top (exact matches)
        bottom_keys: List of keys to appear at the bottom (supports wildcards)
        
    Returns:
        New dictionary with keys reordered according to rules
    """
    ordered = {}
    
    # Add top keys in specified order
    for pattern in top_keys:
        if '*' in pattern:
            # For wildcard patterns, add all matching keys in their original order
            for key, value in frontmatter.items():
                if fnmatch.fnmatch(key, pattern):
                    ordered[key] = value
        else:
            # For exact matches, only add if they exist
            if pattern in frontmatter:
                ordered[pattern] = frontmatter[pattern]
    
    # Add middle keys (those not matching any patterns in top or bottom)
    for key, value in frontmatter.items():
        if not matches_pattern(key, top_keys) and not matches_pattern(key, bottom_keys):
            ordered[key] = value
    
    # Add bottom keys
    bottom_matches = {}
    for key, value in frontmatter.items():
        if matches_pattern(key, bottom_keys):
            bottom_matches[key] = value
    
    # Add all bottom matches in their original order
    ordered.update(bottom_matches)
    
    return ordered

def process_file(filepath: str, top_keys: List[str], bottom_keys: List[str]) -> bool:
    """
    Process a single markdown file, reordering its frontmatter if present.
    
    Args:
        filepath: Path to the markdown file
        top_keys: List of keys to appear at the top
        bottom_keys: List of keys to appear at the bottom
        
    Returns:
        True if file was successfully processed, False otherwise
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, remaining_content, has_frontmatter = extract_frontmatter(content)
        if not has_frontmatter:
            print(f"Warning: No valid frontmatter found in {filepath}")
            return False
        
        ordered_frontmatter = reorder_frontmatter(frontmatter, top_keys, bottom_keys)
        
        # Create new content with ordered frontmatter
        new_content = "---\n"
        new_content += yaml.dump(ordered_frontmatter, allow_unicode=True, sort_keys=False)
        new_content += "---\n"
        new_content += remaining_content
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    
    except Exception as e:
        print(f"Error processing {filepath}: {str(e)}")
        return False

def main():
    """
    Main entry point for the script.
    
    Reads configuration and processes markdown files in the specified directory.
    Only processes files directly in the given directory, not in subdirectories.
    Reports the outcome of the processing.
    """
    parser = argparse.ArgumentParser(description='Reorder YAML frontmatter in markdown files.')
    parser.add_argument('directory', help='Directory containing markdown files')
    parser.add_argument('--config', default='frontmatter_config.json',
                      help='Path to configuration file (default: frontmatter_config.json)')
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return
    
    if not os.path.isfile(args.config):
        print(f"Error: Configuration file {args.config} not found")
        return
    
    top_keys, bottom_keys = load_config(args.config)
    
    processed_files = 0
    success_count = 0
    
    # Only process files in the root directory
    for file in os.listdir(args.directory):
        if file.endswith('.md'):
            filepath = os.path.join(args.directory, file)
            if os.path.isfile(filepath):  # Ensure it's a file, not a directory
                processed_files += 1
                if process_file(filepath, top_keys, bottom_keys):
                    success_count += 1
    
    print(f"\nProcessed {processed_files} files:")
    print(f"- Successfully reordered: {success_count}")
    print(f"- Failed: {processed_files - success_count}")

if __name__ == "__main__":
    main()
