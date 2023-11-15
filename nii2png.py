#!/usr/bin/env python
#########################################
#       nii2png for Python 3.7          #
#         NIfTI Image Converter         #
#                v0.2.9                 #
#                                       #
#     Written by Alexander Laurence     #
# http://Celestial.Tokyo/~AlexLaurence/ #
#    alexander.adamlaurence@gmail.com   #
#              09 May 2019              #
#              MIT License              #
#########################################

import scipy, numpy, shutil, os, nibabel
import sys, getopt

import imageio
import os.path
from PIL import Image

def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print('nii2png.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('nii2png.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
        elif opt in ("-o", "--output"):
            outputfile = arg

    # set fn as your 4d nifti file
    image_array = nibabel.load(inputfile).get_fdata()

    # if 3D image inputted
    if len(image_array.shape) == 3:
        # set 4d array dimension values
        nx, ny, nz = image_array.shape

        # set destination folder
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)

        if image_array.shape[1] == image_array.shape[2]:
            total_slices = image_array.shape[0]
        elif image_array.shape[0] == image_array.shape[2]:
            total_slices = image_array.shape[1]
        elif image_array.shape[0] == image_array.shape[1]:
            total_slices = image_array.shape[2]
        else:
            print('Unsupported resolution')

        # iterate through slices)
        for current_slice in range(0, total_slices):
            # alternate slices
            if image_array.shape[1] == image_array.shape[2]:
                data = image_array[current_slice, :, :]
            elif image_array.shape[0] == image_array.shape[2]:
                data = image_array[:, current_slice, :]
            elif image_array.shape[0] == image_array.shape[1]:
                data = image_array[:, :, current_slice]

            #alternate slices and save as png
            image_name = inputfile[:-4] + "_z" + "{:0>3}".format(str(current_slice+1))+ ".png"
            imageio.imwrite(image_name, Image.fromarray(data).convert("L"))
    else:
        print('Not a 3D Image. Please try again.')

# call the function to start the program
if __name__ == "__main__":
   main(sys.argv[1:])
