from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel

from schemas import StoreSchema

blueprint = Blueprint(
                        "store", 
                        __name__, 
                        description="Operations on Store"
                    )

@blueprint.route("/store")
class StoreList(MethodView):
    @blueprint.response(201, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blueprint.arguments(StoreSchema)
    @blueprint.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A Store with the same name already exist."
            )
        except SQLAlchemyError:
            abort(
                500,
                message="An error occured while creating the store."
            )
        
        return store


@blueprint.route("/store/<string:store_id>")
class StoreWithId(MethodView):
    @blueprint.response(201, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store Deleted"}

