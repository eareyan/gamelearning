from structures.game import Game
import itertools


class GameFactory:

    @staticmethod
    def getWelfareGame(input_game: Game) -> Game:
        strategy_space = [tuple(strats) for strats in itertools.product(
            *[[a for a in range(0, input_game.listOfPlayers[j].numActions)] for j in range(0, input_game.numPlayers)])]
        welfare_payoffs = {}
        for s in strategy_space:
            total = 0
            for p in range(0, input_game.numPlayers):
                total += input_game.payoffs[s + (p,)]
            for p in range(0, input_game.numPlayers):
                welfare_payoffs[s + (p,)] = total
        return Game("Welfare game of " + input_game.name, input_game.listOfPlayers, welfare_payoffs)


"""from tests import test_games

game = test_games.get_prisonersDilemma()
# game = test_games.get_game3Players()
# game = test_games.get_testGame()
# game = test_games.get_game2Players()

from congestion.congestion_game_lib import congestionGame1

game = congestionGame1
print("*", GameFactory.getWelfareGame(game))"""
