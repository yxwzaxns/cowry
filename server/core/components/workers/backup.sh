#!/usr/bin/env bash
scp -i /certs/server.key -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $1 cowry@backup:/data
