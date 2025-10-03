#!/bin/bash
set -e
cd "$(dirname "$0")"

podman run \
  --rm \
  --name lgsl_postgres \
  -e POSTGRES_USER=guest \
  -e POSTGRES_PASSWORD='asdf;lkj' \
  -e POSTGRES_DB=lgsl \
  -p 5432:5432 \
  postgres:latest
