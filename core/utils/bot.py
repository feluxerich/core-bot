from os import listdir
from typing import Type

from discord import Object
from discord.ext.commands import Bot, ExtensionNotLoaded

from utils.config import Config


class ExtendedBot(Bot):
    DEFAULT_GUILD: Object

    def __init__(self, config: Type[Config], command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.config = config
        self.DEFAULT_GUILD = Object(id=self.config.GUILD)

    async def setup_hook(self) -> None:
        for file in listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(f'Loaded {file}')
                except ExtensionNotLoaded:
                    print(f'Not a python file: {file}')
            else:
                print(f'Not a python file: {file}')
        await self.sync_commands()

    async def sync_commands(self) -> None:
        await self.tree.sync(guild=self.DEFAULT_GUILD)
