#!/usr/bin/env python3
import requests, sys, json
from config import endpoint

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " <number of chunks> <encrypted metadata>", file=sys.stderr)
    sys.exit(1)

metadata = sys.stdin.buffer.read().decode("utf-8")

print(
    requests.post(
        "{}/upload".format(endpoint), 
        data={'metadata': sys.argv[2], 'deletepassword': json.loads(metadata)["deletepassword"], "numberofchunks": sys.argv[1]}, 
    ).text
)
