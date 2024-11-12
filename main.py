import discord
from discord.ext import commands
import json
from datetime import datetime


intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.presences = True


bot = commands.Bot(command_prefix='$', intents=intents)

def getsecret():
    f = open("secret.json")
    data = json.load(f)
    f.close()
    return data

def setsecret(target:dict):
    with open("secret.json", "w") as sec:
        json.dump(target, sec)


data = getsecret()
 

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}") 
    print("------")

@bot.listen('on_message')
async def process_github(message: discord.message.Message):
    if (message.author == bot.user):
        return
    # must be in webhook channel and be the webhook bot
    if (message.channel.id != 1305266938779402322 and message.author.id != 1305266962800185356):
        return
    data = getsecret()
    author = message.embeds[0].author.name
    commits = message.embeds[0].description.splitlines()
    for key, value in data["users"].items():
        if (author == value["github"]):
            if (message.created_at.date() > datetime.strptime(value["last_commit"], "%Y-%m-%d").date()):
                pts = 10 + len(commits) - 1
                data["users"][key]["points"] += pts
                await message.channel.send(f"Gave {pts} points to user {key}!")

            else:
                data["users"][key]["points"] += len(commits)
                if len(commits) == 1:
                    msg = f"Gave one point to user {key}!" 
                else:
                    msg = f"Gave {len(commits)} points to user {key}!"
                await message.channel.send(msg)

            data["users"][key]["last_commit"] = str(message.created_at.date())
            setsecret(data)
            await update_leaderboard(message, data)
            return

    await message.channel.send(f"No user found with github of \"{author}\"")


async def update_leaderboard(message: discord.message.Message, data):
    leaderboard_chan = message.guild.get_channel(int(data["leaderboard"]["channel_id"]))
    leaderboard = await leaderboard_chan.fetch_message(int(data["leaderboard"]["message_id"]))

    em:discord.Embed = leaderboard.embeds[0]
    for i in range(len(em.fields)):
        em.remove_field(i)
    
    userdict = {}

    for key, value in data["users"].items():
        userdict[value["points"]] = {"name": key, "github": value["github"], "last_commit": value["last_commit"]}

    myKeys = list(userdict.keys())
    myKeys.sort()

    sd = {i: userdict[i] for i in myKeys}
    print(sd) 

    for key, value in sd.items():
        em.add_field(name=f"{value["name"]} ({value["github"]}: {value["last_commit"]})", value=f"Points: {key}")

    await leaderboard.edit(embed=em)
    
    # TODO: access message and update from database. Sort users by points and add any new ones here

@bot.command()
async def init_leaderboard(ctx: commands.Context):
    data = getsecret()
    embed = discord.Embed(
        title=f"The Almighty Leaderboard",
        color=discord.Color.random(),
    )

    for key, value in data["users"].items():
        embed.add_field(name=f"{key} ({value["github"]}: {value["last_commit"]})", value=f"Points: {value["points"]}") 

    msg = await ctx.send(embed=embed)
    data["leaderboard"] = {"channel_id":ctx.channel.id,"message_id": msg.id}
    setsecret(data)

@bot.command()
async def register(ctx: commands.Context, arg:str):
    data = getsecret()
    if (len(arg) == 0):
        await ctx.send("Please provide your github username as an argument")
        return
    tg = ctx.author.name
    users:dict = data["users"]
    if (tg in users.keys()):
        await ctx.send("user already exists, updating information")
    users[tg] = {"github":arg, "points": 0, "last_commit":"2020-11-10"}
    setsecret(data)
    # TODO: Add new user to leaderboard upon register
    

bot.run(data["token"])
