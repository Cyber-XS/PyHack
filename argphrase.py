import argparse

parse = argparse.ArgumentParser()

parse.add_argument(
    "--target", "-t", required=True, help="Enter your Target IP or Host Name"
)
parse.add_argument(
    "--ports", "-p", default="1-1024", help="Enter ports [ Default : 1-1024 ]"
)
parse.add_argument(
    "--threads", type=int, default=100, help="Enter Theads [ Default : 100 ]"
)
parse.add_argument("--output", help="Save your result in Output file")
parse.add_argument("--verbose", action="store_true", help="Display verbose Output")

args = parse.parse_args()

print(f"Target : {args.target}")
print(f"Ports : {args.ports}")
print(f"Threads : {args.threads}")
print(f"Output : {args.output}")
print(f"Verbose : {args.verbose}")
