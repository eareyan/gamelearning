from tests import test_games
from congestion import congestion_game_lib

# test_game = test_games.get_game3Players()
# test_game = congestion_game_lib.simpleCongestionGame2()
test_game = test_games.get_prisonersDilemma()

print(test_game)
l = test_game.get_pure_eps_nash(eps=0.5)

print("l = ", l)

ppoa = test_game.get_pure_price_of_anarchy()
print("ppoa = ", ppoa)
