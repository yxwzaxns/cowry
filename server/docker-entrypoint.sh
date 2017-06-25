#!/bin/bash
set -e

if [[ "$*" == bash ]]; then
  exec /bin/bash
fi

sleep 20

if [[ -f /cowry/cowry.conf.default ]]; then
  sed -i 's/cluster = 0/cluster = 1/g' /cowry/cowry.conf.default
  # sed -i 's/type = sqlite/type = mysql/g' /cowry/cowry.conf.default
  # sed -i 's/host = 127.0.0.1/host = mysql/g' /cowry/cowry.conf.default
fi

if [[ ! -f /cowry/cowry.conf ]]; then
  python cowry -n
  #ln -sf "/cowry/cowry.conf" "/conf/"
fi

exec "$@"
