#!/bin/bash
# This script copies .env.example to .env in each subdirectory of steps/

# Exit immediately if a command exits with a non-zero status.
set -e

# Find all .env.example files in the steps directory and copy them to .env in the same directory.
for example_file in steps/*/.env.example; do
    if [ -f "$example_file" ]; then
        # Get the directory of the .env.example file
        dir=$(dirname "$example_file")
        # Copy the file
        cp "$example_file" "$dir/.env"
        echo "Created $dir/.env"
    fi
done

echo "All .env files have been created." 