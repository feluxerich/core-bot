from discord.ext.commands import Bot


class ExtendedBot(Bot):
    def __init__(self, config, command_prefix, **options):
        super().__init__(command_prefix, **options)
        self.config = config
