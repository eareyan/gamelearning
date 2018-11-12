from prob import util_random
from algos import sampling, psp
import pandas as pd
import matplotlib.pyplot as plt

n, m = 4, 4
test_game = util_random.generate_random_game(n, m)
print(test_game)


delta = 0.1
initial_num_samples = 10

verbose = False
results_list = []
for eps in range(1, 20):
    for max_num_samples in [i * initial_num_samples * 10 for i in range(1, 15)]:
        print(eps, max_num_samples)

        x = sampling.progressive_sampling(test_game, eps=eps, delta=delta, initial_num_samples=initial_num_samples, max_num_samples=max_num_samples, verbose=verbose)
        y = psp.psp(test_game, eps=eps, delta=delta, initial_num_samples=initial_num_samples, max_num_samples=max_num_samples, verbose=verbose)

        results_list = results_list + [(eps, max_num_samples, 0 if x[0] is None else 1, 0 if y[0] is None else 1)]

results = pd.DataFrame(results_list, columns=['eps', 'max_num_samples', 'ps', 'psp'])

yes = results[results['ps'] == 1]
no = results[results['ps'] == 0]
plt.scatter(yes['max_num_samples'], yes['eps'], color='b')
plt.scatter(no['max_num_samples'], no['eps'], color='r')
plt.title('Performance of progressive sampling, ' + str(n) + ' by ' + str(m) + ' game')
plt.xlabel('max number of samples')
plt.ylabel(r'$\epsilon$')
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/ps_' + str(n) + '_x_' + str(m) + '_plot.png')


yes = results[results['psp'] == 1]
no = results[results['psp'] == 0]
plt.scatter(yes['max_num_samples'], yes['eps'], color='b')
plt.scatter(no['max_num_samples'], no['eps'], color='r')
plt.title('Performance of progressive sampling with pruning, ' + str(n) + ' by ' + str(m) + ' game')
plt.xlabel('max number of samples')
plt.ylabel(r'$\epsilon$')
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/psp_' + str(n) + '_x_' + str(m) + 'plot.png')
