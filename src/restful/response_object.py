class ResponseSuccess(object):
    SUCCESS = "SUCCESS"

    def __init__(self, value=None):
        self.type = self.SUCCESS
        self.value = value

    def __nonzero__(self):
        return True

    __bool__ = __nonzero__


class ResponseFailure(object):
    RESOURCE_ERROR = "RESOURCE_ERROR"
    PARAMETERS_ERROR = "PARAMETERS_ERROR"
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"
    SYSTEM_ERROR = "SYSTEM_ERROR"

    def __init__(self, type_, message):
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, msg):
        if isinstance(msg, Exception):
            return f"{msg.__class__.__name__}: {msg}"
        return msg

    @property
    def value(self):
        return {"type": self.type, "message": self.message}

    def __bool__(self):
        return False

    @classmethod
    def build_resource_error(cls, message=None):
        return cls(cls.RESOURCE_ERROR, message)

    @classmethod
    def build_system_error(cls, message=None):
        return cls(cls.SYSTEM_ERROR, message)

    @classmethod
    def build_parameters_error(cls, message=None):
        return cls(cls.PARAMETERS_ERROR, message)

    @classmethod
    def build_entity_error(cls, message=None):
        return cls(cls.UNPROCESSABLE_ENTITY, message)
