#!/bin/bash
set -e

if [[ "$*" == bash ]]; then
  exec /bin/bash
fi

if [[ ! -f /cowry/cowry.conf ]]; then
  python cowry -n
  #ln -sf "/cowry/cowry.conf" "/conf/"
fi

if [[ -f /cowry/cowry.conf ]]; then
  sed -i 's/cluster = 0/cluster = 1/g' /cowry/cowry.conf
fi

exec "$@"
