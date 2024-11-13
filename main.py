import discord
from discord.ext import tasks, commands
import json
from datetime import datetime, time, timedelta, timezone

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="$", intents=intents)


def getsecret():
    with open("secret.json", "r") as sec:
        data = json.load(sec)
    return data


def setsecret(target: dict):
    with open("secret.json", "w") as sec:
        json.dump(target, sec)


time = time(hour=0, minute=0, tzinfo=timezone(timedelta(hours=-7)))

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminder.start()

    def cog_unload(self):
        self.reminder.cancel()

    @tasks.loop(time=time)
    async def reminder(self):
        if datetime.now().weekday() != 0:
            print("Not today...")
            return
        print("ITS HAPPENING PEOPLE STAY CALM")
        data = getsecret()
        for key, value in data["users"].items():
            lastcmt = datetime.strptime(value["last_commit"], "%Y-%m-%d") + timedelta(
                days=7
            )
            if datetime.now().date() > lastcmt.date():
                await (await self.bot.get_channel(1305266938779402322)).send(
                    f"WEE WOO! LOOKS LIKE <@!{key}> FORGOT TO COMMIT WITHIN THE LAST WEEK! POINT AND LAUGH!"
                )


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("------")
    await bot.add_cog(Reminder(bot))


@bot.listen("on_message")
async def process_github(message: discord.message.Message):
    if message.author == bot.user:
        return
    data = getsecret()

    # must be in webhook channel and be the webhook bot
    if (
        message.channel.id != data["webhook"]["channel_id"]
        or message.author.id != data["webhook"]["bot_id"]
    ):
        return
    author = message.embeds[0].author.name
    commits = message.embeds[0].description.splitlines()
    for key, value in data["users"].items():
        if author == value["github"]:
            if (
                message.created_at.date()
                > datetime.strptime(value["last_commit"], "%Y-%m-%d").date()
            ):
                pts = 10 + len(commits) - 1
                data["users"][key]["points"] += pts
                await message.channel.send(f"Gave {pts} points to user <@!{key}>!")

            else:
                data["users"][key]["points"] += len(commits)
                if len(commits) == 1:
                    msg = f"Gave one point to user <@!{key}>!"
                else:
                    msg = f"Gave {len(commits)} points to user <@!{key}>!"
                await message.channel.send(msg)

            data["users"][key]["last_commit"] = str(message.created_at.date())
            setsecret(data)
            await update_leaderboard(message, data)
            return

    await message.channel.send(f'No user found with github of "{author}"')


async def update_leaderboard(message: discord.message.Message, data: dict):
    leaderboard_chan = message.guild.get_channel(int(data["leaderboard"]["channel_id"]))
    leaderboard = await leaderboard_chan.fetch_message(
        int(data["leaderboard"]["message_id"])
    )

    em: discord.Embed = leaderboard.embeds[0]
    for i in range(len(em.fields)):
        em.remove_field(i)

    userdict = {}

    for key, value in data["users"].items():
        userdict[value["points"]] = {
            "name": key,
            "github": value["github"],
            "last_commit": value["last_commit"],
        }

    # Shamelessly copied from geeksforgeeks <3
    myKeys = list(userdict.keys())
    myKeys.sort()

    sd = {i: userdict[i] for i in myKeys}
    print(sd)

    for key, value in sd.items():
        em.add_field(
            name=f"{(await bot.fetch_user(value["name"])).name} ({value["github"]}: {value["last_commit"]})",
            value=f"Points: {key}",
        )

    await leaderboard.edit(embed=em)


@bot.command()
async def init_leaderboard(ctx: commands.Context):
    data = getsecret()
    embed = discord.Embed(
        title=f"The Almighty Leaderboard",
        color=discord.Color.random(),
    )

    for key, value in data["users"].items():
        embed.add_field(
            name=f"{(await bot.fetch_user(key)).name} ({value["github"]}: {value["last_commit"]})",
            value=f"Points: {value["points"]}",
        )

    msg = await ctx.send(embed=embed)
    data["leaderboard"] = {"channel_id": ctx.channel.id, "message_id": msg.id}
    setsecret(data)


@bot.command()
async def init_webhook(ctx: commands.Context, arg: str):
    data = getsecret()
    try:
        i_arg= int(arg)
    except ValueError:
        await ctx.send(
            "Make sure to provide the webhook's ID as a numerical argument to this command"
        )
        return

    data["webhook"] = {"channel_id": ctx.channel.id, "bot_id": i_arg}
    setsecret(data)
    await ctx.send("Successfully set webhook data!")


@bot.command()
async def register(ctx: commands.Context, arg: str):
    data = getsecret()
    if len(arg) == 0:
        await ctx.send("Please provide your github username as an argument")
        return
    tg = ctx.author.id
    users: dict = data["users"]
    if tg in users.keys():
        await ctx.send("user already exists, updating information")
    users[tg] = {"github": arg, "points": 0, "last_commit": "2020-11-10"}
    setsecret(data)
    await ctx.send("Registration complete :)")
    # TODO: Add new user to leaderboard upon register


data = getsecret()
bot.run(data["token"])
