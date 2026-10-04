import socket
import sys
import os
import argparse
import queue

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from ipaddress import ip_network


# =========================
# VERSION
# =========================

VERSION = "2.0"


# =========================
# COLORS
# =========================

R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
C = "\033[96m"
B = "\033[95m"
W = "\033[0m"


# =========================
# BANNER
# =========================

BANNER = f"""
{R}
 _   _      _    _____
| \\ | |    | |  / ____|
|  \\| | ___| |_ | (___   ___ __ _ _ __
| . ` |/ _ \\ __||\\___ \\ / __/ _` | '_ \\
| |\\  |  __/ |_ ____) | (_| (_| | | | |
|_| \\_|\\___|\\__|_____/ \\___\\__,_|_| |_|

        Script to Shell
     Python for Ethical Hackers
              v{VERSION}
{W}
"""


# =========================
# BANNER GRABBER
# =========================

def grab_banner(ip, port, timeout=1):
    """
    Connect to an open port and
    attempt to read its service banner.
    """

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as s:

            s.settimeout(timeout)

            s.connect(
                (ip, port)
            )

            banner = s.recv(
                1024
            ).decode(
                errors="ignore"
            ).strip()

            return banner

    except (socket.timeout, OSError):

        return ""


# =========================
# PORT SCANNER
# =========================

def scan_port(ip, port, result):
    """
    Check whether a single port is open.
    """

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as s:

            s.settimeout(0.5)

            if s.connect_ex(
                (ip, port)
            ) == 0:

                banner = grab_banner(
                    ip,
                    port
                )

                result.put(
                    (port, banner)
                )

    except OSError:

        pass


# =========================
# PORT RANGE SCANNER
# =========================

def scan_range(
    ip,
    start,
    end,
    threads=200
):
    """
    Threaded port-range scanner.
    """

    result = queue.Queue()

    print(
        f"\n{Y}"
        f"[*] Scanning {ip} "
        f"({start}-{end}) "
        f"with {threads} threads..."
        f"{W}\n"
    )

    start_time = datetime.now()

    with ThreadPoolExecutor(
        max_workers=threads
    ) as executor:

        for port in range(
            start,
            end + 1
        ):

            executor.submit(
                scan_port,
                ip,
                port,
                result
            )

    elapsed = (
        datetime.now() - start_time
    ).total_seconds()

    results = sorted(
        list(result.queue),
        key=lambda x: x[0]
    )

    for port, banner in results:

        if banner:

            print(
                f"{G}"
                f"[+] {port:5d} OPEN"
                f"{W} - "
                f"{banner[:70]}"
            )

        else:

            print(
                f"{G}"
                f"[+] {port:5d} OPEN"
                f"{W}"
            )

    print(
        f"\n{Y}"
        f"[*] Scan complete in "
        f"{elapsed:.1f} seconds"
        f"{W}"
    )

    print(
        f"{C}"
        f"[*] Open ports: "
        f"{len(results)}"
        f"{W}\n"
    )

    return results


# =========================
# SAVE RESULTS
# =========================

def save_results(
    results,
    target,
    filename=None
):
    """
    Save scan results to a text file.

    If filename is not supplied,
    create a timestamped filename.
    """

    if filename:

        fn = filename

    else:

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        safe_target = (
            target
            .replace(".", "_")
            .replace("/", "_")
        )

        fn = (
            f"scan_{safe_target}_"
            f"{timestamp}.txt"
        )

    with open(
        fn,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "========================================\n"
        )

        f.write(
            "          NetScan v1.0 Report\n"
        )

        f.write(
            "========================================\n\n"
        )

        f.write(
            f"Target : {target}\n"
        )

        f.write(
            f"Time   : {datetime.now()}\n\n"
        )

        f.write(
            "PORT\tBANNER\n"
        )

        f.write(
            "----\t------\n"
        )

        for port, banner in results:

            f.write(
                f"{port}\t{banner}\n"
            )

    print(
        f"{G}"
        f"[+] Results saved to {fn}"
        f"{W}"
    )

    return fn


# =========================
# PORT PARSER
# =========================

def parse_ports(port_range):
    """
    Convert:

    80
    1-1024

    into start and end ports.
    """

    try:

        if "-" in port_range:

            parts = port_range.split("-")

            if len(parts) != 2:

                return None

            start = int(parts[0])
            end = int(parts[1])

        else:

            start = int(port_range)
            end = start

        if (
            start < 1
            or end > 65535
            or start > end
        ):

            return None

        return start, end

    except ValueError:

        return None


# =========================
# TARGET VALIDATION
# =========================

def validate_target(target):
    """
    Check whether target is an IP,
    hostname, or CIDR network.
    """

    if not target:

        return False

    # Check CIDR
    if "/" in target:

        try:

            ip_network(
                target,
                strict=False
            )

            return True

        except ValueError:

            return False

    # Check IP
    try:

        socket.inet_aton(target)

        return True

    except OSError:

        pass

    # Check hostname
    allowed = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "0123456789"
        ".-_"
    )

    for char in target:

        if char not in allowed:

            return False

    return True


# =========================
# HOST SWEEP
# =========================

