from congestion.congestion_games import CongestionGame
from structures import brg

def simpleCongestionGame1():
    # An example of a concrete game. In this game, there is a unique pure nash.
    # facilities may have different cost functions
    m = 6
    # facilities_cost_functions = {0: lambda x: x, 1: lambda x: x, 2: lambda x: x,
    #                             3: lambda x: 2 * x, 4: lambda x: 2 * x, 5: lambda x: 2 * x}
    # With the following costs, there are two pure nash and the price of anarchy is 5/2.
    facilities_cost_functions = {0: lambda x: x, 1: lambda x: x, 2: lambda x: x,
                                 3: lambda x: x, 4: lambda x: x, 5: lambda x: x}
    # players strategies
    n = 3
    strats = {0: {0: set([0, 3]), 1: set([1, 5, 4])},
              1: {0: set([1, 4]), 1: set([2, 3, 5])},
              2: {0: set([2, 5]), 1: set([0, 3, 4])}}

    congestionGame1 = CongestionGame("A simple congestion game", n, m, strats, facilities_cost_functions)
    congestionGame1BRG = brg.BRG.get_true_brg(congestionGame1)
    list_of_pureNash_CongestionGame1 = brg.BRG.getListOfPureNash(congestionGame1, congestionGame1BRG)

    #print(congestionGame1)
    #print("There are " + str(len(list_of_pureNash_CongestionGame1)) + " pure Nash -> ", list_of_pureNash_CongestionGame1)

    # Create Welfare graph. For a given strategy profile, the welfare graph has payoffs equal to the sum for every players
    # payoff in the profile.
    return congestionGame1
