from random import shuffle, choice
import os, os.path
from base import Game, Player

class Deception(Game):
    def __init__(self):
        super().__init__()
        self.name = "Deception"
        self._players = []

    async def start(self):
        self._players = [Player(player) for player in self.players]
        shuffle(self._players)

        try:
            await self._players[0].user.send(f"""Você é o **Cientista Forense!** Use as pistas para auxiliar os detetives na resolução do caso!
    *Assassino:* {self._players[1].user.mention}
    *Cumplice:* {self._players[2].user.mention}
    *Testemunha:* {self._players[3].user.mention}""")

            await self._players[1].user.send(f"""Você é o **Assassino!** Escolha uma pista e uma evidência para cometer um assassinato!
    *Cumplice:* {self._players[2].user.mention}""")

            await self._players[2].user.send(f"""Você é o **Cumplice!** Descubra quem é a testemunha e live a barra do assassino!
    *Assassino:* {self._players[1].user.mention}""")

            await self._players[3].user.send(f"""Você é a **Testemunha!** Guie os outros detetives sem ser desoberto!
    *Assassino:* {self._players[1].user.mention}""")

            for player in self._players[4:]:
                await player.user.send("Você é um **Detetive!** Descubra quem é o assassino usando as pistas dadas pelo *Cientista Forense!*")
        except: pass

        self._players.pop(0)
        shuffle(self._players)

        cards = [[], []]
        evidence_path = "c:/Users/User/Desktop/tigo/codingkk/Python/Bots/Arnitem/deception/evidence/"
        weapons_path = "c:/Users/User/Desktop/tigo/codingkk/Python/Bots/Arnitem/deception/weapons/"

        evidence = [name for name in os.listdir(evidence_path) if os.path.isfile(os.path.join(evidence_path, name))]
        weapon = [name for name in os.listdir(weapons_path) if os.path.isfile(os.path.join(weapons_path, name))]
        
        message = "Iniciando jogo!"
        for player in self._players[1:]:
            player_index = self._players.index(player)
            while len(cards[0]) < player_index * 4:
                random_evidence = choice(range(len(evidence)))
                if random_evidence not in cards[0]:
                    player.add_card(evidence[random_evidence])
                    cards[0].append(random_evidence)

            while len(cards[1]) < player_index * 4:
                random_weapon = choice(range(len(weapon)))
                if random_weapon not in cards[0]:
                    player.add_card(weapon[random_weapon])
                    cards[1].append(random_weapon)

            message += f"""\nCartas do {player.user.mention}:
    Evidências:
        {', '.join([evidence[:-4] for evidence in player.cards[:4]])}
    Armas:
        {', '.join([weapon[:-4] for weapon in player.cards[4:]])}"""

        return message