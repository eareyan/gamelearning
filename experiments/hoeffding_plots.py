import matplotlib.pyplot as plt
import pandas as pd
import math


def compute_num_samples(eps_tol, delta_tol, size_of_game):
    return -1.0 * (math.log(1.0 - (1.0 - delta_tol) ** (1.0 / size_of_game)) / (2 * eps_tol * eps_tol))


# def compute_epsilon(sample_size, delta_tol, size_of_game):
#    return 2.0 * math.sqrt((math.log((2.0 * size_of_game) / delta_tol)) / (2.0 * sample_size))


def compute_epsilon(sample_size, delta_tol, size_of_game):
    return 2.0 * math.sqrt(-1.0 * math.log(1.0 - (1.0 - delta_tol) ** (1.0 / size_of_game)) / (2 * sample_size))


data = pd.read_csv('/Users/enriqueareyan/Documents/workspace/gamelearning/data/hoeffding/test.csv')

c_noise = 1
c_payoffs = 10

x = data[(data['c_noise'] == c_noise) & (data['c_payoffs'] == c_payoffs)]

# for N_gamma, d in x.groupby('N_gamma').sum().iterrows():
line_styles = ['-', '--', '-.', ':']
line_styles_iterator = iter(line_styles)
for N_gamma in [1024, 324, 24, 8]:
    # for N_a in [5, 4, 3, 2]:
    # Get psp data
    psp = x[(x['algo'] == 'psp') & (x['N_gamma'] == N_gamma)]
    # psp = x[(x['algo'] == 'psp') & (x['N_a'] == N_a) & (x['N_p'] == 3)]
    psp = psp.sort_values('eps')
    print(psp)
    # Get gs data
    # gs = x[(x['algo'] == 'gs') & (x['N_gamma'] == N_gamma)]
    # gs = x[(x['algo'] == 'gs') & (x['N_a'] == N_a) & (x['N_p'] == 3)]
    # gs = gs.sort_values('eps')
    # Plot in a log scale
    # plt.semilogy(gs['eps'], gs['m'], label='gs ' + str(N_gamma), color='g')
    # plt.semilogy(psp['eps'], psp['m'], label='psp' + str(N_gamma), color='r')
    # plt.semilogx(gs['m'], gs['eps'], label='gs ' + str(N_gamma), color='g')

    # Plot eps(m)
    next_line_style = next(line_styles_iterator)
    plt.semilogx(psp['m'], psp['eps'], label=r'$N_\Gamma$ = ' + str(N_gamma), color='r', linestyle=next_line_style)
    plt.semilogx(psp['m'], [compute_epsilon(t / N_gamma, 0.1, N_gamma) for t in psp['m']], label=r'$N_\Gamma$ = ' + str(N_gamma),
                 color='g', linestyle=next_line_style)
    plt.text(1500, 0.30, "Algorithm 1 (GS)", fontdict={#'family': 'serif',
                                                  'color': 'green',
                                                  'weight': 'normal',
                                                  'size': 12,
                                                  })
    plt.text(1500, 0.28, "Algorithm 2 (PSP)", fontdict={#'family': 'serif',
                                                  'color': 'red',
                                                  'weight': 'normal',
                                                  'size': 12,
                                                  })

    # Plot m(eps)
    # plt.semilogy(psp['eps'], psp['m'], label='psp ' + str(N_gamma), color='r')
    # plt.semilogy([compute_epsilon(t / N_gamma, 0.1, N_gamma) for t in psp['m']], psp['m'], label='gs ' + str(N_gamma), color='g')

    # plt.xlabel(r'$\epsilon$')
    # plt.ylabel('Number of samples')

plt.xlabel('Number of samples')
plt.ylabel(r'$\epsilon$')

plt.legend()
#plt.show()
plt.tight_layout()
plt.savefig('/Users/enriqueareyan/Documents/workspace/gamelearning/data/plots/GvPSP/GvPSP.png')
