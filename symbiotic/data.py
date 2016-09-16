"""Wrapper around data access"""


import json
from itertools import chain

from symbiotic import utils
from symbiotic.agent import Agent


DATAFILE = 'data/base.json'


class Data:

    def __init__(self, graph, agents, options):
        self.graph = utils.completed(dict(graph))
        self.agents = frozenset(agents)
        self.options = dict(options)

    @property
    def humans(self):
        return self.get_agents('human')
    @property
    def printers(self):
        return self.get_agents('printer')
    @property
    def rooms(self):
        return self.get_agents('room')

    @property
    def locate_options(self):
        return self.options['locate']

    @property
    def news_options(self):
        return self.options['news']

    def get_agents(self, type):
        return tuple(agent for agent in self.agents if agent.type == type)

    @staticmethod
    def from_file(*, datafile=DATAFILE):
        with open(datafile) as fd:
            payload = json.load(fd)
        return Data.from_json(payload)

    @staticmethod
    def from_json(json_payload):
        assert 'humans' in json_payload
        assert 'printers' in json_payload
        assert 'rooms' in json_payload
        assert 'room graph' in json_payload
        graph = {pred: frozenset(succs) for pred, succs in json_payload['room graph'].items()}
        agents = set(chain.from_iterable(
            Agent.yield_from_json(json_payload[field], type=field.rstrip('s'))
            for field in ('humans', 'printers', 'rooms')
        ))
        # add all rooms in the graph that are not in agent
        for room_name in utils.all_nodes(graph):
            if not any(agent.name == room_name for agent in agents if agent.is_room):
                agents.add(Agent(room_name, None, {}, type='room'))

        return Data(graph, agents, json_payload['options'])
