from discord import Member, VoiceState, PermissionOverwrite, NotFound
from discord.abc import GuildChannel
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.guild import update_member_count


class EventsCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client
        self.talks: list[int] = []

    @Cog.listener()
    async def on_member_join(self, _):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))

    @Cog.listener()
    async def on_member_remove(self, _):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if after.channel and after.channel.id != self.client.config.CREATE_VOICE_CHANNEL:
            return
        if before.channel and before.channel.id in self.talks and len(before.channel.members) == 0:
            try:
                self.talks.remove(before.channel.id)
                await before.channel.delete(reason='auto_voice_talk_empty')
            except NotFound as _:
                pass
        if not after.channel:
            return
        new_voice = await after.channel.category.create_voice_channel(
            f'{member.display_name}\'s Talk',
            reason='auto_voice_talk_created'
        )
        await new_voice.set_permissions(target=member, overwrite=PermissionOverwrite(
            manage_channels=True
        ), reason='auto_voice_set_permissions')
        self.talks.append(new_voice.id)
        await member.move_to(channel=new_voice, reason='auto_voice_member_moved')

    @Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel):
        if channel.id not in self.talks:
            return
        self.talks.remove(channel.id)


async def setup(client):
    await client.add_cog(EventsCog(client))
