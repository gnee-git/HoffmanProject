# Author: George Needham

# Classes for pyanalyze
# pyanalyze is a package for loading and converting Analyze images

# This file contains the following classes:
#  - AnalyzeImg

# This file contains the following functions:
#  - LoadImage
#  - AddImage
#  - ImageMultiply
#  - ConstantMultiply


# Base imports for the package
import numpy as np
import nibabel as nib
import os
import pandas as pd
from matplotlib.pyplot import imshow


SCANNERS = {"GE":["Discovery 690",
                "Discovery 710",
                "Discovery STE 8",
                "Discovery STE 12",
                "Discovery ST",
                "Discovery VCT"],
            "Philips":["Gemini TF 64"],
            "Siemens":["Biograph mCT",
                    "Biograph Vision",
                    "HRRT",
                    "Biograph TruePoint"]
}

REF_FILE = pd.read_csv("D:/Hoffman/GN/MasterRefDF.csv")

def LoadImage(filename):
    
    if not os.path.isfile(filename):
        raise FileNotFoundError("File not found")
    if not filename.endswith(".hdr"):
        raise ValueError("File must be an Analyze image .hdr file")
    
    else:
        headername = filename
        imagename = filename[:-4] + ".img"
        data = nib.AnalyzeImage.from_filename(imagename).get_fdata()
        np.nan_to_num(data,copy=False)
        header = nib.AnalyzeHeader.from_fileobj(open(headername, 'rb'))
        
    return data, header, headername, imagename

class AnalyzeImg:

# global variables:
    format = None # WILL BE PET or CT
    data = None # NUMPY ARRAY OF IMAGE DATA - UNADJUSTED FROM DICOM
    header = None # NIBABEL HEADER OBJECT
    headername = None # NAME OF HEADER FILE
    imagename = None # NAME OF IMAGE FILE
    type = "AnalyzeImage" # TYPE OF OBJECT
    shape = None # SHAPE OF IMAGE DATA ARRAY (X,Y,Z)
    centre = None # NAME OF CENTRE
    seriesnumber = None # ASSIGNED NUMBER OF IMAGE WITHIN CENTRE SERIES
    activity = None # ACTIVITY AS PER CENTRE DOC. (MBq)
    scanner = None # SCANNER USED TO ACQUIRE IMAGE
    skull = None # BOOLEAN, SKULL INSERT USED OR NOT
    reslice = None # TUPLE OF RESLICE PARAMETERS (RESLICE T/F, RESLICE PARAMETERS...)
        
    def __init__(self, filename):
        self.filename = filename
        self.data, self.header, self.headername, self.imagename = LoadImage(filename)
        self.shape = self.data.shape
        self.centre = self.filename.split("/")[-1].split("_")[-2]
        self.seriesnumber = self.filename.split("/")[-1].split("_")[-1].split(".")[0]
        # print("AnalyzeImage object created for file " + self.headername)
        # print("Centre: " + self.centre)
        # print("Series Number: " + self.seriesnumber)
        # print(REF_FILE.loc[(REF_FILE["Centre"] == self.centre) & (REF_FILE["SeriesNum"] == int(self.seriesnumber))])
        self.activity = REF_FILE.loc[(REF_FILE["Centre"] == self.centre) & (REF_FILE["SeriesNum"] == self.seriesnumber),"Activity"].values
        self.scanner = REF_FILE.loc[(REF_FILE["Centre"] == self.centre) & (REF_FILE["SeriesNum"] == self.seriesnumber),"Scanner"].values
        self.skull = REF_FILE.loc[(REF_FILE["Centre"] == self.centre) & (REF_FILE["SeriesNum"] == self.seriesnumber),"Skull"].values
        if "reslice" in filename:
            self.reslice = True
        else:
            self.reslice = False
            
        print("AnalyzeImage object created for file " + self.headername)

        

    # def __init__(self):
    #     self.data = np.array([])

        
    def __str__(self):
        return "AnalyzeImage object for file " + self.headername
    
    def SaveImageData(self,filename):
        if not filename.endswith(".npy"):
            filename = filename + ".npy"
        np.save(filename,self.data.get_fdata())
        return "Image data saved to " + filename
        
    def ShowSlice(self,slice):
        imshow(self.data[:,:,slice],cmap='gray')
    

def AddImage(image1,image2):
    if image1.type == "AnalyzeImage" and image2.type == "AnalyzeImage":
        if image1.data.shape == image2.data.shape:
            return image1.data + image2.data
        else:
            raise ValueError("Images must be the same size")
    else:
        return TypeError("Both objects must be AnalyzeImage objects")

def ImageMultiply(image1,image2):
    if image1.type == "AnalyzeImage" and image2.type == "AnalyzeImage":
        if image1.data.shape == image2.data.shape:
            return image1.data * image2.data
        else:
            raise ValueError("Images must be the same size")
    else:
        return TypeError("Both objects must be AnalyzeImage objects")
    
def ConstantMultiply(image1,constant):
    if image1.type == "AnalyzeImage":
        return image1.data * constant
    else:
        return TypeError("Both objects must be AnalyzeImage objects")
    
