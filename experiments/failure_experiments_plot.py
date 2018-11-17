import pandas as pd
import matplotlib.pyplot as plt

expt_id = 'JSO81S'
expt_data = pd.read_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/' + expt_id + '.csv')

g = expt_data.groupby(['noise', 'delta', 'discount']).mean().reset_index()
colors = ['g', 'b', 'r', 'y', 'k']
my_colors = iter(colors)
for discount in [1.0, 0.875, 0.75, 0.625, 0.5]:
    the_color = next(my_colors)
    data = g[(g['discount'] == discount) & (g['noise'] == 5)]
    print(data)
    plt.fill_between(data['delta'], data['upper'], data['lower'], color=the_color, alpha=.5)
    plt.plot(data['delta'], data['mean'], color=the_color, linestyle='--', label=r'$\rho =  $' + str(discount))

plt.ylim(0.5, 1.05)
plt.xlim(0.02, 0.2)
plt.plot([0, 0.2], [1, 0.8], 'k-')
plt.xlabel(r'$\delta$')
plt.ylabel("Average failure rate")
plt.tight_layout()
plt.legend()
plt.show()
plt.clf()

"""
colors = ['g', 'b', 'r', 'y', 'o']
n = 0
num_samples = 200
for i, r in expt_data.groupby('noise').sum().iterrows():
    data = expt_data[expt_data['noise'] == i]
    plt.fill_between(data['delta'], data['upper'], data['lower'], color=colors[n], alpha=.5)
    plt.plot(data['delta'], data['mean'], color=colors[n], linestyle='--', label=r'$c =  $' + str(i))
    #plt.title('Empirical failure probability as a function of ' + r'$\delta$' + '\n using ' + str(num_samples) + ' samples per run of simple algorithm')
    plt.xlabel(r'$\delta$')
    plt.ylabel("Empirical failure")
    plt.plot([0, 0.5], [1, 0.5], 'k-')
    plt.tight_layout()
    plt.legend()
    plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/prob_failure/' + expt_id + '_plot.png')
    n += 1
plt.show()
"""
