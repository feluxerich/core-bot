from dataclasses import dataclass
from os.path import isfile
from pathlib import Path
from typing import Type

import yaml

from exceptions.no_config_found import NoConfigFound


@dataclass
class Config:
    # General
    OWNER: int
    GUILD: int
    PRESENCES: list[str]
    PRESENCE_TIMEOUT: int

    # Embed
    COLORS: dict[str, str]
    EMBEDS: dict[str, dict[str, str | dict[str, dict[str, str]]]]  # dict[str, dict[str, typing.Any]]

    # Reaction Roles
    ROLES_CHANNEL: int
    ROLES: dict[str, int]

    # Server
    MEMBER_COUNT_CHANNEL: int
    CREATE_VOICE_CHANNEL: int


def load_config(path: Path) -> Type[Config]:
    if not isfile(path):
        raise NoConfigFound
    with path.open() as f:
        config = yaml.safe_load(f)
    Config.OWNER = config['owner']
    Config.GUILD = config['guild']
    Config.PRESENCES = [presence for presence in config['presences']]
    Config.PRESENCE_TIMEOUT = config['presence-timeout']

    Config.COLORS = {name: color for name, color in config['color-palette'].items()}
    Config.EMBEDS = {name: {key: value for key, value in configs.items()} for name, configs in config['embeds'].items()}

    Config.ROLES_CHANNEL = config['roles-channel']
    Config.ROLES = {emoji: role_id for emoji, role_id in config['roles'].items()}

    Config.MEMBER_COUNT_CHANNEL = config['member-count-channel']
    Config.CREATE_VOICE_CHANNEL = config['create-voice-channel']

    print('Loaded Config')
    return Config
