import discord
from discord.ext import commands
import json

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
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
    message = await message.channel.fetch_message(1305268184617586729)
    author = message.embeds[0].author.name
    for key, value in data["users"].items():
        if (author == value["github"]):
            data["users"][key]["points"] += 1
            setsecret(data)
            await message.channel.send(f"Gave one point to user {key}!")
            await update_leaderboard()
            return
    await message.channel.send(f"No user found with github of \"{author}\"")

async def update_leaderboard():
    leaderboard_chan = bot.get_channel(1305704135924125736)
    leaderboard = leaderboard_chan.fetch_message()
    # TODO: access message and update from database. Sort users by points and add any new ones here

@bot.command()
async def init_leaderboad(ctx):
    embed = discord.Embed(
        title=f"The Almighty Leaderboard",
        color=discord.Color.random(),
    )

    for key, value in data["users"].items():
        embed.add_field(name=f"{key} ({value["github"]})", value=f"Points: {value["points"]}") 

    await ctx.send(embed=embed)

@bot.command()
async def register(ctx: commands.Context, arg:str):
    tg = ctx.author.name
    users:dict = data["users"]
    if (tg in users.keys()):
        await ctx.send("user already exists, updating information")
    users[tg] = {"github":arg, "points": 0}
    setsecret(data)
    # TODO: Add new user to leaderboard upon register
    

bot.run(data["token"])
