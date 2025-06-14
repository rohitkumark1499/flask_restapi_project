import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)


# Get all store details
@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


# Get details of particular store
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        # return {"message": "Store not found"}, 404
        abort(404, message="Store not found.")


# Create a store
@app.post("/store")
def create_store():
    store_data = request.get_json()

    if ("name" not in store_data):
        abort(400, message="Bad request. Ensure 'name' are included in json payload")

    for store in stores.values():
        if (store_data["name"] == store["name"]):
            abort(400, message=f"Store already exists.")

    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


# Delete a store
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted"}
    except KeyError:
        abort(404, message=f"Store not found")


# Get all items list
@app.get("/item")
def get_all_items():
    return {"items": list(items.values())}


# Get details of paricular items
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        # return {"message": "Item not found"}, 404
        abort(404, message="Item not found.")


# Create items
@app.post("/item")
def create_item():
    item_data = request.get_json()

    if ("price" not in item_data or "store_id" not in item_data or "name" not in item_data):
        abort(400, message="Bad request. Ensure 'price','store_id' and 'name' are included in json payload")

    for item in items.values():
        if (item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]):
            abort(400, message=f"Item already exists.")

    if item_data["store_id"] not in stores:
        # return {"message": "Store not found"}, 404
        abort(404, message="Store not found.")

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item, 201


# update the item details
@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if ("price" not in item_data or "name" not in item_data):
        abort(400, message="Bad request. Ensure 'price' and 'name' are in json payload.")

    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:
        abort(404, message=f"Item not found")


# Delete an item
@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted"}
    except KeyError:
        abort(404, message=f"Item not found")
