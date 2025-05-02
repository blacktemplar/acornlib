#!/bin/bash
# Acorn linter/formatter

# 1. Remove trailing whitespace
find . -name "*.ac" -exec sed -i '' 's/[[:space:]]*$//' {} \;

# 2. Validate file structure
find . -name "*.ac" -exec grep -nEH '[^[:space:]]$' {} \; | awk '{print "Trailing whitespace fixed in: " $1}'
