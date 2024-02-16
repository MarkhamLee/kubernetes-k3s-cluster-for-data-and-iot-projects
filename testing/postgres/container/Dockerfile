FROM python:3.12.2-slim as build

COPY main.py logging_util.py requirements.txt postgres_client.py /
RUN pip install -r /requirements.txt

CMD python3 main.py 