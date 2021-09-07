import discord, random
import numpy as np
from discord.ext import commands

Edgar = commands.Bot(command_prefix = '!', case_insensitive=True)

@Edgar.event
async def on_ready():
    print('Logged in as')
    print(Edgar.user.name)
    print(Edgar.user.id)
    print('------')

def get_results(content):
    try:
        index = content[0].lower().find('d')
        if index < 0: raise ValueError

        rolls = int(content[0][:index])
        dice = int(content[0][index+1:])

        if dice < 2: dice = 2

        if rolls > 100: rolls = 100
        elif rolls < 1: rolls = 1

        result = [random.choices(range(1, dice + 1), k=rolls), '', rolls, dice]

        value = int(content[1])

        value_checks = np.array([101, value, value//2, value//5])
        value_success = {
            101:'\nFalha!',
            value:'\nSucesso Normal!',
            value//2:'\nSucesso Bom!',
            value//5:'\nSucesso Extremo!'
        }

        for _result in result[0]:
            check = value_checks[value_checks >= _result].min()
            result[1] += (value_success[check])

    except IndexError:
        pass
    except ValueError:
        result = False
    finally:
        return result

@Edgar.event
async def on_message(message):
    if message.author.id == Edgar.user.id or not len(message.content): return

    if 'd' in message.content[1:4].lower():
        dice_data = get_results(message.content.split())

        if not dice_data: return

        msg = f"{message.author.mention} jogou {dice_data[2]} dado(s) de {dice_data[3]} lados\n{dice_data[0]} → {sum(dice_data[0])} {dice_data[1]}"

        await message.channel.send(msg)
    else: return

Edgar.run('NjQ1NDA3MDA4OTY2ODM2MjU0.XdCIRA.UEZVG5ktUWWFbRzx-JOOfSqCEWk')