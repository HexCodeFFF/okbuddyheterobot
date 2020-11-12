import discord
from discord.ext import commands
import asyncio
import logging
import json
import re
from functools import wraps
import random
from py_expression_eval import Parser

# initialize
parser = Parser()
logging.basicConfig(format='%(levelname)s:[%(asctime)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    level=logging.INFO)
logging.info(f"Discord Version {discord.__version__}")
logging.info("Initalizing")
bot = commands.Bot(command_prefix='d!', description='okbuddyhetero bot')
bot.remove_command('help')
with open('db.json') as f:
    db = json.load(f)
with open('help.txt') as f:
    helptxt = f.read()
with open('adminhelp.txt') as f:
    adminhelptxt = f.read()


# functions
def save_db():
    with open('db.json', 'w') as outfile:
        json.dump(db, outfile, indent=4)


def is_authorized(function):
    @wraps(function)
    async def wrapper(ctx, *args, **kwargs):
        if str(ctx.author.id) in db["admins"]:
            await function(ctx, *args, **kwargs)
        else:
            await ctx.channel.send("You are not authorized to use this command.")

    return wrapper


async def reactionfunction(msg):
    await msg.add_reaction(bot.get_emoji(746881074583437352))  # okbh upvote
    await msg.add_reaction(bot.get_emoji(746881238752690268))  # okbh downvote
    # await msg.add_reaction(bot.get_emoji(776226766640513045))  # ztools2 upvote
    # await msg.add_reaction(bot.get_emoji(776226783103942656))  # ztools2 downvote


# onready
@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name}!")
    game = discord.Activity(name=f"d!help | r/okbh bot",
                            type=discord.ActivityType.listening)
    await bot.change_presence(activity=game)
    # while not bot.is_closed():


# @everyone commands
@bot.command()
async def help(ctx):
    await ctx.send(helptxt)


@bot.command()
async def owoify(ctx, *, text="above"):
    if text == "above":
        messages = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        text = messages[0].content
    await ctx.send(
        text.replace("r", "w").replace("R", "W").replace("l", "w").replace("L", "W").replace("@", "\\@") + " owo~")


@bot.command(name="8ball")
async def eightball(ctx, *, question=""):
    await ctx.send("shut the hell up")


@bot.command(name="m")
async def macro(ctx, name="list"):
    if name == "list":
        k = db["macros"].keys()
        if k:
            out = "Available macros:\n"
            for m in k:
                out += f"`{m}`, "
            await ctx.send(out.rstrip(", "))
        else:
            await ctx.send("No macros available")
    elif name in db["macros"]:
        await ctx.send(db["macros"][name])
    else:
        await ctx.send("That macro does not exist.")


# authorized/admin commands
@bot.command()
@is_authorized
async def addmacro(ctx, name, *, content):
    if name in db["macros"]:
        out = f"🔅 Macro `{name}` already exists."
    else:
        db["macros"][name] = content
        out = f"✅ Added macro `{name}`."
    save_db()
    logging.info(out)
    await ctx.send(out)


@bot.command()
@is_authorized
async def removemacro(ctx, name):
    if name in db["macros"]:
        del db["macros"][name]
        out = f"✅ Removed macro `{name}`"
    else:
        out = f"❌ Macro `{name}` does not exist."

    save_db()
    logging.info(out)
    await ctx.send(out)


@bot.command()
async def featurerequest(ctx, *, feature):
    if ctx.author.id == 776512576338788374:  # annoying cunt
        await ctx.send("shut the hell up sophia")
    else:
        await bot.get_user(214511018204725248).send(f"<@{ctx.author.id}> Requests:\n>>> {feature}")
        await ctx.send("✅ Requested!")


def diceeval(dicearg):
    out = [0, f"{dicearg} = "]
    dice = dicearg.split("d")
    if dice[0] == "":
        dice[0] = 1
    dice[0] = int(dice[0])
    dice[1] = int(dice[1])
    for i in range(dice[0]):
        diceiter = random.randint(1, dice[1])
        out[0] += diceiter
        if dice[0] > 1:
            out[1] += f"{diceiter} + "
    if dice[0] > 1:
        out[1] = out[1].rstrip("+ ")
        out[1] += f" = {out[0]}"
    else:
        out[1] += str(out[0])
    return out


