import discord, asyncio
import sqlite3 as sql
from discord.ext import commands

class EdgarCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.acoes = dict()         

    @commands.command()
    async def ficha(self, ctx, personagem = "", *, atributos = ""):
        def author_check(msg):
            return msg.author == ctx.author
        
        def action_check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == "\u2795" or str(reaction.emoji) == "\u2796")

        sheet_data = sql.connect(f"RPG/f{ctx.guild.id}.db")
        sheet = sheet_data.cursor()
        sheet.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        fichas = [ficha[0].capitalize() for ficha in sheet.fetchall()]

        ListSheets = True
        if personagem.capitalize() in fichas:
            if atributos:
                atr_lst = [(atr[:atr.find(' ')], atr[atr.find(' ')+1:]) for atr in atributos.split(', ') if atr.find(' ') != -1]
                for atr_val in atr_lst:
                    sheet.execute(f"UPDATE {personagem.lower()} SET valor=:valor WHERE atributo=:atributo",
                                 {"atributo":atr_val[0].upper(), "valor":atr_val[1].capitalize()})

            sheet.execute(f"SELECT * FROM {personagem.lower()}")
            msg_content = "\n".join(
                f"**{atributo[0]}:** {atributo[1]}" for atributo in sheet.fetchall())
            sheet_data.commit()
            ListSheets = False
        
        else: msg_content = "Fichas disponiveis:\n" + ', '.join(fichas) + "\nUsagem: !ficha `personagem`"

        msg = await ctx.send(msg_content)
        await msg.add_reaction("\u2795")
        await msg.add_reaction("\u2796")

        try:
            if ctx.author in self.acoes:
                self.acoes[ctx.author].close()
            self.acoes[ctx.author] = self.bot.wait_for("reaction_add", timeout = 10, check = action_check)
            reaction, user = await self.acoes[ctx.author]
        except asyncio.TimeoutError:
            await msg.remove_reaction("\u2795", self.bot.user)
            await msg.remove_reaction("\u2796", self.bot.user)
            return

        if reaction.emoji == "\u2795" and not ListSheets:
            msg = await ctx.send("Adicionar atributos:\nInsira o nome dos atributos (separado por \" \"):")

            try: atributos = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            atr_lst = atributos.content.split(' ')

            for atributo in atr_lst:
                sheet.execute(f"INSERT INTO {personagem.lower()} VALUES (:atributo, '-')",
                             {"atributo":atributo.upper()})
            await ctx.send(f"Adicionado os atributos: {', '.join(atr_lst)} à ficha de: {personagem.capitalize()}")

        elif reaction.emoji == "\u2796" and not ListSheets:
            await ctx.send("Remover atributos:\nInsira o nome dos atributos (separado por \" \"):")

            try: atributos = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            atr_lst = atributos.content.split(' ')

            for atributo in atr_lst:
                sheet.execute(f"DELETE FROM {personagem.lower()} WHERE atributo=:atributo",
                             {"atributo":atributo.upper()})
            await ctx.send(f"Removido o atributo: {', '.join(atr_lst)} da ficha de: {personagem.capitalize()}")

        elif reaction.emoji == "\u2795" and ListSheets:
            msg = await ctx.send("Adicionar nova ficha:\nInsira o nome do personagem:")

            try: personagem = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            sheet.execute(f"""CREATE TABLE {personagem.content.lower()}(
                          atributo text NOT NULL,
                          valor text NOT NULL)""")
            sheet.execute(f"INSERT INTO {personagem.content.lower()} VALUES ('NOME', :nome)",
                         {"nome":personagem.content.capitalize()})

            await ctx.send(f"Adicionada a ficha de {personagem.content.capitalize()}")

        elif reaction.emoji == "\u2796" and ListSheets:
            msg = await ctx.send("Remover ficha:\nInsira o nome do personagem:")

            try: personagem = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            if personagem.content.capitalize() not in fichas: return await ctx.send("Ficha indisponivel")

            sheet.execute(f"DROP TABLE {personagem.content.lower()}")
        
            await ctx.send(f"Removida a ficha de {personagem.content.capitalize()}")
        sheet_data.commit()

    @commands.command()
    async def mochila(self, ctx, personagem = "", *, itens = ""):
        def author_check(msg):
            return msg.author == ctx.author

        def action_check(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == "\u2795" or str(reaction.emoji) == "\u2796")
        
        inv_data = sql.connect(f"RPG/i{ctx.guild.id}.db")
        inv = inv_data.cursor()
        inv.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        mochilas = [mochila[0].capitalize() for mochila in inv.fetchall()]

        ListBags = True
        if personagem.capitalize() in mochilas:
            if itens:
                item_lst = [(item[:item.rfind(' ')], item[item.rfind(' ')+1:]) for item in itens.split(', ') if item.find(' ') != -1]
                for item_quan in item_lst:
                    inv.execute(f"UPDATE {personagem.lower()} SET quantidade=:quantidade WHERE item=:item",
                                {"item":item_quan[0].upper(), "quantidade":item_quan[1].upper()})
            
            inv.execute(f"SELECT * FROM {personagem.lower()}")
            msg_content = "**ITEM | QUANTIDADE**\n" + "\n".join(
                f"{item[0]} | {item[1]}" for item in inv.fetchall())
            inv_data.commit()                
            ListBags = False
        
        else: msg_content = "Mochilas disponiveis:\n" + ', '.join(mochilas) + "\nUsagem: !mochila `personagem`"

        msg = await ctx.send(msg_content)
        await msg.add_reaction("\u2795")
        await msg.add_reaction("\u2796")

        try:
            if ctx.author in self.acoes:
                self.acoes[ctx.author].close()
            self.acoes[ctx.author] = self.bot.wait_for("reaction_add", timeout = 10, check = action_check)
            reaction, user = await self.acoes[ctx.author]
        except asyncio.TimeoutError:
            await msg.remove_reaction("\u2795", self.bot.user)
            await msg.remove_reaction("\u2796", self.bot.user)
            return

        if reaction.emoji == "\u2795" and not ListBags:
            msg = await ctx.send("Adicionar itens:\nInsira o nome dos itens (separado por \", \"):")

            try: itens = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            item_lst = itens.content.split(", ")

            for item in item_lst:
                inv.execute(f"INSERT INTO {personagem.lower()} VALUES (:item, '1')",
                            {'item':item.upper()})
            await ctx.send(f"Adicionado os items: {', '.join(item_lst)} à mochila de {personagem.capitalize()}")

        elif reaction.emoji == "\u2796" and not ListBags:
            msg = await ctx.send("Remover itens:\nInsira o nome dos itens (separado por \", \"):")

            try: itens = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            item_lst = itens.content.split(", ")

            for item in item_lst:
                inv.execute(f"DELETE FROM {personagem.lower()} WHERE item=:item",
                            {'item':item.upper()})
            await ctx.send(f"Removido os items: {', '.join(item_lst)} da mochila de {personagem.capitalize()}")

        elif reaction.emoji == "\u2795" and ListBags:
            msg = await ctx.send("Adicionar mochila:\nInsira o nome do personagem:")

            try: personagem = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            inv.execute(f"""CREATE TABLE {personagem.content.lower()}(
                          item text NOT NULL,
                          quantidade text NOT NULL)""")

            await ctx.send(f"Adicionada a mochila de {personagem.content.capitalize()}")

        elif reaction.emoji == "\u2796" and ListBags:
            msg = await ctx.send("Remover mochila:\nInsira o nome do personagem:")

            try: personagem = await self.bot.wait_for("message", timeout = 20, check = author_check)
            except asyncio.TimeoutError: return await msg.edit(content="Operação cancelada.")

            if personagem.content.capitalize() not in mochilas: return await ctx.send("Mochila indisponivel")

            inv.execute(f"DROP TABLE {personagem.content.lower()}")
        
            await ctx.send(f"Removida a mochila de {personagem.content.capitalize()}")

        inv_data.commit()

    @commands.command()
    async def o(self, ctx):
        await ctx.send(GetPledge("https://www.catarse.me/ordem"))