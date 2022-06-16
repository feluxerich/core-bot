from discord import Guild, VoiceChannel
from discord.utils import get

from utils.bot import ExtendedBot


async def update_member_count(client: ExtendedBot, guild: Guild):
    channel: VoiceChannel = get(guild.voice_channels, id=client.config.MEMBER_COUNT_CHANNEL)
    await channel.edit(name=f'Member: {guild.member_count}')
