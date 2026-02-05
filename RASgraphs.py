import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim
import math
import scipy.signal as scp

def file_read_ras(filename):
    f = open(filename)
    read = False
    theta = []
    intensity = []
    for line in f:
        if(line == "*RAS_INT_END\n"):
            print("Data end found.")
            read = False
        if(read):
            i = 0
            for j in range(2):
                s = ""
                while(line[i] != ' '):
                    s += line[i]
                    i += 1
                if(j == 0):
                    theta.append(float(s))
                else:
                    intensity.append(float(s))
                i += 1
        if(line == "*RAS_INT_START\n"):
            print("Data start found")
            read = True
    return theta, intensity

def file_read_int(filename):
    f = open(filename)
    read = False
    theta = []
    intensity = []
    peaks = []
    for line in f:
        if(read):
            i = 0
            while(line[i] == ' '):
                i += 1
            for j in range(2):
                s = ""
                while(line[i] != ' '):
                    s += line[i]
                    i += 1
                if(j == 0):
                    theta.append(float(s))
                else:
                    intensity.append(float(s))
                while(line[i] == ' '):
                    i += 1
        if(line[:-1].isdigit()):
            print("Data start found")
            read = True
    return theta, intensity

def file_read_gen(filename):
    if(filename[-4:] == ".ras"):
        theta, intensity = file_read_ras(filename)
    elif(filename[-4:] == ".int"):
        theta, intensity = file_read_int(filename)
    return theta, intensity
        
def plot(theta, intensity, title, color, label, spacing):

    ax = plt.subplot(1, 1, 1)

    nt = np.array(theta)
    ni = np.array(intensity)
    
    ax.plot(nt, ni, color = color, label = label)
    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (arb. units)")

    xticks1 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing/2)
    xticks2 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing)
    ax.set_xlim(theta[0], theta[len(theta)-1])
    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax.set_title(title)

    plt.legend()
    plt.show()

def plot_gen(axes, ind, theta, intensity, title, color, label, spacing, axis_vis = True):

    ax = axes[ind]

    nt = np.array(theta)
    ni = np.array(intensity)
    
    ax.plot(nt, ni, color = color, label = label)
    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Normalized Intensity (arb. units)")

    xticks1 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing/2)
    xticks2 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing)
    ax.set_xlim(theta[0], theta[len(theta)-1])
    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax.get_xaxis().set_visible(axis_vis)

    ax.set_title(title)

    ax.legend()

def change_axes(axes, theta, spacing):
    for ax in axes:
        xticks1 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing/2)
        xticks2 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing)
        ax.set_xlim(theta[0], theta[len(theta)-1])
        ax.set_xticks(xticks1, minor = True)
        ax.set_xticks(xticks2)
        ax.tick_params(which = "minor", length = 5)
        ax.tick_params(which = "major", length = 8)

def plotn(n, theta, intensity, title, color, label, spacing):

    ax = plt.subplot(1, 1, 1)
    
    for i in range(n):
        nt = np.array(theta[i])
        ni = np.array(intensity[i])
        ax.plot(nt, ni, color = color[i], label = label[i])
    
    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (arb. units)")

    xticks1 = np.arange(theta[0][0], theta[0][len(theta[0])-1]+1, spacing/2)
    xticks2 = np.arange(theta[0][0], theta[0][len(theta[0])-1]+1, spacing)
    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax.set_title(title)

    plt.legend()
    plt.show()

def plot2(theta, intensity, title):

    ax = plt.subplot(2, 1, 2)
    ax2 = plt.subplot(2, 1, 1)

    colors = ["blue", "red"]

    nt = np.array(theta[0])
    ni = np.array(intensity[0])
    ax.plot(nt, ni, color = colors[0], label = "Side A")

    nt2 = np.array(theta[1])
    ni2 = np.array(intensity[1])
    ax2.plot(nt2, ni2, color = colors[1], label = "Side B")

    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (arb. units)")
    ax2.set_ylabel("Intensity (arb. units)")

    xticks1 = np.arange(theta[0][0], theta[0][len(theta[0])-1]+1, 5)
    xticks2 = np.arange(theta[0][0], theta[0][len(theta[0])-1]+1, 10)

    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax2.get_xaxis().set_visible(False)
    plt.subplots_adjust(hspace = 0.0)

    ax.legend()
    ax2.legend()

    plt.title(title)

    plt.show()

