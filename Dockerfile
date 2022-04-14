FROM python:3.10.4

USER root

ENV APP_DIR="/app"
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY drobo_keepalive.py drobo_keepalive.py

ENTRYPOINT ["/usr/local/bin/python3"]
CMD ["drobo_keepalive.py"]
