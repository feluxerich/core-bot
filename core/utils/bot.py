from os import listdir

import asyncio
from discord.ext.commands import Bot, ExtensionNotLoaded
from termcolor import colored


class ExtendedBot(Bot):
    def __init__(self, config, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.config = config

    async def setup_hook(self) -> None:
        for file in listdir('./cogs'):
            if file.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{file[:-3]}')
                    print(colored(f'Loaded {file}', 'green'))
                except ExtensionNotLoaded:
                    print(colored(f'Not a python file: {file}', 'red'))
            else:
                print(colored(f'Not a python file: {file}', 'red'))