def plotsuper(theta, intensity, title):

    ax = plt.subplot(1, 1, 1)

    for i in range(len(intensity[1])):
        intensity[1][i] += 250
    
    nt = np.array(theta[0])
    ni = np.array(intensity[0])

    nt2 = np.array(theta[1])
    ni2 = np.array(intensity[1])

    ax.plot(nt, ni, color = "blue", label = "Side A")
    ax.plot(nt2, ni2, color = "red", label = "Side B")

    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Modified Intensity (arb. units)")

    xticks1 = np.arange(theta[0][0], theta[0][len(theta[0])-1]+1, 5)
    xticks2 = np.arange(theta[0][0], theta[0][len(theta[0])-1]+1, 10)
    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax.set_title(title)
    ax.legend()

    plt.show()

def plot_peaks_gen(axes, ind, theta, peaks, spacing):
    pks = axes[ind]
    pks.bar(peaks, 1, width = 0.02*spacing)

    xticks1 = np.arange(theta[0], theta[len(theta)-1]+1, spacing/2)
    xticks2 = np.arange(theta[0], theta[len(theta)-1]+1, spacing)
    pks.set_xticks(xticks1, minor = True)
    pks.set_xticks(xticks2)
    pks.tick_params(which = "minor", length = 5)
    pks.tick_params(which = "major", length = 8)
    pks.get_yaxis().set_visible(False)
    pks.set_xlim(theta[0], theta[len(theta)-1])

    pks.set_xlabel("2θ (degrees)")

def restrict_range(theta_r, theta_i):
    for i in range(len(theta_i)):
        if(theta_i[i] - theta_r[0] < 0.01):
            start = i
        elif(theta_i[i] - (theta_r[len(theta_r)-1]) < 0.01):
            end = i
    return start, end

def normalize(intensity_r):
    max_i = -1
    for i in intensity_r:
        if(i > max_i):
            max_i = i
    for i in range(len(intensity_r)):
        intensity_r[i] /= max_i
        intensity_r[i] *= 100

def rmv_bckg(theta, intensity, deg):
    nt = np.array(theta)
    
    coeffs = np.polyfit(theta, intensity, deg)
    nfit = coeffs[deg]
    for i in range(deg):
        nfit += coeffs[i]*nt**(deg-i)

    for i in range(len(intensity)):
        intensity[i] -= nfit[i]

    return intensity

def plot_poly(ras, deg):
    theta_r, intensity_r = file_read_ras(ras)
    
    ax = plt.subplot(1, 1, 1)

    nt = np.array(theta_r)
    ni = np.array(intensity_r)

    coeffs = np.polyfit(theta_r, intensity_r, deg)
    nfit = coeffs[deg]
    for i in range(deg):
        nfit += coeffs[i]*nt**(deg-i)

    ax.plot(nt, ni, color = "blue", label = "exp")
    ax.plot(nt, nfit)

    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (arb. units)")

    xticks1 = np.arange(theta_r[0], theta_r[len(theta_r)-1]+1, 5)
    xticks2 = np.arange(theta_r[0], theta_r[len(theta_r)-1]+1, 10)
    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax.set_title("background removal")

    plt.legend()
    plt.show()

def plot_poly_gen(axes, ind, theta, intensity, deg, title, color, label, spacing, axis_vis = True):
    ax = axes[ind]

    nt = np.array(theta)
    ni = np.array(intensity)

    coeffs = np.polyfit(theta, intensity, deg)
    nfit = coeffs[deg]
    for i in range(deg):
        nfit += coeffs[i]*nt**(deg-i)

    ax.plot(nt, ni, color = color, label = label)
    ax.plot(nt, nfit)

    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (arb. units)")

    xticks1 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing/2)
    xticks2 = np.arange(theta[0], theta[len(theta)-1]+0.01, spacing)
    ax.set_xlim(theta[0], theta[len(theta)-1])
    ax.set_xticks(xticks1, minor = True)
    ax.set_xticks(xticks2)
    ax.tick_params(which = "minor", length = 5)
    ax.tick_params(which = "major", length = 8)

    ax.get_xaxis().set_visible(axis_vis)

    ax.set_title(title)

    ax.legend()