@bot.command(name="dice")
async def diceparse(ctx, *, arg):
    arg = arg.lower()
    arg = re.sub("[^-+/*()^%d.\\d]", "", arg)  # remove all invalid chars
    out = ""
    while True:
        dice = re.search("\\d*d\\d+", arg)
        if dice:
            dice = dice.group()
            deval = diceeval(dice)
            out += deval[1] + "\n"
            arg = arg.replace(dice, str(deval[0]), 1)
        else:
            break
    final = parser.parse(arg).evaluate({})
    if str(final) == str(arg):
        await ctx.send(f"{out}**{final}**")
    else:
        await ctx.send(f"{out}{arg}\n**{final}**")


@bot.command()
@is_authorized
async def adminhelp(ctx, *, arg):
    await ctx.send(adminhelptxt)


@bot.command()
@is_authorized
async def addchannel(ctx, *, arg):
    search = re.findall(r"\d{18}", arg)
    if search:
        out = ""
        for ch in search:
            channel = bot.get_channel(int(ch))
            if channel:
                if ch in db["channels"]:
                    out += f"🔅 <#{ch}> was already registered.\n"
                else:
                    db["channels"].append(ch)
                    out += f"✅ Added <#{ch}>\n"
            else:
                out += f"❌ {ch} is not a valid channel id.\n"
        save_db()
        logging.info(out)
        await ctx.send(out.strip())
    else:
        await ctx.send("❌ Invalid parameter. Please link a channel or send it's ID. You can do multiple at once.")


@bot.command()
@is_authorized
async def removechannel(ctx, *, arg):
    search = re.findall(r"\d{18}", arg)
    if search:
        out = ""
        for ch in search:
            if ch in db["channels"]:
                db["channels"].remove(str(ch))
                out += f"✅ Removed <#{ch}>\n"
            else:
                out += f"❌ <#{ch}> was not registered.\n"
        save_db()
        logging.info(out)
        await ctx.send(out.strip())
    else:
        await ctx.send("❌ Invalid parameter. Please link a channel or send it's ID. You can do multiple at once.")


@bot.command()
@is_authorized
async def addadmin(ctx, *, arg):
    search = re.findall(r"\d{18}", arg)
    if search:
        out = ""
        for user in search:
            channel = bot.get_user(int(user))
            if channel:
                if user in db["admins"]:
                    out += f"🔅 <@{user}> is already an admin.\n"
                else:
                    db["admins"].append(user)
                    out += f"✅ Added <@{user}>\n"
            else:
                out += f"❌ {user} is not a valid user id.\n"
        save_db()
        logging.info(out.strip())
        await ctx.send(out)
    else:
        await ctx.send("❌ Invalid parameter. Please link a user or send their ID. You can do multiple at once.")


@bot.command()
@is_authorized
async def removeadmin(ctx, *, arg):
    search = re.findall(r"\d{18}", arg)
    if search:
        out = ""
        for user in search:
            if user in db["admins"]:
                db["admins"].remove(str(user))
                out += f"✅ Removed <@{user}>\n"
            else:
                out += f"❌ <@{user}> is not an admin.\n"
        save_db()
        logging.info(out.strip())
        await ctx.send(out)
    else:
        await ctx.send("❌ Invalid parameter. Please link a user or send their ID. You can do multiple at once.")


@bot.command()
@is_authorized
async def listchannels(ctx):
    if db["channels"]:
        out = "Registered channels:\n"
        for ch in db["channels"]:
            out += f"- <#{ch}>\n"
    else:
        out = "No channels registered."
    await ctx.send(out)


@bot.command()
@is_authorized
async def listadmins(ctx):
    if db["admins"]:
        out = "Registered admins:\n"
        for ch in db["admins"]:
            out += f"- <@{ch}>\n"
    else:
        out = "No admins registered."
    await ctx.send(out)


@bot.command()
@is_authorized
async def testreaction(ctx):
    await reactionfunction(ctx.message)


# owner commands
@bot.command()
@commands.is_owner()
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.channel.send(msg)


@bot.command()
@commands.is_owner()
async def die(ctx):
    await bot.close()


@bot.command()
@commands.is_owner()
async def edit(ctx, msgid, *, content):
    await ctx.message.delete()
    msg = await ctx.channel.fetch_message(int(msgid))
    await msg.edit(content=content)


@bot.listen()
async def on_message(msg):
    if str(msg.channel.id) in db["channels"]:  # suggestions-meta
        await reactionfunction(msg)


@bot.listen()
async def on_command_error(ctx, error):
    await ctx.send(str(error).replace("@", "\\@"))
    logging.error(error)


bot.run("Nzc2MTgyMzM3MDEyMTA1MjY2.X6xKIQ.Qz3U7-aBR8cbO22bjQJUdb42YwE")
