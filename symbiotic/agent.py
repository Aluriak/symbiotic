"""High-level routine for agent handling"""


from symbiotic import utils


FIELDS = {
    'team':    lambda t: '' + str(t),
    'room':    lambda r: 'salle ' + str(r),
    'next to': lambda n: 'à côté de ' + str(n),
    'under':   lambda u: 'en-dessous ' + str(u),
    'is':      lambda i: 'est ' + str(i),
    'color':   lambda c: 'couleur' if c else 'monochrome',
    'A3':      lambda a: 'A3 et A4' if a else 'A4 uniquement',
    'common name': lambda n: 'appelée ' + str(n),
    'features'   : lambda f: 'propose ' + str(f),
    None:  lambda v: str(v)  # all other cases
}


class Agent:
    """Describes a human, printer or room"""

    def __init__(self, firstname, lastname, properties, type):
        """
        firstname -- agent's firstname
        lastname -- agent's lastname
        properties -- dict of properties, like {'team': 'dyliss'} for humans
        type -- agent's type: human, printer or room

        """
        self.firstname = str(firstname)
        self.lastname = lastname or None
        self.properties = dict(properties)
        self.type = str(type)
        assert self.type in ('human', 'printer', 'room')


    def as_lines(self, *, room_graph=None, agents_per_room=None):
        """Return a printable version of self

        room_graph -- mapping room: next rooms
        agents_per_room -- mapping room: agent

        If both room_graph and other_agents are provided,
        the representation will includes some hints to find the named agent.

        """
        return [self.name] + [FIELDS[field](value) for field, value in
                              self.properties.items() if value is not None]

    @property
    def fields(self):
        return self.name, tuple(self.properties.items()), self.type

    def __hash__(self):
        return hash(self.fields)

    def __eq__(self, othr):
        return self.fields == othr.fields


    def __str__(self):
        return '; '.join(self.as_lines())

    @property
    def is_human(self):
        return self.type == 'human'

    @property
    def is_printer(self):
        return self.type == 'printer'

    @property
    def is_room(self):
        return self.type == 'room'

    @property
    def name(self):
        return self.firstname + (' ' + self.lastname if self.lastname else '')

    @property
    def room(self):
        return self.properties.get('room', None)

    @property
    def next_to(self):
        return self.properties.get('next to', None)

    @property
    def under(self):
        return self.properties.get('under', None)

    @property
    def common_name(self):
        return self.properties.get('common name', None)

    @staticmethod
    def yield_from_json(json_payload, type):
        for name, properties in json_payload.items():
            firstname, *lastname = name.split(' ')
            yield Agent(firstname, ' '.join(lastname), properties, type)
