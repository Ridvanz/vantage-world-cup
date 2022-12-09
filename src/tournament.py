from utils import load_jsons
from entities import Player
from scene import PenaltyScene

class TournamentSystem():
    def __init__(self, sm):
        self.players = []
        self.sm = sm
        self.winners = []
        self.loser = []

    def get_players(self):
        
        player_dicts = load_jsons()
        
        for player_dict in player_dicts:
            
            player = Player()
            player.set_attributes(player_dict)
        
            self.players.append(player)
    
            
    def play_tournement(self):
        
        while len(self.players) > 1:
            P1 = self.players.pop()
            P2 = self.players.pop()
            
            self.play_match(P1, P2)
    
        pass
        

    def play_match(self, P1, P2):
        
        scene = PenaltyScene(P1, P2, 0)
        self.sm.push(scene)