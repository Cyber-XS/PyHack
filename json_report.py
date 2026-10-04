import json
import subprocess
import time
from pathlib import Path


REPORT_DIR = Path.home() / "CyberSift-Reports"


def run(cmd, tool_name):

    start_time = time.time()

    report = {
        "tool": tool_name,
        "command": cmd,
        "stdout": "",
        "exit_code": None,
        "duration": None
    }

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    output = []

    while True:

        line = process.stdout.readline()

        if line == "" and process.poll() is not None:
            break

        if line:

            print(line, end="")

            output.append(line)

    exit_code = process.wait()

    report["stdout"] = "".join(output)
    report["exit_code"] = exit_code
    report["duration"] = time.time() - start_time

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = REPORT_DIR / f"{tool_name}.json"

    with open(report_file, "w") as f:

        json.dump(
            report,
            f,
            indent=4
        )

    print(f"\nReport saved: {report_file}")


run(
    ["nmap", "-sV", "192.168.1.8"],
    "nmap"
)
