#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:34:48 2018

@author: eareyanv
    All operations related to constructing BRGs are here. 
    Graphs are all implemented using the networkx library.
"""
import networkx as nx
import matplotlib.pyplot as plt

class BRG:
    
    @staticmethod
    def get_true_brg(game_input, eps = 0):
        """ Just a wrapper function to get individual BRGs into a single multidigraph """
        return BRG.merge_directed_graphs(BRG.construct_all_true_individual_restricted_brgs(game_input, eps))
    
    @staticmethod
    def construct_all_true_individual_restricted_brgs(game_input, eps = 0):
        return {i : BRG.compute_true_restricted_brg_for_player(game_input, i, eps) for i in range(0, game_input.numPlayers)}
    
    @staticmethod
    def compute_true_restricted_brg_for_player(game_input, player_index, eps = 0):
        """ Given a player index, returns the best response graph restricted to that player. """
        player_zero_strats_with_player = game_input.get_zero_strategies(player_index)
        individual_restricted_BRG = nx.DiGraph()
        # For each strategy profile of other agents, where player_index play zero
        for s in player_zero_strats_with_player:
            # Compute the neighborhood of the strategy 0 for fixed strategy of other players
            list_neigh_strats_with_payoffs = [(strat, game_input.payoffs[strat]) for strat in game_input.get_neiborhood(s)]
            # Compute a strategy with maximal payoff
            max_strat = max(list_neigh_strats_with_payoffs, key = lambda e:e[1])
            # Partition the neiborhood into max and min, where max are all the profiles with maximal utility
            max_neigh = [strat_profile_player for (strat_profile_player, utility) in list_neigh_strats_with_payoffs if utility >= max_strat[1] - eps]
            min_neigh = [strat_profile_player for (strat_profile_player, utility) in list_neigh_strats_with_payoffs if utility <  max_strat[1] - eps]
            # Add directed egde between every pair of nodes in max_neigh
            individual_restricted_BRG.add_edges_from([(s1, s2) for s1 in max_neigh for s2 in max_neigh])
            # Add directed edge between every member of min_neigh and every member of max_neigh
            individual_restricted_BRG.add_edges_from([(m, M) for m in min_neigh for M in max_neigh])
        return individual_restricted_BRG
    
    @staticmethod
    def get_estimated_eps_brg(game_input, conf_util):
        """ Just a wrapper function to take individual restricted BRGs into a single multidigraph """
        return BRG.merge_directed_graphs(BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf_util))
    
    @staticmethod
    def construct_all_estimated_eps_individual_restricted_brgs(game_input, conf_util):
        """
            Given all the confidence intervals of the game, construct individual restricted BRGs
            where the restriction means only a single player is considered in each individual BRG.
            This function returns a dictionary {i : \hat{BRG}{\eps}_i}, where \hat{BRG}{\eps}_i
            is the estimated eps BRG restricted to i.
        """
        #if not(isinstance(game_input, Game)):
        #    raise Exception('To construct an individual, restricted BRG, a Game object must be given')
        #TODO: (refactor) feels a bit hacky at the moment. Given all the confidence interval, this function
        #is doing too much, it is both filtering samples and constructing the BRGs. Perhaps
        # a better design is to have one function that takes samples of all the profiles of a single
        # player and construct the restriction for that single player. Calling this new function for
        # each player would be equivalent to calling this function with ALL the samples for ALL players.
        # May 2, 2018. Now I think that is is fine. This functions takes ALL samples and constructs 
        # individual graphs, whereas the function for TRUE BRG does not have samples but TRUE payoffs. 
        # but it is still the case that the function could be refactor to avoid repeat work
        individual_restricted_brgs = {}
        for (strat_profile_player, conf) in conf_util.items():
            player = strat_profile_player[len(strat_profile_player) - 1]
            if not(player in individual_restricted_brgs):
                individual_restricted_brgs[player] = nx.DiGraph()
                individual_restricted_brgs[player].add_nodes_from([strat_profile_player 
                               for (strat_profile_player, conf) in conf_util.items() 
                               if strat_profile_player[len(strat_profile_player)-1] == player])
            neigh = game_input.get_neiborhood(strat_profile_player)
            conf_neigh = {s: conf_util[s] for s in neigh}        
            max_inter = max(conf_neigh.items(), key = lambda e:e[1][1])[1]
            max_neigh = [strat_profile_player for (strat_profile_player, conf) in conf_neigh.items() if conf[1] >= max_inter[0]]
            min_neigh = [strat_profile_player for (strat_profile_player, conf) in conf_neigh.items() if conf[1] <  max_inter[0]]
            # Add directed egde between every pair of nodes in max_neigh
            individual_restricted_brgs[player].add_edges_from([(s1, s2) for s1 in max_neigh for s2 in max_neigh])
            # Add directed edge between every member of min_neigh and every member of max_neigh
            individual_restricted_brgs[player].add_edges_from([(m, M) for m in min_neigh for M in max_neigh])
        return individual_restricted_brgs
    
    @staticmethod
    def merge_directed_graphs(list_of_restricted_brg):
        """ Given a dictionary: {player_index : restricted BRG}, construct the final best response graph. """
        BRG = nx.MultiDiGraph()
        for (player, restricted_BRG) in list_of_restricted_brg.items():
            for (u, v) in restricted_BRG.edges():
                BRG.add_edge(u[:-1], v[:-1], player = player)
        return BRG
        
    @staticmethod
    def isG1ContainedInG2(G1, G2):
        """ Given two graph, check if G1 \subseteq G2, in our context, chec if: 
            1) V_1 = V_2, and
            2) if (u,v) \in G1 then (u,v) \in G2."""
        return set(G1.nodes()).issubset(G2.nodes()) and set(G1.edges()).issubset(G2.edges())
    
    #TODO: if at all interesting, try to plot the BRG. Here is an example.
    @staticmethod
    def plot_graph(G):
        pos = nx.layout.spring_layout(G)
        node_sizes = [300 for i in range(len(G))]
        M = G.number_of_edges()
        edge_colors = range(2, M + 2)
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
        nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                                   arrowsize=10, edge_color=edge_colors,
                                   edge_cmap=plt.cm.Blues, width=2)
        nx.draw_networkx_labels(G,pos,{n:n for n in G.nodes()},font_size=16)
        ax = plt.gca()
        ax.set_axis_off()
        plt.show()        