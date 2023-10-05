from services.document_service.document_service import DocumentService
from tests.unit.mock_data.mock_recipe_provider import MockStorageRecipeProvider


def get_mock_document_service(
    blueprint_provider,
    repository_provider=None,
    recipe_provider=MockStorageRecipeProvider(
        "src/tests/unit/mock_data/mock_storage_recipes/mock_storage_recipes.json"
    ).provider,
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
