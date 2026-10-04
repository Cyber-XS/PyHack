import sys
import subprocess
import importlib.util
import argparse
from datetime import datetime

# Colors
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[94m"
B = "\033[95m"
W = "\033[0m"

# System tools
SYSTEM_TOOLS = [
    "nmap",
    "netcat",
    "wireshark",
    "hydra",
    "sqlmap",
    "john",
    "hashcat",
    # Added tools
    "gobuster",
    "dirb",
    "enum4linux",
]

# Python libraries
PYTHON_LIBS = ["requests", "scapy", "impacket", "dns"]

# Lab hosts
LAB_HOST = {"metasploitable 2": "192.168.1.6"}


def print_banner():
    print(f"{G}")
    print(" ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
    print(" ■ env_checker.py v2.0 ■")
    print(" ■ Script to Shell — Module 01 ■")
    print(" ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■")
    print(f"{W}")


def check_python_version(quiet=False):
    """
    Check if Python version is 3.8 or higher.
    """

    major = sys.version_info.major
    minor = sys.version_info.minor

    if major == 3 and minor >= 8 or major > 3:
        if not quiet:
            print(f"{G} [OK] {W} Python {major}.{minor} (Python 3.8+ required)")
        return True

    else:
        print(f"{R} [MISSING] {W} Python {major}.{minor} (Python 3.8+ required)")
        return False


def check_system_tools(quiet=False):
    print(f"{Y} [*] Checking System Tools...{W}")

    missing = []

    for tool in SYSTEM_TOOLS:
        result = subprocess.run(["which", tool], capture_output=True, text=True)

        if result.returncode == 0:
            if not quiet:
                path = result.stdout.strip()

                print(f"{G} [OK] {W} {tool:<25} {path}")

        else:
            print(f"{R} [MISSING] {W} {tool}")
            missing.append(tool)

    return missing


def check_python_libs(quiet=False):
    print(f"{Y} [*] Checking Python Libraries...{W}")

    missing = []

    for lib in PYTHON_LIBS:
        spec = importlib.util.find_spec(lib)

        if spec is None:
            print(f"{R} [MISSING] {W} {lib}")
            missing.append(lib)

        else:
            if not quiet:
                print(f"{G} [OK] {W} {lib}")

    return missing


def check_lab_connectivity(quiet=False):
    print(f"{Y} [*] Checking Active Victim Systems...{W}")

    for name, ip in LAB_HOST.items():
        result = subprocess.run(
            ["ping", "-c", "1", "-w", "2", ip], capture_output=True, text=True
        )

        if result.returncode == 0:
            if not quiet:
                print(f"{G} [REACHABLE] {W} {name} {ip}")

        else:
            print(f"{R} [UNREACHABLE] {W} {name} {ip}")


def save_missing_tools(missing_tools):
    """
    Save missing tools to missing_tools.txt
    with a timestamp.
    """

    if not missing_tools:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("missing_tools.txt", "a") as file:
        file.write(f"\n{'=' * 50}\n")

        file.write(f"Check Time: {timestamp}\n")

        file.write("Missing Tools:\n")

        for tool in missing_tools:
            file.write(f"- {tool}\n")

    print(f"{C} [+] Missing tools saved to missing_tools.txt{W}")


def fix_missing_items(missing_tools, missing_libs):
    """
    Automatically install missing tools
    and Python libraries.
    """

    if missing_tools:
        print(f"{Y} [*] Installing missing system tools...{W}")

        subprocess.run(["sudo", "apt", "install", "-y"] + missing_tools)

    if missing_libs:
        print(f"{Y} [*] Installing missing Python libraries...{W}")

        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_libs)


def main():

    # Argument parser
    parser = argparse.ArgumentParser(description="Cybersecurity Environment Checker")

    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Only show missing items"
    )

    parser.add_argument(
        "--fix",
        action="store_true",
        help="Automatically install missing tools and libraries",
    )

    args = parser.parse_args()

    # Banner
    if not args.quiet:
        print_banner()

    # Python version
    if not args.quiet:
        print(f"{Y} [*] Checking Python Version...{W}")

    python_ok = check_python_version(args.quiet)

    # System tools
    missing_tools = check_system_tools(args.quiet)

    # Python libraries
    missing_libs = check_python_libs(args.quiet)

    # Lab connectivity
    check_lab_connectivity(args.quiet)

    # Save missing tools
    save_missing_tools(missing_tools)

    # Automatically fix missing items
    if args.fix:
        fix_missing_items(missing_tools, missing_libs)

    # Final summary
    if not args.quiet:
        print(f"\n{Y} {'=' * 45} {W}")

        if not missing_tools and not missing_libs and python_ok:
            print(f"{G} [+] All checks passed | Lab is ready {W}")

        else:
            if not python_ok:
                print(f"{R} [!] Python 3.8+ is required {W}")

            if missing_tools:
                print(f"{R} [!] Missing Tools: {','.join(missing_tools)} {W}")

                print(f"Fix: sudo apt install {' '.join(missing_tools)}")

            if missing_libs:
                print(f"{R} [!] Missing Libraries: {','.join(missing_libs)} {W}")

                print(f"Fix: {sys.executable} -m pip install {' '.join(missing_libs)}")

        print(f"\n{Y} {'=' * 45} {W}")


if __name__ == "__main__":
    main()
