import pytest

import networkx as nx
from networkx.utils import pairwise


class TestGreedyPath:
    @classmethod
    def setup_class(cls):
        edges = [
            ("s", "u", 10),
            ("s", "x", 5),
            ("u", "v", 1),
            ("u", "x", 2),
            ("v", "y", 1),
            ("x", "u", 3),
            ("x", "v", 5),
            ("x", "y", 2),
            ("y", "s", 7),
            ("y", "v", 6),
        ]
        cls.XG = nx.DiGraph()
        cls.XG.add_weighted_edges_from(edges)

    def test_greedy1(self):
        assert nx.greedy_path(self.XG, "s", "v") == ["s", "x", "v"]

    def test_greedy2(self):
        XG2 = nx.DiGraph()
        edges = [
            (1, 4, 1),
            (4, 5, 1),
            (5, 6, 1),
            (6, 3, 1),
            (1, 3, 50),
            (1, 2, 100),
            (2, 3, 100),
        ]
        XG2.add_weighted_edges_from(edges)
        assert nx.greedy_path(XG2, 1, 3) == [1, 3]

    def test_greedy3(self):
        heuristic_values = {"n5": 36, "n2": 4, "n1": 0, "n0": 0}

        def h(u, v):
            return heuristic_values[u]

        edges = [("n5", "n1", 11), ("n5", "n2", 9), ("n2", "n1", 1), ("n1", "n0", 32)]
        graph = nx.DiGraph()
        graph.add_weighted_edges_from(edges)
        answer = ["n5", "n1", "n0"]
        assert nx.greedy_path(graph, "n5", "n0", h) == answer

    def test_greedy4(self):
        edges = [
            ("a", "b", 1),
            ("a", "c", 1),
            ("b", "d", 2),
            ("c", "d", 1),
            ("d", "e", 1),
        ]
        graph = nx.DiGraph()
        graph.add_weighted_edges_from(edges)
        assert nx.greedy_path(graph, "a", "e") == ["a", "c", "d", "e"]

    def test_greedy5(self):
        G = nx.DiGraph()
        G.add_edges_from(
            [
                ("s", "u"),
                ("s", "x"),
                ("u", "v"),
                ("u", "x"),
                ("v", "y"),
                ("x", "u"),
                ("x", "w"),
                ("w", "v"),
                ("x", "y"),
                ("y", "s"),
                ("y", "v"),
            ]
        )
        assert nx.greedy_path(G, "s", "v") == ["s", "u", "v"]

    def test_greedy_nopath(self):
        with pytest.raises(nx.NodeNotFound):
            nx.greedy_path(self.XG, "s", "moon")