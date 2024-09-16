import matplotlib.pyplot as plt
import random

from nooverlap import Pusher

random_words = """Bravely bold Sir Robin rode forth from Camelot. He was not afraid to die, O brave Sir Robin. He was not at all afraid to be killed in nasty ways, Brave, brave, brave, brave Sir Robin!
He was not in the least bit scared to be mashed into a pulp, Or to have his eyes gouged out and his elbows broken, To have his kneecaps split and his body burned away And his limbs all hacked and mangled, brave Sir Robin!
His head smashed in and his heart cut out And his liver removed and his bowels unplugged And his nostrils raped and his bottom burned off And his pen""".split(' ')

def random_text():
    n = len(random_words)
    i = random.randint(0,n-1)
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
    ax.plot(x,y,'r.')


L = ax.set_xlabel('X')
ax.set_ylabel('Y')

# get all the text objects from ax
texts = ax.texts

assert L not in texts

# get all the positions from texts
pusher = Pusher()
for text in texts:
    r = fig.canvas.get_renderer()
    expand = (1.0, 1.0)
    ext = text.get_window_extent(r).expanded(*expand).transformed(ax.transData.inverted())
    position = text.get_position()

    x0 = position[0]
    y0 = position[1]

    d_left = position[0] - ext.xmin
    d_right = ext.xmax - position[0]
    d_top = ext.ymax - position[1]
    d_bottom = position[1] - ext.ymin

    pusher.add_box(x0,y0,d_left,d_right,d_top,d_bottom)

# push the boxes
pusher.push_free(0.3, 0.3)

# re-position the text objects
for i, text in enumerate(texts):
    position = pusher.get_position(i)
    print(position)
    text.set_position(position)

plt.show()