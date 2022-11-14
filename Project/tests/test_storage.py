from django.test import override_settings

from Project.storage import ImageStorage
from Project.storage import aws_variables_set
from Project.storage import get_image_storage


class TestProjectStorage:
    @override_settings(AWS_ACCESS_KEY_ID=None)
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_aws_variables_set_returns_False_if_one_is_None(self) -> None:
        assert not aws_variables_set()

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_aws_variables_set_returns_True_if_all_are_set(self) -> None:
        assert aws_variables_set()

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME="test")
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_get_image_storage_returns_ImageStorage_instance_if_aws_keys_are_set(
        self,
    ) -> None:
        assert isinstance(get_image_storage(), ImageStorage)

    @override_settings(AWS_ACCESS_KEY_ID="test")
    @override_settings(AWS_SECRET_ACCESS_KEY="test")
    @override_settings(AWS_STORAGE_IMAGE_BUCKET_NAME="test")
    @override_settings(AWS_S3_REGION_NAME=None)
    @override_settings(AWS_S3_SIGNATURE_VERSION="test")
    def test_get_image_storage_returns_None_if_a_aws_keys_is_not_set(
        self,
    ) -> None:
        assert not get_image_storage()
