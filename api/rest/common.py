from flask import jsonify, request, abort

from services.database import model_db
from utils.schema_tools import mongo_document_to_json_schema, json_schema_to_mongo_document


def common_get(collection, path):
    document = model_db[f'{collection}'].find_one({"_id": path})
    if not document:
        return abort(404)
    schema = mongo_document_to_json_schema(document)
    return jsonify(schema)


def common_put(collection, path):
    data = request.get_json()
    data['_id'] = path
    document = json_schema_to_mongo_document(data)
    try:
        model_db[f'{collection}'].replace_one({'_id': path}, document, upsert=True)
        return path
    except Exception as e:
        abort(500, f"Something went wrong: {e}")
