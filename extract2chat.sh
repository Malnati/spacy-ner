#!/bin/bash

# Find all files up to a depth of 3 levels, including hidden files and directories, excluding the .git directory
find . -path './.git' -prune -o -type f -print | while read -r file; do
  echo "File: $file"
  cat "$file"
  echo ""
done