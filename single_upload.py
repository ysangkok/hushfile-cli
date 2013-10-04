#!/usr/bin/env python3
import requests

print(
    requests.post(
        "http://localhost:8801/api/upload", 
        data={'metadata': 'metadata','deletepassword': 'deletepassword'}, 
        files={"cryptofile": open("large_file.txt","rb")}
        #headers={"Content-Length": len(prolog) + os.stat('large_file.txt').st_size * 3, "Content-Type": "application/x-www-form-urlencoded"}
    ).text
)
