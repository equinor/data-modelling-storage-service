from services.document_service.document_service import DocumentService


def get_mock_document_service(
    blueprint_provider,
    repository_provider=None,
    recipe_provider=None,
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
