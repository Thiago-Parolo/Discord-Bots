from base import Game, Player
from random import shuffle, choice

class Coup(Game):
    def __init__(self):
        super().__init__()
        self.name = "Coup"
        self.deck = []
        self.cemitery = []
        self._players = []

    async def start(self):
        if len(self.players) < 6:
            self.deck = ["duque", "capitão", "assassino", "condessa"] * 3 #"embaixador"
        elif len(self.players) < 8:
            self.deck = ["duque", "capitão", "assassino", "condessa"] * 4
        else:
            self.deck = ["duque", "capitão", "assassino", "condessa"] * 5
        shuffle(self.deck)
        print(self.deck, len(self.deck))
        for player in self.players:
            cards = self.deck[:2]
            self.deck = self.deck[2:]

            _player = Player(player)
            _player.cards = cards
            self._players.append(_player)
            await player.send(f"As suas cartas são:\n{', '.join(cards)}")

        return f"As cartas foram distribuidas! {choice(self.players).mention} começa o jogo!."