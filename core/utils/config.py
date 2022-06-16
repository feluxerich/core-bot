import logging
from os.path import isfile
from pathlib import Path
from typing import Type

import yaml
from termcolor import colored

from core.exceptions.no_config_found import NoConfigFound


class Config:
    # General
    OWNER: int
    GUILD: int
    PRESENCES: list[str]
    PRESENCE_TIMEOUT: int

    # Embed
    COLORS: dict[str, str]

    # Reaction Roles
    ROLES_CHANNEL: int
    ROLES: dict[str, int]

    # Server Stats
    MEMBER_COUNT_CHANNEL: int


def config_exists(function):
    def wrapper(*args, **kwargs):
        if isfile(kwargs.get('path')):
            return function(*args, **kwargs)
        raise NoConfigFound


def load_config(path: Path) -> Type[Config]:
    with path.open() as f:
        config = yaml.safe_load(f)
    Config.OWNER = config['owner']
    Config.GUILD = config['guild']
    Config.PRESENCES = [presence for presence in config['presences']]
    Config.PRESENCE_TIMEOUT = config['presence-timeout']

    Config.COLORS = {name: color for name, color in config['color-palette'].items()}

    Config.ROLES_CHANNEL = config['roles-channel']
    Config.ROLES = {emoji: role_id for emoji, role_id in config['roles'].items()}

    Config.MEMBER_COUNT_CHANNEL = config['member-count-channel']

    print(colored('Loaded Config', 'green'))
    return Config
