import json
from dataclasses import dataclass, field

from fastapi import FastAPI, HTTPException, Response

app = FastAPI()


@dataclass
class Product:
    id: str
    name: str
    tags: list[str] = field(default_factory=list)
    description: str = ""


products: dict[str, Product] = {}

with open("products.json", encoding="utf8") as file:
    products_raw = json.load(file)
    for product_raw in products_raw:
        product = Product(**product_raw)
        products[product.id] = product


@app.get("/")
def read_root() -> Response:
    return Response("The server is running.")


@app.get("/products/{product_id}", response_model=Product)
def read_item(product_id: str) -> Product:
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    return products[product_id]
