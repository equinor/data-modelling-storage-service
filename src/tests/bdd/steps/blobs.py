import mimetypes

from behave import given

from storage.data_source_class import DataSource
from storage.internal.data_source_repository import get_data_source


@given('there exists a blob with id "{id}" in data source "{data_source}" loaded from "{path}"')
def step_impl(context, id, data_source, path):
    data_source: DataSource = get_data_source(data_source_id=data_source, user=context.user)
    try:
        with open(path, "rb") as blob_file:
            guess = mimetypes.guess_type(blob_file.name)
            content_type: str | None = ""
            if guess:
                content_type = guess[0]
            data_source.update_blob(id, blob_file.name, content_type, blob_file)
    except FileNotFoundError as err:
        raise FileNotFoundError(
            f"The file {path}, was not found. Make sure the working directory of "
            + "the test are set to be the source root (./src)"
        ) from err
