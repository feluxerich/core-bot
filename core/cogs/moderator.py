from datetime import timedelta
from typing import Optional

from discord import Member, Interaction
from discord.app_commands.checks import has_permissions
from discord.ext.commands import Cog
from discord.app_commands import command, describe

from utils.bot import ExtendedBot
from utils.message import send, make_embed


class ModeratorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='timeout', description='Timeout of a member who behaves inappropriately')
    @describe(member='The member to be timeouted', duration='Time formatted like 1w for one week')
    @has_permissions(moderate_members=True)
    async def timeout(self, interaction: Interaction, member: Member, duration: str, *, reason: Optional[str] = None):
        until_timedelta: timedelta = timedelta(hours=1)
        if type(duration) != timedelta:
            time = float(duration[:-1])
            unit = duration[-1]
            match unit:
                case 'w':
                    until_timedelta = timedelta(weeks=time)
                case 'd':
                    until_timedelta = timedelta(days=time)
                case 'h':
                    until_timedelta = timedelta(hours=time)
                case 'm':
                    until_timedelta = timedelta(minutes=time)
                case 's':
                    until_timedelta = timedelta(seconds=time)

        await member.timeout(until_timedelta, reason=reason)
        embed = make_embed(self.client, 'timeout', member=member.mention, reason=reason, until=until_timedelta)
        embed.set_thumbnail(url=member.display_avatar)
        await send(interaction=interaction, embed=embed)


async def setup(client: ExtendedBot):
    await client.add_cog(ModeratorCog(client), guild=client.DEFAULT_GUILD)
