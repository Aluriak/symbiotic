"""

usage:
    symbiotic locate printer [<name>...]
    symbiotic locate room <name>...
    symbiotic locate <firstname> [<lastname>...]
    symbiotic news [<n>] [<rss_url>]
    symbiotic pause
    symbiotic blague [--rigolote]
    symbiotic validate


"""

import docopt

from symbiotic import locate
from symbiotic import blague
from symbiotic import news
from symbiotic import pause
from symbiotic import data


if __name__ == "__main__":
    args = docopt.docopt(__doc__)
    args['<name>'] = ' '.join(args['<name>'])
    args['<lastname>'] = ' '.join(args['<lastname>'])

    if args['locate']:
        if args['printer']:
            locate.from_name(args['<name>'], None, type='printer')
        elif args['room']:
            locate.from_name(args['<name>'], None, type='room')
        else:  # search for human
            assert args['<firstname>']
            locate.from_name(args['<firstname>'], args['<lastname>'], type='human')
    if args['blague']:
        blague.tell(rigolote=args['--rigolote'])
    if args['news']:
        news.fetch(int(args['<n>'] or 0), args['<rss_url>'] or None)
    if args['pause']:
        pause.detect()

    if args['validate']:
        payload = data.Data.from_file()
        for agent in payload.agents:
            for prop, value in agent.properties.items():
                if value is None or value == '':
                    print("Agent of name {} have {} set to '{}'.".format(
                        agent.name, prop, value))

