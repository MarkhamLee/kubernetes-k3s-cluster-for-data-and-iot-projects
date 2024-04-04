# temp stage 

FROM python:alpine as builder

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc  python3-dev

COPY /hw_monitoring_libraries/requirements.txt .

RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:alpine

COPY ./hw_monitoring_libraries ./hw_monitoring_libraries

WORKDIR /hw_telemetry

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip3 install --no-cache /wheels/*

COPY ./rockchip3588 ./

ENTRYPOINT ["python3", "/hw_telemetry/main.py"] 