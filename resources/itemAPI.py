import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blueprint = Blueprint(
    "items",
    __name__,
    description="Operation on Items"
)

@blueprint.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    @blueprint.arguments(ItemUpdateSchema)
    def post(self, item_data):
        for item in items.values():
            if(
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(
                    400,
                    message="Items already exists."
                )

        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201

@blueprint.route("/item/<string:item_id>")
class ItemwithID(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(
                404,
                message="item not found."
                )
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item Deleted."}
        except KeyError:
            abort(
                404,
                message="Item not found."
            )

    @blueprint.arguments(ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
    
        except KeyError:
            abort(
                404,
                message="Item not found"
            )