#!/usr/bin/env python3
import sys, subprocess, os, json, shlex, time
from math import ceil
from traceback import print_exc

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " <file> <passphrase>", file=sys.stderr)
    sys.exit(1)

infilepath = sys.argv[1]
passphrase = sys.argv[2]

chunksize = 1000000

stats = os.stat(infilepath)
base64enlargement = lambda x: ceil(x / 3) * 4
numberchunks = int(ceil(base64enlargement(stats.st_size) / chunksize))
if numberchunks > 30:
    print("File too large or chunks too small. Number chunks: " + str(numberchunks), file=sys.stderr)
    sys.exit(1)

chunkpipes = ["chunk{}".format(str(i).zfill(len(str(numberchunks-1)))) for i in range(numberchunks)]

for i in chunkpipes:
    os.mkfifo(i)

try:
    c = subprocess.check_output(["./initchunked.py", str(numberchunks)])
    fileid = json.loads(c.decode("utf-8"))["fileid"]
    
    cmd = ["./multi_progress.py"] + [json.dumps(["./addchunk.py", chunksize, fileid, x[0], x[1]]) for x in enumerate(chunkpipes)]
    #print(" ".join(shlex.quote(x) for x in cmd), file=sys.stderr)
    #input("continue?")
    p = subprocess.Popen(" ".join(shlex.quote(x) for x in cmd) + "&", shell=True, stderr=subprocess.PIPE)
    time.sleep(1)

    subprocess.check_call("cat " + shlex.quote(infilepath) + " | openssl enc -aes-256-cbc -pass pass:" + shlex.quote(passphrase) + " -e -base64 | ./distribute_over_pipes.py " + str(chunksize) + " " + " ".join([shlex.quote(i) for i in chunkpipes]) + "", shell=True)

    p.wait(timeout=5)
    stderr = p.stderr.read().decode("utf-8")
    if stderr:
        print(stderr, file=sys.stderr)

    assert json.loads(subprocess.check_output(["./concatchunks.py", fileid]).decode("utf-8"))["status"] == "ok"

    print(fileid)
finally:
    for i in chunkpipes: os.remove(i)
