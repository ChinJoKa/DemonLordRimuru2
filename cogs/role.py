import discord
from discord.ext import commands
from mydecorators import *
from pprint import pprint

from db import roldb

class SelectMenu(discord.ui.Select):
    def __init__(self, guild, member, roles):
        self.roles = roles
        options = []
        for role in self.roles:
            if role in member.roles:
                options.append(discord.SelectOption(label=role.name, default=True))
            else:
                options.append(discord.SelectOption(label=role.name, default=False))

        super().__init__(placeholder= "Takip etmek istediklerinizi seçiniz.", options= options, min_values=0 ,max_values=len(self.roles))
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Rolleriniz eklenmiştir.", ephemeral=True)

        for r in self.roles:
            if r.name in self.values and r not in interaction.user.roles:
                await interaction.user.add_roles(r)
            elif r.name not in self.values and r in interaction.user.roles:
                await interaction.user.remove_roles(r)

        msg = ", ".join(self.values)
        if len(self.values)>0:
            await interaction.edit_original_response(f"> **{msg}** rolünüz/rolleriniz eklenmiştir.")
        else:
            await interaction.edit_original_response(f"> Tüm rolleriniz kaldırılmıştır.")

class SelectButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.db = roldb()

    def role_list(self, guild):
        data = self.db.getAll()        
        roles = []
        for r in data:
            role = discord.utils.get(guild.roles, id=r["rolID"])
            roles.append(role)
        
        roles = self.role_splitter(roles)
        return roles
        
    def role_splitter(self, roles):
        role_list = []
        while len(roles) > 25:
            role_list.append(roles[0:25])
            del roles[0:25]
        else:
            role_list.append(roles)
        return role_list

    @discord.ui.button(label="Rol Seç", style=discord.ButtonStyle.green, custom_id="1")
    async def rol(self, interaction: discord.Interaction, Button:discord.ui.Button):
        roles = self.role_list(interaction.guild)
        view = PaginationView(interaction.guild, interaction.user, roles)
        await view.send(interaction)
    
    @discord.ui.button(label="Manga/Webtoon", style=discord.ButtonStyle.green, custom_id="2")
    async def all(self, interaction: discord.Interaction, Button:discord.ui.Button):
        view = MultipleSelect(interaction.guild, interaction.user)
        await view.send(interaction)

class MultipleSelect(discord.ui.View):
    def __init__(self, guild, member:discord.Member):
        super().__init__()
        self.guild = guild
        self.member = member
        self.mangaID = 1020464698166100069
        self.webtoonID = 1271119836256145469
        self.mangaRol = None
        self.webtoonRol = None
        # self.update_buttons()

    def getroles(self):
        self.mangaRol = discord.utils.get(self.guild.roles, id= self.mangaID)
        self.webtoonRol = discord.utils.get(self.guild.roles, id= self.webtoonID)

    def update_buttons(self):
        if self.mangaRol == None or self.webtoonRol == None:
            self.getroles()
        
        if self.mangaRol in self.member.roles:
            self.manga.style(discord.ButtonStyle.green)
        else:
            self.manga.style(discord.ButtonStyle.gray)
        
        if self.webtoonRol in self.member.roles:
            self.webtoon.style(discord.ButtonStyle.green)
        else:
            self.webtoon.style(discord.ButtonStyle.gray)

    async def send(self, interaction: discord.Interaction):
        self.interaction = interaction
        await self.interaction.response.send_message(view=self, ephemeral=True)
    
    async def edit(self, content = None):
        # self.update_buttons()
        await self.interaction.edit_original_response(content=content, view=self)

    @discord.ui.button(label="Manga", style=discord.ButtonStyle.gray, row=2)
    async def manga(self, interaction: discord.Interaction, Button:discord.ui.Button):
        await interaction.response.defer()
        mangaRol = discord.utils.get(self.guild.roles, id= self.mangaID)
        if mangaRol in self.member.roles:
            await self.member.remove_roles(mangaRol)
        else:
            await self.member.add_roles(mangaRol)
        await self.send()
        # self.update_buttons()

    @discord.ui.button(label="Webtoon", style=discord.ButtonStyle.gray, row=2)
    async def webtoon(self, interaction: discord.Interaction, Button:discord.ui.Button):

        webtoonRol = discord.utils.get(self.guild.roles, id= self.webtoonID)
        if webtoonRol in self.member.roles:
            await self.member.remove_roles(webtoonRol)
            await interaction.response.send_message(content=f"**{webtoonRol}** rolünüz kaldırıldı", ephemeral=True)
        else:
            await self.member.add_roles(webtoonRol)
            await interaction.response.send_message(content=f"**{webtoonRol}** rolünüz eklendi", ephemeral=True)
        # self.update_buttons()

