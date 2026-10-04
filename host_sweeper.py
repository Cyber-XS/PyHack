import subprocess
from concurrent.futures import ThreadPoolExecutor
from ipaddress import ip_network

results = []

def ping_host(ip):
    result = subprocess.run(['ping', '-c', '1', '-w', '2', str(ip)], capture_output=True, text=True)
    if result.returncode == 0:
        results.append(ip)
        return True
    return False

def sweep_subnet(subnet, threads=100):
    network = ip_network(subnet, strict=False)
    print(f' Sweeping {subnet} \n')
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for ip in network.hosts():
            executor.submit(ping_host, ip)
    print(f' Found {len(results)} active host ')
    return sorted(results)
