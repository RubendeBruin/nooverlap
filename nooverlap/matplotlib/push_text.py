from nooverlap import Pusher

def push_text_free(fig, ax, max_x_shift = 0.3, max_y_shift = 0.3):
    """Pushes all text-elements in ax of figure to avoid overlap.

    The maximum push per iteration is max_x_shift and max_y_shift. These
    are factors of the width and height of the text-boxes.

    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The figure containing the axes.
    ax : matplotlib.axes.Axes
        The axes containing the text-elements.

    max_x_shift : float
    max_y_shift : float

    """
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
    pusher.push_free(max_x_shift, max_y_shift)

    # re-position the text objects
    for i, text in enumerate(texts):
        position = pusher.get_position(i)
        text.set_position(position)
