import secret
import nextcord
from nextcord.ext import commands

token = secret.Your_Token
intents = nextcord.Intents.all()

bot = commands.Bot(command_prefix='!',intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    channel = bot.get_channel(1116747276275155024)
    i = 0

    async for message in channel.history(limit=None):
        await message.delete()
        i = i+1
        print(f"{str(i)} Files deleted")
    print("Done!")

    await  bot.close()
bot.run(token)