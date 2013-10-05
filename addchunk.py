#!/usr/bin/env python3
import requests, time, urllib.parse, sys, base64, json
from config import endpoint

if len(sys.argv) < 5:
    print("Usage: " + sys.argv[0] + " <size of this chunk> <file id> <chunk number> <infile>", file=sys.stderr)
    sys.exit(1)

totalsize = int(sys.argv[1])
fileid = sys.argv[2]
chunknumber = sys.argv[3]
infilepath = sys.argv[4]

def f():
    yield b"fileid=" + fileid.encode("ascii") + b"&chunknumber=" + chunknumber.encode("ascii") + b"&cryptochunk="
    read = 0
    with open(infilepath, "rb") as f:
        oldnum = -1
        while True:
            c = f.read(min(1024, totalsize))
            if not c: break
            #yield "".join(["%" + hex(i)[2:].upper().zfill(2) for i in c]).encode("ascii")
            #yield urllib.parse.quote_plus(base64.b64encode(c)).encode("ascii")
            yield urllib.parse.quote_plus(c.decode("ascii")).encode("ascii")
            #yield urllib.parse.quote_plus(c).encode("ascii")
            read += len(c)
            num = int(read / totalsize * 99)
            if num > 99: num = 99
            if num != oldnum: print(num)
            oldnum = num
    print(100)

req = requests.post( "{}/addchunk".format(endpoint), data=f(), headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    assert json.loads(req.text)["status"] == "ok"
except:
    print(req.text, file=sys.stderr)
