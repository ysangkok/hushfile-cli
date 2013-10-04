#!/usr/bin/env python3
import requests, sys

if len(sys.argv) < 2:
    print("Usage: " + sys.argv[0] + " <file id>")
    sys.exit(1)

print(
    requests.post(
        "http://localhost:8801/api/concatchunks",
        data={'fileid': sys.argv[1]}
    ).text
)