def plot_int_gen(axes, ind, theta, intensity, title, color, label, spacing, axis_vis = True):
    int_intensity = []
    sum = 0
    for i in range(len(theta)-1):
        sum += intensity[i] * (theta[i+1]-theta[i]) #left sum
        int_intensity.append(sum)
    sum += intensity[len(intensity)-1]*(theta[len(theta)-1]-theta[len(theta)-1])
    int_intensity.append(sum)
    
    for i in range(len(int_intensity)):
        int_intensity[i] *= 100

    plot_gen(axes, ind, theta, int_intensity, title, color, label, spacing, axis_vis)

def plot_hahafunny_gen(axes, ind, theta, intensity, title, color, label, spacing, axis_vis = True):

    dx = ((theta[len(theta)-1]-theta[0])/10000)
    haha_2 = np.gradient(intensity, dx)
    normalize(haha_2)

    plot_gen(axes, ind, theta, haha_2, title, color, label, spacing, axis_vis)

def plot_hahafunny2_gen(axes, ind, theta, intensity, title, color, label, spacing, axis_vis = True):

    haha_1 = smoothen(theta, intensity)
    for i in range(30):
        haha_1 = smoothen(theta, haha_1)

    redshift(haha_1, intensity)

    normalize(haha_1)

    plot_gen(axes, ind, theta, haha_1, title, color, label, spacing, axis_vis)

    plot_hahafunny_gen(axes, ind, theta, haha_1, title, color, label, spacing, axis_vis)

def plot_hahafunny_peaks_gen(axes, ind, theta, intensity, spacing, cutoff):

    haha_1 = smoothen(theta, intensity)
    for i in range(40):
        haha_1 = smoothen(theta, haha_1)

    redshift(haha_1, intensity)

    dx = ((theta[len(theta)-1]-theta[0])/10000)
    haha_2 = np.gradient(haha_1, dx)
    normalize(haha_2)

    peaks = []

    for i in range(len(haha_2)-1):
        if((haha_2[i] >= 0) and (haha_2[i+1] < 0)):
            peaks.append(theta[i])

    actualized = []

    normalize(intensity)
    print(intensity[0])

    left_cutoff = 0
    right_cutoff = len(intensity)-1

    for i in range(len(intensity)):
        if(intensity[i] - intensity[0] > cutoff):
            left_cutoff = i
            break 

    for i in range(len(intensity)):
        if(intensity[len(intensity)-1-i] - intensity[0] > cutoff):
            right_cutoff = len(intensity)-1-i
            break
    
    left_cutoff_changed = False
    right_cutoff_changed = False

    for i in range(left_cutoff, 0, -1):
        if(haha_2[i] >= 0 and haha_2[i-1] < 0):
            left_cutoff = i
            left_cutoff_changed = True
            break

    for i in range(right_cutoff, len(intensity)-1):
        if(haha_2[i] >= 0 and haha_2[i-1] < 0):
            right_cutoff = i
            right_cutoff_changed = True
            break

    if(not left_cutoff_changed):
        left_cutoff = int(len(theta)/8)

    if(not right_cutoff_changed):
        right_cutoff = int(7*len(theta)/8)

    print(left_cutoff)
    print(theta[left_cutoff])
    print(right_cutoff)
    print(theta[right_cutoff])

    max_noise = -1
    min_noise = 101
    for i in range(left_cutoff):
        if(haha_2[i] > max_noise):
            max_noise = haha_2[i] #potential signal to noise usage
        if((haha_2[i] < min_noise)):
            min_noise = haha_2[i]
    
    for i in range(right_cutoff, len(intensity)-1):
        if(haha_2[i] > max_noise):
            max_noise = haha_2[i] #potential signal to noise usage
        if((haha_2[i] < min_noise)):
            min_noise = haha_2[i]
    
    if((abs(min_noise) > max_noise) and min_noise != 101):
        max_noise = abs(min_noise)

    if(max_noise < 7.3):
        max_noise = 7.3

    print(max_noise)

    for i in range(len(peaks)):
        if(i == 0):
            left_half = theta[0]
            right_half = (peaks[i]+(peaks[i+1]-peaks[i])/4)
        elif (i == len(peaks) - 1):
            left_half = (peaks[i] + (peaks[i-1]-peaks[i])/4)
            right_half = theta[len(theta)-1]
        else:
            left_half = (peaks[i] + (peaks[i-1]-peaks[i])/4)
            right_half = (peaks[i]+(peaks[i+1]-peaks[i])/4)
        left_ind = int((left_half - theta[0])/(theta[1]-theta[0]))
        right_ind = int(((right_half - theta[0])/(theta[1]-theta[0])))
        max = haha_2[left_ind]
        min = haha_2[left_ind]
        for j in range(left_ind, right_ind):
            if(haha_2[j] > max):
                max = haha_2[j]
            if(haha_2[j] < min):
                min = haha_2[j]
        if((max - min) > 2*max_noise):
            print(max-min)
            actualized.append(peaks[i])

    plot_peaks_gen(axes, ind, theta, actualized, spacing)

