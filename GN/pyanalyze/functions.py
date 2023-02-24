# FUNCTIONS FROM BOOK1

import pydicom as dcm
import os
import nibabel as nib
import numpy as np
from glob import glob
from tqdm import tqdm, tqdm_notebook
import dcmstack
import sys
from IPython.display import clear_output
import pandas as pd
import shutil
import matplotlib.pyplot as plt
# suppress warnings
import warnings
warnings.filterwarnings('ignore')
from pyanalyze.classes import *

# Write a function to determine whether a given path is equivalent to or a subpath of the other
def isPathOrSubpath(path, subpath):
    path = os.path.abspath(path)
    subpath = os.path.abspath(subpath)
    if path == subpath:
        return True
    elif path in subpath:
        return True
    else:
        return False

def get_3d_array_from_dicom_folder(folder):
    # Get a list of all the dicom files in the folder
    files = os.listdir(folder)
    # Create a list to hold the dicom objects
    dicoms = []
    # Loop over the files and read in the dicom objects
    for file in files:
        dicoms.append(dcm.dcmread(folder + file))
    # Sort the dicoms by InstanceNumber
    dicoms.sort(key=lambda x: int(x.InstanceNumber))
    # Create a list to hold the pixel arrays
    pixel_arrays = []
    # Loop over the dicoms and append the pixel array to pixel_arrays
    for d in dicoms:
        pixel_arrays.append(d.pixel_array)
    # Convert pixel_arrays to a numpy array
    pixel_arrays = np.array(pixel_arrays)
    # Return the pixel_arrays array
    return pixel_arrays


def get_roi_mean(an_impath,an_roi):
    imdata,_,_,_ = LoadImage(an_impath)
    return np.mean(np.multiply(an_roi,imdata))

def get_roi_std(an_impath,an_roi):
    imdata,_,_,_ = LoadImage(an_impath)
    return np.std(np.multiply(an_roi,imdata))


def get_dcm_pixel_spacing(dcm_file):
    if os.path.isdir(dcm_file):
        dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
    hdr = dcm.dcmread(dcm_file)
    x,y = hdr.PixelSpacing
    z = hdr.SliceThickness
    return x,y,z

def get_dcm_matrix_size(dcm_file):
    if os.path.isdir(dcm_file):
        dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
    hdr = dcm.dcmread(dcm_file)
    if hasattr(hdr,"NumberOfSlices"):
        return hdr.Rows,hdr.Columns,hdr.NumberOfSlices
    else:
        # z is the number of files in the folder
        z = len(glob(os.path.join(os.path.dirname(dcm_file),"*")))
        return hdr.Rows,hdr.Columns,z
    
def get_manufacturer(dcm_file):
    if os.path.isdir(dcm_file):
        dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
    hdr = dcm.dcmread(dcm_file)
    return hdr.Manufacturer

def get_iterations_subsets(dcm_file):
    if os.path.isdir(dcm_file):
        dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
    # else:
    #     return np.nan,np.nan
    hdr = dcm.dcmread(dcm_file)
    if not hasattr(hdr,"Manufacturer"):
        return np.nan,np.nan
    else:
        manufacturer = hdr.Manufacturer
        if manufacturer == "GE MEDICAL SYSTEMS":
            if any([x in hdr for x in [(0x000910b2),(0x000910b3)]]):
                return int(hdr[(0x000910b2)].value),int(hdr[(0x000910b3)].value)
            else:
                return np.nan,np.nan
        elif manufacturer == "SIEMENS":
            if (0x0054,0x1103) not in hdr:
                return np.nan,np.nan
            else:
                info = hdr[0x0054,0x1103].value.split(" ")[-1]
                return int(info.split("i")[0]),int(info.split("i")[1].strip("s"))
        elif manufacturer == "Philips Medical Systems":
            return 3,33
        
def BoolRandomsOn(dcm_file):
    try:
        if os.path.isdir(dcm_file):
            dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
        else:
            return False
        if os.path.isdir(dcm_file):
            return False
        hdr = dcm.dcmread(dcm_file)
        if (0x0054,0x1100) not in hdr:
            return False
        else:
            manufacturer = hdr.Manufacturer
            if manufacturer == "GE MEDICAL SYSTEMS":
                if hdr[0x0054,0x1100].value == "SING":
                    return True
                elif hdr[0x0054,0x1100].value == "DLYD":
                    return True
                else:
                    return False
            elif manufacturer == "SIEMENS":
                if hdr[0x0054,0x1100].value == "DLYD":
                    return True
                else:
                    return False
            elif manufacturer == "Philips Medical Systems":
                if hdr[0x0054,0x1100].value == "DLYD":
                    return True
                else:
                    return False
    except:
        return False
        
def BoolScatterOn(dcm_file):
    try:
        if os.path.isdir(dcm_file):
            dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
        else:
            return False
        if os.path.isdir(dcm_file):
            return False
        hdr = dcm.dcmread(dcm_file)
        if (0x0054,0x1105) not in hdr:
            return False
        else:
            if hdr[0x0054,0x1105].value != "NONE":
                return True
            else:
                return False
    except:
        return False
    
def BoolAttenuationOn(dcm_file):
    try:
        if os.path.isdir(dcm_file):
            dcm_file = os.path.join(dcm_file,os.listdir(dcm_file)[0])
        else:
            return False
        if os.path.isdir(dcm_file):
            return False
        hdr = dcm.dcmread(dcm_file)
        if (0x0054,0x1101) not in hdr:
            return False
        else:
            if hdr[0x0054,0x1101].value != "NONE":
                return True
            else:
                return False
    except:
        return False