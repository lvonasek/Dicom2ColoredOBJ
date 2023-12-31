# Dicom2ColoredOBJ

This project creates colored OBJ from CT scan in DICOM (.dcm) format. It was created just out of interest, all fame to the authors of TotalSegmentator paper.

![Screenshot of the result in Blender](https://github.com/lvonasek/Dicom2ColoredOBJ/blob/main/screenshot.png?raw=true)

Tested on Ubuntu 24.04. TotalSegmentator supports processing just one scan at the time. You can split the data easily using free software called 3DimViewer.

### Installation

```
pip install nii2png png TotalSegmentator vtk
```

### Generate 3D model

```
# convert demo dicom data (replace demo_data with your own path to process it)
TotalSegmentator -i demo_data -o segmentations --preview

# convert segmentations into colored 3D model `output.obj`
python3 meshall.py

# convert segmentations and generate colored images into demo data directory
python3 meshall.py demo_data
```

If you change the dataset then delete the `segmentations` folder before calling `TotalSegmentator` again.

### Used code

https://github.com/wasserth/TotalSegmentator

https://github.com/MahsaShk/MeshProcessing

https://github.com/alexlaurence/NIfTI-Image-Converter

https://github.com/hphuongdhsp/dicom2png
