#!/bin/bash
set -e

if [[ -f /certs/server.pub.key ]]; then
  ssh-keygen -f /certs/server.pub.key -i -m PKCS8 > /tmp/key
  export SSH_AUTHORIZED_KEYS=`cat /tmp/key`
else
  echo "not find server.pub.key"
fi
echo "start alter user privilege"
chown cowry:cowry /data

exec "$@"
