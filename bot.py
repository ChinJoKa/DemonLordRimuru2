import asyncio
import discord
import os
from discord.ext import commands, tasks
from itertools import cycle
from mydecorators import is_me
from dotenv import load_dotenv

class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix=commands.when_mentioned_or("*"), intents=intents)
    async def setup_hook(self) -> None:
        pass

client = PersistentViewBot()

pstatus = ['Tempest Tarikatı', 'Demon Lord Rimuru', 'Jura Tempest Ormanı']
playing = cycle(pstatus)

@client.event
async def on_ready():
    change_status.start()
    if not hasattr(client, 'appinfo'):
        client.appinfo = await client.application_info()
    print('Bot is ready.')

@tasks.loop(seconds=6)
async def change_status():
    await client.change_presence(activity=discord.Game(next(playing)))

@client.command()
@is_me()
async def load(ctx, extension):
    if ctx.author.id == 283641823778570242:
        await ctx.message.delete()
        await client.load_extension(f'cogs.{extension}')
        await(await ctx.send(f'{extension} loaded')).delete(delay=3)
    else:
        await ctx.send(f"You don't have that permission")

@client.command()
@is_me()
async def unload(ctx, extension):
    if ctx.author.id==283641823778570242:
        await ctx.message.delete()
        await client.unload_extension(f'cogs.{extension}')
        await(await ctx.send(f'{extension} unloaded')).delete(delay=3)
    else:
        await ctx.send(f"You don't have that permission")

@client.command()
@is_me()
async def reload(ctx, extension):
    if ctx.author.id==283641823778570242:
        await ctx.message.delete()
        await client.unload_extension(f'cogs.{extension}')
        await client.load_extension(f'cogs.{extension}')
        await(await ctx.send(f'{extension} reloaded')).delete(delay=3)
    else:
        await ctx.send(f"You don't have that permission")

async def load():
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension(f"cogs.{file[:-3]}")

async def main():
    async with client:
        await load()
        load_dotenv()
        TOKEN = os.getenv("TOKEN")
        await client.start(TOKEN)
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())
