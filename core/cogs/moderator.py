from datetime import timedelta

from discord import Embed, Member, Interaction
from discord.ext.commands import Cog
from discord.app_commands import command, describe, check

from utils.bot import ExtendedBot
from utils.message import send


class ModeratorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command(name='timeout', description='Timeout of a member who behaves inappropriately')
    @describe(member='The member to be timeouted', until='Time formatted like 1w for one week')
    async def timeout(self, interaction: Interaction, member: Member, until: str = None, *, reason: str = None):
        until_timedelta: timedelta = timedelta(hours=1)
        if type(until) != timedelta:
            time = float(until[:-1])
            unit = until[-1]
            match unit:
                case 'w' | 'week' | 'weeks':
                    until_timedelta = timedelta(weeks=time)
                case 'd' | 'day' | 'days':
                    until_timedelta = timedelta(days=time)
                case 'h' | 'hour' | 'hours':
                    until_timedelta = timedelta(hours=time)
                case 'm' | 'minute' | 'minutes' | 'mins':
                    until_timedelta = timedelta(minutes=time)
                case 's' | 'second' | 'seconds' | 'secs':
                    until_timedelta = timedelta(seconds=time)

        await member.timeout(until_timedelta, reason=reason)

        format_keys = {
            'reason': reason,
            'until': until_timedelta
        }
        embed = Embed(
            title=self.client.config.EMBEDS['timeout']['title'],
            description=self.client.config.EMBEDS['timeout']['description'].format(member=member.mention),
            color=self.client.config.COLORS[self.client.config.EMBEDS['timeout']['color']]
        )
        embed.set_thumbnail(url=member.display_avatar)
        for field in self.client.config.EMBEDS['timeout']['fields']:
            embed.add_field(
                name=self.client.config.EMBEDS['timeout']['fields'][field]['name'],
                value=self.client.config.EMBEDS['timeout']['fields'][field]['value'].format(**format_keys),
                inline=bool(self.client.config.EMBEDS['timeout']['fields'][field]['inline'])
            )
        await send(interaction=interaction, embed=embed)


async def setup(client: ExtendedBot):
    await client.add_cog(ModeratorCog(client), guild=client.DEFAULT_GUILD)
