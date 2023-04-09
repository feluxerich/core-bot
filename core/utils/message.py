from discord import Embed, Message, Interaction


async def send(interaction: Interaction, embed: Embed) -> Message:
    return await interaction.response.send_message(embed=embed)

