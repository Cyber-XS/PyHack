import subprocess
import re
from ipaddress import ip_network
from concurrent.futures import ThreadPoolExecutor

def fingerprint_samba(ip):
    try:
        cmd = ['nmap', '-Pn', '-p', '139,445', '--script', 'smb-os-discovery', '-oN', '-', ip]
        result = subprocess.run(cmd,
            capture_output=True,
            text=True,
            timeout=15)
        output = result.stdout
        if 'Samba' not in output:
            return
        match = re.search(r"Samba\s+([^\s\)]+)",
        output,
        re.IGNORECASE
        )

        version = match.group(1) if match else 'Unknown'

        ports = []

        if re.search(r"139/tcp\s+open", output):
            ports.append('139')
        if re.search(r"445/tcp\s+open", output):
            ports.append('445')

        print(f'\n Samba detected: {ip}')
        print(f'    Service: Samba')
        print(f'    Version: {version}')
        print(f'    Ports: {','.join(ports)}')
    except subprocess.TimeoutExpired:
        print(f' [-] {ip}: Timeout ')
    except Exception as e:
        print(f' [-] {ip}:{e} ')

def main():
    subnet = input('Subnet: ').strip()

    hosts = [str(ip) for ip in ip_network(subnet, strict=False).hosts()]

    print(f'[*] Scanning {subnet}')
    print(f'[*] Hosts: {len(hosts)}\n')

    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(fingerprint_samba, hosts)

if __name__ == '__main__':
    main()
