from nooverlap import Pusher


def test_push_text_free():
    pusher = Pusher()

    pusher.add_box(
                x0=5, 
                y0=5, 
                d_left=-2, 
                d_right=4, 
                d_top=0, 
                d_bottom=2
            )


    pusher.add_box(
                x0=6, 
                y0=5, 
                d_left=-2, 
                d_right=4, 
                d_top=0, 
                d_bottom=2
            )


    pusher.push_free(push_factor_horizontal=0.1, push_factor_vertical=0.3)

    x1, y1 = pusher.get_position(0)
    x2, y2 = pusher.get_position(1)

    assert round(10*x1) == 44
    assert round(10*x2) == 66
    assert y1 == y2

if __name__ == "__main__":
    test_push_text_free()
