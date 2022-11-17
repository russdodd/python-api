# main.py

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry import metrics
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

app = FastAPI()

item_request_counter = meter.create_counter(
    "item_request_counter",
    description="The number of items requested",
)

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return read_item(item_id)

def read_item(item_id: int) -> dict:
    with tracer.start_as_current_span("read_item") as item_span:
        item_span.set_attribute("item.id", item_id)
        wait_a_little()
        item_request_counter.add(1, {"item.id": item_id})
        return {"message": "Hello World", "item": item_id}

def wait_a_little():
    x = 1
    for i in range(10000000):
        x+=1