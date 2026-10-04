import socket
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor

vulnerable = []


def check_vsftpd(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)

        s.connect((ip, 21))

        banner = s.recv(1024).decode(errors="ignore").strip()

        s.close()

        if "vsftpd 2.3.4" in banner.lower():
            print(f"[+] Vulnerable: {ip} - {banner}")
            vulnerable.append(ip)

    except: pass


def scan_subnet(subnet):
    network = ip_network(subnet, strict=False)

    print(f"Scanning {subnet} for vsftpd 2.3.4...\n")

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_vsftpd, [str(ip) for ip in network.hosts()])

    print(f"\nFound {len(vulnerable)} Potentially Vulnerable Hosts")

    return vulnerable


if __name__ == "__main__":
    subnet = input("Subnet: ").strip()
    scan_subnet(subnet)
