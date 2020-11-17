import os
import sys
import traceback
from datetime import datetime

import discord
from discord.ext import commands
import asyncio
import logging
import json
import re
from functools import wraps
import random
from py_expression_eval import Parser
import praw
import itertools
from discord.ext.commands.cooldowns import BucketType  # for cooldown? idfk

intents = discord.Intents.default()
intents.members = True

reddit = praw.Reddit(
    client_id="-5OEySRzJgxoxw",
    client_secret="4lx7sD16C_Yh9Lmn_eh7qEvbM58Ksw",
    user_agent="python lol"
)
# initialize
parser = Parser()
log_file = "log/" + str(datetime.utcnow().strftime('%Hh%Mm-%dd%mm%yy')) + '.log'
logging.basicConfig(format='%(levelname)s [%(asctime)s] %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S%p', level=logging.INFO,
                    handlers=[logging.FileHandler(log_file, encoding='utf-8'), logging.StreamHandler()])
logging.info(f"Logging to {log_file}")
logging.info(f"Discord Version {discord.__version__}")
logging.info("Initalizing")
bot = commands.Bot(command_prefix='d!', description='okbuddyhetero bot', intents=intents)
bot.remove_command('help')
with open('db.json', encoding='utf-8') as f:
    db = json.load(f)
with open('help.txt', encoding='utf-8') as f:
    helptxt = f.read()
with open('adminhelp.txt', encoding='utf-8') as f:
    adminhelptxt = f.read()
regionals = {'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}', 'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
             'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
             'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}', 'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
             'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
             'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}', 'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
             'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
             'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}', 'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
             'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
             'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}', 'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
             'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
             'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}', 'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
             'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
             's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}', 't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
             'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
             'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}', 'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
             'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
             'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}', 'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
             '0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣',
             '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣', '8': '8⃣', '9': '9⃣', '!': '\u2757',
             '?': '\u2753'}


# functions
def save_db():
    with open('db.json', 'w') as outfile:
        json.dump(db, outfile, indent=4)


# formerly used for d!catboy and d!femboy commands, some images were lewd so this has to be changed :/

def random_from_reddit(subreddit):
    random_submission = reddit.subreddit(subreddit).random()
    if random_submission is None:  # subreddit does not support random sort :/
        random_submission = reddit.subreddit(subreddit).top("month")
        rand = random.randint(0, 100)
        random_submission = list(itertools.islice(random_submission, rand, rand + 1, 1))[0]
    if random_submission.over_18:
        return f"Random post was NSFW, try again :/"
    else:
        return random_submission.url


def random_from_folder(folder):
    return f"{folder}/{random.choice(os.listdir(folder))}"


def is_authorized(function):
    @wraps(function)
    async def wrapper(ctx, *args, **kwargs):
        if str(ctx.author.id) in db["admins"]:
            await function(ctx, *args, **kwargs)
        else:
            await ctx.channel.send("❌ You are not authorized to use this command.")

    return wrapper


async def reassign_gen3(toadd="random", toremove="random"):
    okbh = bot.get_guild(746458625068892333)
    gen3role = okbh.get_role(777378971850506272)
    gen3 = okbh.get_channel(777186916432347136)
    if toremove == "random":
        while True:
            memb = random.choice(okbh.members)
            if gen3role in memb.roles and memb.id != 214511018204725248 and memb.id != 776182337012105266:
                toremove = memb
                break
    else:
        toremove = okbh.get_member(int(toremove))
    if toadd == "random":
        while True:
            memb = random.choice(okbh.members)
            if gen3role not in memb.roles:
                toadd = memb
                break
    else:
        toadd = okbh.get_member(int(toadd))
    logging.info(f"gen-3: adding {toadd.display_name} and removing {toremove.display_name}")
    await toremove.remove_roles(gen3role)
    await toadd.add_roles(gen3role)
    await gen3.send(f"{toremove.mention} has been replaced by {toadd.mention}!")
    return [toadd, toremove]


