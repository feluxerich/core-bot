from datetime import timedelta

from discord import Embed, Member
from discord.ext.commands import Cog, command

from utils.bot import ExtendedBot
from utils.message import send


class ModeratorCog(Cog):
    def __init__(self, client: ExtendedBot):
        self.client = client

    @command()
    async def timeout(self, ctx, member: Member, until: str = None, *, reason=None):
        until_timedelta: timedelta = timedelta(hours=1)
        if type(until) != timedelta:
            time = float(until[:-1])
            unit = until[-1]
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
        await send(context=ctx, embed=embed)


async def setup(client):
    await client.add_cog(ModeratorCog(client))