def host_sweep(
    subnet,
    threads=100
):
    """
    Find active hosts inside a CIDR range.
    """

    try:

        network = ip_network(
            subnet,
            strict=False
        )

    except ValueError:

        print(
            f"{R}"
            f"[!] Invalid CIDR range"
            f"{W}"
        )

        return []

    active_hosts = []
    result = queue.Queue()

    print(
        f"\n{Y}"
        f"[*] Sweeping {subnet}"
        f"{W}\n"
    )

    def ping_host(ip):

        try:

            result = subprocess.run(
                [
                    "ping",
                    "-c",
                    "1",
                    "-W",
                    "1",
                    str(ip)
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:

                return str(ip)

        except OSError:

            pass

        return None

    # Import here so the main imports stay simple
    import subprocess

    with ThreadPoolExecutor(
        max_workers=threads
    ) as executor:

        futures = [
            executor.submit(
                ping_host,
                ip
            )
            for ip in network.hosts()
        ]

        for future in futures:

            host = future.result()

            if host:

                result.put(host)

                print(
                    f"{G}"
                    f"[+] {host} ACTIVE"
                    f"{W}"
                )

    active_hosts = sorted(
        list(result.queue),
        key=lambda ip: tuple(
            int(x)
            for x in ip.split(".")
        )
    )

    print(
        f"\n{C}"
        f"[*] Active hosts: "
        f"{len(active_hosts)}"
        f"{W}\n"
    )

    return active_hosts


# =========================
# PORT SCAN
# =========================

def run_port_scan(args):

    target = args.target

    if not target:

        target = input(
            "Target IP / Hostname / CIDR > "
        ).strip()

    if not validate_target(target):

        print(
            f"{R}"
            f"[!] Invalid target"
            f"{W}"
        )

        return

    ports = parse_ports(
        args.ports
    )

    if not ports:

        print(
            f"{R}"
            f"[!] Invalid port range"
            f"{W}"
        )

        return

    start, end = ports

    # CIDR target
    if "/" in target:

        try:

            network = ip_network(
                target,
                strict=False
            )

            print(
                f"\n{Y}"
                f"[*] CIDR target detected"
                f"{W}"
            )

            for host in network.hosts():

                print(
                    f"\n{C}"
                    f"========== {host} =========="
                    f"{W}"
                )

                results = scan_range(
                    str(host),
                    start,
                    end,
                    args.threads
                )

                if results:

                    save_results(
                        results,
                        str(host),
                        args.output
                    )

        except ValueError:

            print(
                f"{R}"
                f"[!] Invalid CIDR"
                f"{W}"
            )

    else:

        results = scan_range(
            target,
            start,
            end,
            args.threads
        )

        save_results(
            results,
            target,
            args.output
        )


# =========================
# HOST SWEEP MENU
# =========================

def run_host_sweep(args):

    subnet = input(
        "CIDR Range "
        "(Example: 192.168.1.0/24) > "
    ).strip()

    if not subnet:

        print(
            f"{R}"
            f"[!] CIDR range required"
            f"{W}"
        )

        input(
            "\nPress Enter to continue..."
        )

        return

    host_sweep(
        subnet,
        args.threads
    )

    input(
        "\nPress Enter to continue..."
    )


# =========================
# MENU
# =========================

def show_menu():

    os.system(
        "cls"
        if os.name == "nt"
        else "clear"
    )

    print(BANNER)

    print(
        f"{G}"
        "[1] Port Scan"
        f"{W}"
    )

    print(
        f"{G}"
        "[2] Host Sweep"
        f"{W}"
    )

    print(
        f"{R}"
        "[0] Exit"
        f"{W}\n"
    )


# =========================
# ARGPARSE
# =========================

def parse_args():

    parser = argparse.ArgumentParser(
        description="NetScan v1.0 - "
                    "Python for Ethical Hackers"
    )

    parser.add_argument(
        "--target",
        "-t",
        help="Target IP, hostname or CIDR"
    )

    parser.add_argument(
        "--ports",
        "-p",
        default="1-1024",
        help="Port or range "
             "[Default: 1-1024]"
    )

    parser.add_argument(
        "--threads",
        type=int,
        default=200,
        help="Number of threads "
             "[Default: 200]"
    )

    parser.add_argument(
        "--output",
        "-o",
        help="Output filename"
    )

    parser.add_argument(
        "--scan",
        "-s",
        choices=[
            "port",
            "sweep"
        ],
        help="Run scan directly "
             "without menu"
    )

    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Do not display banner"
    )

    args = parser.parse_args()

    if args.threads < 1:

        parser.error(
            "--threads must be greater than 0"
        )

    if args.threads > 1000:

        parser.error(
            "--threads cannot exceed 1000"
        )

    return args


# =========================
# MAIN
# =========================

def main(args):

    while True:

        show_menu()

        choice = input(
            "Choose > "
        ).strip()

        if choice == "1":

            run_port_scan(args)

            input(
                "\nPress Enter to continue..."
            )

        elif choice == "2":

            run_host_sweep(args)

        elif choice == "0":

            print(
                f"\n{R}"
                "[*] Exiting NetScan..."
                f"{W}"
            )

            sys.exit()

        else:

            print(
                f"{R}"
                "[!] Invalid option"
                f"{W}"
            )

            input(
                "\nPress Enter to continue..."
            )


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":

    args = parse_args()

    if not args.no_banner:

        print(BANNER)

    print(
        f"{G}"
        f"[*] NetScan Version: {VERSION}"
        f"{W}"
    )

    print(
        f"{G}"
        f"[*] Started: "
        f"{datetime.now()}"
        f"{W}"
    )

    # Direct CLI mode
    if args.scan == "port":

        run_port_scan(args)

    elif args.scan == "sweep":

        if not args.target:

            print(
                f"{R}"
                "[!] --target is required "
                "for sweep mode"
                f"{W}"
            )

            sys.exit(1)

        host_sweep(
            args.target,
            args.threads
        )

    # Interactive mode
    else:

        main(args)
