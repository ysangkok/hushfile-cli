#!/usr/bin/env python3
import requests, sys
from config import endpoint

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <file id>", file=sys.stderr)
    sys.exit(1)

print(
    requests.post(
        "{}/concatchunks".format(endpoint),
        data={'fileid': sys.argv[1]}
    ).text
)