def smoothen(theta, intensity):
    int_intensity = []
    sum = 0
    for i in range(len(theta)-1):
        sum += intensity[i] * (theta[i+1]-theta[i]) #left sum
        int_intensity.append(sum)
    sum += intensity[len(intensity)-1]*(theta[len(theta)-1]-theta[len(theta)-1])
    int_intensity.append(sum)

    for i in range(len(int_intensity)):
        int_intensity[i] *= 100

    dx = ((theta[len(theta)-1]-theta[0])/10000)
    haha_1 = np.gradient(int_intensity, dx)
    normalize(haha_1)
    return haha_1

def polyapprox(value, coeffs, degree):
    nfit = coeffs[degree]
    for j in range(degree):
        nfit += coeffs[j]*value**(degree-j)
    return nfit

def smoothen_savgol(theta, intensity, degree, window):
    smoothened = []
    coeffs = np.polyfit(range(0, window), intensity[0: window], degree)
    vals = []
    for i in range(len(intensity)):
        vals.append(i)
    for i in range(0, int(window/2)):
        smoothened.append(polyapprox(i, coeffs, degree))
    for i in range(int(window/2), len(intensity) - int(window/2)):
        print(range(i - int(window/2), i+int(window/2)+1))
        print(intensity[i - int(window/2): i+int(window/2)+1])
        coeffs = np.polyfit(vals[i - int(window/2): i+int(window/2)+1], intensity[i - int(window/2): i+int(window/2)+1], degree)
        print(coeffs)
        print(intensity[i])
        print(polyapprox(intensity[i], coeffs, degree))
        smoothened.append(polyapprox(i, coeffs, degree))
    coeffs = np.polyfit(vals[len(intensity) - int(window/2):len(intensity)], intensity[len(intensity) - int(window/2):], degree)
    for i in range(len(intensity) - int(window/2), len(intensity)):
        smoothened.append(polyapprox(i, coeffs, degree))
    return smoothened

def plot_comparison(filename, degree, window, spacing):
    theta, intensity = file_read_ras(filename)

    fig, axes = plt.subplots(2, 1, height_ratios = [100, 1])

    haha_1 = smoothen(theta, intensity)
    for i in range(30):
        haha_1 = smoothen(theta, haha_1)

    redshift(haha_1, intensity)

    normalize(haha_1)
    normalize(intensity)

    plot_gen(axes, 0, theta, intensity, "", "cyan", "", spacing)

    #plot_gen(axes, 0, theta, haha_1, "", "blue", "", spacing)

    #plot_hahafunny_gen(axes, 0, theta, haha_1, "", "blue", "", spacing)
    #for i in range(10):
        #savgol = smoothen_savgol(theta, intensity, degree, window)
    #normalize(savgol)

    #plot_gen(axes, 0, theta, savgol, "", "red", "", spacing)

    #plot_hahafunny_gen(axes, 0, theta, savgol, "", "red", "", spacing)
    for i in range(10):
        savgol2 = scp.savgol_filter(intensity, 10, 5)

    #plot_gen(axes, 0, theta, savgol2, "", "green", "", spacing)
    #plot_hahafunny_gen(axes, 0, theta, savgol2, "", "green", "", spacing)


    savgol2 = scp.savgol_filter(intensity, 50, 5)

    #plot_gen(axes, 0, theta, savgol2, "", "red", "", spacing)
    #plot_hahafunny_gen(axes, 0, theta, savgol2, "", "red", "", spacing)
    #plot_hahafunny_gen(axes, 0, theta, savgol2, "", "green", "", spacing)
    
    plt.show()


