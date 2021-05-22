# Load NeuroKit and other useful packages
import neurokit2 as nk
import numpy as np
import pandas as pd
import math

fs = 256    # sample ratre

def e_c_g(str):
    out = []

    ### Load CSV file
    df = pd.read_csv(str)
    df = np.array(df['ecg2'])

    # Clean ECG
    ecg = nk.ecg_clean(ecg_signal=df, sampling_rate=fs)

    # Default processing pipeline
    signals, info = nk.ecg_process(df, sampling_rate=fs)

    # HRV analysis
    rpeaks = nk.ecg_findpeaks(ecg, sampling_rate=256)
    hrv = nk.hrv(rpeaks, sampling_rate=256, show=False)

    # Feature Extraction
    rri = np.diff(rpeaks['ECG_R_Peaks']) / fs * 1000
    min_nni = np.min(rri)
    max_nni = np.max(rri)
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
    out.append(round(np.nanmean(signals['ECG_Rate']), 3))
    out.append(round(min_nni, 3))
    out.append(round(max_nni, 3))
    out.append(round(hrv.iloc[0, 1], 3))
    out.append(round(hrv.iloc[0, 9], 3))
    out.append(round(hrv.iloc[0, 2], 3))
    out.append(round(hrv.iloc[0, 0], 3))
    out.append(round(hrv.iloc[0, 3], 3))
    out.append(round(hrv.iloc[0, 22], 3))
    out.append(round(hrv.iloc[0, 23], 3))
    out.append(round(hrv.iloc[0, 14], 3))
    out.append(round(hrv.iloc[0, 15], 3))
    out.append(round(hrv.iloc[0, 16], 3))
    out.append(round(hrv.iloc[0, 19], 3))
    out.append(round(hrv.iloc[0, 20], 3))
    if lf+hf+vlf == 0 :
        out.append(0)
        out.append(0)
        out.append(0)
    else:
        out.append(round(vlf / (lf + hf + vlf), 3))
        out.append(round(lf / (lf + hf + vlf), 3))
        out.append(round(hf / (lf + hf + vlf), 3))
    return out

