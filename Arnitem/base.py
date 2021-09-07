class Game:
    def __init__(self):
        self.players = []

    def add_player(self, player):
        if (player in self.players):
            return f"Você já está no jogo, {player.mention}!"
        self.players.append(player)
        return f"{player.mention} entrou no jogo!"

    def remove_player(self, player):
        if (player in self.players):
            self.players.remove(player)
            return f"{player.mention} saiu do jogo!"
        return f"Você não está no jogo, {player.mention}."

    def list_players(self):
        return f"{len(self.players)} jogadores estão presentes! \n  {', '.join([player.mention for player in self.players])}"

class Player:
    def __init__(self, user):
        self.user = user
        self.cards = []
        self.role = None
        self.points = 0

    def add_points(self, amount):
        self.points += amount

    def set_role(self, new_role):
        self.role = new_role

    def add_card(self, card):
        self.cards.append(card)
    
    def remove_card(self, card):
        self.cards.remove(card)