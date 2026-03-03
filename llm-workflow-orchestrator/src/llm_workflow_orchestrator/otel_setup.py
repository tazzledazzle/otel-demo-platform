"""OpenTelemetry setup: tracer provider, OTLP export, httpx instrumentation."""

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from llm_workflow_orchestrator.config import get_otlp_endpoint


def setup_otel(service_name: str = "llm-workflow-orchestrator") -> None:
    """Configure global TracerProvider with OTLP export and instrument httpx (for LLM API calls)."""
    endpoint = get_otlp_endpoint()
    # Strip http:// or https:// for gRPC; endpoint is host:port
    if endpoint.startswith("http://"):
        endpoint = endpoint[7:]
    elif endpoint.startswith("https://"):
        endpoint = endpoint[8:]

    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=endpoint or "localhost:4317", insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    HTTPXClientInstrumentor().instrument()
