import socket

def check_banner(ip, port=6667):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        print(f' [*] Connecting to {ip}:{port} ')
        sock.connect((ip, port))

        print(' [+] Connected ')
        print(' [*] Waiting for IRC banner ')
        print()

        banner = sock.recv(4096).decode(errors='ignore')

        print('========== IRC BANNER ==========')
        print(banner.strip())
        print('================================')

        sock.close()

    except socket.timeout:
        print(' [!] Connection Timeout ')
    except ConnectionRefusedError:
        print(' [!] Connection Refused ')
    except Exception as e:
        print(' [!] Error {e} ')

def main():
    ip = input('Targer > ').strip()

    check_banner(ip)

if __name__ == "__main__":
    main()
