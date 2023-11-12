import glob
import re
import os
import vtk


def nii_2_mesh(filename_nii, filename_obj, label):

    # read the file
    print(filename_nii)
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

    # define color mapping in HSV (note that saturation value is ignored)
    colors = {}
    colors["spleen.nii.gz"] = [2.13, 0.64, 0.86]
    colors["kidney_right.nii.gz"] = [1.20, 0.39, 0.07]
    colors["kidney_left.nii.gz"] = [1.20, 0.39, 0.07]
    colors["gallbladder.nii.gz"] = [0.0, 0.0, 0.0]
    colors["liver.nii.gz"] = [0.28, 0.57, 0.92]
    colors["stomach.nii.gz"] = [3.60, 0.65, 0.77]
    #TODO: add colors
    colors["pancreas.nii.gz"] = [0.0, 0.0, 0.0]
    colors["adrenal_gland_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["adrenal_gland_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["lung_upper_lobe_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["lung_lower_lobe_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["lung_upper_lobe_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["lung_middle_lobe_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["lung_lower_lobe_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["esophagus.nii.gz"] = [0.0, 0.0, 0.0]
    colors["trachea.nii.gz"] = [0.0, 0.0, 0.0]
    colors["thyroid_gland.nii.gz"] = [0.0, 0.0, 0.0]
    colors["small_bowel.nii.gz"] = [0.0, 0.0, 0.0]
    colors["duodenum.nii.gz"] = [0.0, 0.0, 0.0]
    colors["colon.nii.gz"] = [0.0, 0.0, 0.0]
    colors["urinary_bladder.nii.gz"] = [0.0, 0.0, 0.0]
    colors["prostate.nii.gz"] = [0.0, 0.0, 0.0]
    colors["kidney_cyst_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["kidney_cyst_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["sacrum.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_S1.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_L5.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_L4.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_L3.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_L2.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_L1.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T12.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T11.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T10.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T9.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T8.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T7.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T6.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T5.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T4.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T3.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T2.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_T1.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C7.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C6.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C5.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C4.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C3.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C2.nii.gz"] = [0.0, 0.0, 0.0]
    colors["vertebrae_C1.nii.gz"] = [0.0, 0.0, 0.0]
    colors["heart.nii.gz"] = [0.0, 0.0, 0.0]
    colors["aorta.nii.gz"] = [0.0, 0.0, 0.0]
    colors["pulmonary_vein.nii.gz"] = [0.0, 0.0, 0.0]
    colors["brachiocephalic_trunk.nii.gz"] = [0.0, 0.0, 0.0]
    colors["subclavian_artery_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["subclavian_artery_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["common_carotid_artery_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["common_carotid_artery_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["brachiocephalic_vein_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["brachiocephalic_vein_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["atrial_appendage_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["superior_vena_cava.nii.gz"] = [0.0, 0.0, 0.0]
    colors["inferior_vena_cava.nii.gz"] = [0.0, 0.0, 0.0]
    colors["portal_vein_and_splenic_vein.nii.gz"] = [0.0, 0.0, 0.0]
    colors["iliac_artery_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["iliac_artery_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["iliac_vena_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["iliac_vena_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["humerus_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["humerus_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["scapula_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["scapula_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["clavicula_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["clavicula_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["femur_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["femur_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["hip_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["hip_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["spinal_cord.nii.gz"] = [0.0, 0.0, 0.0]
    colors["gluteus_maximus_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["gluteus_maximus_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["gluteus_medius_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["gluteus_medius_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["gluteus_minimus_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["gluteus_minimus_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["autochthon_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["autochthon_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["iliopsoas_left.nii.gz"] = [0.0, 0.0, 0.0]
    colors["iliopsoas_right.nii.gz"] = [0.0, 0.0, 0.0]
    colors["brain.nii.gz"] = [0.0, 0.0, 0.0]
    colors["skull.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_4.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_3.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_1.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_2.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_3.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_4.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_5.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_6.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_7.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_8.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_9.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_10.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_11.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_left_12.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_1.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_2.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_5.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_6.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_7.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_8.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_9.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_10.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_11.nii.gz"] = [0.0, 0.0, 0.0]
    colors["rib_right_12.nii.gz"] = [0.0, 0.0, 0.0]
    colors["sternum.nii.gz"] = [0.0, 0.0, 0.0]
    colors["costal_cartilages.nii.gz"] = [0.0, 0.0, 0.0]

    # prepare variables
    offset = 0
    temp = "temp.obj"

    # write header of the output file
    output = open('output.obj', 'w')
    output.write("mtllib material.mtl\n")
    output.write("usemtl default\n")

    # run the loop
    for file in glob.glob("segmentations/*.gz"):

        # generate mesh for a single object
        count = 0
        nii_2_mesh(file, temp, 1)

        # append the mesh of the single object into the output
        if os.path.isfile(temp):
            color = [0, 0, 0]
            if os.path.basename(file) in colors.keys():
                color = colors[os.path.basename(file)]
            output.write("o " + os.path.basename(file) + "\n")
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

            # update indices offset, object color and remove temp file
            offset += count
            os.remove(temp)
