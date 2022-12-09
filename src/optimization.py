from simulate import simulation
from tournament import TournamentSystem 

def main():
    
    players = TournamentSystem(0).get_players()
    print(players)

    results = simulation()
    print(results)
    
if __name__ == "__main__":
    main()

