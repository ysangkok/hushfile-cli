#!/bin/bash -ex
. config
INFILE="large_file.txt"
PASSPHRASE="Secret Passphrase"
FILEID=$(./moren.py "$INFILE" "$PASSPHRASE" | tail -n1)
URL="$ENDPOINT/file?fileid=$FILEID"
curl "$URL" | openssl enc -d -aes-256-cbc -pass pass:"$PASSPHRASE" -base64 | diff - "$INFILE"
