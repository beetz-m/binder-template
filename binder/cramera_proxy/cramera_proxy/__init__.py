"""jupyter-server-proxy entry point: serve the static cramera site at <lab>/cramera/."""
import os


def setup_cramera():
    site = os.environ.get("CRAMERA_SITE", os.path.join(os.environ.get("REPO_DIR", "/home/repo"), "cramera_site"))
    return {
        "command": ["python3", "-m", "http.server", "{port}", "--bind", "127.0.0.1", "--directory", site],
        "absolute_url": False,
        "timeout": 30,
        "launcher_entry": {"enabled": True, "title": "cramera viewer"},
    }
