from os import environ

import pytest

from Project.utils.services_urls import set_services_urls


class TestServicesURLSSetter:
    def test_get_custom_urls(self) -> None:
        environ["PROJECT_URL"] = "test"
        environ["GRAFANA_URL"] = "test"
        environ["PROMETHEUS_URL"] = "test"
        environ["FLOWER_URL"] = "test"
        set_services_urls()
        assert environ.get("PROJECT_URL") == "test"
        assert environ.get("GRAFANA_URL") == "test"
        assert environ.get("PROMETHEUS_URL") == "test"
        assert environ.get("FLOWER_URL") == "test"

    def test_get_default_urls(self) -> None:
        del environ["PROJECT_URL"]
        del environ["GRAFANA_URL"]
        del environ["PROMETHEUS_URL"]
        del environ["FLOWER_URL"]
        set_services_urls()
        assert environ.get("PROJECT_URL") == "localhost"
        assert environ.get("GRAFANA_URL") == "localhost:3000/"
        assert environ.get("PROMETHEUS_URL") == "localhost:9090/"
        assert environ.get("FLOWER_URL") == "localhost:5555/"
