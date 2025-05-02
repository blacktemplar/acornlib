import os
import re
import sys

def lint_file(filepath):
    modified = False
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # Remove trailing whitespace
        cleaned = re.sub(r'[ \t]+$', '', line)
        # Ensure newline at EOF
        cleaned = cleaned.rstrip('\n') + '\n'
        new_lines.append(cleaned)
        if cleaned != line:
            modified = True
    
    if modified:
        with open(filepath, 'w') as f:
            f.writelines(new_lines)
        print(f"Formatted {filepath}")
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python acorn_linter.py [file1.ac] [file2.ac] ...")
        sys.exit(1)
    
    changed_files = []
    for pattern in sys.argv[1:]:
        for root, _, files in os.walk('.'):
            for file in files:
                if file.endswith('.ac'):
                    full_path = os.path.join(root, file)
                    if lint_file(full_path):
                        changed_files.append(full_path)
    
    if changed_files:
        print(f"Formatted {len(changed_files)} files")
        sys.exit(1)  # Exit with error to abort commit if used in pre-commit
    else:
        print("All files are clean!")
        sys.exit(0)