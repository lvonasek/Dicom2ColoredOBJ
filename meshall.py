import glob
import gzip
import imageio
import nibabel
import numpy
import png
import pydicom
import re
import os
import shutil
import sys
import vtk

from PIL import Image


def nii_2_mesh(filename_nii, filename_obj, label):

    # read the file
    reader = vtk.vtkNIFTIImageReader()
    reader.SetFileName(filename_nii)
    reader.Update()

    # apply marching cube surface generation
    surf = vtk.vtkDiscreteMarchingCubes()
    surf.SetInputConnection(reader.GetOutputPort())
    surf.SetValue(0, label) # use surf.GenerateValues function if more than one contour is available in the file
    surf.Update()
    
    # smoothing the mesh
    smoother= vtk.vtkWindowedSincPolyDataFilter()
    smoother.SetInputConnection(surf.GetOutputPort())
    smoother.SetNumberOfIterations(100) 
    smoother.NonManifoldSmoothingOn()
    smoother.NormalizeCoordinatesOn() #The positions can be translated and scaled such that they fit within a range of [-1, 1] prior to the smoothing computation
    smoother.GenerateErrorScalarsOn()
    smoother.Update()

    # save the output
    writer = vtk.vtkOBJWriter()
    writer.SetInputConnection(smoother.GetOutputPort())
    writer.SetFileName(filename_obj)
    writer.Write()


def nii2png(inputfile, outputfile):

    # set fn as your 4d nifti file
    image_array = nibabel.load(inputfile).get_fdata()

    # if 3D image inputted
    orientation = -1
    if len(image_array.shape) == 3:
        # set 4d array dimension values
        nx, ny, nz = image_array.shape

        # set destination folder
        if not os.path.exists(outputfile):
            os.makedirs(outputfile)

        # TODO: support non-square resolutions
        if image_array.shape[1] == image_array.shape[2]:
            total_slices = image_array.shape[0]
            orientation = 0
        elif image_array.shape[0] == image_array.shape[2]:
            total_slices = image_array.shape[1]
            orientation = 1
        elif image_array.shape[0] == image_array.shape[1]:
            total_slices = image_array.shape[2]
            orientation = 2
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
    return orientation
    

