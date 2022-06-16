import logging
from asyncio import sleep
from os import getenv, listdir
from pathlib import Path

from discord import Intents, Embed, Game, Status
from discord.ext.commands import when_mentioned_or, ExtensionNotLoaded
from termcolor import colored

from utils.bot import ExtendedBot
from utils.config import load_config
from utils.guild import update_member_count

client = ExtendedBot(
    config=load_config(path=Path('config.yaml')),
    command_prefix=when_mentioned_or('.'),
    intents=Intents.all(),
    help_command=None
)


@client.event
async def on_ready():
    print(colored(f'Bot is now ready with ID: {client.user.id}', 'magenta'))
    await update_member_count(client, client.get_guild(client.config.GUILD))
    client.loop.create_task(status_task())


async def status_task():
    while True:
        count = 0
        for _ in client.guilds:
            count += 1
        for status in client.config.PRESENCES:
            await client.change_presence(activity=Game(status), status=Status.online)
            await sleep(client.config.PRESENCE_TIMEOUT)


@client.command(description='Reloads the bot')
async def reload(ctx):
    successful = str()
    failed = str()
    for file in listdir('./cogs'):
        if file.endswith('.py'):
            try:
                client.reload_extension(f'cogs.{file[:-3]}')
                successful += f'Loaded `{file}`\n'
            except ExtensionNotLoaded:
                failed += f'Not a python file: `{file}`\n'
        else:
            failed += f'Not a python file: `{file}`\n'
    reload_embed = Embed(
        title='Reload',
    )
    reload_embed.add_field(name='Successful', value=successful, inline=False)
    reload_embed.add_field(name='Failed', value=failed, inline=False)
    await ctx.send(embed=reload_embed)


for file in listdir('./cogs'):
    if file.endswith('.py'):
        try:
            client.load_extension(f'cogs.{file[:-3]}')
            print(colored(f'Loaded {file}', 'green'))
        except ExtensionNotLoaded:
            print(colored(f'Not a python file: {file}', 'red'))
    else:
        print(colored(f'Not a python file: {file}', 'red'))

if __name__ == '__main__':
    client.run(getenv('BOT_TOKEN'))
