from django.utils.translation import gettext
from django.utils.translation import override


def get_translation_in(language: str, text: str) -> str:
    with override(language):
        return gettext(text)
