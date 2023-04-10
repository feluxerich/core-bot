from asyncio import sleep
from os import getenv
from pathlib import Path
from typing import Any

from discord import Intents, Game, Status, Interaction
from discord.app_commands import MissingPermissions

from utils import ExtendedBot
from utils.config import load_config
from utils.guild import update_member_count
from utils.message import send, make_embed

client = ExtendedBot(
    config=load_config(path=Path('config.yaml')),
    command_prefix='.',
    intents=Intents.all(),
    help_command=None
)


@client.event
async def on_ready():
    print(f'Bot is now ready with ID: {client.user.id}')
    await update_member_count(client, client.get_guild(client.config.GUILD))
    client.loop.create_task(status_task())


@client.tree.error
async def on_app_command_error(interaction: Interaction, error: Any):
    error_messages = {
        MissingPermissions: 'Missing Permissions'
    }
    await send(interaction=interaction, embed=make_embed(
        client,
        'error',
        error_message=error_messages[type(error)]
    ))


async def status_task():
    while True:
        for status in client.config.PRESENCES:
            await client.change_presence(activity=Game(status), status=Status.online)
            await sleep(client.config.PRESENCE_TIMEOUT)


if __name__ == '__main__':
    client.run(getenv('BOT_TOKEN'))
