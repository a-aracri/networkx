import networkx as nx
from itertools import count
from heapq import heappop, heappush
from networkx.algorithms.shortest_paths.weighted import _weight_function

__all__ = ['greedy_path']

def greedy_path(G, source, target, heuristic=None, weight="weight"):
    if (source not in G or target not in G):
        msg = f"Either source {source} or target {target} is not in G"
        raise nx.NodeNotFound(msg)

    push = heappush
    pop = heappop

    # Queue stores: priority (heuristic's value), counter, node, cost to reach 
    # and parent.
    c = count()
    queue = [(0, next(c), source, 0, None)]
    # Saving in enqueued cost to reach a node and the heuistic's value
    enqueued = {}
    # Savin visited nodes with parents
    explored = {}

    # Using weight if heuristic is None
    weight = _weight_function(G, weight)
    if heuristic is None:
        def heuristic(u,v):
            cost, _ = enqueued[u]
            return cost

    while queue:
        _, __, curnode, dist, parent = pop(queue)

        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path
        
        if curnode in explored:
            if explored[curnode] is None:
                continue
            # Skipping worst paths
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue
        
        explored[curnode] = parent

        for neighbor, w in G[curnode].items():
            ncost = dist + weight(curnode, neighbor, w)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                
                if qcost <= ncost:
                    continue
            else:
                # Setting costs in case heuristic is None
                enqueued[neighbor] = ncost, ncost
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (h, next(c), neighbor, ncost, curnode))
    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")