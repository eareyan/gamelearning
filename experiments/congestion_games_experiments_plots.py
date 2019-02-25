import matplotlib.pyplot as plt
import pandas as pd

""" Save a couple of plots.
def getPlotTitle(title, numer_of_trials, congestionGame, list_of_pureNash):
    return "Random Power Law Game. \n" + str(title) \
           + str(numer_of_trials) + " trials." + "\n Players = " + str(congestionGame.numPlayers) + ", Facilities = " \
           + str(congestionGame.numFacilities) + ". Number of pure Nash: " + str(len(list_of_pureNash)) + "."
"""

expt_id = 'I7ISX8'

data_eps = pd.read_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/epsilon/' + expt_id + '.csv')

print(data_eps)

colors = ['g', 'b', 'r', 'y', 'o']
plt.rc('font', size=12)

my_colors = iter(colors)
for noise, noise_data in data_eps.groupby('noise').sum().iterrows():
    which_color = next(my_colors)
    print(noise, which_color)
    slice_of_data = data_eps[data_eps['noise'] == noise]
    # Average epsilon plot
    plt.fill_between(slice_of_data['num_samples'], slice_of_data['eps_upper'], slice_of_data['eps_lower'], color=which_color, alpha=.5)
    plt.plot(slice_of_data['num_samples'], slice_of_data['eps_mean'], color=which_color, linestyle='--', label=r'$c = ' + str(noise) + '$')
# plt.title(getPlotTitle("Avg. # epsilon value as a function of # of samples, ", numer_of_trials, congestionGame, list_of_pureNash))
plt.title('(a) 95% confidence intervals around ' + r'$\epsilon$.')
plt.xlabel("Number of samples")
plt.ylabel("Average epsilon")
plt.legend()
plt.tight_layout()
plt.show()
# plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/plots/epsilon/' + expt_id + '.png')

"""
plt.clf()

my_colors = iter(colors)
for noise, noise_data in data_eps.groupby('noise').sum().iterrows():
    which_color = next(my_colors)
    print(noise, which_color)
    slice_of_data = data_eps[data_eps['noise'] == noise]
    # Average number of nash plot
    plt.fill_between(slice_of_data['num_samples'], slice_of_data['num_nash_upper'], slice_of_data['num_nash_lower'], color=which_color, alpha=.5)
    plt.plot(slice_of_data['num_samples'], slice_of_data['num_nash_mean'], color=which_color, linestyle='--',  label=r'$c = ' + str(noise) + '$')
    #plt.title(getPlotTitle("Avg. # of pure Nash equilibria as a function of # of samples, ", numer_of_trials, congestionGame, list_of_pureNash))
    plt.xlabel("Number of samples")
    plt.ylabel("Average number of Pure Nash equilibria")
    plt.legend()
    # Need to change this next line by hand!
    plt.axhline(1)
    plt.tight_layout()
    plt.show()
    #plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/plots/epsilon/' + expt_id + '_num_nash_plot.png')

plt.clf()


data_nash = pd.read_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/csv/epsilon/' + expt_id + '-nash.csv')

print(data_nash)

which_num_samples = [50, 150, 250, 500]
which_num_samples = iter(which_num_samples)
fig, axs = plt.subplots(2, 2)
for i, ax in enumerate(fig.axes):
    # ax.set_ylabel(str(i))
    # Histogram of nash frequencies
    # for num_samples, data in data_nash.groupby('num_samples').sum().iterrows():
    # df = pd.DataFrame({'Nash': [k for k in map_of_nash.keys()], 'Freq': [v for v in map_of_nash.values()]})
    # df = df.sort_values('Freq', ascending=False)
    num_samples = next(which_num_samples)
    print("num_samples = ", num_samples)
    df = data_nash[(data_nash['num_samples'] == num_samples) & (data_nash['noise'] == 2)]
    print(df)
    df = df.sort_values('count', ascending=False)
    df.plot.bar(x='strategy', y='count', rot=75, legend=None, ax=ax)
    ax.set_xlabel(str(num_samples) + ' samples')
    # ax.set_xlabel('')
    ax.set_xticklabels(())
    # ax.invert_yaxis()
    ax.invert_xaxis()

# plt.tight_layout()
plt.suptitle('(b) Frequency of pure ' + r'$2\epsilon$' + '-Nash equilibria')
# axs.xlabel("Strategy Profile")
# plt.ylabel("Frequency as a sampled Nash")
# plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/plots/epsilon/' + expt_id + '_freq_nash_plot.png')
plt.show()
plt.clf()
"""
