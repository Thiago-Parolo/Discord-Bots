from discord.ext import commands
import discord
from deception import Deception
from coup import Coup
from random import choice

class ArnitemCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.avaliable_games = {"872082299460669490": Coup, "870389428458242058": Deception}
        self.running_games = {}    

    @commands.command(name="start")
    async def _start(self, ctx):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            game = self.avaliable_games.get(str(ctx.channel.id), None)()

            if not game:
                await ctx.send("Esse não é um canal de jogos.")
                return

            await ctx.send(f"Começando uma nova partida de {game.name}!")
            self.running_games[str(ctx.channel.id)] = game

            await ctx.send(game.add_player(ctx.author))

            return

        if game.players[0] != ctx.author:
            await ctx.send(f"Já existe uma partida em espera! Somente {game.players[0].mention} pode começar o jogo!")
            return

        await ctx.send(await game.start())
        return

    @commands.command(name="join")
    async def _join(self, ctx):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")

            return

        await ctx.send(game.add_player(ctx.author))
        return

    @commands.command(name="leave")
    async def _leave(self, ctx):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")

            return

        await ctx.send(game.remove_player(ctx.author))
        return

    @commands.command(name="list")
    async def _list(self, ctx):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")

            return

        await ctx.send(game.list_players())
        return

    @commands.command(name="income", aliases=["pagamento", "extra", "taxa", "renda"])
    async def _rend(self, ctx, coins: int = 1):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")

            return

        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")

        for player in game._players:
            if player.user == ctx.author:
                player.add_points(coins)

                await ctx.send(f"A poupança de {ctx.author.mention} foi modificada")
                return

    @commands.command(name="balance", aliases=["carteira", "poupança", "banco"])
    async def _balance(self, ctx, target: discord.User = None):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")
            return
            
        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")

        if not target: target = ctx.author

        for player in game._players:
            if player.user == target:
                await ctx.channel.send(f"{player.user.mention} tem {player.points} moedas!")
                return

    @commands.command(name="cemitery", aliases=["cemiterio"])
    async def _cemitery(self, ctx):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")
            return
            
        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")

        await ctx.send(f"As cartas já reveladas são:\n{', '.join(game.cemitery)}")

    @commands.command(name="cards", aliases=["cartas"])
    async def _cards(self, ctx):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")
            return
            
        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")
        
        for player in game._players:
            if player.user == ctx.author:
                await ctx.author.send(f"As suas cartas são:\n{', '.join(player.cards)}")
                return

    @commands.command(name="coup", aliases=["golpe"])
    async def _coup(self, ctx, target: discord.User = None):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")
            return
            
        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")

        if not target:
            await ctx.send(f'Você precisa especificar um alvo para usar o assassino, {ctx.author.mention}.')
            return

        for player in game._players:
            if player.user == ctx.author:
                if player.points < 7:
                    await ctx.send(f"Você precisa de pelo menos 7 moedas para usar o assassino, {ctx.author.mention}")
                    return

                player.add_points(-7)
                break

        for player in game._players:
            if player.user == target:
                card = choice(player.cards)
                game.cemitery.append(card)
                player.remove_card(card)

                await target.send(f"Suas novas cartas são:\n{', '.join(player.cards)}")
                await ctx.send(f"{ctx.author.mention} deu um golpe e matou *{card}* de {target.mention}.")
                return

    @commands.command(name="kill", aliases=["assassinar", "assassino", "matar"])
    async def _kill(self, ctx, target: discord.User = None):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")
            return
            
        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")

        if not target:
            await ctx.send(f'Você precisa especificar um alvo para usar o assassino, {ctx.author.mention}.')
            return
        
        for player in game._players:
            if player.user == ctx.author:
                if player.points < 3:
                    await ctx.send(f"Você precisa de pelo menos 3 moedas para usar o assassino, {ctx.author.mention}")
                    return

                player.add_points(-3)
                break

        for player in game._players:
            if player.user == target:
                card = choice(player.cards)
                game.cemitery.append(card)
                player.remove_card(card)

                await target.send(f"Suas novas cartas são:\n{', '.join(player.cards)}")
                await ctx.send(f"{ctx.author.mention} usou o assassino para matar um *{card}* de {target.mention}.")
                return

    @commands.command(name="doubt", aliases=["duvidar", "duvido"])
    async def _doubt(self, ctx, target: discord.User = None, card: str = None):
        game = self.running_games.get(str(ctx.channel.id), None)

        if not game:
            await ctx.send("Não tem jogo rolando nesse canal! **!start** em um cana de jogo para iniciar uma partida.")
            return
            
        if not isinstance(game, Coup):
            await ctx.send("Esse não é um comando desse jogo! O canal correto para esse comando é o #coup!")

        if not target or not card:
            await ctx.send(f'Você precisa especificar um alvo e uma carta para duvidar, {ctx.author.mention}.')
            return

        for player in game._players:
            if player.user == ctx.author:
                player_author = player
            if player.user == target:
                player_target = player

        await ctx.send(f"{ctx.author.mention} duvidou que {target.mention} tinha *{card}*!")

        if card not in player_target.cards:
            target_card = choice(player_target.cards)
            player_target.remove_card(target_card)
            game.cemitery.append(target_card)

            await ctx.send(f"E acertou! {target.mention} perdeu um *{target_card}* por ser pego blefando!")
            await player_target.user.send(f"Suas novas cartas são:\n{', '.join(player_target.cards)}")
            return

        target_card = choice(player_author.cards)

        player_author.remove_card(target_card)
        game.cemitery.append(target_card)

        game.deck.append(card)
        new_card = game.deck[0]
        game.deck = game.deck[1:]
        player_target.remove_card(card)
        player_target.add_card(new_card)

        await ctx.send(f"E errou! {ctx.author.mention} perdeu um *{target_card}* por duvidar errado!")
        await player_target.user.send(f"Suas novas cartas são:\n{', '.join(player_target.cards)}")
        await player_author.user.send(f"Suas novas cartas são:\n{', '.join(player_author.cards)}")
        return



                