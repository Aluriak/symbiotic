"""Various pure functions"""


import itertools
from functools import lru_cache
from collections import defaultdict


try:
    import Levenshtein
except ImportError as e:  # no levenstein module: use the handmade one
    print('ImportError:', e)
    print("The python-Levenshtein module is not installed. An handmade"
          " implementation will be used, but you should expect the name"
          " comparison to be slower.\n\n")
    class Levenshtein:
        @staticmethod
        def distance(a, b):
            return handmade_levenstein(a, b, len(a), len(b))


def similarity(a, b):
    """Return a similarity score in [0;1]"""
    distance = Levenshtein.distance(a, b)
    return 1 - (distance / max((len(a), len(b))))


@lru_cache()  # consequent speed up (almost like Levenshtein module)
def handmade_levenstein(a, b, i, j):
    if min((i, j)) == 0:
        return max((i, j))
    return min((
        handmade_levenstein(a, b, i=i-1, j=j) + 1,
        handmade_levenstein(a, b, i=i, j=j-1) + 1,
        handmade_levenstein(a, b, i=i-1, j=j-1) + (0 if a[i-1] == b[j-1] else 1),
    ))


def completed(graph):
    ret = defaultdict(set)
    for pred, succs in graph.items():
        ret[pred] |= set(succs)
        for succ in succs:
            ret[succ].add(pred)
    return dict(ret)


def reverted(graph):
    ret = defaultdict(set)
    for pred, succs in graph.items():
        for succ in succs:
            ret[succ].add(pred)
    return dict(ret)


def all_nodes(graph):
    yield from itertools.chain(
        itertools.chain.from_iterable(graph.values()),
        graph.keys()
    )
