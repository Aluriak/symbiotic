"""API for localization of agents"""


import itertools

from symbiotic.data import Data
from symbiotic import utils


MAX_FOUND = 3
MIN_SIMILARITY = 0.5


def roomates_of(agent, graph, agents_at):
    """Return roomates of given agent that are next.

    agent -- an Agent instance
    graph -- {room: next rooms}
    agents_at -- {room: agents in room}

    """
    if agent.room:
        yield from (roomate for roomate in agents_at[agent.room]
                    if roomate != agent)


def neighbors_of(agent, graph, agents_at):
    """Yield iterable of neighbor agents in the same room.

    agent -- an Agent instance
    graph -- {room: next rooms}
    agents_at -- {room: agents in room}
    return -- {room: agents} for each neighboring room

    """
    ret = {}
    if agent.room:
        assert agent.room in graph, "agent {} have no room assigned".format(agent.name)
        for next_room in graph[agent.room]:
            if next_room in agents_at:
                ret[next_room] = agents_at[next_room]
    return ret


def from_name(firstname, lastname, type='human', *, show_close_agents=True,
              show_roomates=True):
    """Return useful informations about given agent of given type

    show_close_agents -- print some of close agents in stdout
    show_roomates -- print agents in the same room

    """
    payload = Data.from_file()
    min_simil = payload.locate_options['min_similarity']
    max_found = payload.locate_options['max_found']
    graph = payload.graph
    agents = payload.get_agents(type)
    agents_at = utils.reverted({  # room name: agents
        agent: {agent.room} for agent in payload.agents if agent.room
    })
    # add empty rooms
    for room in payload.rooms:
        if room.name not in agents_at:
            agents_at[room.name] = ()
    # printed value
    output = []

    # get all possible agents
    candidates = valid_agents(firstname, lastname, agents,
                              min_sim=min_simil, max_found=max_found)
    if len(candidates) == 0:  # if nothing found, retry without similarity limit
        candidates = valid_agents(firstname, lastname, agents,
                                  min_sim=0, max_found=max_found)

    for candidate in candidates:
        output.append(str(candidate))

        if candidate.is_room:
            if show_close_agents and graph.get(candidate.name, ()):
                output.append('\tÀ côté de {}'.format(
                    ', '.join(graph[candidate.name])
                ))
            if show_roomates and agents_at.get(candidate.name, ()):
                output.append('\tHéberge {}'.format(
                    ', '.join(a.name for a in agents_at[candidate.name])
                ))
            output.append('')  # line break
            continue
        # Indicate roomates
        if show_roomates and candidate.room:
            roomates = frozenset(roomates_of(candidate, graph, agents_at))
            if roomates:
                output.append('\tRoomates: {}'.format(
                    ', '.join(roomate.name for roomate in roomates)
                ))
        # Indicate next agents
        if show_close_agents and candidate.room:
            neighbors_per_room = neighbors_of(candidate, graph, agents_at)
            for next_room, neighbors in neighbors_per_room.items():
                inhabitants = ', '.join(neighbor.name for neighbor in neighbors)
                output.append('\tÀ côté de la salle {}'.format(next_room) +
                              ('({})'.format(inhabitants) if inhabitants else '')
                )
        output.append('')  # line break
    print('\n'.join(output))


def valid_agents(firstname, lastname, agents, *, max_found=MAX_FOUND,
                 min_sim=MIN_SIMILARITY):
    """Subset of valid_names that match or are close to given name.

    firstname -- string, the firstname of searched agent.
    lastname -- string, the lastname of searched agent.
    agents -- iterable of existing agents.
    max_found -- maximal number of valid name to be returned.
    min_found -- minimal similarity with valid name to be returned.
    return -- tuple of valid_names, ordered by decreasing score of similarity.

    If any found agent have a perfect match,
    any agent with a lesser match is discarded.

    """
    perfect_match = False
    if not firstname and not lastname:  # no name to search
        return tuple(agents)[:max_found]
    if firstname and lastname:
        fullname = firstname + ' ' + lastname
    else:
        fullname = firstname if firstname else lastname
    score = {}
    for ref in agents:
        if fullname:
            ref_name = ref.name
        else:
            ref_name = ref.firstname if firstname else ref.lastname
        similarity = utils.similarity(ref_name.lower(), fullname.lower())
        if ref.common_name:  # compare also to common name
            common_name_similarity = utils.similarity(ref.common_name.lower(), fullname.lower())
            similarity = max((common_name_similarity, similarity))
        if similarity >= min_sim:
            score[ref] = similarity
            if similarity == 1:
                perfect_match = True

    sorted_score = sorted(score.keys(), key=lambda k: score[k], reverse=True)
    if perfect_match:
        return tuple(itertools.takewhile(lambda k: score[k] == 1, sorted_score))
    else:  # no agent have been found with absolute certitude
        return tuple(sorted_score)[:max_found]