class Questionnaire(discord.ui.Modal, title='Manga Arama'):
    part = discord.ui.TextInput(label='Seri Adı/Parçası')
    db = roldb()
    
    def role_list(self, guild, phrase):
        data = self.db.getAll()        
        roles = []
        for r in data:
            if phrase.lower() in r["name"].lower():
                role = discord.utils.get(guild.roles, id=r["rolID"])
                roles.append(role)
        
        roles = self.role_splitter(roles)
        return roles
        
    def role_splitter(self, roles):
        role_list = []
        while len(roles) > 25:
            role_list.append(roles[0:25])
            del roles[0:25]
        else:
            role_list.append(roles)
        return role_list

    async def on_submit(self, interaction: discord.Interaction):
        roles = self.role_list(interaction.guild, str(self.part))
        view= PaginationView(interaction.guild, interaction.user, roles)
        await view.send(interaction)

class PaginationView(discord.ui.View):
    def __init__(self, guild, member, roles):
        super().__init__()
        self.current_page = 1
        self.guild = guild
        self.member = member
        self.roles = roles
        self.menu = SelectMenu(guild, member, roles[self.current_page - 1])
        self.add_item(self.menu)
        self.update_buttons()

    def update_buttons(self):
        if self.current_page == 1:
            self.left.disabled = True
            self.first.disabled = True
        else:
            self.left.disabled = False
            self.first.disabled = False

        if self.current_page == len(self.roles):
            self.right.disabled = True
            self.last.disabled = True
        else:
            self.right.disabled = False
            self.last.disabled = False

    async def send(self, interaction: discord.Interaction):
        self.interaction = interaction
        await self.interaction.response.send_message(view=self, ephemeral=True)
    
    async def edit(self, content = None):
        self.remove_item(self.menu)
        self.menu = SelectMenu(self.guild, self.member, self.roles[self.current_page - 1])
        self.add_item(self.menu)
        self.update_buttons()
        await self.interaction.edit_original_response(content=content, view=self)

    @discord.ui.button(label="|<", style=discord.ButtonStyle.green, row=2)
    async def first(self, interaction: discord.Interaction, Button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1
        await self.edit(content=f"{self.current_page}. Sayfadasınız.")

    @discord.ui.button(label="<", style=discord.ButtonStyle.green, row=2)
    async def left(self, interaction: discord.Interaction, Button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.edit(content=f"{self.current_page}. Sayfadasınız.")

    @discord.ui.button(label="Ara", style=discord.ButtonStyle.green, row=2)
    async def search(self, interaction: discord.Interaction, Button:discord.ui.Button):
        await interaction.response.send_modal(Questionnaire())

    @discord.ui.button(label=">", style=discord.ButtonStyle.green, row=2)
    async def right(self, interaction: discord.Interaction, Button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.edit(content=f"{self.current_page}. Sayfadasınız.")
    
    @discord.ui.button(label=">|", style=discord.ButtonStyle.green, row=2)
    async def last(self, interaction: discord.Interaction, Button:discord.ui.Button):
        await interaction.response.defer()
        self.current_page = len(self.roles)
        await self.edit(content=f"{self.current_page}. Sayfadasınız.")

class RolSelect(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.persistent_view = SelectButton()
    
    @commands.command()
    @is_me()
    async def rctest(self, ctx):
        await ctx.send(content="> Aşağıdaki butona basıp istediğiniz rolleri seçiniz.", view=SelectButton())

    async def cog_load(self):
        self.client.add_view(self.persistent_view)
    
    async def cog_unload(self):
        self.persistent_view.stop()

async def setup(bot):
    await bot.add_cog(RolSelect(bot))