### required libraries
import pandas as pd
import numpy as np
import scipy.signal as ss
import neurokit2 as nk
from scipy.stats import kurtosis, skew

fs = 256

### Load CSV file
df = pd.read_csv("2_gsr_ppg_mathtest.csv")
gsr = np.array(df['gsr'])

# 1st quantile , 2nd quantile , 3rd quantile feature
feature_quantile = [np.quantile(gsr, .25), np.quantile(gsr, .5), np.quantile(gsr, .75)]
print("GSR Q1 =", round(feature_quantile[0], 3))
print("GSR Q2 =", round(feature_quantile[1], 3))
print("GSR Q3 =", round(feature_quantile[2], 3))

# Interquartile range (IQR)
print("Interquartile range =", round(feature_quantile[2] - feature_quantile[0], 3))

# percentile
per_2dot5 = np.percentile(gsr, 2.5)
per_10 = np.percentile(gsr, 10)
per_90 = np.percentile(gsr, 90)
per_97dot5 = np.percentile(gsr, 97.5)
per_gsr = [per_2dot5, per_10, per_90, per_97dot5]
print("Percentile 2.5 =", round(per_gsr[0], 3))
print("Percentile 10 =", round(per_gsr[1], 3))
print("Percentile 90 =", round(per_gsr[2], 3))
print("Percentile 97.5 =", round(per_gsr[3], 3))

# Fequency domain feature Extraction in band (0-2.4)
FFT = np.fft.fft(gsr)


def bandpower(x, fs, fmin, fmax):
    f, Pxx = ss.periodogram(x, fs=fs, return_onesided=False)
    ind_min = np.argmax(f > fmin) - 1
    ind_max = np.argmax(f > fmax) - 1
    return np.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])


FFT_feature = bandpower(FFT, fs=256, fmin=0, fmax=2.4)
print("band in power (0-2.4)Hz =", FFT_feature)

# other features 1- 9
print("others 1 - 9 ")

# used NK2 lib for GSR  feature extraction
signals, info = nk.eda_process(gsr, sampling_rate=fs)

# Visualise the processing
nk.eda_plot(signals, sampling_rate=256)

# feature extraction
df = pd.DataFrame.from_dict(info)
print("Number of peaks =", len(df["SCR_Peaks"]))
scr_amp = np.array(df["SCR_Amplitude"])
print("Max Amplitude of the peak =", round(np.max(scr_amp), 3))
print("Min Amplitude of the peak =", round(np.min(scr_amp), 3))
scr_peaks = df["SCR_Peaks"]
# Peaks
df = signals.loc[signals["SCR_Peaks"] == 1]
mcp = df["EDA_Phasic"]
print("Mean conductance of peaks =", round(np.mean(mcp), 3))

# ROOT Mean square of SCR
rms = np.sqrt(np.mean(df["EDA_Phasic"] ** 2))
print("RMS =", round(rms, 3))

absmcp = np.absolute(mcp)
std = np.std(absmcp)
print("STD of absolute value of peaks =", round(std, 3))
print("Mean of absolute value of Peaks =", round(np.mean(absmcp), 3))
print("Skewness of Peaks =", round(skew(mcp), 3))
print("Kurtosis of Peaks =", round(kurtosis(mcp), 3))