if __name__ == '__main__':

    # decode dicom images
    images = []
    if len(sys.argv) > 1:
        for file in numpy.sort(glob.glob(sys.argv[1] + "/*")):
            if file[-3:] == "png":
                continue
            ds = pydicom.dcmread(file)
            shape = ds.pixel_array.shape
            image_2d = ds.pixel_array.astype(float)
            image_2d_scaled = numpy.uint32((numpy.maximum(image_2d,0) / image_2d.max()) * 255.0)
            image_2d_colored = numpy.zeros([shape[0], shape[1] * 3], dtype=numpy.uint32)
            for y in range(shape[1]):
                image_2d_colored[:, y * 3 + 0] = image_2d_scaled[:, y]
                image_2d_colored[:, y * 3 + 1] = image_2d_scaled[:, y]
                image_2d_colored[:, y * 3 + 2] = image_2d_scaled[:, y]
            images.append(image_2d_colored)

    # palette from 3DSlicer/SlicerTotalSegmentator
    colors = [
        [255, 0, 255],  #0
        [157, 108, 162],#1
        [185, 102, 83], #2
        [135, 150, 98], #3
        [221, 130, 101],#4
        [216, 132, 105],#5
        [249, 180, 111],#6
        [249, 186, 150],#7
        [172, 138, 150],#8
        [224, 186, 162],#9
        [202, 164, 140],#10
        [211, 171, 143],#11
        [182, 228, 255],#12
        [62, 162, 114], #13
        [205, 167, 142],#14
        [255, 253, 229],#15
        [204, 168, 143],#16
        [222, 154, 132],#17
        [230, 158, 140],#18
        [205, 205, 100],#19
        [212, 188, 102],#20
        [212, 208, 122],#21
        [226, 202, 134],#22
        [255, 255, 207],#23
        [206, 110, 84], #24
        [224, 97, 76],  #25
        [186, 77, 64],  #26
        [196, 121, 79], #27
        [216, 101, 89], #28
        [216, 101, 69], #29
        [0, 112, 165],  #30
        [10, 105, 155], #31
        [0, 151, 206],  #32
        [0, 161, 196],  #33
        [0, 141, 226],  #34
        [216, 101, 79], #35
        [205, 179, 108],#36
        [255, 238, 170],#37
        [244, 214, 49], #38
        [188, 95, 76],  #39
        [178, 105, 76], #40
        [178, 95, 86],  #41
        [171, 85, 68],  #42
        [188, 95, 76],  #43
        [250, 250, 225],#44
        [241, 213, 144],#45
        [253, 232, 158],#46
        [244, 217, 154],#47
        [111, 184, 210],#48
        ]

    # mapping from 3DSlicer/SlicerTotalSegmentator
    mapping = {}
    mapping["spleen.nii.gz"] = 1
    mapping["kidney_right.nii.gz"] = 2
    mapping["kidney_left.nii.gz"] = 2
    mapping["gallbladder.nii.gz"] = 3
    mapping["liver.nii.gz"] = 4
    mapping["stomach.nii.gz"] = 5
    mapping["pancreas.nii.gz"] = 6
    mapping["adrenal_gland_right.nii.gz"] = 7
    mapping["adrenal_gland_left.nii.gz"] = 7
    mapping["lung_upper_lobe_left.nii.gz"] = 8
    mapping["lung_lower_lobe_left.nii.gz"] = 9
    mapping["lung_upper_lobe_right.nii.gz"] = 8
    mapping["lung_middle_lobe_right.nii.gz"] = 10
    mapping["lung_lower_lobe_right.nii.gz"] = 9
    mapping["esophagus.nii.gz"] = 11
    mapping["trachea.nii.gz"] = 12
    mapping["thyroid_gland.nii.gz"] = 13
    mapping["small_bowel.nii.gz"] = 14
    mapping["duodenum.nii.gz"] = 15
    mapping["colon.nii.gz"] = 16
    mapping["urinary_bladder.nii.gz"] = 17
    mapping["prostate.nii.gz"] = 18
    mapping["kidney_cyst_left.nii.gz"] = 19
    mapping["kidney_cyst_right.nii.gz"] = 19
    mapping["sacrum.nii.gz"] = 20
    mapping["vertebrae_S1.nii.gz"] = 21
    mapping["vertebrae_L5.nii.gz"] = 20
    mapping["vertebrae_L4.nii.gz"] = 20
    mapping["vertebrae_L3.nii.gz"] = 20
    mapping["vertebrae_L2.nii.gz"] = 20
    mapping["vertebrae_L1.nii.gz"] = 20
    mapping["vertebrae_T12.nii.gz"] = 22
    mapping["vertebrae_T11.nii.gz"] = 22
    mapping["vertebrae_T10.nii.gz"] = 22
    mapping["vertebrae_T9.nii.gz"] = 22
    mapping["vertebrae_T8.nii.gz"] = 22
    mapping["vertebrae_T7.nii.gz"] = 22
    mapping["vertebrae_T6.nii.gz"] = 22
    mapping["vertebrae_T5.nii.gz"] = 22
    mapping["vertebrae_T4.nii.gz"] = 22
    mapping["vertebrae_T3.nii.gz"] = 22
    mapping["vertebrae_T2.nii.gz"] = 22
    mapping["vertebrae_T1.nii.gz"] = 22
    mapping["vertebrae_C7.nii.gz"] = 23
    mapping["vertebrae_C6.nii.gz"] = 23
    mapping["vertebrae_C5.nii.gz"] = 23
    mapping["vertebrae_C4.nii.gz"] = 23
    mapping["vertebrae_C3.nii.gz"] = 23
    mapping["vertebrae_C2.nii.gz"] = 23
    mapping["vertebrae_C1.nii.gz"] = 23
    mapping["heart.nii.gz"] = 24
    mapping["aorta.nii.gz"] = 25
    mapping["pulmonary_vein.nii.gz"] = 26
    mapping["brachiocephalic_trunk.nii.gz"] = 27
    mapping["subclavian_artery_right.nii.gz"] = 28
    mapping["subclavian_artery_left.nii.gz"] = 29
    mapping["common_carotid_artery_right.nii.gz"] = 30
    mapping["common_carotid_artery_left.nii.gz"] = 31
    mapping["brachiocephalic_vein_left.nii.gz"] = 32
    mapping["brachiocephalic_vein_right.nii.gz"] = 33
    mapping["atrial_appendage_left.nii.gz"] = 33
    mapping["superior_vena_cava.nii.gz"] = 34
    mapping["inferior_vena_cava.nii.gz"] = 32
    mapping["portal_vein_and_splenic_vein.nii.gz"] = 32
    mapping["iliac_artery_left.nii.gz"] = 35
    mapping["iliac_artery_right.nii.gz"] = 35
    mapping["iliac_vena_left.nii.gz"] = 32
    mapping["iliac_vena_right.nii.gz"] = 32
    mapping["humerus_left.nii.gz"] = 36
    mapping["humerus_right.nii.gz"] = 36
    mapping["scapula_left.nii.gz"] = 20
    mapping["scapula_right.nii.gz"] = 20
    mapping["clavicula_left.nii.gz"] = 36
    mapping["clavicula_right.nii.gz"] = 36
    mapping["femur_left.nii.gz"] = 37
    mapping["femur_right.nii.gz"] = 37
    mapping["hip_left.nii.gz"] = 20
    mapping["hip_right.nii.gz"] = 20
    mapping["spinal_cord.nii.gz"] = 38
    mapping["gluteus_maximus_left.nii.gz"] = 39
    mapping["gluteus_maximus_right.nii.gz"] = 39
    mapping["gluteus_medius_left.nii.gz"] = 40
    mapping["gluteus_medius_right.nii.gz"] = 40
    mapping["gluteus_minimus_left.nii.gz"] = 41
    mapping["gluteus_minimus_right.nii.gz"] = 41
    mapping["autochthon_left.nii.gz"] = 42
    mapping["autochthon_right.nii.gz"] = 42
    mapping["iliopsoas_left.nii.gz"] = 43
    mapping["iliopsoas_right.nii.gz"] = 43
    mapping["brain.nii.gz"] = 44
    mapping["skull.nii.gz"] = 45
    mapping["rib_right_4.nii.gz"] = 46
    mapping["rib_right_3.nii.gz"] = 46
    mapping["rib_left_1.nii.gz"] = 46
    mapping["rib_left_2.nii.gz"] = 46
    mapping["rib_left_3.nii.gz"] = 46
    mapping["rib_left_4.nii.gz"] = 46
    mapping["rib_left_5.nii.gz"] = 46
    mapping["rib_left_6.nii.gz"] = 46
    mapping["rib_left_7.nii.gz"] = 46
    mapping["rib_left_8.nii.gz"] = 46
    mapping["rib_left_9.nii.gz"] = 46
    mapping["rib_left_10.nii.gz"] = 46
    mapping["rib_left_11.nii.gz"] = 46
    mapping["rib_left_12.nii.gz"] = 46
    mapping["rib_right_1.nii.gz"] = 46
    mapping["rib_right_2.nii.gz"] = 46
    mapping["rib_right_5.nii.gz"] = 46
    mapping["rib_right_6.nii.gz"] = 46
    mapping["rib_right_7.nii.gz"] = 46
    mapping["rib_right_8.nii.gz"] = 46
    mapping["rib_right_9.nii.gz"] = 46
    mapping["rib_right_10.nii.gz"] = 46
    mapping["rib_right_11.nii.gz"] = 46
    mapping["rib_right_12.nii.gz"] = 46
    mapping["sternum.nii.gz"] = 47
    mapping["costal_cartilages.nii.gz"] = 48

    # prepare variables
    current = 0
    offset = 0
    list = glob.glob("segmentations/*.gz")
    size = len(list)
    temp = "temp.obj"

    # write header of the output file
    output = open('output.obj', 'w')
    output.write("mtllib material.mtl\n")
    output.write("usemtl default\n")
    with open("palette.png", 'wb') as png_file:
        palette = numpy.reshape(numpy.array(colors), (1, len(colors) * 3))
        w = png.Writer(len(colors), 1, greyscale=False)
        w.write(png_file, numpy.uint8(palette))

    # run the loop
    for file in list:

        # generate mesh for a single object
        count = 0
        current += 1
        print(str(current) + "/" + str(size) + " " + file)
        nii_2_mesh(file, temp, 1)

        # append the mesh of the single object into the output
        name = os.path.basename(file)
        if os.path.isfile(temp):
            index = 0
            if name in mapping.keys():
                index = mapping[name]
            color = colors[index]
            output.write("o " + name + "\n")
            with open(temp) as f:
                for line in re.split("\n", f.read()):
                    data = re.split("\s+", line)

                    # write vertex coordinates
                    if data[0] == 'v':
                        output.write(line + "\n")
                        output.write("vt " + str((index + 0.5) / len(colors)) + " 0\n")
                        count += 1

                    # write triangle indices
                    if data[0] == 'f':
                        a = str(int(data[1]) + offset)
                        b = str(int(data[2]) + offset)
                        c = str(int(data[3]) + offset)
                        output.write("f " + a + "/" + a + " " + b + "/" + b + " " + c + "/" + c + "\n")

            # update indices offset and remove temp file
            offset += count
            os.remove(temp)

            if len(sys.argv) > 1:
                # unpack image data
                unpacked = "segmentations/temp.nii"
                with gzip.open(file, 'rb') as f_in:
                    with open(unpacked, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                orientation = nii2png(unpacked, "segmentations/")

                # colorize images
                index = len(images) - 1
                for image in numpy.sort(glob.glob("segmentations/*.png")):
                    if os.path.basename(image)[:4] != "temp":
                        continue
                    frame = numpy.array(Image.open(image).getdata())
                    frame = numpy.reshape(frame, (shape[0], shape[1]))
                    multiplier = numpy.uint32(numpy.array(color))
                    for y in range(shape[1]):
                        # TODO: this doesn't seem to be universally correct, test it on more data
                        if orientation == 0:
                            row = frame[shape[1] - y - 1, shape[0] - numpy.arange(shape[0]) - 1]
                        else:
                            row = frame[y, shape[0] - numpy.arange(shape[0]) - 1]
                        images[index][:, y * 3 + 0] = numpy.add(images[index][:, y * 3 + 0], row * multiplier[0])
                        images[index][:, y * 3 + 1] = numpy.add(images[index][:, y * 3 + 1], row * multiplier[1])
                        images[index][:, y * 3 + 2] = numpy.add(images[index][:, y * 3 + 2], row * multiplier[2])
                    index -= 1

    # save images
    if len(sys.argv) > 1:
        count = 0
        for image in images:
            with open(sys.argv[1] + "/" + str(count) + ".png", 'wb') as png_file:
                w = png.Writer(shape[1], shape[0], greyscale=False)
                w.write(png_file, numpy.uint8(numpy.minimum(image, 255)))
                count += 1
