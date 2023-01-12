from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.guild import update_member_count


class EventsCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @Cog.listener()
    async def on_member_join(self, _):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))

    @Cog.listener()
    async def on_member_remove(self, _):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))


async def setup(client):
    await client.add_cog(EventsCog(client))
