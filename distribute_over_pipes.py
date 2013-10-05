#!/usr/bin/env python3
import sys

if len(sys.argv) < 3:
    print("Usage: " + sys.argv[0] + " <chunk size> <chunk 0> [<chunk 1> [<chunk n> ...]]", file=sys.stderr)
    sys.exit(1)

chunksize = int(sys.argv[1])

leng = len(sys.argv[2:])
for i, filename in enumerate(sys.argv[2:]):
    #print("opening " + filename, file=sys.stderr)
    with open(filename, "wb") as f:
        #print("writing " + filename, file=sys.stderr)
        written_to_this_fd = 0
        while True:
            c = sys.stdin.buffer.read(min(1024, chunksize))
            if not c:
                if i < leng - 1:
                    print("warning: input ended before we reached last chunk", file=sys.stderr)
                    sys.exit(1)
                sys.exit(0) # normal exit
            f.write(c)
            written_to_this_fd += len(c)
            if written_to_this_fd >= chunksize and i < leng - 1: break
