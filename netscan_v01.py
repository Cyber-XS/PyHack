import socket
import sys
import os
import argparse
from datetime import datetime

from banner_grabber import banner_grab
from port_scanner_v1 import scan_range, save_results


# =========================
# CONFIGURATION
# =========================

VERSION = "1.0"


# ANSI Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
B = '\033[94m'
W = '\033[0m'


# =========================
# BANNER
# =========================

BANNER = rf"""
{G}  _   _      _    _____
 | \ | |    | |  / ____|
 |  \| | ___| |_| (___   ___ __ _ _ __
 | . ` |/ _ \ __|\___ \ / __/ _` | '_ \
 | |\  |  __/ |_ ____) | (_| (_| | | | |
 |_| \_|\___|\__|_____/ \___\__,_|_| |_|
{W}
{B} Script to Shell - Python for Ethical Hackers | Version: {VERSION} {W}
"""


# =========================
# ARGUMENT PARSER
# =========================

def parse_args():

    parser = argparse.ArgumentParser(
        prog='netscan',
        description='Netscan - Python Port Scanner',
        epilog='Example: python3 netscan.py -t 192.168.1.2'
    )

    parser.add_argument(
        '--target',
        '-t',
        help='Target IP or Target Hostname'
    )

    parser.add_argument(
        '--ports',
        '-p',
        default='1-1024',
        help='Port range, example: 1-1024'
    )

    parser.add_argument(
        '--threads',
        default=100,
        type=int,
        help='Number of threads'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Output filename'
    )

    parser.add_argument(
        '--sweep',
        action='store_true',
        help='Enable host sweeping'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Enable verbose output'
    )

    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip printing the startup banner'
    )

    return parser.parse_args()


# =========================
# SCREEN CLEARING
# =========================

def clear_screen(args):
    """
    Clear the terminal screen.

    If Python-only clearing is enabled,
    print blank lines instead of using os.system().
    """

    if args.python_clear:
        print('\n' * 50)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')


# =========================
# TARGET VALIDATION
# =========================

def validate_target(target):
    """
    Perform simple target validation.

    This is not strict IP/hostname validation.
    """

    if not target:
        return False, 'Target cannot be empty.'

    allowed = set(
        'abcdefghijklmnopqrstuvwxyz'
        'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        '0123456789.-'
    )

    # Warn about unusual characters
    if any(char not in allowed for char in target):
        return True, (
            "Warning: This doesn't look like a normal "
            "IP address or hostname."
        )

    # Simple hostname/IP check
    if '.' not in target and target.lower() != 'localhost':
        return True, (
            "Warning: This doesn't look like a typical "
            "IP address or hostname."
        )

    return True, None


def set_target(args):

    clear_screen(args)

    print(f'\n {C}[+] {W}Set Target\n')

    target = input(' Enter New Target > ').strip()

    valid, message = validate_target(target)

    if not valid:
        input(
            f' {R}[!] {W}{message} Press Enter...'
        )
        return

    args.target = target

    print(
        f' {G}[+] {W}'
        f'Target set to: {args.target}'
    )

    if message:
        print(
            f' {Y}[!] {W}{message}'
        )

    input('\n Press Enter...')


# =========================
# SETTINGS MENU
# =========================

