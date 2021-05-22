import os
import pandas as pd
from PPG import p_p_g as ppg
from ECG import e_c_g as ecg
from GSR import g_s_r as gsr
# X:\ThesisMHR75\dataset\CLAS\Participants\Part1\all_separate ThesisMHR75\dataset\CLAS\Participants\Part1\by_block
for i in range(0, 61):
    numeric = str(i)
    paths = "ThesisMHR75\\dataset\\CLAS\\Participants\\Part"+numeric+"\\by_block"
    directory = os.path.join("X:\\",paths)
    for root,dirs,files in os.walk(directory):
        count = 0
        out = []
        out1 = []
        out2 = []
        print("Participants",i)
        for file in files:
            strf = "X:\\" + paths + "\\" + file
            print(strf,"\n")
            if(count ==63):
                break
            if count % 2 ==0:
                out = ecg(strf)
            else:
                out1 = gsr(strf)
                out2 = ppg(strf)
                print("File name =",file)
                print(out)
                print(out1)
                print(out2)
            count = count + 1
            print("progress =",count)
            # if file.endswith(".csv"):
            #     csvdir = "X:\\"+paths+"\\"+file

