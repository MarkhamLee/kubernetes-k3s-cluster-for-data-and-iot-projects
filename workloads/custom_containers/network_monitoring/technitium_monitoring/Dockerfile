# Temp Stage
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update -y && apt-get install -y \
    gcc python3-dev g++ libblas-dev liblapack-dev build-essential

COPY technitium_monitoring/requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Final Stage
FROM python:3.12-slim-bookworm


COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt /requirements.txt


RUN pip install --no-cache-dir /wheels/* && \
    rm -rf /wheels && \
    useradd --create-home --uid 10001 appuser

COPY --chown=appuser:appuser  ./network_monitoring_libraries ./network_monitoring_libraries

WORKDIR /technitium_monitoring

COPY --chown=appuser:appuser  ./technitium_monitoring ./

USER appuser

ENTRYPOINT ["python3", "/technitium_monitoring/main.py"]