def redshift(haha_1, intensity):
    max = haha_1[0]
    max_haha = 0
    for i in range(len(haha_1)):
        if(haha_1[i] > max):
            max_haha = i
            max = haha_1[i]

    max = intensity[0]
    max_int = 0
    for i in range(len(intensity)):
        if(intensity[i] > max):
            max_int = i
            max = intensity[i]

    shift = max_int - max_haha
    if(shift > 0):
        haha_1[shift:] = haha_1[0:len(haha_1)-shift]
        haha_1[0:shift] = haha_1[0]

def get_peaks(theta, intensity, cutoff):
    peaks = []
    for i in range(len(intensity)):
        if(intensity[i] > cutoff):
            peaks.append(theta[i])
    return peaks

def get_peaks_2(theta, intensity, cutoff):
    peak_start = []
    peak_end = []
    peak_avg = []
    peak_max = []
    peak_track = False
    for i in range(len(theta)):
        if(not peak_track):
            if(intensity[i] > cutoff):
                peak_track = True  
                peak_start.append(theta[i])
                max = intensity[i]
                max_ind = i
        else:
            if(intensity[i] < cutoff):
                peak_end.append(theta[i])
                peak_max.append(theta[max_ind])
                peak_track = False
            elif(intensity[i] > max):
                max_ind = i
                max = intensity[i]
    for i in range(len(peak_start)):
        peak_avg.append((peak_start[i]+peak_end[i])/2)
    return peak_start, peak_end, peak_avg, peak_max

def get_peaks_ras_2(ras, cutoff, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    peak_start, peak_end, peak_avg, peak_max = get_peaks_2(theta_r, intensity_r, cutoff)
    print(peak_avg)
    print(peak_max)
    print(peak_start)
    print(peak_end)

def plot_ras_int_comp(ras, dotint, cutoff_r, cutoff_i):
    
    theta_r, intensity_r = file_read_ras(ras)
    theta_i, intensity_i, peaks_i = file_read_int(dotint, cutoff_i)
    
    start, end = restrict_range(theta_r, theta_i)
    theta_i = theta_i[start:end+1]
    intensity_i = intensity_i[start:end+1]
    intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)
    peaks_r = get_peaks(theta_r, intensity_r, cutoff_r)

    f, (ax, pks) = plt.subplots(2, 1, height_ratios = [10, 1])

    ntr = np.array(theta_r)
    nir = np.array(intensity_r)
    nti = np.array(theta_i)
    nii = np.array(intensity_i)
    
    ax.plot(ntr, nir, color = "cyan", label = "exp")
    ax.plot(nti, nii, color = "black", label = "VESTA")

    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (arb. units)")

    xticks1 = np.arange(theta_r[0], theta_r[len(theta_r)-1]+1, 5)
    xticks2 = np.arange(theta_r[0], theta_r[len(theta_r)-1]+1, 10)
    ax.set_xlim(theta_r[0], theta_r[len(theta_r)-1])
    #ax.set_xticks(xticks1, minor = True)
    #ax.set_xticks(xticks2)
    #ax.tick_params(which = "minor", length = 5)
    #ax.tick_params(which = "major", length = 8)
    ax.get_xaxis().set_visible(False)

    ax.set_title("Comparison with VESTA model")

    pks.bar(peaks_i, 1, width = 0.01)
    pks.bar(peaks_r, 1, width = 0.01, bottom = 1.1)

    pks.set_xticks(xticks1, minor = True)
    pks.set_xticks(xticks2)
    pks.tick_params(which = "minor", length = 5)
    pks.tick_params(which = "major", length = 8)
    pks.get_yaxis().set_visible(False)
    pks.set_xlim(theta_r[0], theta_r[len(theta_r)-1])
    
    pks.set_xlabel("2θ (degrees)")

    plt.subplots_adjust(hspace = 0.0)

    ax.legend()
    plt.show()

