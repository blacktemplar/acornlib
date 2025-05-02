import os
import re
import sys
import subprocess

def lint_file(filepath):
    modified = False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        print(f"Skipping {filepath}: Not a UTF-8 text file")
        return False
    
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

def get_git_tracked_files():
    """Get list of all git-tracked files"""
    try:
        cmd = ['git', 'ls-files']
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"Git command failed: {result.stderr}")
        
        return [f for f in result.stdout.strip().split('\n') if f]
    except Exception as e:
        print(f"Error getting git-tracked files: {e}")
        return []

if __name__ == "__main__":
    changed_files = []
    
    # If specific files are provided, lint only those
    if len(sys.argv) > 1:
        for file_path in sys.argv[1:]:
            if os.path.exists(file_path):
                if lint_file(file_path):
                    changed_files.append(file_path)
    # Otherwise, lint all git-tracked files
    else:
        git_files = get_git_tracked_files()
        if git_files:
            for file_path in git_files:
                if os.path.exists(file_path):
                    try:
                        if lint_file(file_path):
                            changed_files.append(file_path)
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
        else:
            # Fallback to all files if git command fails, but skip .git directories
            for root, _, files in os.walk('.'):
                if '.git' in root.split(os.path.sep):
                    continue
                for file in files:
                    full_path = os.path.join(root, file)
                    try:
                        if lint_file(full_path):
                            changed_files.append(full_path)
                    except Exception as e:
                        print(f"Error processing {full_path}: {e}")
    
    if changed_files:
        print(f"Formatted {len(changed_files)} files")
        sys.exit(1)  # Exit with error to abort commit if used in pre-commit
    else:
        print("All files are clean!")
        sys.exit(0)
