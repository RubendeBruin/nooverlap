import nooverlap
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

np.random.seed(0)
n = 50     
x = 5*np.random.rand(n)
y = 2*np.random.rand(n)
w = np.random.rand(n)
h = 0.3*np.random.rand(n)


# make some random box data
def make_data(fac):
   
    # create a nooverlap object
    no = nooverlap.Pusher()

    # add the boxes
    for i in range(n):
        no.add_box(x[i], y[i], w[i]/2, w[i]/2, h[i]/2, h[i]/2)

    no.push_free(fac, fac)

    return no

# draw the boxes 
fig, ax = plt.subplots()



ax.set_xlim(-1,6)
ax.set_ylim(-0.5,2.5) 

for fac in (0.001, 0.3):
    no = make_data(fac)
    for i in range(n):
        _x,_y = no.get_position(i)
        _w = w[i]
        _h = h[i]
        ax.add_patch(plt.Rectangle((_x-0.5*_w, _y-0.5*_h), width=_w, height=_h , facecolor=(3*fac,3*fac,3*fac), edgecolor='black'))
        ax.plot([_x,x[i]],[_y,y[i]])



plt.show()

