import os

from django.utils.html import format_html

from Project.settings.labels_with_svg import black_list_with_icon
from Project.settings.labels_with_svg import block_label_with_icon
from Project.settings.labels_with_svg import email_label_with_icon
from Project.settings.labels_with_svg import log_label_with_icon
from Project.settings.labels_with_svg import notification_with_icon
from Project.settings.labels_with_svg import profile_label_with_icon
from Project.settings.labels_with_svg import redoc_label_with_icon
from Project.settings.labels_with_svg import suggestion_label_with_icon
from Project.settings.labels_with_svg import swagger_label_with_icon
from Project.settings.labels_with_svg import user_label_with_icon


if not os.environ.get("PROJECT_URL"):
    os.environ.setdefault("PROJECT_URL", "localhost")
if not os.environ.get("GRAFANA_URL"):
    os.environ.setdefault("GRAFANA_URL", f"{os.environ['PROJECT_URL']}:3000/")
if not os.environ.get("PROMETHEUS_URL"):
    os.environ.setdefault(
        "PROMETHEUS_URL", f"{os.environ['PROJECT_URL']}:9090/"
    )
if not os.environ.get("FLOWER_URL"):
    os.environ.setdefault("FLOWER_URL", f"{os.environ['PROJECT_URL']}:5555/")

"""
JET Documentation: https://django-jet-reboot.readthedocs.io/
"""

X_FRAME_OPTIONS = "ALLOWALL"


JET_SIDE_MENU_COMPACT: bool = True


JET_THEMES: list = [
    {
        "theme": "default",  # theme folder name
        "color": "#47bac1",  # color of the theme's button in user menu
        "title": "Default",  # theme title
    },
    {"theme": "green", "color": "#44b78b", "title": "Green"},
    {"theme": "light-green", "color": "#2faa60", "title": "Light Green"},
    {"theme": "light-violet", "color": "#a464c4", "title": "Light Violet"},
    {"theme": "light-blue", "color": "#5EADDE", "title": "Light Blue"},
    {"theme": "light-gray", "color": "#222", "title": "Light Gray"},
]


JET_SIDE_MENU_ITEMS: list = [
    {
        "label": ("People"),
        "app_label": "Users",
        "items": [
            {"name": "user", "label": format_html(user_label_with_icon)},
            {"name": "profile", "label": format_html(profile_label_with_icon)},
        ],
    },
    {
        "label": ("Email"),
        "app_label": "Emails",
        "items": [
            {
                "name": "suggestion",
                "label": format_html(suggestion_label_with_icon),
            },
            {"name": "email", "label": format_html(email_label_with_icon)},
            {
                "name": "notification",
                "label": format_html(notification_with_icon),
            },
            {"name": "block", "label": format_html(block_label_with_icon)},
            {"name": "blacklist", "label": format_html(black_list_with_icon)},
        ],
    },
    {
        "label": ("Administration"),
        "app_label": "admin",
        "items": [
            {"name": "logentry", "label": format_html(log_label_with_icon)}
        ],
    },
    {
        "label": "Documentation",
        "items": [
            {
                "label": format_html(swagger_label_with_icon),
                "url": "/docs/swagger/",
                "url_blank": True,
            },
            {
                "label": format_html(redoc_label_with_icon),
                "url": "/docs/redoc/",
                "url_blank": True,
            },
        ],
    },
    {
        "label": ("Others"),
        "items": [
            {
                "label": "Grafana",
                "url": f"http://{os.environ['GRAFANA_URL']}",
                "url_blank": True,
            },
            {
                "label": "Prometheus",
                "url": f"http://{os.environ['PROMETHEUS_URL']}",
                "url_blank": True,
            },
            {
                "label": "Flower",
                "url": f"http://{os.environ['FLOWER_URL']}",
                "url_blank": True,
            },
        ],
    },
]
