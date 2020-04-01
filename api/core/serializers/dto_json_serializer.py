import json

from api.classes.dto import DTO


class DTOSerializer(json.JSONEncoder):
    def default(self, dto: DTO):
        try:
            return dto.to_dict()
        except AttributeError:
            return super().default(dto)
