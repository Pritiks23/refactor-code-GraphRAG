import subprocess

def main():
    with open("dependency-manifest.txt", "w", encoding="utf-8") as f:
        f.write("# Dependency Tree\n\n")
        out = subprocess.check_output(["pipdeptree"], text=True)
        f.write(out)

if __name__ == "__main__":
    main()
