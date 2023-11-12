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

    # prepare variables
    color = 0
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
            output.write("o " + os.path.basename(file) + "\n")
            with open(temp) as f:
                for line in re.split("\n", f.read()):
                    data = re.split("\s+", line)

                    # write vertex coordinates
                    if data[0] == 'v':
                        output.write(line + "\n")
                        output.write("vt " + str(color) + " 0\n")
                        count += 1

                    # write triangle indices
                    if data[0] == 'f':
                        a = str(int(data[1]) + offset)
                        b = str(int(data[2]) + offset)
                        c = str(int(data[3]) + offset)
                        output.write("f " + a + "/" + a + " " + b + "/" + b + " " + c + "/" + c + "\n")

            # update indices offset, object color and remove temp file
            offset += count
            color += 1.0 / 64.0 #Color range is 0..1 but it is better to have contrast colors than unique colors
            os.remove(temp)
