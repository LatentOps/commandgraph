from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_synonyms() -> dict[str, list[str]]:
    return load_json(DATA_DIR / "synonyms.json")


def load_risk_rules() -> list[dict[str, Any]]:
    payload = load_json(DATA_DIR / "risk_rules.json")
    return payload["rules"]


def load_commands() -> list[dict[str, Any]]:
    commands_dir = DATA_DIR / "commands"
    commands = []
    for path in sorted(commands_dir.glob("*.json")):
        commands.append(load_json(path))
    return commands


def find_command(command_name: str) -> dict[str, Any] | None:
    normalized = command_name.strip().lower()
    for command in load_commands():
        if command.get("command", "").lower() == normalized:
            return command
    return None


def data_health() -> dict[str, Any]:
    commands = load_commands()
    risk_rules = load_risk_rules()
    command_names = [command.get("command") for command in commands]
    missing_schema = [
        command.get("command", "<unknown>")
        for command in commands
        if not command.get("schema_version")
    ]
    duplicate_commands = sorted(
        {
            command
            for command in command_names
            if command_names.count(command) > 1
        }
    )
    return {
        "command_count": len(commands),
        "risk_rule_count": len(risk_rules),
        "missing_schema": missing_schema,
        "duplicate_commands": duplicate_commands,
        "ok": not missing_schema and not duplicate_commands,
    }
