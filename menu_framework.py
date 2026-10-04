import sys
import argparse
import os

R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'

BANNER = rf"""
{R}  _   _      _    _____
 | \ | |    | |  / ____|
 |  \| | ___| |_| (___   ___ __ _ _ __
 | . ` |/ _ \ __|\___ \ / __/ _` | '_ \
 | |\  |  __/ |_ ____) | (_| (_| | | | |
 |_| \_|\___|\__|_____/ \___\__,_|_| |_|
 {W}
Script for Shell - Python for Ethical Hackers
"""


def show_menu():
    os.system('clear')
    print(BANNER)

    print(f'[1] {G} Port Scanning {W}')
    print(f'[2] {G} Banner Grabber {W}')
    print(f'[3] {G} Host Sweeper {W}')
    print(f'[0] {R} Exit {W}\n')


def run_port_scanner():
    os.system('clear')
    print(f'{C} Port Scanner {W}\n')

    target = input('Target IP or Hostname > ').strip()

    if not target:
        print(f'{R} Target Not Found {W}')
        input('\nPress Enter to Return to Menu ')
        return

    print(f"{Y} [*] Scanning {target}..... {W}")
    input('\nPress Enter to Return to Menu ')


def run_banner_grabber():
    os.system('clear')
    print(f'\n{C} Banner Grabber {W}\n')

    target = input('Enter Target > ').strip()
    port = input('Enter Port > ').strip()

    print(f'\n{Y} [*] Grabbing Banner of {target}:{port}..... {W}')
    input('\nPress Enter to Return to Menu ')


def run_host_sweeper():
    os.system('clear')
    print(f'\n{C} Host Sweeper {W}\n')

    subnet = input('Subnet (Example: 192.168.1.0/24) > ').strip()

    print(f'{Y} [*] Sweeping {subnet}..... {W}')
    input('\nPress Enter to Return to Menu ')


def main():
    while True:
        show_menu()
        user_choice = input('Choose > ').strip()

        if user_choice == '1':
            run_port_scanner()
        elif user_choice == '2':
            run_banner_grabber()
        elif user_choice == '3':
            run_host_sweeper()
        elif user_choice == '0':
            print(f'{R} [*] Exit..... {W}')
            sys.exit()
        else:
            input(f'{R} [!] Invalid Option. Press Enter..... {W}')


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--target", "-t",
        help="Enter your Target IP or Host Name"
    )

    parser.add_argument(
        "--scan", "-s",
        choices=['Ports', 'Banner', 'Sweep'],
        help='Run a Specific Scan Directly'
    )

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.scan == 'Ports':
        run_port_scanner()
    elif args.scan == 'Banner':
        run_banner_grabber()
    elif args.scan == 'Sweep':
        run_host_sweeper()
    else:
        main()
