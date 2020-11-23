import os

for i in range(100):
    os.system('cmd /c "python main.py --player=agent --train=q --screen=hard --steps=500 --speed=fast --restart=1"')