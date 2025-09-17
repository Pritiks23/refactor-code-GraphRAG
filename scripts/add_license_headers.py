import os, re

LICENSE = """# Copyright (c) 2025 Refactor Bot
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
"""

def should_skip(path):
    return any(part in path for part in [".venv", "site-packages", "__pycache__", "node_modules", ".github/workflows"])

def has_license(text):
    return "Licensed under the MIT License" in text

def process_file(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if has_license(content):
        return False
    if path.endswith(".py"):
        new = LICENSE + "\n" + content
    elif path.endswith((".js", ".ts", ".jsx", ".tsx")):
        new = "\n".join(["// " + line[2:] if line.startswith("# ") else "// " + line for line in LICENSE.splitlines()]) + "\n" + content
    else:
        return False
    with open(path, "w", encoding="utf-8") as f:
        f.write(new)
    return True

def main():
    changed = 0
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith((".py", ".js", ".ts", ".jsx", ".tsx")):
                full = os.path.join(root, file)
                if should_skip(full):
                    continue
                if process_file(full):
                    changed += 1
    print(f"License headers added to {changed} files.")

if __name__ == "__main__":
    main()
