from discord import Member, VoiceChannel, VoiceState, StageChannel
from discord.ext.commands import Cog

from utils.bot import ExtendedBot
from utils.guild import update_member_count


class EventsCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client
        self.talks: list[VoiceChannel] = []

    @Cog.listener()
    async def on_member_join(self, _):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))

    @Cog.listener()
    async def on_member_remove(self, _):
        await update_member_count(self.client, self.client.get_guild(self.client.config.GUILD))

    @Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if type(before.channel) == StageChannel or type(after.channel) == StageChannel \
                or not after.channel or after.channel.id != self.client.config.CREATE_VOICE_CHANNEL:
            return
        if before.channel in self.talks and len(before.channel.members) == 0:
            await before.channel.delete(reason='talk_empty')
            self.talks.remove(before.channel)
        new_voice = await after.channel.category.create_voice_channel(
            f'{member.display_name}\'s Talk',
            reason='talk_created'
        )
        self.talks.append(new_voice)
        await member.move_to(channel=new_voice, reason='member_moved')


async def setup(client):
    await client.add_cog(EventsCog(client))
