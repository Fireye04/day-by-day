import discord
from discord.ext import commands
from discord import app_commands


intents = discord.Intents.all()


client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=1304510973390094367))
    print(f"Logged in as {client.user}") 
    print("------")

@client.event
async def on_message(message):
    print("fuck")
    await bot.get_context(message)
    await bot.process_commands(message)



@tree.command(
    name="ping",
    description="Ping command to check bot's latency.",
    guild=discord.Object(id=1304510973390094367),
)
async def slash_ping(ctx):
    latency = round(client.latency * 1000)  # Latency in milliseconds
    await ctx.response.send_message(f"Pong! Latency: {latency}ms")

@bot.command(aliases=["w"])
async def test_wh(ctx: commands.Context ):
    print("gothere")
    message = ctx.fetch_message(1305268184617586729)
    print(message)

@bot.command()
async def fuck(ctx: commands.Context):
    await ctx.send("Holy fucking shit your thing works my god chill out")

with open(".secret.txt", "r") as secret:
    token = secret.readlines()[0]
client.run(token)
