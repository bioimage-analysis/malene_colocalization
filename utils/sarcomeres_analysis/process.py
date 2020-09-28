import numpy as np
from scipy import stats
from skimage import filters
from skimage.morphology import reconstruction
import matplotlib.animation

def hdome(img):

    img_back_sub = np.empty(img.shape)
    for frame, img_to_analyse in enumerate(img):
        vmin, vmax = stats.scoreatpercentile(img_to_analyse, (0.5, 99.5))
        dat = np.clip(img_to_analyse, vmin, vmax)
        dat = (dat - vmin) / (vmax - vmin)
        image = filters.gaussian(dat , sigma=1)
        mask = image

        h = filters.threshold_yen(image)
        seed = image - h
        dilated = reconstruction(seed, mask, method='dilation')
        img_back_sub[frame] = image - dilated

    return (img_back_sub)
