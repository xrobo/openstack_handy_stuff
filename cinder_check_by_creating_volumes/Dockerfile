FROM alpine:latest

RUN /sbin/apk add \
	python3 zabbix-utils \
	py3-pip python3-dev gcc musl-dev linux-headers \
	&& /usr/bin/python3 -m pip install python-cinderclient \
	&& /sbin/apk del python3-dev gcc musl-dev linux-headers
	
ENTRYPOINT ["/usr/bin/python3"]

CMD ["--help"]
