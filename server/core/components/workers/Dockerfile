FROM cowry-dev
MAINTAINER i@aong.cn

RUN mkdir /cowry-workers
RUN mkdir /data

ADD ./ /cowry-workers

WORKDIR /cowry-workers

RUN pip3 install -r requirements.txt

RUN chmod a+x /cowry-workers/docker-entrypoint.sh
ENTRYPOINT ["/cowry-workers/docker-entrypoint.sh"]

EXPOSE 2334

CMD ["python", "/cowry-workers/workerd.py"]
