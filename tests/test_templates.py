from commandgraph.slots import extract_slots
from commandgraph.templates import render_template


def test_extracts_common_slots():
    slots = extract_slots('find files named "*.py" in ./src on port 3000')
    assert slots["port"] == "3000"
    assert slots["pattern"] == "*.py"
    assert slots["path"] == "./src"


def test_extracts_url_slot():
    slots = extract_slots("check endpoint https://example.com/health")
    assert slots["url"] == "https://example.com/health"
    assert slots["host"] == "example.com"


def test_renders_template_when_slots_exist():
    command = render_template("lsof -i :{port}", {"port": "3000"})
    assert command == "lsof -i :3000"


def test_does_not_render_when_slot_missing():
    command = render_template("curl -I {url}", {})
    assert command is None