def plot_ras(ras, title, color, label, spacing, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot(theta_r, intensity_r, title, color, label, spacing)

def plot_ras_int_comp_2(ras, dotint, title, color, label, spacing, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    theta_i, intensity_i, peaks = file_read_int(dotint, 0)
    
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    start, end = restrict_range(theta_r, theta_i)
    theta_i = theta_i[start:end+1]
    intensity_i = intensity_i[start:end+1]

    theta = []
    intensity = []
    theta.append(theta_r)
    intensity.append(intensity_r)
    theta.append(theta_i)
    intensity.append(intensity_i)

    plotn(2, theta, intensity, title, color, label, spacing)

def plot_ras_gen(axes, ind, ras, title, color, label, spacing, axis_vis = True, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot_gen(axes, ind, theta_r, intensity_r, title, color, label, spacing, axis_vis)

def plot_peaks_ras_gen(axes, ind, ras, cutoff, spacing, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    peak_start, peak_end, peak_avg, peak_max = get_peaks_2(theta_r, intensity_r, cutoff)

    plot_peaks_gen(axes, ind, theta_r, peak_max, spacing)

def plot_poly_ras_gen(axes, ind, ras, deg, title, color, label, spacing, axis_vis = True, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot_poly_gen(axes, ind, theta_r, intensity_r, deg, title, color, label, spacing, axis_vis = True)

def plot_int_ras_gen(axes, ind, ras, title, color, label, spacing, axis_vis = True, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot_int_gen(axes, ind, theta_r, intensity_r, title, color, label, spacing, axis_vis)

def plot_haha_ras_gen(axes, ind, ras, title, color, label, spacing, axis_vis = True, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot_hahafunny_gen(axes, ind, theta_r, intensity_r, title, color, label, spacing, axis_vis)

def plot_haha2_ras_gen(axes, ind, ras, title, color, label, spacing, axis_vis = True, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot_hahafunny2_gen(axes, ind, theta_r, intensity_r, title, color, label, spacing, axis_vis)

def plot_hahafunnypeaks_ras_gen(axes, ind, ras, spacing, cutoff, amorphous = False):
    theta_r, intensity_r = file_read_ras(ras)
    if(amorphous):
        intensity_r = rmv_bckg(theta_r, intensity_r, 11)
    normalize(intensity_r)

    plot_hahafunny_peaks_gen(axes, ind, theta_r, intensity_r, spacing, cutoff)

def custom_plot_ras(axes, ras, title, color, label, spacing, cutoff, amorphous = False):
    plot_ras_gen(axes, 0, ras, title, color, label, spacing, axis_vis = False, amorphous = amorphous)
    plot_hahafunnypeaks_ras_gen(axes, 1, ras, spacing, cutoff, amorphous = amorphous)
    plt.subplots_adjust(hspace = 0.0)

def custom_smro_plot_ras(ras, cutoff, spacing, axes):
    custom_plot_ras(axes, ras, "SMRO", "blue", "SMRO", spacing, cutoff)

def custom_smro_hahaplot_ras(ras, title, spacing, axes):
    plot_haha2_ras_gen(axes, 0, ras, title, "cyan", "haha2", spacing, axis_vis = False)

def updatefig(i, files, spacing, axes):
    names = ["SMRO 25C", "SMRO 50C", "SMRO 75C", "SMRO 100C", "SMRO 125C", "SMRO 150C", 
             "SMRO 175C", "SMRO 200C", "SMRO 225C", "SMRO 250C", "SMRO 275C", "SMRO 300C"]
    for j in range(len(axes)):
        axes[j].clear()
    plot_ras_gen(axes, 0, files[i], names[i], "blue", names[i], spacing, axis_vis = False)
    plot_hahafunnypeaks_ras_gen(axes, 1, files[i], spacing, 15)
    plt.subplots_adjust(hspace = 0.0)
    plt.draw()

def custom_smro_animation_ras(files, spacing):
    fig, axes = plt.subplots(2, 1, height_ratios = [10, 1])
    test = anim.FuncAnimation(fig, updatefig, len(files), fargs = (files, spacing, axes))
    test.save("smro.gif", writer = 'pillow', fps=1)

def plot_int_gen(axes, ind, dotint, title, color, label, spacing, axis_vis = True):
    theta_i, intensity_i = file_read_int(dotint)
    normalize(intensity_i)

    plot_gen(axes, ind, theta_i, intensity_i, title, color, label, spacing, axis_vis)

def plot_hahafunnypeaks_int_gen(axes, ind, dotint, spacing, cutoff):
    theta_i, intensity_i = file_read_int(dotint)
    normalize(intensity_i)

    plot_hahafunny_peaks_gen(axes, ind, theta_i, intensity_i, spacing, cutoff)

def plot_file_gen(axes, ind, filename, title, color, label, spacing, offset = 0, axis_vis = True, amorphous = False):
    theta, intensity = file_read_gen(filename)
    if(amorphous):
        intensity = rmv_bckg(theta, intensity, 11)
    normalize(intensity)
    for i in range(len(intensity)):
        intensity[i] += offset

    plot_gen(axes, ind, theta, intensity, title, color, label, spacing, axis_vis)

def plot_hahafunnypeaks_file_gen(axes, ind, filename, spacing, cutoff, amorphous = False):
    theta, intensity = file_read_gen(filename)
    if(amorphous):
        intensity = rmv_bckg(theta, intensity, 11)
    normalize(intensity)

    plot_hahafunny_peaks_gen(axes, ind, theta, intensity, spacing, cutoff)

def custom_plot_gen(axes, filename, title, color, label, spacing, cutoff, offset = 0, amorphous = False):
    plot_file_gen(axes, 0, filename, title, color, label, spacing, offset, axis_vis = False, amorphous = amorphous)
    plot_hahafunnypeaks_file_gen(axes, 1, filename, spacing, cutoff, amorphous = amorphous)
    plt.subplots_adjust(hspace = 0.0)

def log(intensity):
    for i in range(len(intensity)):
        intensity[i] = math.log(intensity[i])

def color_map(fig, axes, plots, plot_ind, files, cmapys, title, ylabel, logsc = False):
    theta = []
    intensity = []
    t = []
    for i in plots[plot_ind]:
        theta_i, intensity_i = file_read_gen(files[plots[plot_ind][i]])
        if(logsc):
            log(intensity_i)    
        theta.append(theta_i)
        intensity.append(intensity_i)
    for i in range(len(theta)):
        t.append([])
        for j in range(len(theta[i])):
            t[i].append(cmapys[plot_ind][i])
    
    mesh = axes.pcolormesh(theta, t, intensity)
    fig.colorbar(mesh)
    axes.set_xlabel("2θ (degrees)")
    axes.set_ylabel(ylabel)
    axes.set_title(title)
    




if __name__ == "__main__":
    #plot_ras_int_comp("YBCO_annealedOfurnace_20260113_1p5dpm_SIDEA.ras", "test3.int", 20, 3)
    #plot_poly("YBCO_annealedOfurnace_20260113_1p5dpm_SIDEA.ras", 11)
    #plot_ras("C:/Users/Jeff/Documents/Research/XRD/SMRO/2026-01-14/SMRO_19-1_204_omega_correct_Ka1.ras", "SMRO", "blue", "SMRO", 1)
    #plot_ras_int_comp_2("C:/Users/Jeff/Documents/Research/XRD/SMRO/2026-01-14/SMRO_19-1_204_omega_correct_Ka1.ras", "C:/Users/Jeff/Documents/Research/XRD/SMRO/Sr2MgReO6_COD.int", "SMRO vs CIF", ["blue", "black"], ["SMRO", "VESTA"], 1)
    plot_comparison("C:/Users/Jeff/Documents/Research/XRD/SMRO/2026-01-14/SMRO_19-1_204_omega_correct_Ka1.ras", 5, 10, 1)
    plot_comparison("C:/Users/Jeff/Documents/Research/XRD/SMRO/2026-01-14/Post Temp Loop/SMRO_19-1_204_omega_Ka1_postheatloop.ras", 5, 10, 1)
    plot_comparison("C:/Users/Jeff/Documents/Research/XRD/SMRO/2026-01-14/Temp Loop/RAS/SMRO_19-1_204_CuKa1_2theta-scan_25_0025_0175-0C.ras", 5, 10, 1)

    