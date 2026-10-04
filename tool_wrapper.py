import sys, subprocess, os


class ToolWrapper:
    def __init__(self, tool_name: str, description: str = ""):
        self.tool = tool_name
        self.desc = description

    def run(self, args: list[str]) -> int:
        try:
            cmd = [self.tool] + args

            print(f"[*] Running: {' '.join(cmd)}")
            print()

            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            while True:
                line = proc.stdout.readline() if proc.stdout else ""

                if line == "" and proc.poll() is not None:
                    break

                if line:
                    sys.stdout.write(line)
                    sys.stdout.flush()

            print()
            return proc.returncode

        except FileNotFoundError:
            print(f"[!] {self.tool} not found")
            print(f"[*] Try: sudo pacman -S {self.tool}")
            return -1

        except PermissionError:
            print("[!] Permission denied")

            if args:
                print(f"[*] Try: sudo {self.tool} {' '.join(args)}")
            else:
                print(f"[*] Try: sudo {self.tool}")

            return -1

        except Exception as e:
            print(f"[!] Error: {e}")
            return -1


if __name__ == "__main__":
    nmap = ToolWrapper(
        "nmap",
        "Network Mapper"
    )

    exit_code = nmap.run([
        "-sV",
        "-v",
        "192.168.1.8"
    ])

    print(f"[*] Exit Code: {exit_code}")

    sys.exit(exit_code)
