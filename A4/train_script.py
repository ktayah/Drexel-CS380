import os
import sys

difficulties = ['easy', 'medium', 'hard']

# the q table file name
train_filename = sys.argv[1] if len(sys.argv) > 1 else 'q'

for difficulty in difficulties:
    for restart in range(1, 9):
        for iteration in range(0, 10):
            cmd = f'python main.py --player=agent --train={train_filename} --screen={difficulty} --steps=1000 --speed=fast --restart={restart}'
            print(cmd)
            os.system(f'cmd /c "{cmd}"')