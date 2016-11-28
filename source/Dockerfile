FROM python:3.5

MAINTAINER Kor de Jong <k.dejong1@uu.nl>
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi

COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY emis_query_executor /emis_query_executor
COPY uwsgi.ini /
COPY cmd.sh /
COPY server.py /
COPY server_flask.py /
COPY server_wsgi.py /
COPY test /test

USER uwsgi
CMD ["/cmd.sh"]
