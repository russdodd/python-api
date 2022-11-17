# main.py

from fastapi import FastAPI
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

app = FastAPI()

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return read_item(item_id)

def read_item(item_id: int) -> dict:
    with tracer.start_as_current_span("read_item") as item_span:
        item_span.set_attribute("item.id", item_id)
        return {"message": "Hello World", "item": item_id}
