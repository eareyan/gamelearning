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
from structures import game


class BRG:

    @staticmethod
    def get_true_brg(game_input: game, eps: float = 0) -> nx.MultiDiGraph:
        """ Just a wrapper function to get individual BRGs into a single multidigraph """
        return BRG.merge_directed_graphs(BRG.construct_all_true_individual_restricted_brgs(game_input, eps))

    @staticmethod
    def construct_all_true_individual_restricted_brgs(game_input: game, eps: float = 0) -> dict:
        return {i: BRG.compute_true_restricted_brg_for_player(game_input, i, eps) for i in
                range(0, game_input.numPlayers)}

    @staticmethod
    def compute_true_restricted_brg_for_player(game_input: game, player_index: int, eps: float = 0) -> nx.DiGraph:
        """ Given a player index, returns the best response graph restricted to that player. """
        player_zero_strats_with_player = game_input.get_zero_strategies(player_index)
        individual_restricted_BRG = nx.DiGraph()
        # For each strategy profile of other agents, where player_index play zero
        for s in player_zero_strats_with_player:
            # Compute the neighborhood of the strategy 0 for fixed strategy of other players
            list_neigh_strats_with_payoffs = [(strat, game_input.payoffs[strat]) for strat in
                                              game_input.get_neighborhood(s)]
            # Compute a strategy with maximal payoff
            max_strat = max(list_neigh_strats_with_payoffs, key=lambda e: e[1])
            # Partition the neiborhood into max and min, where max are all the profiles with maximal utility
            max_neigh = [strat_profile_player for (strat_profile_player, utility) in list_neigh_strats_with_payoffs if
                         utility >= max_strat[1] - eps]
            min_neigh = [strat_profile_player for (strat_profile_player, utility) in list_neigh_strats_with_payoffs if
                         utility < max_strat[1] - eps]
            # Add directed egde between every pair of nodes in max_neigh
            individual_restricted_BRG.add_edges_from([(s1, s2) for s1 in max_neigh for s2 in max_neigh])
            # Add directed edge between every member of min_neigh and every member of max_neigh
            individual_restricted_BRG.add_edges_from([(m, M) for m in min_neigh for M in max_neigh])
        return individual_restricted_BRG

    @staticmethod
    def get_estimated_eps_brg(game_input: game, conf_util: dict) -> nx.MultiDiGraph:
        """ Just a wrapper function to take individual restricted BRGs into a single multidigraph """
        return BRG.merge_directed_graphs(
            BRG.construct_all_estimated_eps_individual_restricted_brgs(game_input, conf_util))

    @staticmethod
    def construct_all_estimated_eps_individual_restricted_brgs(game_input: game, conf_util: dict) -> dict:
        """
            Given all the confidence intervals of the game, construct individual restricted BRGs
            where the restriction means only a single player is considered in each individual BRG.
            This function returns a dictionary {i : \hat{BRG}{\eps}_i}, where \hat{BRG}{\eps}_i
            is the estimated eps BRG restricted to i.
        """
        individual_restricted_brgs = {}
        for (strat_profile_player, conf) in conf_util.items():
            player = strat_profile_player[len(strat_profile_player) - 1]
            if not (player in individual_restricted_brgs):
                individual_restricted_brgs[player] = nx.DiGraph()
                individual_restricted_brgs[player].add_nodes_from([strat_profile_player
                                                                   for (strat_profile_player, conf) in conf_util.items()
                                                                   if strat_profile_player[
                                                                       len(strat_profile_player) - 1] == player])
            (max_neigh, min_neigh) = BRG.compute_max_min_neigh(game_input, strat_profile_player, conf_util)
            # Add directed egde between every pair of nodes in max_neigh
            individual_restricted_brgs[player].add_edges_from([(s1, s2) for s1 in max_neigh for s2 in max_neigh])
            # Add directed edge between every member of min_neigh and every member of max_neigh
            individual_restricted_brgs[player].add_edges_from([(m, M) for m in min_neigh for M in max_neigh])
        return individual_restricted_brgs

    @staticmethod
    def compute_max_min_neigh(game_input: game, strat_profile_player: tuple, conf_util: dict) -> tuple:
        neigh = game_input.get_neighborhood(strat_profile_player)
        conf_neigh = {s: conf_util[s] for s in neigh}
        max_inter = max(conf_neigh.items(), key=lambda e: e[1][0])[1]
        max_neigh = [strat_profile_player for (strat_profile_player, conf) in conf_neigh.items() if
                     conf[1] >= max_inter[0]]
        min_neigh = [strat_profile_player for (strat_profile_player, conf) in conf_neigh.items() if
                     conf[1] < max_inter[0]]
        return (max_neigh, min_neigh)

    @staticmethod
    def merge_directed_graphs(dict_of_restricted_brg: dict) -> nx.MultiDiGraph:
        """ Given a dictionary: {player_index : restricted BRG}, construct the final best response graph. """
        the_brg = nx.MultiDiGraph()
        for player, restricted_BRG in dict_of_restricted_brg.items():
            for (u, v) in restricted_BRG.edges():
                the_brg.add_edge(u[:-1], v[:-1], player=player)
        return the_brg

    @staticmethod
    def isG1ContainedInG2(G1: nx.MultiDiGraph, G2: nx.MultiDiGraph) -> bool:
        """ Given two graph, check if G1 \subseteq G2, in our context, chec if: 
            1) V_1 = V_2, and
            2) if (u,v) \in G1 then (u,v) \in G2."""
        return set(G1.nodes()).issubset(G2.nodes()) and set(G1.edges()).issubset(G2.edges())

    @staticmethod
    def getListOfPureNash(game_input: game, G: nx.MultiDiGraph) -> list:
        """Given a BRG, return a list with all the nodes that are pure Nash"""
        pure_nash = []
        for n in G.nodes():
            edges_data = G.get_edge_data(n, n)
            # Warning: we currently rely on the fact that the dictionary of data of edges contains EXACTLY
            # as many data as number of players to conclude that a node is a Nash.
            pure_nash = pure_nash + [n] if edges_data is not None and len(edges_data) == game_input.numPlayers \
                else pure_nash
        return pure_nash

    @staticmethod
    def brg_containment_checker(game_input: game, dict_individual_brgs_1: dict, dict_individual_brgs_2: dict):
        """ Given a game and two dictionaries of individual BRGS, check if the first BRG is contained in the second. """
        # For each player, check if the first brg is contained in the second.
        for i in range(0, game_input.numPlayers):
            if not (BRG.isG1ContainedInG2(dict_individual_brgs_1[i], dict_individual_brgs_2[i])):
                return False
        return True

    # TODO: if at all interesting, try to plot the BRG. Here is an example.
    @staticmethod
    def plot_graph(G: nx.MultiDiGraph) -> None:
        pos = nx.layout.spring_layout(G)
        node_sizes = [300 for i in range(len(G))]
        M = G.number_of_edges()
        edge_colors = range(2, M + 2)
        nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
        nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                               arrowsize=10, edge_color=edge_colors,
                               edge_cmap=plt.cm.Blues, width=2)
        nx.draw_networkx_labels(G, pos, {n: n for n in G.nodes()}, font_size=16)
        ax = plt.gca()
        ax.set_axis_off()
        plt.show()
