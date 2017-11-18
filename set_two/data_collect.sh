#!/usr/bin/env bash



last -Fwx > last_batch_$1.log


cat last_batch_$1 | awk '{ print $7 }' > stripped_batch_$1.txt
