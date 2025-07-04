#!/usr/bin/env bash

version=$(awk -F\" '/__version__/ {print $2}' ./src/main.py | head -n1)
base_tag='ghcr.io/steveharsant/tide-invite'

echo "$GITHUB_TOKEN" | docker login ghcr.io -u steveharsant --password-stdin
docker build -t "$base_tag:latest" -t "$base_tag:$version" .
docker push "$base_tag:latest"
docker push "$base_tag:$version"
docker logout