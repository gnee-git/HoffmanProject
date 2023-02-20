import time
import matplotlib.pyplot as plt
import nibabel as nib
from glob import glob
#suppress warnings
# import warnings
# warnings.filterwarnings("ignore")

# iterate over all of the images in the NiftiImages folder
# open the image in nibabel, display the central slice, and ask the user if the image is inverted L-R
# record the y/n response in a text file alongside the image name
# close the image and flush the display output
for img in glob("D:/Hoffman/AnalyzeImages/Cambridge_*.img"):
    
    # # if "Aberdeen" or "Cambridge" in img:
    # #     print(img)
    # #     continue
    
    # # nii = nib.load(img)
    # print(img)
    # # Use nibabel to load the image header
    print(img)
    hdr = nib.AnalyzeHeader.from_fileobj(open(img.replace(".img",".hdr"), 'rb'))
    imdata = nib.AnalyzeImage.from_filename(img)
    nii = nib.Nifti1Image(imdata.get_fdata(), None, hdr)
    plt.imshow(nii.get_fdata()[nii.shape[0]//2,:,:], cmap="gray",aspect=0.3)
    plt.show(block=False)
    plt.pause(3)
    plt.close('all')
    # plt.show()
    # print(img)
    # ans = input("Is the image inverted L-R? (y/n): ")
    # with open("D:/Hoffman/GN/InvertedImages.txt", "a") as f:
    #     f.write(img + " " + ans + "\n")
    # plt.close()
    # sys.stdout.flush()
    
