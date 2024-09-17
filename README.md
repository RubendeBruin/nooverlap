Library to avoid overlap of graphical objects.

TLDR;
```python
from nooverlap import push_text_free
push_text_free(fig, ax)
```



![image](https://github.com/user-attachments/assets/d5d20aab-9604-4c2d-a2f1-8004ecfd6f0f)

And fast enough to run in real-time:

https://github.com/user-attachments/assets/b0fc651f-8964-4481-a8b3-dd749a5bd3fe

Steps:
- define "Pusher"
- add boxes
- push
- get new box positions

Algorithm:

- loop over all boxes combinations (n^2)
- if boxes overlap: push then away from eachother by the overlapping distance in the direction of overlap
- but maximize the horizontal and vertical push distances to the user-provided factor times the average widht or height
- repeat until there is no overlap anymore.

User setttings:
- maximum push distance in vertical direction per iteration as fraction of the box size
- maximum push distance in horizontal direction per iteration as fraction of the box size
Set one of the two to zero to get only horizontal or vertical shift.
  




Example use for matplotlib:

```python
import matplotlib.pyplot as plt
import random

from nooverlap import push_text_free

random_words = """Bravely bold Sir Robin rode forth from Camelot. He was not afraid to die, O brave Sir Robin. He was not at all afraid to be killed in nasty ways, Brave, brave, brave, brave Sir Robin!
He was not in the least bit scared to be mashed into a pulp, Or to have his eyes gouged out and his elbows broken, To have his kneecaps split and his body burned away And his limbs all hacked and mangled, brave Sir Robin!
His head smashed in and his heart cut out And his liver removed and his bowels unplugged And his nostrils raped and his bottom burned off And his pen""".split(
    ' ')

def random_text():
    n = len(random_words)
    i = random.randint(0, n - 1)
    return random_words[i]

# Create a figure and axes
fig, ax = plt.subplots()

# Add 100 random text elements
texts = []
for _ in range(100):
    x = random.random()
    y = random.random()
    text = random_text()
    ax.text(x, y, text, ha='center', va='center')

ax.set_xlabel('X')
ax.set_ylabel('Y')

push_text_free(fig, ax)

plt.show()
```



