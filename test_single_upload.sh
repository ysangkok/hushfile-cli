#!/bin/bash -ex
. config
CON="$(./single_upload.py)"
echo $CON
FILEID=$(echo $CON | python3 -c "import sys; import json; l = sys.stdin.read(); print(json.loads(l)['fileid']);")
curl -o download.txt "$ENDPOINT/file?fileid=$FILEID"
diff download.txt large_file.txt
echo $?
