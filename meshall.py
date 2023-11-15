import colorsys
import glob
import gzip
import numpy
import nii2png
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
            image_2d_scaled = numpy.uint8((numpy.maximum(image_2d,0) / image_2d.max()) * 255.0)
            image_2d_colored = numpy.zeros([shape[0], shape[1] * 3], dtype=numpy.uint8)
            for y in range(shape[1]):
                image_2d_colored[:, y * 3 + 0] = image_2d_scaled[:, y]
                image_2d_colored[:, y * 3 + 1] = image_2d_scaled[:, y]
                image_2d_colored[:, y * 3 + 2] = image_2d_scaled[:, y]
            images.append(image_2d_colored)

    # define color mapping in HSV (note that saturation value is ignored)
    colors = {}
    colors["spleen.nii.gz"] = [2.13, 0.64, 0.86]
    colors["kidney_right.nii.gz"] = [1.09, 0.79, 0.18]
    colors["kidney_left.nii.gz"] = [1.09, 0.79, 0.18]
    colors["gallbladder.nii.gz"] = [0.65, 0.48, 0.71]
    colors["liver.nii.gz"] = [0.28, 0.57, 0.92]
    colors["stomach.nii.gz"] = [3.60, 0.65, 0.77]
    colors["pancreas.nii.gz"] = [1.39, 0.76, 0.88]
    colors["adrenal_gland_right.nii.gz"] = [1.55, 0.70, 0.57]
    colors["adrenal_gland_left.nii.gz"] = [1.55, 0.70, 0.57]
    colors["lung_upper_lobe_left.nii.gz"] = [2.79, 0.98, 0.76]
    colors["lung_lower_lobe_left.nii.gz"] = [0.52, 0.63, 0.93]
    colors["lung_upper_lobe_right.nii.gz"] = [2.79, 0.98, 0.76]
    colors["lung_middle_lobe_right.nii.gz"] = [3.60, 0.65, 0.77]
    colors["lung_lower_lobe_right.nii.gz"] = [0.52, 0.63, 0.93]
    colors["esophagus.nii.gz"] = [1.55, 0.70, 0.61]
    colors["trachea.nii.gz"] = [0.88, 0.88, 0.55]
    colors["thyroid_gland.nii.gz"] = [2.98, 0.93, 0.45]
    colors["small_bowel.nii.gz"] = [2.79, 0.98, 0.64]
    colors["duodenum.nii.gz"] = [0.52, 0.63, 0.93]
    colors["colon.nii.gz"] = [0.66, 0.49, 0.70]
    colors["urinary_bladder.nii.gz"] = [0.88, 0.88, 0.55]
    colors["prostate.nii.gz"] = [1.60, 0.53, 0.56]
    colors["kidney_cyst_left.nii.gz"] = [3.0, 1.0, 1.0]
    colors["kidney_cyst_right.nii.gz"] = [3.0, 1.0, 1.0]
    colors["sacrum.nii.gz"] = [3.51, 0.82, 0.98]
    colors["vertebrae_S1.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_L5.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_L4.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_L3.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_L2.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_L1.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T12.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T11.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T10.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T9.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T8.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T7.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T6.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T5.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T4.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T3.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T2.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_T1.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C7.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C6.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C5.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C4.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C3.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C2.nii.gz"] = [0.74, 0.35, 0.97]
    colors["vertebrae_C1.nii.gz"] = [0.74, 0.35, 0.97]
    colors["heart.nii.gz"] = [3.60, 1.0, 1.0]
    colors["aorta.nii.gz"] = [2.79, 0.98, 0.76]
    colors["pulmonary_vein.nii.gz"] = [0.88, 0.87, 0.49]
    colors["brachiocephalic_trunk.nii.gz"] = [3.43, 0.79, 0.45]
    colors["subclavian_artery_right.nii.gz"] = [1.70, 0.20, 0.97]
    colors["subclavian_artery_left.nii.gz"] = [1.70, 0.20, 0.97]
    colors["common_carotid_artery_right.nii.gz"] = [2.97, 0.88, 0.39]
    colors["common_carotid_artery_left.nii.gz"] = [2.97, 0.88, 0.39]
    colors["brachiocephalic_vein_left.nii.gz"] = [3.43, 0.79, 0.45]
    colors["brachiocephalic_vein_right.nii.gz"] = [3.43, 0.79, 0.45]
    colors["atrial_appendage_left.nii.gz"] = [1.09, 0.79, 0.18]
    colors["superior_vena_cava.nii.gz"] = [2.79, 0.98, 0.76]
    colors["inferior_vena_cava.nii.gz"] = [0.87, 0.88, 0.60]
    colors["portal_vein_and_splenic_vein.nii.gz"] = [0.29, 0.57, 0.92]
    colors["iliac_artery_left.nii.gz"] = [3.60, 0.65, 0.73]
    colors["iliac_artery_right.nii.gz"] = [3.60, 0.65, 0.73]
    colors["iliac_vena_left.nii.gz"] = [0.66, 0.49, 0.70]
    colors["iliac_vena_right.nii.gz"] = [0.66, 0.49, 0.70]
    colors["humerus_left.nii.gz"] = [0.74, 0.35, 0.97]
    colors["humerus_right.nii.gz"] = [0.74, 0.35, 0.97]
    colors["scapula_left.nii.gz"] = [0.74, 0.35, 0.97]
    colors["scapula_right.nii.gz"] = [0.74, 0.35, 0.97]
    colors["clavicula_left.nii.gz"] = [0.74, 0.35, 0.97]
    colors["clavicula_right.nii.gz"] = [0.74, 0.35, 0.97]
    colors["femur_left.nii.gz"] = [0.74, 0.35, 0.97]
    colors["femur_right.nii.gz"] = [0.74, 0.35, 0.97]
    colors["hip_left.nii.gz"] = [0.74, 0.35, 0.97]
    colors["hip_right.nii.gz"] = [0.74, 0.35, 0.97]
    colors["spinal_cord.nii.gz"] = [2.40, 0.84, 0.70]
    colors["gluteus_maximus_left.nii.gz"] = [1.40, 0.76, 0.90]
    colors["gluteus_maximus_right.nii.gz"] = [1.40, 0.76, 0.90]
    colors["gluteus_medius_left.nii.gz"] = [0.87, 0.88, 0.60]
    colors["gluteus_medius_right.nii.gz"] = [0.87, 0.88, 0.60]
    colors["gluteus_minimus_left.nii.gz"] = [2.13, 0.63, 0.82]
    colors["gluteus_minimus_right.nii.gz"] = [2.13, 0.63, 0.82]
    colors["autochthon_left.nii.gz"] = [3.60, 0.65, 0.77]
    colors["autochthon_right.nii.gz"] = [3.60, 0.65, 0.77]
    colors["iliopsoas_left.nii.gz"] = [0.64, 0.48, 0.68]
    colors["iliopsoas_right.nii.gz"] = [0.64, 0.48, 0.68]
    colors["brain.nii.gz"] = [1.70, 0.20, 0.94]
    colors["skull.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_4.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_3.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_1.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_2.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_3.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_4.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_5.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_6.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_7.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_8.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_9.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_10.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_11.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_left_12.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_1.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_2.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_5.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_6.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_7.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_8.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_9.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_10.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_11.nii.gz"] = [0.74, 0.35, 0.97]
    colors["rib_right_12.nii.gz"] = [0.74, 0.35, 0.97]
    colors["sternum.nii.gz"] = [0.74, 0.35, 0.97]
    colors["costal_cartilages.nii.gz"] = [0.74, 0.35, 0.97]

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
            color = [1.8, 1.0, 1.0]
            if name in colors.keys():
                color = colors[name]
            rgb = colorsys.hsv_to_rgb(color[0] / 3.6, 1.0, color[2])
            output.write("o " + name + "\n")
            with open(temp) as f:
                for line in re.split("\n", f.read()):
                    data = re.split("\s+", line)

                    # write vertex coordinates
                    if data[0] == 'v':
                        output.write(line + "\n")
                        output.write("vt " + str(color[0] / 3.6) + " " + str(color[2] * 0.99 + 0.005) + "\n")
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
                nii2png.main(["-i", unpacked, "-o", "segmentations/"])

                # colorize images
                imcount = 0
                for image in numpy.sort(glob.glob("segmentations/*.png")):
                    if os.path.basename(image)[:4] != "temp":
                        continue
                    frame = numpy.array(Image.open(image).getdata())
                    frame = numpy.reshape(frame, (shape[0], shape[1]))
                    multiplier = numpy.uint8(numpy.array(rgb) * 255)
                    for y in range(shape[1]):
                        row = frame[shape[1] - y - 1, shape[0] - numpy.arange(shape[0]) - 1]
                        images[imcount][:, y * 3 + 0] = numpy.add(images[imcount][:, y * 3 + 0], row * multiplier[0])
                        images[imcount][:, y * 3 + 1] = numpy.add(images[imcount][:, y * 3 + 1], row * multiplier[1])
                        images[imcount][:, y * 3 + 2] = numpy.add(images[imcount][:, y * 3 + 2], row * multiplier[2])
                    imcount += 1

    # save images
    if len(sys.argv) > 1:
        count = 0
        for image in images:
            with open(sys.argv[1] + "/" + str(count) + ".png", 'wb') as png_file:
                w = png.Writer(shape[1], shape[0], greyscale=False)
                w.write(png_file, numpy.minimum(image, 255))
                count += 1
