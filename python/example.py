import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
x, y = np.random.random((2,80))

# x = [0.5488135039273248,0.7151893663724195,0.6027633760716439,0.5448831829968969,0.4236547993389047,0.6458941130666561,0.4375872112626925,0.8917730007820798,0.9636627605010293,0.3834415188257777,0.7917250380826646,0.5288949197529045,0.5680445610939323,0.925596638292661,0.07103605819788694,0.08712929970154071,0.02021839744032572,0.832619845547938,0.7781567509498505,0.8700121482468192,0.978618342232764,0.7991585642167236,0.46147936225293185,0.7805291762864555,0.11827442586893322,0.6399210213275238,0.1433532874090464,0.9446689170495839,0.5218483217500717,0.4146619399905236]
# y = [0.26455561210462697,0.7742336894342167,0.45615033221654855,0.5684339488686485,0.018789800436355142,0.6176354970758771,0.6120957227224214,0.6169339968747569,0.9437480785146242,0.6818202991034834,0.359507900573786,0.43703195379934145,0.6976311959272649,0.06022547162926983,0.6667667154456677,0.6706378696181594,0.2103825610738409,0.1289262976548533,0.31542835092418386,0.3637107709426226,0.5701967704178796,0.43860151346232035,0.9883738380592262,0.10204481074802807,0.2088767560948347,0.16130951788499626,0.6531083254653984,0.2532916025397821,0.4663107728563063,0.24442559200160274]

# print(','.join([str(n) for n in x]))
# print(','.join([str(n) for n in y]))

fig, ax = plt.subplots()
plt.plot(x, y, 'bo')
texts = [plt.text(x[i], y[i], 'Text%s' %i, ha='center', va='center') for i in range(len(x))]

# get text sizes
plt.draw()
r = fig.canvas.get_renderer()
expand = (1.0, 1.0)

class Box():
    def __init__(self, position, left, right, bottom, top):
        self.x = position[0]
        self.y = position[1]

        self.x0 = self.x
        self.y0 = self.y

        self.dl = self.x - left
        self.dr = right - self.x
        self.du = top - self.y
        self.dd = self.y - bottom
        self.to_be_moved = np.array((0,0), dtype=float)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def reset(self):
        self.to_be_moved = np.array((0,0), dtype=float)

    def do_move(self):
        self.move(*self.to_be_moved)

    @property
    def cx(self):
        return self.x + 0.5 * self.dr - 0.5*self.dl

    @property
    def cy(self):
        return self.y + 0.5 * self.du - 0.5*self.dd

    @property
    def width(self):
        return self.dr + self.dl

    @property
    def height(self):
        return self.du + self.dd

    @property
    def r(self):
        return ((0.5*self.width)**2 + (0.5*self.height)**2 ) ** (0.5)

    @property
    def left(self):
        return self.x - self.dl

    @property
    def right(self):
        return self.x + self.dr

    @property
    def top(self):
        return self.y + self.du

    @property
    def bottom(self):
        return self.y - self.dd

    def plot_home(self, ax):
        ax.plot((self.x, self.x0),
                (self.y, self.y0))

    def plot_box(self, ax):

        if self.width == 0 or self.height == 0:
            ax.plot(self.cx, self.cy, 'r.')
        else:
            ax.plot([self.left, self.left, self.right, self.right, self.left],
                    [self.bottom, self.top, self.top, self.bottom, self.bottom])

    def add_force_to_home(self, factor = 0.1):
        dx = self.cx - self.x0
        dy = self.cy - self.y0

        self.to_be_moved[0] = self.to_be_moved[0] - factor * dx
        self.to_be_moved[1] = self.to_be_moved[1] - factor * dy

    def add_force_from(self, other, factor = 1.2):
        if other.left > self.right:
            return
        if other.right < self.left:
            return
        if other.top < self.bottom:
            return
        if other.bottom > self.top:
            return

        self_to_other = (other.cx - self.cx, other.cy - self.cy)
        distance = np.linalg.norm(self_to_other)

        if  distance > 1e-10:
            D = np.array(self_to_other) / np.linalg.norm(self_to_other)
        else:
            D = np.array((0,1),dtype=float)

        overlap = distance - factor*self.r - factor*other.r

        self.to_be_moved = self.to_be_moved + 0.5 * overlap * D





boxes = []
points = []

for i in texts:
    ext = i.get_window_extent(r).expanded(*expand).transformed(ax.transData.inverted())
    #
    #
    # plt.plot([ext.xmin, ext.xmax, ext.xmax, ext.xmin, ext.xmin],[ext.ymax, ext.ymax, ext.ymin, ext.ymin, ext.ymax])
    # print(i.get_position())
    # print(ext)
    boxes.append(Box(i.get_position(), left = ext.xmin, right = ext.xmax, top = ext.ymax, bottom = ext.ymin))

    x,y = i.get_position()
    #
    points.append(Box(i.get_position(), x,x,y,y))


# Position iteratively
for i in range(100):

    for b in boxes:
        dx = b.cx - b.x0
        dy = b.cy - b.y0
        b.move(-0.1*dx,-0.1*dy)

    for b in boxes:
        for bb in boxes:
            if b == bb:
                continue
            b.add_force_from(bb)

        for p in points:
            b.add_force_from(p)

        b.do_move()
        b.reset()



for b in boxes:
    b.plot_box(ax=ax)
    b.plot_home(ax=ax)

for p in points:
    p.plot_box(ax=ax)



for t,b in zip(texts, boxes):
    t.set_position((b.x, b.y))



plt.show()