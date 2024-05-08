from discord.ext import commands

def is_me():
    def predicate(ctx):
        return ctx.message.author.id == 283641823778570242
    return commands.check(predicate)

def is_ekip():
    def predicate(ctx):
        roles = ctx.author.roles
        roleids = [i.id for i in roles]
        return (831627010954231868 in roleids) or (494123546910523393 in roleids)
    return commands.check(predicate)

# def can_use():
#     def predicate(ctx):
#         return False
#     return commands.check(predicate)