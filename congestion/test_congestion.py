from congestion.congestion_games_factory import CongestionGamesFactory

m = 3
n = 5
cost_functions = {j: lambda x: x for j in range(0, m)}
ub_num_strats = 6

i = 0
while True:
    congestion_game = CongestionGamesFactory.get_random_congestion_game(n, m, cost_functions, ub_num_strats)
    if len(congestion_game.get_pure_eps_nash()) > 1 and congestion_game.get_pure_price_of_anarchy()[0] < 0.51:
        # if congestion_game.get_pure_price_of_anarchy()[0] < 0.7:
        break
    else:
        if i % 100 == 0:
            print("Attempt #: ", i)
        i += 1
print("\nlist of pn = ", congestion_game.get_pure_eps_nash())
for pn in congestion_game.get_pure_eps_nash():
    print(pn, congestion_game.get_sum_of_payoffs(pn))
print("ppoa = ", congestion_game.get_pure_price_of_anarchy())
dir = '/Users/enriqueareyan/Documents/workspace/gamelearning/data/pure_poa/'
congestion_game.save_game(dir + 'congestion_game.p')
