#!/bin/bash
set -eu
mkdir -p ./rendered/

for f in ./deployment/*.yml
do
  filename=$(basename "$f")
  envsubst < "$f" > "./rendered/$filename"
done
