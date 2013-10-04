#!/usr/bin/env python3
import requests, time, urllib.parse, sys, base64, json

if len(sys.argv) < 4:
    print("Usage: " + sys.argv[0] + " <size of this chunk> <file id> <chunk number>")
    sys.exit(1)

totalsize = int(sys.argv[1])
fileid = sys.argv[2]
chunknumber = sys.argv[3]

def f():
    yield b"fileid=" + fileid.encode("ascii") + b"&chunknumber=" + chunknumber.encode("ascii") + b"&cryptochunk="
    read = 0
    while True:
        c = sys.stdin.buffer.read(1024)
        if not c: break
        #yield "".join(["%" + hex(i)[2:].upper().zfill(2) for i in c]).encode("ascii")
        yield urllib.parse.quote_plus(base64.b64encode(c)).encode("ascii")
        #yield urllib.parse.quote_plus(c).encode("ascii")
        read += len(c)
        print(int(read / totalsize * 100))

req = requests.post( "http://localhost:8801/api/addchunk", data=f(), headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    assert json.loads(req.text)["status"] == "ok"
except:
    print(req.text)
