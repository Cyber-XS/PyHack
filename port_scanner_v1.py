import socket
from datetime import datetime


# =========================
# BANNER GRABBER
# =========================

def grab_banner(ip, port, timeout=1):
    """
    Connect to a port and attempt
    to read the service banner.
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

            return s.recv(
                1024
            ).decode(
                errors='ignore'
            ).strip()

    except (socket.timeout, OSError):

        return None


# =========================
# PORT SCANNER
# =========================

def scan_port(ip, port, timeout=0.5):
    """
    Check if a single port is open
    using connect_ex().
    """

    try:

        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as s:

            s.settimeout(timeout)

            return (
                s.connect_ex(
                    (ip, port)
                ) == 0
            )

    except OSError:

        return False


# =========================
# PORT RANGE SCANNER
# =========================

def scan_range(ip, start, end):
    """
    Scan a range of ports on the target.
    """

    results = []

    print(
        f' Scanning {start}-{end}...\n'
    )

    for port in range(
        start,
        end + 1
    ):

        if scan_port(ip, port):

            banner = (
                grab_banner(ip, port)
                or ''
            )

            results.append(
                (port, banner)
            )

            print(
                f'\n'
                f' {port:5d} OPEN\n'
                f' {banner[:55]}'
            )

    return results


# =========================
# SAVE RESULTS
# =========================

def save_results(results, ip, filename=None):
    """
    Save scan results to a file.

    If filename is provided, use that filename.
    Otherwise create a timestamped filename.
    """

    # Use user-provided filename
    if filename:

        fn = filename

    # Otherwise create automatic filename
    else:

        timestamp = datetime.now().strftime(
            '%Y%m%d_%H%M%S'
        )

        safe_ip = ip.replace(
            '.',
            '_'
        )

        fn = (
            f'scan_{safe_ip}_'
            f'{timestamp}.txt'
        )

    # Write results
    with open(
        fn,
        'w',
        encoding='utf-8'
    ) as f:

        f.write(
            f'Scan: {ip}\n'
        )

        f.write(
            f'Time: {datetime.now()}\n\n'
        )

        for port, banner in results:

            f.write(
                f'{port}\t{banner}\n'
            )

    return fn


# =========================
# STANDALONE TEST
# =========================

if __name__ == '__main__':

    target = input(
        'Target IP: '
    ).strip()

    results = scan_range(
        target,
        1,
        1024
    )

    print(
        f'\nFound {len(results)} '
        f'open ports.\n'
    )

    filename = save_results(
        results,
        target
    )

    print(
        f'Saved to {filename}'
    )
