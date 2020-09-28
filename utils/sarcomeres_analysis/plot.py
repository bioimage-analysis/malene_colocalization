from ipywidgets import interact, Output
import matplotlib.pyplot as plt
import matplotlib.animation
import matplotlib
from matplotlib.pyplot import cm
from skimage.draw import line

def plot_int_under_line(raw_img, img_back_sub, cmap='gray'):

    t, x, y =  raw_img.shape
    out = Output()

    @interact(plane=(0, t - 1), y_pos =(0, y-1) , continuous_update=False)
    def display_slice(plane=0, y_pos = 50):
        fig, ax = plt.subplots(2, 2, figsize=(16, 16))
        with out:
            ax[0,0].imshow(raw_img[plane])
            ax[0,0].axhline(y=y_pos, color='r', linestyle='-')
            ax[1,0].imshow(img_back_sub[plane])
            ax[1,0].axhline(y=y_pos, color='r', linestyle='-')
            ax[0,1].plot(raw_img[plane,y_pos,:], color='r', linestyle='-')
            ax[1,1].plot(img_back_sub[plane,y_pos,:], color='r', linestyle='-')

    return display_slice

def movie(img):

    img_to_anim = img[::8]

    fig, ax = plt.subplots(figsize=(6, 6))

    im = ax.imshow(img_to_anim[0])

    def animate(i):
        im.set_data(img_to_anim[i])

    ani = matplotlib.animation.FuncAnimation(fig, animate, frames = img_to_anim.shape[0], interval = 100)

    plt.close(fig)
    return ani

def draw_lines_napari(viewer, img):
    lines = []
    for coord in viewer.layers[1].data:
        lines.append(line(int(coord[0,2]), int(coord[0,1]), int(coord[1,2]), int(coord[1,1])))

    plt.imshow(img[0])
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for i, li in enumerate(lines):
        plt.plot(li[0], li[1], c=cycle[i])

    return lines

def draw_lines(img):
    matplotlib.use('Qt5Agg')

    plt.imshow(img[0])
    x = plt.ginput(-1, timeout = 90)
    lines = []
    for i in range(0, len(x), 2):
        lines.append(line(int(x[i][0]),int(x[i][1]),int(x[i+1][0]), int(x[i+1][1])))

    plt.imshow(img[0])
    cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    for i, li in enumerate(lines):
        plt.plot(li[0], li[1], c=cycle[i])

    return lines
