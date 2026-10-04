import socket, sys, queue

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

result = queue.Queue()

def grab_banner(ip, port, timeout=1):
    try:
        with socket.socket(socket.AddressFamily.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((ip, port))
            return s.recv(1024).decode(errors='ignore').strip()
    except: return ''

def scan_port(ip, port, timeout=0.5):
    try:
        with socket.socket(socket.AddressFamily.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            if s.connect_ex((ip, port)) == 0:
                banner = grab_banner(ip, port)
                result.put((port, banner))
    except OSError: pass

def threaded_scan(target, start=1, end=65535, threads=200):
    print(f'Scanning {target} ({start}-{end}) with {threads} threads \n')
    start_time = datetime.now()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for port in range(start, end + 1):
            executor.submit(scan_port, target, port)
    elapsed = (datetime.now() - start_time).total_seconds()
    open_ports = sorted(result.queue)
    print(f'\n Scan Completed in {elapsed:.1f} seconds ')
    return open_ports

if __name__ == '__main__':
    target = input('Target > ').strip()
    result_list = threaded_scan(target, 1, 65535, threads=300)
    for port, banner in result_list:
        print(f' {port}:{banner} ')
