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
        if not cleaned.endswith('\n'):
            cleaned += '\n'
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
    changed_files = []
    
    # If specific files are provided, lint only those
    if len(sys.argv) > 1:
        for pattern in sys.argv[1:]:
            for root, _, files in os.walk('.'):
                for file in files:
                    full_path = os.path.join(root, file)
                    if lint_file(full_path):
                        changed_files.append(full_path)
    # Otherwise, lint all .ac files
    else:
        for root, _, files in os.walk('.'):
            for file in files:
                full_path = os.path.join(root, file)
                if lint_file(full_path):
                    changed_files.append(full_path)
    
    if changed_files:
        print(f"Formatted {len(changed_files)} files")
        sys.exit(1)  # Exit with error to abort commit if used in pre-commit
    else:
        print("All files are clean!")
        sys.exit(0)
