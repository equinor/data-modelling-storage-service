class UseCase:
    def execute(self, request_object=None):
        return self.process_request(request_object)

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")
