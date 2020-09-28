import numpy as np
from scipy.signal import find_peaks, peak_widths, peak_prominences
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, peak_widths, peak_prominences
import pandas as pd


def dist_sarco(img, meta, lines, directory, plot=False, save = False):
    dist = np.empty((len(lines), len(img)))
    for frame, im in enumerate(img):
        for num, li in enumerate(lines):
            peak, _ = find_peaks(im[li[1], li[0]], distance=7)
            dist_p = np.diff(peak)*meta['PhysicalSizeX']
            dist[num, frame] = np.mean(dist_p)

    dist_smooth = []
    for i in range(len(dist)):
        dist_smooth.append(savgol_filter(dist[i], 31, 5))

    if plot:
        fig, ax = plt.subplots(nrows = 1+(len(dist)*2), figsize=(12,36))
        ax[0].imshow(img[0])

        cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

        for i, li in enumerate(lines):
            ax[0].plot(li[0], li[1], c=cycle[i])
        k=0
        j=1
        for i in range(len(dist)):
            k+=2

            ax[j].plot(meta['Timepoint']*100, dist[i], label="Raw Data")
            ax[j].plot(meta['Timepoint']*100, dist_smooth[i], label="Smoothed Data", c = cycle[i-1])
            ax[j].legend()
            ax[j].set_xlabel('Time in ms')
            ax[j].set_ylabel('Sarcomere length (um)')
            ax[j].set_title('Example 1')

            positive_raw = 100-((dist[i] / np.percentile(dist[i], 90)))*100
            positive_smooth = 100-((dist_smooth[i] / np.percentile(dist_smooth[i], 90)))*100

            ax[k].plot(meta['Timepoint']*100, positive_raw, label="Raw Data")
            ax[k].plot(meta['Timepoint']*100, positive_smooth, label="Smoothed Data")
            ax[k].legend()
            ax[k].set_xlabel('Time in ms')
            ax[k].set_ylabel('Sarcomere shortening (%)')

            j+=2
        plt.savefig("sarcomere_ex1_data.pdf", transparent=True)

        if save:
            try:
                filename = meta['Name']+'.pdf'
                plt.savefig(directory+'/'+filename, transparent=True)
            except FileNotFoundError:
                plt.savefig(filename, transparent=True)
    return dist_smooth

def av_dist_sarco(img, meta, lines, directory, plot=True, save = False):
    mean_time = np.empty(len(img))
    for frame, im in enumerate(img):
        peaks_lst = []
        for li in lines:
            peaks, _ = find_peaks(im[li[1], li[0]], distance=7)
            peaks_lst.append(peaks)
        dists = []
        for peak in peaks_lst:

            dists.append(np.diff(peak)*meta['PhysicalSizeX'])
        mean_time[frame] = np.mean(np.hstack(dists))
    mean_time_smooth = savgol_filter(mean_time, 31, 5)

    if plot:
        fig, ax = plt.subplots(nrows = 3, figsize=(12,12))
        ax[0].imshow(img[0])

        cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

        for i, li in enumerate(lines):
            ax[0].plot(li[0], li[1], c=cycle[i])

        ax[1].plot(meta['Timepoint']*100, mean_time, label="Raw Data")
        ax[1].plot(meta['Timepoint']*100, mean_time_smooth, label="Smoothed Data")
        ax[1].legend()
        ax[1].set_xlabel('Time in ms')
        ax[1].set_ylabel('Sarcomere length (um)')
        ax[1].set_title('Example 1')

        positive_raw = 100-((mean_time / np.percentile(mean_time, 90)))*100
        positive_smooth = 100-((mean_time_smooth / np.percentile(mean_time_smooth, 90)))*100

        ax[2].plot(meta['Timepoint']*100, positive_raw, label="Raw Data")
        ax[2].plot(meta['Timepoint']*100, positive_smooth, label="Smoothed Data")
        ax[2].legend()
        ax[2].set_xlabel('Time in ms')
        ax[2].set_ylabel('Sarcomere shortening (%)')
        plt.savefig("sarcomere_ex1_data.pdf", transparent=True)

        if save:
            try:
                filename = meta['Name']+'.pdf'
                plt.savefig(directory+'/'+filename, transparent=True)
            except FileNotFoundError:
                plt.savefig(filename, transparent=True)
    return mean_time_smooth

def to_dataframe(result, meta, directory, line_num="average", save=False):
    peaks, _ = find_peaks(-result, distance=50)
    SS = peak_prominences(-result, peaks, wlen = 70)
    CD50 = peak_widths(-result, peaks, rel_height=0.5, prominence_data=SS)
    CD90 = peak_widths(-result, peaks, rel_height=0.9, prominence_data=SS)
    time_frame = meta['Timepoint'][-1]/600 *100

    max_contract = []
    max_relax = []
    for i in range (len(peaks)):
        max_contract.append(np.max(np.diff(-result[SS[1][i]:peaks[i]]))*time_frame)
        max_relax.append(np.min(np.diff(-result[peaks[i]:SS[2][i]:]))*time_frame)

    df = pd.DataFrame(result[SS[1]], columns = ['Basal length'])
    df['Peak length in um'] = result[peaks]
    df['Time to peak in msec'] = peaks*time_frame - SS[1]*time_frame
    df['CD90 in msec'] = CD90[0] * time_frame
    df['CD50 in msec'] = CD50[0] * time_frame
    df['Max contractile in um/msec'] = max_contract
    df['Max relaxation in um/msec'] = max_relax
    int_peak = np.zeros(len(peaks), 'int')
    int_peak[1:] = np.diff(peaks)
    df['Peak intervals in ms'] = int_peak *time_frame
    beat_rate = np.zeros(len(peaks))
    beat_rate[1:] = 6000/((np.diff(peaks)*time_frame)/2)
    df['Beating rate in beat/min'] = beat_rate

    if save == True:
        try:
            df.to_csv(directory+'/'+'line'+line_num+'_'+'{}.csv'.format(meta["Name"]))
        except FileNotFoundError:
            df.to_csv('line'+line_num+'_'+'{}.csv'.format(meta["Name"]))

    return df
