import socket

def banner_grab(ip, port, timeout=3):
    try:
        with socket.socket(socket.AF_INET, socket.SocketKind.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            banner = s.recv(1024).decode(errors='ignore').strip()
            return banner
    except(socket.timeout, ConnectionRefusedError, OSError):
        return None

if __name__ == '__main__':
    target = input('Target IP > ').strip()
    print(f'\n Scanning {target}...\n')
    for port in [21, 22, 23, 25, 80, 3306, 5432, 5900]:
        banner = banner_grab(target, port)
        if banner:
            print(f'Port {port:5d}: {banner[:80]} ')
