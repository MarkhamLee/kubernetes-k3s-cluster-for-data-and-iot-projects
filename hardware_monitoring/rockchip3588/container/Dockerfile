FROM python:3.12.2-slim as build

RUN apt-get update -y && apt-get install -y gcc  python3-dev

COPY requirements.txt rockchip_3588.py main.py influx_client.py /
RUN pip install -r /requirements.txt

CMD python3 main.py 