FROM python:3.12.2-slim as build

RUN apt-get update -y && apt-get install -y gcc  python3-dev

COPY requirements.txt amd_5560u.py main.py /
RUN pip install -r /requirements.txt

CMD python3 main.py 