async def reactionfunction(msg):
    await msg.add_reaction(bot.get_emoji(746881074583437352))  # okbh upvote
    await msg.add_reaction(bot.get_emoji(746881238752690268))  # okbh downvote
    # for emoji in random.choice(
    #         ["PENISHA", "1984", "amongus", "bigsex", "10ogecs", "gay", "oga", "why", "no", "yes", "redit", "gen1",
    #          "naruto", "help", "modsl", "l", "fortnie", "ROSEBAD", "bigcoke", "monke", "trol", "cum", "golira",
    #          "doge","thanks","uh"]):
    #     await msg.add_reaction(regionals[emoji.lower()] if emoji.isalnum() or emoji in ["!", "?"] else emoji)
    # await msg.add_reaction(bot.get_emoji(776226766640513045))  # ztools2 upvote
    # await msg.add_reaction(bot.get_emoji(776226783103942656))  # ztools2 downvote


# onready
@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user.name}!")
    game = discord.Activity(name=f"d!help | r/okbh bot",
                            type=discord.ActivityType.listening)
    await bot.change_presence(activity=game)
    while not bot.is_closed():
        await asyncio.sleep(60 * 60)
        await reassign_gen3()


# @everyone commands
@commands.cooldown(1, 10, BucketType.user)
@bot.command(name="help")
async def helpcommand(ctx):
    await ctx.send(helptxt)


