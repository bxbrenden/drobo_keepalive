FROM python:3.9.7

USER root

ENV APP_DIR="/app"
RUN mkdir $APP_DIR
WORKDIR $APP_DIR

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY drobo_keepalive.py drobo_keepalive.py

CMD ["python3", "drobo_keepalive.py"]
