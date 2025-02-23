# test to see if the example on the README works
def test_example():
    import random
    import matplotlib.pyplot as plt
    
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

    # plt.show()


if __name__ == "__main__":
    test_example()
    import matplotlib.pyplot as plt
    plt.show()