#!/bin/bash
set -e

if [[ "$*" == bash ]]; then
  exec /bin/bash
fi
if [[ ! -f /setup.py ]]; then
  python /cowry-workers/setup.py
fi

exec "$@"
