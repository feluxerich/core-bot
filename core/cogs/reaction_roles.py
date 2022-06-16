from discord.utils import get
from discord.ext.commands import Cog


class ReactionRoleCog(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if not payload.channel_id == self.client.config.ROLES_CHANNEL or \
                str(payload.emoji) not in self.client.config.ROLES:
            return
        await payload.member.add_roles(get(payload.member.guild.roles, id=self.client.config.ROLES[str(payload.emoji)]))

    @Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        server = self.client.get_guild(payload.guild_id)
        member = server.get_member(payload.user_id)
        if not payload.channel_id == self.client.config.ROLES_CHANNEL or \
                str(payload.emoji) not in self.client.config.ROLES:
            return
        await member.remove_roles(get(member.guild.roles, id=self.client.config.ROLES[str(payload.emoji)]))


def setup(client):
    client.add_cog(ReactionRoleCog(client))
