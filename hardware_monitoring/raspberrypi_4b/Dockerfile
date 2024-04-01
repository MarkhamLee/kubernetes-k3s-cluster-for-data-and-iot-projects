# temp stage

FROM python:3.12-slim as builder

RUN apt-get update -y && apt-get install -y gcc  python3-dev


# final stage 
FROM python:3.12-slim

COPY ./hw_monitoring_libraries ./hw_monitoring_libraries

RUN pip install -r /hw_monitoring_libraries/requirements.txt

WORKDIR /hw_telemetry

COPY ./raspberrypi_4b ./

ENTRYPOINT ["python3", "/hw_telemetry/main.py"] 