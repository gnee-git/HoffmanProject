# convert dcm to nii

import pandas as pd
import numpy as np
from glob import glob
import os
import pydicom as dcm
import nibabel as nib

ct_dirs = pd.read_csv("D:/Hoffman/CT_AllCentres/CT_Analyze/CT_tracker.txt", sep="\t", header=None).iloc[:,0].tolist()
outfiles = pd.read_csv("D:/Hoffman/CT_AllCentres/CT_Analyze/CT_tracker.txt", sep="\t", header=None).iloc[:,1].tolist()

for inpath,outpath in zip(ct_dirs, outfiles):
    
    print("Processing {0}".format(inpath))
    
    # read in the dicom files
    files = glob(os.path.join(inpath, "*"))
    # files.sort()
    ds = [dcm.dcmread(f) for f in files]
    
    # get the pixel data
    pixeldata = [d.pixel_array for d in ds]
    
    # get the spacing
    spacing = ds[0].SliceThickness
    
    # get the orientation
    orientation = ds[0].ImageOrientationPatient
    
    # get the position
    position = ds[0].ImagePositionPatient
    
    # get the number of slices
    nslices = len(ds)
    
    # create the affine matrix
    # affine = nib.affines.from_matvec(np.array([[orientation[0], orientation[3], 0, position[0]],[orientation[1], orientation[4], 0, position[1]],[orientation[2], orientation[5], 0, position[2]],[0, 0, spacing, 0]]))
    affine = np.eye(4)    
    # print(max(pixeldata[0].flatten()),min(pixeldata[0].flatten()))

    # create the nifti image
    img = nib.Nifti1Image(np.array(pixeldata), affine)
    
    # save the image
    nib.save(img, outpath+"_EyeAff.nii.gz")
    
    