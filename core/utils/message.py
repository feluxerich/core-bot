from discord import Embed, Message
from discord.ext.commands import Context


async def send(context: Context, embed: Embed) -> Message:
    async with context.typing():
        return await context.send(embed=embed)

