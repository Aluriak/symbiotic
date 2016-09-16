

from symbiotic import utils


def test_similarity():
    assert utils.similarity('a', 'a') == 1
    assert utils.similarity('a', 'b') == 0
    assert utils.similarity('aa', 'ba') == 0.5
    assert utils.similarity('aa', 'ba') == 0.5


def test_reverted():
    graph = {1: {2, 3}, 3: {4, 1}}
    assert utils.reverted(graph)  == {1: {3}, 2: {1}, 3: {1}, 4: {3}}
    assert utils.reverted({}) == {}

def test_completed():
    graph = {1: {2, 3}, 3: {4, 1}}
    assert utils.completed(graph) == {1: {2, 3}, 2: {1}, 3: {1, 4}, 4: {3}}
    assert utils.completed({}) == {}

def test_all_nodes():
    graph = {1: {2, 3}, 3: {4, 1}}
    assert set(utils.all_nodes(graph)) == {1, 2, 3, 4}
