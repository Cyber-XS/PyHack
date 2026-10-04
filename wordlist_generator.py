import argparse, itertools

OUTPUT = "wordlist.txt"

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-w", "--words", nargs="+", default=["msfadmin", "admin", "123456", "password"])
    parser.add_argument("-o", "--output", default=OUTPUT)
    parser.add_argument("-l", "--length", type=int, default=2)

    args = parser.parse_args()

    words = args.words
    passwords = set()

    for length in range(1, args.length + 1):
        for combo in itertools.product(words, repeat=length):
            passwords.add("".join(combo))
    with open(args.output, "w") as file:
        for password in sorted(passwords):
            file.write(password + "\n")

    print("=" * 50)
    print("PyHack - Wordlist Generator")
    print("=" * 50)
    print(f" [*] Words: {len(words)} ")
    print(f" [*] Length: {args.length} ")
    print(f" [*] Entries: {len(passwords)} ")
    print(f" [*] Output: {args.output} ")
    print("=" * 50)

if __name__ == "__main__":
    main()
