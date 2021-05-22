### required libraries
import pandas as pd
import numpy as np
import scipy.signal as ss
import neurokit2 as nk
from scipy.stats import kurtosis, skew

fs = 256



def g_s_r(str):
    out = []

    ### Load CSV file
    df = pd.read_csv(str)
    gsr = np.array(df['gsr'])

    # 1st quantile , 2nd quantile , 3rd quantile feature
    feature_quantile = [np.quantile(gsr, .25), np.quantile(gsr, .5), np.quantile(gsr, .75)]
    out.append(round(feature_quantile[0], 3))
    out.append( round(feature_quantile[1], 3))
    out.append( round(feature_quantile[2], 3))

    # Interquartile range (IQR)
    out.append( round(feature_quantile[2] - feature_quantile[0], 3))

    # percentile
    per_2dot5 = np.percentile(gsr, 2.5)
    per_10 = np.percentile(gsr, 10)
    per_90 = np.percentile(gsr, 90)
    per_97dot5 = np.percentile(gsr, 97.5)
    per_gsr = [per_2dot5, per_10, per_90, per_97dot5]
    out.append(round(per_gsr[0], 3))
    out.append(round(per_gsr[1], 3))
    out.append(round(per_gsr[2], 3))
    out.append(round(per_gsr[3], 3))

    # Fequency domain feature Extraction in band (0-2.4)
    FFT = np.fft.fft(gsr)

    def bandpower(x, fs, fmin, fmax):
        f, Pxx = ss.periodogram(x, fs=fs, return_onesided=False)
        ind_min = np.argmax(f > fmin) - 1
        ind_max = np.argmax(f > fmax) - 1
        return np.trapz(Pxx[ind_min: ind_max], f[ind_min: ind_max])

    FFT_feature = bandpower(FFT, fs=256, fmin=0, fmax=2.4)
    out.append(round( FFT_feature))

    # other features 1- 9

    # used NK2 lib for GSR  feature extraction
    signals, info = nk.eda_process(gsr, sampling_rate=fs)

    # feature extraction
    df = pd.DataFrame.from_dict(info)
    out.append(len(df["SCR_Peaks"]))
    scr_amp = np.array(df["SCR_Amplitude"])
    out.append(round(np.nanmax(scr_amp), 3))
    out.append(round(np.nanmin(scr_amp), 3))
    scr_peaks = df["SCR_Peaks"]
    # Peaks
    df = signals.loc[signals["SCR_Peaks"] == 1]
    mcp = df["EDA_Phasic"]
    out.append(round(np.nanmean(mcp), 3))

    # ROOT Mean square of SCR
    rms = np.sqrt(np.nanmean(df["EDA_Phasic"] ** 2))
    out.append(round(rms, 3))

    absmcp = np.absolute(mcp)
    std = np.std(absmcp)
    out.append(round(std, 3))
    out.append(round(np.nanmean(absmcp), 3))
    out.append(round(skew(mcp), 3))
    out.append(round(kurtosis(mcp), 3))

    return out
