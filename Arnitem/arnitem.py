import discord
from discord.ext import commands
from arnitemCog import ArnitemCog

intents = discord.Intents.all()
Arnitem = commands.Bot(command_prefix = '!', case_insensitive=True, intents=intents)

@Arnitem.event
async def on_ready():
    print('Logged in as')
    print(Arnitem.user.name)
    print(Arnitem.user.id)
    print('------')

Arnitem.add_cog(ArnitemCog(Arnitem))

Arnitem.run('Njc4NzMyMzY5NDM1Mjk1NzU0.XknExw.sxbO2ApahMpVnnphU5wxrkq_emg')