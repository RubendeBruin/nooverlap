Library to avoid overlap of graphical objects.

![image](https://github.com/user-attachments/assets/d5d20aab-9604-4c2d-a2f1-8004ecfd6f0f)

Steps:
- define "Pusher"
- add boxes
- push
- get new box positions

Example use for matplotlib:

```python

def push_free(fig, ax):
    # get all the positions from texts
    texts = ax.texts
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
        text.set_position(position)




if __name__ == '__main__':

    import matplotlib.pyplot as plt
    import random

    from nooverlap import Pusher

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
        ax.plot(x, y, 'r.')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    push_free(fig, ax)

    plt.show()
```

