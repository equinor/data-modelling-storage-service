from restful import response_object as res
import traceback

from utils.exceptions import EntityNotFoundException, FileNotFoundException, InvalidDocumentNameException


class UseCase(object):
    def execute(self, request_object=None):
        try:
            return self.process_request(request_object)
        except EntityNotFoundException as not_found:
            return res.ResponseFailure.build_resource_error(not_found.message)
        except InvalidDocumentNameException as invalid_name:
            return res.ResponseFailure.build_parameters_error(invalid_name.message)
        except FileNotFoundException as not_found:
            return res.ResponseFailure.build_resource_error(
                f"The file '{not_found.file}' was not found on data source '{not_found.data_source_id}'"
            )
        except Exception as exc:
            traceback.print_exc()
            return res.ResponseFailure.build_system_error("{}: {}".format(exc.__class__.__name__, "{}".format(exc)))

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")
