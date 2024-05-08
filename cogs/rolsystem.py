import discord
from discord.ext import commands
from discord import app_commands, Interaction
from mydecorators import *

from discord.app_commands import Group, command
from discord.ext.commands import GroupCog

from db import roldb

@app_commands.default_permissions(administrator=True)
class RolSystem(GroupCog, group_name='seri', group_description='description'):
    db = roldb()

    @command(description="seri seçim sistemine seri ekler")
    async def ekle(self, interaction: Interaction, seriadı:str, rol:discord.Role = None):
        await interaction.response.send_message("İşlem başladı", ephemeral=True)
        if (data:=self.db.bul(name=seriadı)):
            rolID = data["rolID"]
            await interaction.edit_original_response(content=f"Bu isimde rol var: <@&{rolID}>")
            return
        if not rol:
            rol = await interaction.guild.create_role(name=seriadı)
        post = {"name":seriadı, "rolID":rol.id}
        self.db.ekle(post)
        await interaction.edit_original_response(content="Rol sisteme eklenmiştir")
    
    @command(description="seri seçim sistemine seri siler")
    async def sil(self, interaction: Interaction, rol:discord.Role):
        await interaction.response.send_message("Rol aranıyor", ephemeral=True)
        data = self.db.bul(roleID= rol.id)
        rol = discord.utils.get(interaction.guild.roles, id= data["rolID"])
        self.db.sil(data)
        await rol.delete(reason=f"{interaction.user.name}, sistemden kaldırılması yönünde komut kullandı.")
        await interaction.edit_original_response(content="İşlemler tamamlandı, rol hem database ten hem de discorddan kaldırıldı.")

    # @command()
    # async def test(self, interaction: Interaction):
    #     data = self.db.getAll()
    #     data.sort(key=lambda x: x['name'].lower())
    #     print(data)
        
    # @command()
    # async def düzenle(self, interaction: Interaction):
    #     ...

    # subgroup = Group(name='subgroup', description='description')

    # @subgroup.command()
    # async def subsubcommand(self, interaction: Interaction):
    #     ...

async def setup(client):
    await client.add_cog(RolSystem(client))