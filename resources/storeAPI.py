import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreUploadSchema

blueprint = Blueprint(
                        "store", 
                        __name__, 
                        description="Operations on Store"
                    )

@blueprint.route("/store")
class StoreList(MethodView):
    def get(self):
        return {"Stores": list(stores.values())}
    
    @blueprint.arguments(StoreUploadSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(
                    400,
                    message="Store already exist"
                )
        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201


@blueprint.route("/store/<string:store_id>")
class StoreWithId(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id], 201
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted successfully."}
        except KeyError:
            abort(
                404,
                message="Store not found."
            )

