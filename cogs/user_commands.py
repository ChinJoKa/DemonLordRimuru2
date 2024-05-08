import discord
from discord import app_commands
from discord.ext import commands

class user_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.ctx_menu = app_commands.ContextMenu(
            name='Avatar',
            callback=self.Avatar,
        )
        self.sil = app_commands.ContextMenu(
            name='Buraya kadar sil',
            callback=self.MessageSil,
        )
        self.client.tree.add_command(self.ctx_menu)
        self.client.tree.add_command(self.sil)

    async def cog_unload(self) -> None:
        self.client.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)
        self.client.tree.remove_command(self.sil.name, type=self.sil.type)
    
    async def Avatar(self, interaction: discord.Interaction, user: discord.User) -> None:
        embed = discord.Embed(color=user.color)
        embed.set_image(url = user.display_avatar.url)
        embed.set_author(name=user, icon_url=user.avatar.url)
        embed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
    
        await interaction.response.send_message(embed = embed, ephemeral = True)

    @app_commands.default_permissions(manage_channels=True)
    async def MessageSil(self, interaction: discord.Interaction, msg: discord.Message) -> None:
        async for m in interaction.channel.history(limit=None):
            if m.id == msg.id:
                await interaction.response.send_message("Mesajlar silindi.", ephemeral=True, delete_after=10)
                return
            await m.delete()

async def setup(client):
    await client.add_cog(user_commands(client))
