#!/usr/bin/env python3
import requests, sys
from config import endpoint

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <number of chunks>", file=sys.stderr)
    sys.exit(1)

print(
    requests.post(
        "{}/upload".format(endpoint), 
        data={'metadata': 'metadata','deletepassword': 'deletepassword', "numberofchunks": sys.argv[1]}, 
    ).text
)
