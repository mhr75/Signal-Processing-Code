### required libraries
import pandas as pd
import numpy as np
import math
import neurokit2 as nk
from PPG_FEATURES import ppg_process,ppg_plot
import matplotlib.pyplot as plt
fs = 256


def p_p_g(str):
    out = []

    ### Load CSV file
    df = pd.read_csv(str)
    ppg = np.array(df['ppg'])

    # Plotting PPG
    signals, info = ppg_process(ppg, sampling_rate=fs)

    ppg = nk.ppg_clean(ppg,sampling_rate=256)
    # HRV analysis
    rpeaks = nk.ppg_findpeaks(ppg,sampling_rate=256)
    hrv = nk.hrv(rpeaks, sampling_rate=256, show=False)

    #Feature Extraction
    rri = np.diff(rpeaks['PPG_Peaks']) / fs * 1000
    min_nni = np.nanmin(rri)
    max_nni = np.nanmax(rri)
    vlf = round(hrv.iloc[0, 14], 3)
    hf = round(hrv.iloc[0, 16], 3)
    lf = round(hrv.iloc[0, 15], 3)
    if math.isnan(vlf):
        vlf = 0
    if math.isnan(lf):
        lf = 0
    if math.isnan(hf):
        hf = 0

    ### Print Statistical Features
    out.append(round(np.nanmean(signals["PPG_Rate"]), 3))
    out.append(round(min_nni, 3))
    out.append(round(max_nni, 3))
    out.append(round(hrv.iloc[0,1], 3))
    out.append(round(hrv.iloc[0,9], 3))
    out.append(round(hrv.iloc[0,2], 3))
    out.append(round(hrv.iloc[0,0], 3))
    out.append(round(hrv.iloc[0,3], 3))
    out.append(round(hrv.iloc[0, 22], 3))
    out.append(round(hrv.iloc[0, 23], 3))
    out.append(round(hrv.iloc[0, 14], 3))
    out.append(round(hrv.iloc[0, 15], 3))
    out.append(round(hrv.iloc[0, 16], 3))
    out.append(round(hrv.iloc[0, 19], 3))
    out.append(round(hrv.iloc[0, 20], 3))
    if lf + hf + vlf == 0:
        out.append(0)
        out.append(0)
        out.append(0)
    else:
        out.append(round(vlf / (lf + hf + vlf), 3))
        out.append(round(lf / (lf + hf + vlf), 3))
        out.append(round(hf / (lf + hf + vlf), 3))
    return out



