from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My store",
        "items": [
            {
                "name": "chair",
                "price": 15.99
            }
        ]
    }
]

# Get all store deatils


@app.get("/store")
def get_stores():
    return {"stores": stores}

# Create a store


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201

# Create / add items to store


@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_items = {
                "name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_items)
            return new_items, 201
    return {"message": "Store not found"}, 404

# Get details of particular store


@app.get("/store/<string:name>")
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return store
    return {"message": "Store not found"}, 404

# Get details of items in a store


@app.get("/store/<string:name>/item")
def get_item(name):
    for store in stores:
        if store["name"] == name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404
