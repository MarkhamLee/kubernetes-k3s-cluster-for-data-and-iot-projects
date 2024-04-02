# temp stage 
FROM python:3.12.2-slim as build

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc  python3-dev

COPY /hw_monitoring_libraries/requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.12-slim

COPY ./hw_monitoring_libraries ./hw_monitoring_libraries

WORKDIR /hw_telemetry

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY ./rockchip3588 ./

ENTRYPOINT ["python3", "/hw_telemetry/main.py"] 