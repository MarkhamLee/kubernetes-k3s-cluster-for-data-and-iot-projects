# build phase
FROM python:slim-bookworm as builder

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc  python3-dev

COPY ./intel_x86/requirements.txt .

RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# stage two
FROM python:slim-bookworm

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip3 install --no-cache /wheels/*

COPY ./hw_monitoring_libraries ./hw_monitoring_libraries

WORKDIR /hw_telemetry

COPY ./intel_x86_nvidia_gpu ./

ENTRYPOINT ["python3", "/hw_telemetry/main.py"] 