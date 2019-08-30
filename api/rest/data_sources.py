from flask import request
from flask_restful import Resource

from rest.validators.mongo_data_source import validate_mongo_data_source
from services.database import data_modelling_tool_db as database
from utils.logging import logger
from config import Config

collection = database[f"{Config.DATA_SOURCES_COLLECTION}"]


def data_sources_get(document_type: str):
    all_sources = []
    for source in collection.find(filter={"documentType": document_type}, projection=["host", "name", "type"]):
        source["_id"] = str(source["_id"])
        all_sources.append(source)
    return all_sources


def data_source_post():
    document = request.get_json()
    validate_mongo_data_source(document)
    logger.info(f"Inserting new data-source named {document['name']}.")
    result = collection.insert_one(document)
    logger.info(f"Successfully inserted with id {result}")
    return str(result.inserted_id)


def data_source_put(_id):
    document = request.get_json()
    validate_mongo_data_source(document)
    result = collection.replace_one({"_id": _id}, document, upsert=True)
    return str(result.acknowledged)


def data_source_delete(_id):
    result = collection.delete_one(filter={"_id": _id})
    return result.acknowledged


class SingleDataSource(Resource):
    @staticmethod
    def put(_id):
        return data_source_put(_id=_id)

    @staticmethod
    def delete(_id):
        return data_source_delete(_id=_id)


class DataSources(Resource):
    @staticmethod
    def get(document_type):
        return data_sources_get(document_type)

    @staticmethod
    def post():
        return data_source_post()
