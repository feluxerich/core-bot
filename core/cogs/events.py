from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.guild import update_member_count


class EventsCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @Cog.listener()
    async def on_member_join(self, payload):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))

    @Cog.listener()
    async def on_member_remove(self, payload):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))


def setup(client):
    client.add_cog(EventsCog(client))
