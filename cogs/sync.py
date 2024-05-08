from typing import Literal, Optional
from discord.ext.commands import Greedy, Context
import discord
from discord.ext import commands

class appsync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("appsync is ready")
    
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None):
        print(f"{spec=} ")
        if not guilds:
            if spec == "~":
                fmt = await ctx.bot.tree.sync(guild = ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                fmt = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                fmt = []
            else:
                fmt = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(fmt)} commands {'globally' if spec is None else 'to the current guild.'} "
            )
            return
        
        assert guilds is not None
        fmt = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException as e:
                print(e)
            else:
                fmt += 1
        await ctx.send(f"Synched the tree to {fmt}/{len(guilds)} guilds.")

async def setup(bot):
    await bot.add_cog(appsync(bot))