def settings_menu(args):

    while True:

        clear_screen(args)

        print(f'\n {C}[+] {W}Settings\n')

        print(
            f' Current Threads     : {args.threads}'
        )

        print(
            f' Current Output File : '
            f'{args.output or "automatic"}'
        )

        print(
            f' Python-only Clear   : '
            f'{"ON" if args.python_clear else "OFF"}'
        )

        print()

        print(f' {G}[1] {W}Change Threads')
        print(f' {G}[2] {W}Change Output File')
        print(f' {G}[3] {W}Toggle Python-only Clear')
        print(f' {G}[0] {W}Back to Main Menu\n')

        choice = input(' Settings > ').strip()

        # -------------------------
        # Change Threads
        # -------------------------

        if choice == '1':

            value = input(
                ' Enter number of threads > '
            ).strip()

            try:

                threads = int(value)

                if threads <= 0:
                    raise ValueError

                args.threads = threads

                print(
                    f' {G}[+] {W}'
                    f'Threads updated to {args.threads}'
                )

            except ValueError:

                print(
                    f' {R}[!] {W}'
                    f'Threads must be a positive whole number.'
                )

            input('\n Press Enter...')

        # -------------------------
        # Change Output File
        # -------------------------

        elif choice == '2':

            output = input(
                ' Enter output filename '
                '(leave empty for automatic filename) > '
            ).strip()

            args.output = output or None

            print(
                f' {G}[+] {W}'
                f'Output set to: '
                f'{args.output or "automatic"}'
            )

            input('\n Press Enter...')

        # -------------------------
        # Toggle Python Clear
        # -------------------------

        elif choice == '3':

            args.python_clear = not args.python_clear

            state = (
                'ON'
                if args.python_clear
                else 'OFF'
            )

            print(
                f' {G}[+] {W}'
                f'Python-only clear is now {state}'
            )

            input('\n Press Enter...')

        # -------------------------
        # Back
        # -------------------------

        elif choice == '0':
            return

        else:

            input(
                f' {R}[!] {W}'
                f'Invalid option. Press Enter...'
            )


# =========================
# PORT SCANNER
# =========================

def run_port_scan(args):

    clear_screen(args)

    print(f'\n {C}[PORT SCAN] {W}')

    target = args.target

    if not target:
        target = input(
            ' Target > '
        ).strip()

    if not target:
        input(
            f' {R}[!] {W}'
            f'Target cannot be empty. Press Enter...'
        )
        return

    print(
        f'\n {Y}[*] {W}'
        f'Scanning {target} '
        f'(ports {args.ports})\n'
    )

    # -------------------------
    # Parse port range
    # -------------------------

    try:

        if '-' in args.ports:

            start_port, end_port = map(
                int,
                args.ports.split('-', 1)
            )

        else:

            start_port = int(args.ports)
            end_port = start_port

        if not (
            1 <= start_port <= 65535
            and
            1 <= end_port <= 65535
        ):
            raise ValueError

        if start_port > end_port:
            raise ValueError

    except ValueError:

        print(
            f' {R}[!] {W}'
            f'Invalid port range: {args.ports}'
        )

        input('\n Press Enter...')
        return

    # -------------------------
    # Run scanner
    # -------------------------

    try:

        results = scan_range(
            target,
            start_port,
            end_port
        )

    except socket.gaierror:

        print(
            f' {R}[!] {W}'
            f'Could not resolve target: {target}'
        )

        input('\n Press Enter...')
        return

    except Exception as error:

        print(
            f' {R}[!] {W}'
            f'Scan error: {error}'
        )

        input('\n Press Enter...')
        return

    # -------------------------
    # Results
    # -------------------------

    print(
        f'\n {G}[+] {W}'
        f'{len(results)} open ports found'
    )

    # -------------------------
    # ALWAYS SAVE RESULTS
    # -------------------------

    try:

        filename = save_results(
            results,
            target,
            args.output
        )

        print(
            f' {G}[+] {W}'
            f'Result saved to: {filename}'
        )

    except OSError as error:

        print(
            f' {R}[!] {W}'
            f'Could not save result: {error}'
        )

    input(
        f' {Y}\nPress Enter...{W}'
    )


# =========================
# BANNER GRABBER
# =========================

def run_banner_grab(args):

    clear_screen(args)

    print(
        f'\n {C}[+] {W}Banner Grabber'
    )

    target = args.target

    if not target:
        target = input(
            ' Target IP > '
        ).strip()

    if not target:
        input(
            f' {R}[!] {W}'
            f'Target cannot be empty. Press Enter...'
        )
        return

    print(
        f'\n {Y}[*] {W}'
        f'Scanning {target}...\n'
    )

    ports = [
        21,
        22,
        23,
        25,
        80,
        110,
        143,
        443,
        3306,
        5432,
        5900
    ]

    found = False

    for port in ports:

        try:

            banner = banner_grab(
                target,
                port,
                timeout=2
            )

            if banner:

                found = True

                print(
                    f'Port {port:5d}: '
                    f'{banner[:70]}'
                )

        except Exception as error:

            if args.verbose:

                print(
                    f' {R}[!] {W}'
                    f'Port {port}: {error}'
                )

    if not found:

        print(
            f' {Y}[*] {W}'
            f'No banners found.'
        )

    input('\n Press Enter...')


