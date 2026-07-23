# temp stage
FROM python:3.12-slim-bookworm 

WORKDIR /app

RUN apt-get update -y && apt-get install -y gcc python3-dev g++ libblas-dev liblapack-dev build-essential

RUN pip install --upgrade pip setuptools wheel

COPY /technitium_monitoring/requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# final stage
FROM python:3.12-slim-bookworm 

# Create non-root user and group
RUN groupadd --system app_group \
    && useradd --system --create-home --no-log-init --gid app_group app_user

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip3 install --no-cache-dir /wheels/* \
    && rm -rf /wheels

COPY  --chown=appuser:appuser ./network_monitoring_libraries ./network_monitoring_libraries

WORKDIR /technitium_monitoring

COPY --chown=appuser:appuser ./technitium_monitoring ./

# Drop privileges
USER app_user

ENTRYPOINT ["python3", "/technitium_monitoring/main.py"]