from asyncio import sleep
from os import getenv
from pathlib import Path

from discord import Intents, Game, Status

from utils import ExtendedBot
from utils.config import load_config
from utils.guild import update_member_count

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


async def status_task():
    while True:
        for status in client.config.PRESENCES:
            await client.change_presence(activity=Game(status), status=Status.online)
            await sleep(client.config.PRESENCE_TIMEOUT)

if __name__ == '__main__':
    client.run(getenv('BOT_TOKEN'))
