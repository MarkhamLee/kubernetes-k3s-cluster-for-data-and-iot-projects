import os
import time
import random

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.\
    exporter.otlp.proto.\
    http.trace_exporter import OTLPSpanExporter


def env(name: str, default: str) -> str:
    value = os.getenv(name, default).strip()
    if not value:
        return default
    return value


endpoint = env("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT", "http://192.168.47.209:4318/v1/traces")  # noqa: E501
service_name = env("OTEL_SERVICE_NAME", "otel-python-smoke-test-2")
environment = env("OTEL_ENVIRONMENT", "dev")

resource = Resource.create(
    {
        "service.name": service_name,
        "deployment.environment": environment,
        "test.script": "test_otel_trace.py",
    }
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

print(f"Sending trace to: {endpoint}")
print(f"service.name={service_name} deployment.environment={environment}")

with tracer.start_as_current_span("smoke_test_run") as root:
    root.set_attribute("smoke_test", True)
    root.set_attribute("run.id", f"run-{int(time.time())}")
    root.set_attribute("component", "manual-python-test")

    with tracer.start_as_current_span("load_config") as span:
        delay = round(random.uniform(0.05, 0.25), 3)
        span.set_attribute("config.source", "local-env")
        span.set_attribute("simulated.delay_ms", int(delay * 1000))
        time.sleep(delay)

    with tracer.start_as_current_span("call_dependency") as span:
        delay = round(random.uniform(0.1, 0.4), 3)
        span.set_attribute("dependency.name", "fake-api")
        span.set_attribute("dependency.type", "http")
        span.set_attribute("simulated.delay_ms", int(delay * 1000))
        time.sleep(delay)

    with tracer.start_as_current_span("run_query") as span:
        delay = round(random.uniform(0.03, 0.18), 3)
        span.set_attribute("db.system", "postgresql")
        span.set_attribute("db.operation", "SELECT")
        span.set_attribute("db.statement", "select now()")
        span.set_attribute("simulated.delay_ms", int(delay * 1000))
        time.sleep(delay)

provider.shutdown()
print("Done. Check collector logs for spans from service.name=otel-python-smoke-test")  # noqa: E501
