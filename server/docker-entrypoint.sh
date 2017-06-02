#!/bin/bash
set -e

if [[ "$*" == bash ]]; then
  exec /bin/bash
fi

if [[ ! -f /cowry/cowry.conf ]]; then
  python cowry -n
  ln -sf "/cowry/cowry.conf" "/conf/"
fi

exec "$@"
