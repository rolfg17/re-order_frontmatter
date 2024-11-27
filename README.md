# Markdown Frontmatter Reorderer

A Python tool to reorder YAML frontmatter in Markdown files according to configurable rules. It allows you to specify which keys should appear at the top and bottom of the frontmatter, with support for wildcard patterns.

## Features

- Reorder frontmatter keys while preserving content and formatting
- Configure top and bottom keys via JSON configuration
- Support for wildcard patterns (e.g., `ai.*` for all keys starting with "ai.")
- Preserve order of unspecified keys
- Handle nested YAML structures
- Non-destructive: preserves files without frontmatter
- Includes test suite and reset capability

## Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Edit `frontmatter_config.json` to specify your desired key order:

```json
{
    "top_keys": ["Status", "Area", "Project"],
    "bottom_keys": ["ai.*"]
}
```

- `top_keys`: Keys that should appear at the top of the frontmatter (in the specified order)
- `bottom_keys`: Keys that should appear at the bottom (supports wildcards)

Keys not specified in either list will remain in their original order between the top and bottom sections.

If no configuration file is provided or if the file is invalid:
- The script will continue to run with empty top and bottom key lists
- A warning message will be displayed
- No reordering will occur (files will keep their original frontmatter order)
- The script will still validate and process the YAML frontmatter

## Usage

```bash
# Make scripts executable
chmod +x reorder_frontmatter.py reset_tests.py

# Process markdown files in a directory
./reorder_frontmatter.py /path/to/your/markdown/files

# Optionally specify a different config file
./reorder_frontmatter.py /path/to/files --config custom_config.json
```

## Testing

The repository includes a test suite with example files covering various scenarios:

- test1.md: All specified top keys and multiple wildcard-matching keys
- test2.md: Partial top keys and one wildcard-matching key
- test3.md: Some top keys but no wildcard-matching keys
- test4.md: Only wildcard-matching keys
- test5.md: No frontmatter

To run tests:

```bash
# Reset test files to original state
./reset_tests.py

# Run reordering on test files
./reorder_frontmatter.py test_files
```

## Behavior

1. Top Keys:
   - Appear first in frontmatter
   - Only included if they exist in the original file
   - Maintain specified order

2. Middle Keys:
   - Any keys not specified in top or bottom lists
   - Maintain their original order
   - Appear between top and bottom sections

3. Bottom Keys:
   - Support wildcard patterns (e.g., `ai.*`)
   - All matching keys are grouped at the bottom
   - Maintain original order within the group

4. Special Cases:
   - Files without frontmatter are left unchanged
   - Invalid YAML frontmatter is reported as an error
   - Nested YAML structures are preserved

## Requirements

- Python 3.6+
- PyYAML >= 6.0.1

## License

MIT License
