FROM cowry-dev
MAINTAINER i@aong.cn

RUN mkdir /cowry
RUN mkdir /conf

ADD ./ /cowry/
WORKDIR /cowry

RUN pip3 install -r requirements.txt

COPY docker-entrypoint.sh /cowry/entrypoint.sh

RUN chmod a+x /cowry/entrypoint.sh
ENTRYPOINT ["/cowry/entrypoint.sh"]

EXPOSE 2333
EXPOSE 3000

CMD ["/cowry/cowry", "-s", "-q", "-w"]
