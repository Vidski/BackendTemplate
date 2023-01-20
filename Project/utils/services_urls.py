from os import environ


def set_services_urls() -> None:
    if not environ.get("PROJECT_URL"):
        environ.setdefault("PROJECT_URL", "localhost")
    if not environ.get("GRAFANA_URL"):
        environ.setdefault("GRAFANA_URL", f"{environ['PROJECT_URL']}:3000/")
    if not environ.get("PROMETHEUS_URL"):
        environ.setdefault("PROMETHEUS_URL", f"{environ['PROJECT_URL']}:9090/")
    if not environ.get("FLOWER_URL"):
        environ.setdefault("FLOWER_URL", f"{environ['PROJECT_URL']}:5555/")
