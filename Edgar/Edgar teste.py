import discord, random
from discord.ext import commands
from EdgarCog import EdgarCog

Edgar = commands.Bot(command_prefix = '!', case_insensitive=True)

@Edgar.event
async def on_ready():
    print('Logged in as')
    print(Edgar.user.name)
    print(Edgar.user.id)
    print('------')

Edgar.add_cog(EdgarCog(Edgar))

@Edgar.event
async def on_message(message):
    if message.author.id == Edgar.user.id or not len(message.content): return
    if message.content[0] == '!':
        await Edgar.process_commands(message)
    elif 'd' in message.content[1:4].lower():
        content = message.content.split()
        mark = content[0].lower().find('d')
        rolls = content[0][:mark]
        dice = content[0][mark+1:]

        if not rolls.isdigit() or not dice.isdigit() or int(dice) < 2: return
        elif int(rolls) > 100: rolls = 100
        values = random.choices(range(1,int(dice)+1), k=int(rolls))

        msg = f"{message.author.mention}\n{values} → {sum(values)}"
        if len(message.content.split()) > 1:
            check = content[1]

            if not check.isdigit(): return
            else: check = int(check)

            for roll in values:
                if roll > check:
                    msg += "\nFalhou!"
                elif roll > check//2:
                    msg += "\nSucesso normal!"
                elif roll > check//5:
                    msg += "\nSucesso bom!"
                else:
                    msg += "\nSucesso extremo!"
        await message.channel.send(msg)
    else: return

Edgar.run('NjQ1NDA3MDA4OTY2ODM2MjU0.XdCIRA.UEZVG5ktUWWFbRzx-JOOfSqCEWk')