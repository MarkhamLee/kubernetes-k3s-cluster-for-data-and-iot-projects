# Stage 1: build wheels
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY /hw_monitoring_libraries/requirements.txt .

RUN pip3 wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# Stage 2: runtime image
FROM python:3.11-slim-bookworm

# Create non-root user and group
RUN groupadd --system app_group \
    && useradd --system --create-home --no-log-init --gid app_group app_user

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip3 install --no-cache-dir /wheels/* \
    && rm -rf /wheels

COPY --chown=appuser:appuser ./hw_monitoring_libraries ./hw_monitoring_libraries
COPY --chown=appuser:appuser ./amd64 ./amd64

# Set workdir and copy wheels
WORKDIR /hw_telemetry

# Ensure app files are owned by the non-root user
RUN chown -R app_user:app_group ./amd64 ./

# Drop privileges
USER app_user

ENTRYPOINT ["python3", "/hw_telemetry/main.py"]