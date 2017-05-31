FROM daocloud.io/yxwzaxns/cowry-backup
MAINTAINER i@aong.cn

RUN mkdir /certs
RUN mkdir /data

COPY redis.tar.gz /tmp/redis.tar.gz
COPY docker-entrypoint.sh /entrypoint.sh
COPY setup.sh /setup.sh

WORKDIR /tmp
RUN tar zxvf  /tmp/redis.tar.gz

WORKDIR /tmp/redis-2.10.5

RUN python setup.py install

RUN chmod a+x /setup.sh
RUN chmod a+x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/usr/bin/supervisord", "--configuration=/etc/supervisord.conf"]

EXPOSE 22
