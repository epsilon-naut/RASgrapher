import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np



def updatefig(i):
    fig.clear()
    p = plt.plot(np.random.random(100))
    plt.draw()

fig = plt.figure()

anim = animation.FuncAnimation(fig, updatefig, 10)
anim.save("test.gif", writer = 'pillow', fps=1)