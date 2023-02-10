from unittest import mock, skip
from uuid import uuid4

from authentication.models import User
from common.tree_node_serializer import tree_node_to_dict
from features.document.use_cases.add_file_use_case import add_file_use_case


@skip("not working")
def test_without_parameters():
    document_repository = mock.Mock()

    parent_id = str(uuid4())

    # parent = DTO(uid=parent_id, data={path="/", filename="root", type="folder", template_ref=""})

    def mock_add(document):
        pass

    document_repository.add.return_value = mock_add
    document_repository.get.return_value = parent
    user = User()
    data = {"parentId": parent_id, "filename": "new_file", "templateRef": ""}
    use_case_result = add_file_use_case(
        user=user, absolute_ref="", data=data, update_uncontained=False, repository_provider=document_repository
    )

    assert bool(use_case_result) is True
    document_repository.get.assert_called_with(parent_id)

    result = tree_node_to_dict(use_case_result.value)

    assert result["filename"] == data["filename"]
