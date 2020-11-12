import importlib
import sys

from util import Arguments

if __name__ == '__main__':

    args = Arguments()

    player = args.get('player', 'agent')
    screen = args.get('screen', 'medium')
    steps = args.get_int('steps', None)
    train = args.get('train', None)
    speed = args.get('speed', 'fast' if train else 'slow')
    restart = args.get_int('restart', None)
    output = args.get('output', 'graphics')

    from frogger.settings import settings
    settings['use_graphics'] = (output.lower() != 'text')

    from frogger.frogger import Frogger
    game = Frogger(screen)

    if player != 'human':
        agent_module = importlib.import_module(player)
        agent = agent_module.Agent(train=train)
        game.add_agent(agent)

    scores = game.run(steps=steps, speed=speed, restart=restart)
    print('\t'.join([str(score) for score in scores]))