@commands.cooldown(3, 5, BucketType.user)
@bot.command()
async def regional(ctx, *, msg="above"):
    if msg == "above":
        messages = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        msg = messages[0].content
    """Replace letters with regional indicator emojis"""
    msg = list(msg)
    regional_list = [regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
    regional_output = '\u200b'.join(regional_list)
    await ctx.send(regional_output)


@commands.cooldown(3, 5, BucketType.user)
@bot.command()
async def catboy(ctx):
    await ctx.channel.trigger_typing()
    await ctx.send(file=discord.File(random_from_folder("catboys")))
    # await ctx.send(random_from_reddit("nekoboys"))


@commands.cooldown(3, 5, BucketType.user)
@bot.command()
async def femboy(ctx):
    await ctx.channel.trigger_typing()
    await ctx.send(file=discord.File(random_from_folder("femboys")))
    # await ctx.channel.trigger_typing()
    # await ctx.send(random_from_reddit("femboy"))


@commands.cooldown(3, 5, BucketType.user)
@bot.command()
async def randomreddit(ctx, subreddit):
    """
    await ctx.channel.trigger_typing()
    await ctx.send(random_from_reddit(subreddit))
    """
    await ctx.send("❌ Sorry, this command is temporarily disabled at okbh admin's request.")


@commands.cooldown(3, 5, BucketType.user)
@bot.command()
async def owoify(ctx, *, text="above"):
    if text == "above":
        messages = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        text = messages[0].content
    await ctx.send(
        text.replace("r", "w").replace("R", "W").replace("l", "w").replace("L", "W").replace("@", "\\@") + " owo~")


@commands.cooldown(3, 5, BucketType.user)
@bot.command()
async def sparkle(ctx, *, text="above"):
    if text == "above":
        messages = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        text = messages[0].content
    await ctx.send(f"✨ *{' '.join(text)}* ✨")


@commands.cooldown(3, 5, BucketType.user)
@bot.command(name="8ball")
async def eightball(ctx, *, question=""):
    await ctx.send("shut the hell up")


@commands.cooldown(3, 15, BucketType.user)
@bot.command(name="m")
async def macro(ctx, name="list"):
    if name == "list":
        k = db["macros"].keys()
        if k:
            out = "📃 Available macros:\n"
            for m in k:
                out += f"`{m}`, "
            await ctx.send(out.rstrip(", "))
        else:
            await ctx.send("❌ No macros available")
    elif name in db["macros"]:
        await ctx.send(db["macros"][name])
    else:
        await ctx.send(f"❌ Macro `{name}` does not exist.")


@commands.cooldown(1, 5, BucketType.user)
@bot.command()
async def request(ctx, *, feature):
    if int(ctx.author.id) == 776512576338788374:  # annoying cunt
        await ctx.send("shut the hell up sophia")
    else:
        if len(ctx.message.attachments) > 0:
            feature += "\nAttached files: "
            for attach in ctx.message.attachments:
                feature += attach.url + " "
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


# admin only commands
@bot.command()
@is_authorized
async def adminhelp(ctx):
    await ctx.send(adminhelptxt)


@bot.command()
@is_authorized
async def forcegen3(ctx, toadd="random", toremove="random"):
    members = await reassign_gen3(toadd, toremove)
    await ctx.send(f"✅ Done")


@bot.command()
@is_authorized
async def addmacro(ctx, name, *, content):
    if name in db["macros"]:
        out = f"🔅 Macro `{name}` already exists."
    else:
        db["macros"][name] = content
        out = f"✅ Added macro `{name}`."
    save_db()
    logging.info(out.strip())
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
    logging.info(out.strip())
    await ctx.send(out)


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
        logging.info(out.strip())
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
        logging.info(out.strip())
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
        out = "💬 Registered channels:\n"
        for ch in db["channels"]:
            out += f"- <#{ch}>\n"
    else:
        out = "❌ No channels registered."
    await ctx.send(out)


@bot.command()
@is_authorized
async def listadmins(ctx):
    if db["admins"]:
        out = "💬 Registered admins:\n"
        for ch in db["admins"]:
            out += f"- <@{ch}>\n"
    else:
        out = "❌ No admins registered."
    await ctx.send(out)


@bot.command()
@is_authorized
async def testreaction(ctx):
    await reactionfunction(ctx.message)


@bot.command()
@is_authorized
async def listgen3(ctx):
    okbh = bot.get_guild(746458625068892333)
    gen3role = okbh.get_role(777378971850506272)
    gen3s = []
    for member in okbh.members:
        if gen3role in member.roles:
            gen3s.append(member.display_name)
    await ctx.send(f"📃 There are {len(gen3s)} members in gen 3:\n{','.join(gen3s)}")


@bot.command()
@is_authorized
async def force_reaction(ctx, channelid: int, msgid: int):
    await reactionfunction(await bot.get_channel(channelid).fetch_message(msgid))
    await ctx.send("✅ Done")


# owner commands
@bot.command()
@commands.is_owner()
async def addgen3(ctx, membid):
    okbh = bot.get_guild(746458625068892333)
    gen3role = okbh.get_role(777378971850506272)
    await okbh.get_member(int(membid)).add_roles(gen3role)
    await ctx.send("✅ Done")


@bot.command()
@commands.is_owner()
async def giverole(ctx, roleid: int):
    role = ctx.guild.get_role(roleid)
    me = ctx.guild.get_member(bot.user.id)
    await me.add_roles(role)
    await ctx.send("✅ Done")


@bot.command()
@commands.is_owner()
async def say(ctx, *, msg):
    try:
        await ctx.message.delete()
    except Exception as e:
        pass
    await ctx.channel.send(msg)


@bot.command()
@commands.is_owner()
async def nick(ctx, *, nickname="gay ass doge"):
    await ctx.guild.get_member(bot.user.id).edit(nick=nickname)
    await ctx.send(f"✅ Changed nickname to `{nickname}`")


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


@bot.command()
@commands.is_owner()
async def delete(ctx, msgid):
    msg = await ctx.channel.fetch_message(int(msgid))
    await msg.delete()


@bot.command()
@commands.is_owner()
async def pin(ctx, msgid):
    msg = await ctx.channel.fetch_message(int(msgid))
    await msg.pin()


@bot.listen()
async def on_message(msg):
    if str(msg.channel.id) in db["channels"]:  # suggestions-meta
        await reactionfunction(msg)


@bot.listen()
async def on_command(ctx):
    logging.info(f"@{ctx.message.author.name}#{ctx.message.author.discriminator} ({ctx.message.author.display_name}) "
                 f"ran command '{ctx.message.content}' in channel #{ctx.channel.name} in server {ctx.guild}")


@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        err = f"⁉ Command `{ctx.message.content}` does not exist."
        logging.warning(err)
        await ctx.send(err)
    elif isinstance(error, discord.ext.commands.errors.NotOwner):
        err = "❌ You are not authorized to use this command."
        logging.warning(err)
        await ctx.send(err)
    else:
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        await ctx.send("‼ `" + str(error).replace("@", "\\@") + "`")


with open('token.txt') as f:  # not on github for obvious reasons
    token = f.read()
bot.run(token)
