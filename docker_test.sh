#!/bin/sh
docker build -t meta_magical_garden . && docker run --entrypoint ./test.sh --rm meta_magical_garden
