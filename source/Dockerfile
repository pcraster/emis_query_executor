FROM pcraster/emis_base:latest

MAINTAINER Kor de Jong <k.dejong1@uu.nl>

# COPY requirements.txt /
# RUN pip install -r requirements.txt

COPY cmd.sh server.py server_development.py server_production.py /
COPY query_executor /query_executor
COPY test /test

CMD ["/cmd.sh"]
