# Copyright (c) 2025 Refactor Bot
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import subprocess


def main():
    with open("dependency-manifest.txt", "w", encoding="utf-8") as f:
        f.write("# Dependency Tree\n\n")
        out = subprocess.check_output(["pipdeptree"], text=True)
        f.write(out)


if __name__ == "__main__":
    main()
