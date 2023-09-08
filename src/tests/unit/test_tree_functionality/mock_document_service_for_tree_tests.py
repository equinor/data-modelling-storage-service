from services.document_service import DocumentService
from tests.unit.test_tree_functionality.mock_blueprint_provider_for_tree_tests import (
    blueprint_provider,
)
from tests.unit.test_tree_functionality.mock_storage_recipe_provider import (
    mock_storage_recipe_provider,
)


def get_mock_document_service_for_tree_tests(
    repository_provider=None,
    blueprint_provider=blueprint_provider,
    recipe_provider=mock_storage_recipe_provider,
    user=None,
    context=None,
):
    return DocumentService(
        blueprint_provider=blueprint_provider,
        recipe_provider=recipe_provider,
        repository_provider=repository_provider,
        user=user,
        context=context,
    )
