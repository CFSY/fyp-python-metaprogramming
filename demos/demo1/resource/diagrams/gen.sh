#!/usr/bin/env bash

for file in *.d2; do
    [ -e "$file" ] || continue
    base="${file%.d2}"
    d2 -t 300 "$file" "$base.png"
done