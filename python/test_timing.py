import nooverlap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

np.random.seed(0)

# make some random box data
for n in range(100):
        
    x = 5*np.random.rand(n)
    y = 2*np.random.rand(n)
    w = np.random.rand(n)
    h = 0.3*np.random.rand(n)

    # create a nooverlap object
    no = nooverlap.Pusher()

    # add the boxes
    for i in range(n):
        no.add_box(x[i], y[i], w[i]/2, w[i]/2, h[i]/2, h[i]/2)


    from time import time
    start = time()
    no.push_free(0.3)
    elapsed = time() - start
    print(f'number {n} took {elapsed*1000} ms')

# draw the boxes 
fig, ax = plt.subplots()

ax.set_xlim(-1,6)
ax.set_ylim(-0.5,2.5) 
for i in range(n):
    _x,_y = no.get_position(i)
    _w = w[i]
    _h = h[i]
    ax.add_patch(plt.Rectangle((_x-0.5*_w, _y-0.5*_h), width=_w, height=_h , facecolor='lightblue', edgecolor='black'))
    ax.plot([_x,x[i]],[_y,y[i]])



plt.show()
