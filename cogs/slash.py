import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import MissingPermissions

class OnayButton(discord.ui.View):
    def __init__(self, msg_id):
        self.msg_id = msg_id
        super().__init__(timeout=None)

    @app_commands.default_permissions(manage_channels=True)
    @discord.ui.button(label="Onay", style=discord.ButtonStyle.green, custom_id="1")
    async def onay(self, interaction:discord.Interaction, Button:discord.ui.Button):
        await interaction.response.send_message(content="İşlem onaylandı.", ephemeral=True)
        async for m in interaction.channel.history(limit=None):
            if m.id == self.msg_id:
                return
            await m.delete()
    @discord.ui.button(label="İptal", style=discord.ButtonStyle.red, custom_id="iptal")
    async def iptal(self, interaction:discord.Interaction, Button:discord.ui.Button):
        await interaction.response.send_message(content="İşlem iptal edildi.", ephemeral=True)
        await self.stop()

class slashcommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ekip_rol_id = 831627010954231868

    @commands.Cog.listener()
    async def on_ready(self):
        print("slashcommands is ready")

    @app_commands.default_permissions(manage_channels=True)
    @app_commands.command(name="test", description="...")
    async def test(self, interaction: discord.Interaction):
        channel_id = 835874984756248576
        channel = discord.utils.get(interaction.guild.channels, id=channel_id)
        await channel.send("test")
        await interaction.response.send_message("done")

    @app_commands.command(name="ping", description="returns pong")
    async def ping(self, interaction: discord.Interaction):
        """
        Returns pong
        """
        await interaction.response.send_message(f"{round(self.bot.latency * 1000)} ms", ephemeral=True)

    @ping.error
    async def test_error(interaction:discord.Interaction, error):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message("Bu komut için yetkiniz yetersizdir.", ephemeral=True)
        else:
            raise error

    @app_commands.command(name="avatar", description="returns someone's avatar")
    async def avatar(self, interaction: discord.Interaction, user: discord.User, sunucu_avatarı: bool = False, gizli: bool = False):
        """
        Returns avatar
        """
        embed = discord.Embed(color=user.color)
        if sunucu_avatarı:
            embed.set_image(url = user.display_avatar.url)
        else:
            embed.set_image(url = user.avatar.url)
        embed.set_author(name=user, icon_url=user.avatar.url)
        embed.set_footer(text=interaction.user, icon_url=interaction.user.avatar.url)
    
        await interaction.response.send_message(embed = embed, ephemeral = gizli)
    
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.command(name="sil", description="belirtilen miktarda mesaj silme")
    async def purge(self, interaction: discord.Interaction, sayı: int):
        await interaction.response.send_message(content=f"İşleme başlıyorum", ephemeral=True)
        if interaction.channel.id == 800085087336005652:
            await interaction.edit_original_response(content="Bu kanalda bu komutu kullanamazsın.")
            return
        if sayı:
            await interaction.channel.purge(limit=sayı)
            await interaction.edit_original_response(content=f"{sayı} mesaj silindi.")
            await interaction.delete_original_response()

    @app_commands.command(name="çeviri", description="çevirmenlik başvurusu ya da çevirmenlere etiket atmayı sağlar")
    async def ceviri(self, interaction: discord.Interaction):
        ekip = discord.utils.get(interaction.guild.roles, id = self.ekip_rol_id)
        if interaction.channel_id == (ch := 831886784047611909):
            cevirmen = discord.utils.get(interaction.guild.roles, id = 831888472259821649)
            await cevirmen.edit(mentionable = True)
            await interaction.response.send_message(f"{cevirmen.mention}", allowed_mentions=discord.AllowedMentions(roles=True))
            await cevirmen.edit(mentionable = False)
        elif ekip in interaction.user.roles:
            await interaction.response.send_message(f"<#{ch}> kanalında kullanınız", ephemeral=True)
        else:
            await interaction.response.send_message(f"Çevirmenlik başvuruları için <@295791590096502784> a başvuru yapabilirsiniz.", ephemeral=True)

    @app_commands.command(name="edit", description="editörlük başvurusu ya da editörlere etiket atmayı sağlar")
    async def edit(self, interaction: discord.Interaction):
        ekip = discord.utils.get(interaction.guild.roles, id = self.ekip_rol_id)
        if interaction.channel_id == (ch := 857315997214834698):
            editor = discord.utils.get(interaction.guild.roles, id = 857315777644068914)
            await editor.edit(mentionable = True)
            await interaction.response.send_message(f"{editor.mention}", allowed_mentions=discord.AllowedMentions(roles=True))
            await editor.edit(mentionable = False)
        elif ekip in interaction.user.roles:
            await interaction.response.send_message(f"<#{ch}> kanalında kullanınız", ephemeral=True)
        else:
            await interaction.response.send_message(f"Editörlük başvuruları için <@337291026370789398> a başvuru yapabilirsiniz.", ephemeral=True)

    @app_commands.command(name="upload", description="Yükleme yetkisi olanları etiketler.")
    async def upload(self, interaction:discord.Interaction):
        if interaction.channel_id == (ch := 800085087336005652):
            uploader = discord.utils.get(interaction.guild.roles, id = 731444958963171339)
            await uploader.edit(mentionable = True)
            await interaction.response.send_message(f"{uploader.mention}", allowed_mentions=discord.AllowedMentions(roles=True))
            await uploader.edit(mentionable = False)
        else:
            await interaction.response.send_message(f"<#{ch}> bu komutu burada kullanın lütfen.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(slashcommands(bot))