# =========================
# HOST SWEEPER
# =========================

def run_host_sweeper(args):

    clear_screen(args)

    print(
        f'\n {C}[+] {W}Host Sweeper'
    )

    print(
        f'\n {Y}[!] {W}'
        f'Host Sweeper coming in Module 3'
    )

    input('\n Press Enter...')


# =========================
# ABOUT
# =========================

def show_about(args):

    clear_screen(args)

    print(BANNER)

    print(
        f' Version: {VERSION}'
    )

    print(
        '\n NetScan is a Python-based '
        'network scanning tool.'
    )

    print(
        ' Built for educational and '
        'authorized security testing.'
    )

    input('\n Press Enter...')


# =========================
# SESSION LOGGING
# =========================

def log_choice(session_log, choice):

    timestamp = datetime.now().strftime(
        '%Y-%m-%d %H:%M:%S'
    )

    session_log.append(
        f'[{timestamp}] '
        f'User chose option {choice}'
    )


def print_session_log(session_log):

    print(
        f'\n {C}[+] {W}Session Log\n'
    )

    if not session_log:

        print(
            ' No options were recorded.'
        )

    else:

        for entry in session_log:

            print(
                f' {entry}'
            )


# =========================
# MAIN MENU
# =========================

def show_menu(args):

    clear_screen(args)

    print(BANNER)

    target = (
        args.target
        if args.target
        else 'not set'
    )

    print(
        f' {Y}Target: {target}{W}\n'
    )

    print(
        f' {G}[1] {W}Port Scan'
    )

    print(
        f' {G}[2] {W}Banner Grabber'
    )

    print(
        f' {G}[3] {W}Host Sweeper'
    )

    print(
        f' {G}[4] {W}Set Target'
    )

    print(
        f' {G}[5] {W}Settings'
    )

    print(
        f' {G}[?] {W}About'
    )

    print(
        f' {G}[0] {W}Exit\n'
    )


# =========================
# MAIN PROGRAM
# =========================

def main(args):

    # Python-only clear starts disabled
    args.python_clear = False

    # Session log
    session_log = []

    while True:

        show_menu(args)

        choice = input(
            ' Choose > '
        ).strip()

        # Log choice
        log_choice(
            session_log,
            choice
        )

        # -------------------------
        # Port Scan
        # -------------------------

        if choice == '1':

            run_port_scan(args)

        # -------------------------
        # Banner Grabber
        # -------------------------

        elif choice == '2':

            run_banner_grab(args)

        # -------------------------
        # Host Sweeper
        # -------------------------

        elif choice == '3':

            run_host_sweeper(args)

        # -------------------------
        # Set Target
        # -------------------------

        elif choice == '4':

            set_target(args)

        # -------------------------
        # Settings
        # -------------------------

        elif choice == '5':

            settings_menu(args)

        # -------------------------
        # About
        # -------------------------

        elif choice == '?':

            show_about(args)

        # -------------------------
        # Exit
        # -------------------------

        elif choice == '0':

            clear_screen(args)

            print_session_log(
                session_log
            )

            print(
                f'\n {R}Good Bye{W}'
            )

            return

        # -------------------------
        # Invalid Input
        # -------------------------

        else:

            input(
                f' {R}[!] {W}'
                f'Invalid Input. Press Enter...'
            )


# =========================
# PROGRAM ENTRY POINT
# =========================

if __name__ == '__main__':

    args = parse_args()

    # Startup banner
    if not args.no_banner:

        print(BANNER)

    print(
        f' {G}[*] {W}'
        f'NetScan Version: {VERSION}'
    )

    print(
        f' {G}[*] {W}'
        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    )

    main(args)
