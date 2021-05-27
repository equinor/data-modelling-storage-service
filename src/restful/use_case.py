from restful import response_object as res
import traceback

from utils.exceptions import (
    DataSourceAlreadyExistsException,
    DataSourceNotFoundException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    FileNotFoundException,
    InvalidDocumentNameException,
    RootPackageNotFoundException,
)
from utils.logging import logger


class UseCase(object):
    def execute(self, request_object=None):
        try:
            return self.process_request(request_object)
        except (EntityNotFoundException, DataSourceNotFoundException, RootPackageNotFoundException) as not_found:
            logger.warning(not_found.message)
            return res.ResponseFailure.build_resource_error(not_found.message)
        except InvalidDocumentNameException as invalid_name:
            return res.ResponseFailure.build_parameters_error(invalid_name.message)
        except EntityAlreadyExistsException as e:
            return res.ResponseFailure.build_parameters_error(e)
        except FileNotFoundException as not_found:
            return res.ResponseFailure.build_resource_error(
                f"The file '{not_found.file}' was not found on data source '{not_found.data_source_id}'"
            )
        except DataSourceAlreadyExistsException as error:
            return res.ResponseFailure.build_parameters_error(error.message)
        except Exception as exc:
            traceback.print_exc()
            return res.ResponseFailure.build_system_error("{}: {}".format(exc.__class__.__name__, "{}".format(exc)))

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")
