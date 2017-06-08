#!/bin/bash
set -e
echo "start write key to environment variable"
sleep 2
if [[ -f /certs/server.pub.key ]]; then
  ssh-keygen -f /certs/server.pub.key -i -m PKCS8 > /tmp/key
  export SSH_AUTHORIZED_KEYS=`cat /tmp/key`
else
  echo "not find server.pub.key"
fi
exec "$@"
