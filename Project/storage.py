from django.conf import settings
from django.db.models import Model
from storages.backends.s3boto3 import S3Boto3Storage


class ImageStorage(S3Boto3Storage):
    bucket_name: str = settings.AWS_STORAGE_IMAGE_BUCKET_NAME
    access_key: str = settings.AWS_ACCESS_KEY_ID
    secret_key: str = settings.AWS_SECRET_ACCESS_KEY
    region_name: str = settings.AWS_S3_REGION_NAME
    signature_version: str = settings.AWS_S3_SIGNATURE_VERSION


def image_file_upload(instance: Model, filename: str) -> str:
    user_id: int = instance.user.id
    extension: str = filename.split(".")[-1]
    file_name: str = f"profile_image_of_user_{user_id}.{extension}"
    base_path: str = ""
    if not aws_variables_set():
        base_path: str = f"{settings.MEDIA_PATH}/"
    return f"{base_path}profile_images/{user_id}/{file_name}"


def get_image_storage() -> ImageStorage or None:
    if not aws_variables_set():
        return None
    return ImageStorage()


def aws_variables_set() -> bool:
    return (
        settings.AWS_ACCESS_KEY_ID
        and settings.AWS_SECRET_ACCESS_KEY
        and settings.AWS_STORAGE_IMAGE_BUCKET_NAME
        and settings.AWS_S3_REGION_NAME
        and settings.AWS_S3_SIGNATURE_VERSION
    )
