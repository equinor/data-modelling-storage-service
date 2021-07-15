from restful import response_object as res
import traceback

from utils.exceptions import (
    DataSourceAlreadyExistsException,
    DataSourceNotFoundException,
    EntityAlreadyExistsException,
    EntityNotFoundException,
    FileNotFoundException,
    InvalidDocumentNameException,
    InvalidEntityException,
    RootPackageNotFoundException,
)
from utils.logging import logger


class UseCase(object):
    def execute(self, request_object=None):
        try:
            return self.process_request(request_object)
        except (
            EntityNotFoundException,
            DataSourceNotFoundException,
            RootPackageNotFoundException,
            FileNotFoundException,
        ) as not_found:
            logger.warning(not_found)
            return res.ResponseFailure.build_resource_error(not_found)
        except (EntityAlreadyExistsException, InvalidDocumentNameException, InvalidEntityException) as e:
            logger.error(e)
            return res.ResponseFailure.build_entity_error(e)
        except DataSourceAlreadyExistsException as error:
            return res.ResponseFailure.build_parameters_error(error)
        except Exception as exc:
            traceback.print_exc()
            return res.ResponseFailure.build_system_error(f"{exc.__class__.__name__}: {exc}")

    def process_request(self, request_object):
        raise NotImplementedError("process_request() not implemented by UseCase class")
