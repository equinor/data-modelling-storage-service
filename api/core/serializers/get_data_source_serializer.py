import json


class GetDataSourceSerializer(json.JSONEncoder):
    def default(self, obj):
        data_source = obj.value
        try:
            to_serialize = {
                "id": data_source["_id"],
                "name": data_source["name"],
                "host": data_source.get("host", ""),
                "type": data_source["type"],
                "documentType": data_source["documentType"],
            }
            return to_serialize
        except AttributeError:
            return json.JSONEncoder.default(self, {})
