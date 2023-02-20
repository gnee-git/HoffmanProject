# imagej_macromaker.py

# macrotext is here
TEXT = """
File.openSequence("{0}");
run("Analyze... ", "save={1}");
close();"""

# import both glob and os
from glob import glob
import os
import pandas as pd
import pydicom as dcm
import nibabel as nib
import numpy as np

# # create the list of all subdirs using os.walk
l = []
for r,ds,_ in os.walk("D:/Hoffman/CT_AllCentres"):
    for d in ds:
        l.append(os.path.join(r,d))
ct_dirs = [os.path.abspath(c) for c in l]

parentdirs = [os.path.abspath(c) for c in glob("D:/Hoffman/CT_AllCentres/*")] # list of all parent dirs
ct_dirs = [c for c in ct_dirs if os.path.isdir(c) and c not in parentdirs] # remove the parent dirs from the list
ct_dirs = [c for c in ct_dirs if len(os.listdir(c)) > 3 and len(os.listdir(c))<200] # remove the dirs with less than 3 files (empty dirs and topograms)

# write out macro to FILENAME
FILENAME = "ct_analyze_conv.txt"

# iterate through the list of dirs and add the macro text to the file
with open(FILENAME, "w") as f:
    # track which ctfile has which series code
    tracker = []
    centre = ""
    centrecount = 1
    for path in ct_dirs:

        path = path.replace("\\", "/")
        print("Processing {0}".format(path))
        if path.split("/")[3][1:] == centre:
            centrecount+=1
        else: 
            centre = path.split("/")[3][1:]
            centrecount = 1
        outfilename = "D:/Hoffman/CT_AllCentres/CT_Analyze/{0}_CT_{1}".format(centre, centrecount)
        tracker.append((path, outfilename))
        f.write(TEXT.format(path, outfilename))
        
    
    # write out the tracker to a file
    with open("D:/Hoffman/CT_AllCentres/CT_Analyze/CT_tracker.txt", "w") as f:
        for t in tracker:
            f.write("{0}\t{1}\n".format(t[0], t[1]))
            