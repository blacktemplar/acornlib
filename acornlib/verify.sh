#!/bin/bash
# Acorn verifier CLI
# Usage: ./verify.sh <file.ac>

if [ $# -eq 0 ]; then
    echo "Error: No file specified"
    echo "Usage: ./verify.sh <file.ac>"
    exit 1
fi

# Use Node.js to run verification (assuming VS Code extension uses Node)
# Replace with actual verification command from the extension
node -e "require('acorn-vscode/out/verifier').verifyFile('$1')"