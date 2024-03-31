FROM python:3.12-slim as build

RUN apt-get update -y && apt-get install -y gcc  python3-dev

COPY ./hw_monitoring_libraries ./hw_monitoring_libraries

WORKDIR /hw_telemetry

COPY ./raspberrypi_4b ./

RUN pip install -r /hw_telemetry/requirements.txt

CMD python3 /hw_telemetry/main.py 