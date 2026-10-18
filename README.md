# mri_slicer
A simple Python tool for loading a 3D MRI scan and exploring slices in three directions using interactive sliders.

About
This small project explores how MRI images are represented as numerical arrays and how individual slices can be selected and displayed. I put it together as part of my application to the Psychiatry Neuroimaging Laboratory at Brigham and Women’s Hospital.

Features
* Loads MRI scans in NIfTI format using NiBabel
* Reorients the data to the closest canonical orientation
* Displays axial, coronal and sagittal views
* Provides sliders to move through slices along each axis
* Preserves image proportions using voxel spacing
* Saves a static image of the three views

How To Run
Download repository and extract it. Install the required dependencies, and run mri_slice_viewer.py. This should open an interative matplotlib window. It will also save the initial view as an image in the figures folder.

Data
The example scan comes from the publicly available OpenNeuro ds000114 dataset, released under CC0. Dataset citation and source details are included in data/provenance.json.
https://doi.org/10.18112/openneuro.ds000114.v1.0.2

Development
Over a couple of hours, I used AI to help teach myself the basics of working with MRI data in Python. I already have experience with Python and Matplotlib, so the main new piece was learning how to use NiBabel to load MRI scans and work with the image data as NumPy arrays. This basically consisted in learning how a scan is represented as a grid of voxels, how voxel spacing relates to physical dimensions, and how selecting an index along one axis produces a two-dimensional slice.
