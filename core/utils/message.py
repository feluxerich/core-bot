from discord import Embed, Message, Interaction, Color

from utils import ExtendedBot


async def send(interaction: Interaction, embed: Embed) -> Message:
    return await interaction.response.send_message(embed=embed)


def make_embed(client: ExtendedBot, embed_name: str, **format_keys) -> Embed:
    embed = Embed(
        title=client.config.EMBEDS[embed_name]['title'],
        color=Color.from_str(client.config.COLORS[client.config.EMBEDS[embed_name]['color']])
    )
    if 'description' in client.config.EMBEDS[embed_name].keys():
        embed.description = client.config.EMBEDS[embed_name]['description'].format(**format_keys),
    if 'fields' in client.config.EMBEDS[embed_name].keys():
        for field in client.config.EMBEDS[embed_name]['fields']:
            embed.add_field(
                name=client.config.EMBEDS[embed_name]['fields'][field]['name'],
                value=client.config.EMBEDS[embed_name]['fields'][field]['value'].format(**format_keys),
                inline=bool(client.config.EMBEDS[embed_name]['fields'][field]['inline'])
            )
    return embed
