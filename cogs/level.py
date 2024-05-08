from typing import Optional
import discord
from discord.ext import commands
from mydecorators import *
from pprint import pprint

class Level(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.message_count: dict = {}
    
    def make_post(self):
        posts: dict = {{"id":item.key, "message":item.value} for item in self.message_count}

    @commands.Cog.listener()
    async def on_message(self, message):
        return
        print(message.author)
        forum = discord.utils.get(message.guild.forums, id=1147575510302462013)
        if message.author.id == 283641823778570242:
            ...
        if message.channel.id in [841554664516616223, 813894315091820564, 566927796937687080, 823973147510177792, 605024794571702292] or message.channel in forum.threads:
            if (u_id := str(message.author.id)) in self.message_count:
                self.message_count[u_id] += 1
            else:
                self.message_count[u_id] = 1
        print(self.message_count)
    
    @commands.command()
    @is_me()
    async def levelcheck(self, ctx):
        pprint(self.message_count)

async def setup(client):
    await client.add_cog(Level(client))