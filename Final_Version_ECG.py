# Load NeuroKit and other useful packages
import neurokit2 as nk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
fs = 256    # sample ratre

### Load CSV file
df = pd.read_csv("2_ecg_mathtest.csv")
df = np.array(df['ecg2'])

# Clean ECG
ecg = nk.ecg_clean(ecg_signal=df, sampling_rate=fs)

# Default processing pipeline
signals, info = nk.ecg_process(df, sampling_rate=fs)
featured =nk.ecg_intervalrelated(signals,sampling_rate=fs)

# Visualize
plot = nk.ecg_plot(signals,sampling_rate=256)
plt.show()

# HRV analysis
rpeaks = nk.ecg_findpeaks(ecg,sampling_rate=256)
hrv =nk.hrv(rpeaks, sampling_rate=256, show=True)
plt.show()

#Feature Extraction
rri = np.diff(rpeaks['ECG_R_Peaks']) / fs * 1000
min_nni = np.min(rri)
max_nni = np.max(rri)

### Print Statistical Features
print("Mean HR =", round(featured.iloc[0, 0], 3))
print("Min NNI =", round(min_nni, 3))
print("Max NNI =", round(max_nni, 3))
print("Mean NNI =", round(hrv.iloc[0,1], 3))
print("pNN50 =", round(hrv.iloc[0,9], 3))
print("sdnn =", round(hrv.iloc[0,2], 3))
print("RMSSD =", round(hrv.iloc[0,0], 3))
print("Standard deviation of the difference of successive NN intervals =", round(hrv.iloc[0,3], 3))
print("SD1(Short term variability) =", round(hrv.iloc[0, 22], 3))
print("SD2(Long term variability) =", round(hrv.iloc[0, 23], 3))
print("Power in (0-0.04) Hz =", round(hrv.iloc[0, 14], 3))
print("Power in (0.04-0.15) Hz =", round(hrv.iloc[0, 15], 3))
print("Power in (0.15-0.4) Hz =", round(hrv.iloc[0, 16], 3))
print("Low frequency normalized value =", round(hrv.iloc[0, 19], 3))
print("High frequency normalized value =", round(hrv.iloc[0, 20], 3))
vlf = round(hrv.iloc[0, 14], 3)
if math.isnan(vlf):
    vlf = 0
lf = round(hrv.iloc[0, 15], 3)
hf = round(hrv.iloc[0, 16], 3)
print("vlf percentage in power =", round(vlf/(lf+hf+vlf), 3), "%")
print("lf percentage in power =", round(lf/(lf+hf+vlf), 3), "%")
print("hf percentage in power =", round(hf/(lf+hf+vlf), 3), "%")

