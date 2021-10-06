FROM python:3.9-alpine

COPY src /opt/
RUN pip install -e /opt/

ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:7600", "mqtt2json:app"]