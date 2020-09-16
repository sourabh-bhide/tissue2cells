<<<<<<< HEAD
ReadMe
This repository contains methods used for discribing spatial distribution of myosin within a cell in 2D epithelial tissue. (Bhide et al; manuscript in preparation) 
tissue2cells.

This notebook uses output files from tissue analyzer.

=======

Requirements:
	Membrane segmentation results
	If tracking information is available then need the local cell id information 	represented in the segmentation result

=======

Things to keep in mind and change in the tissue2cells.py file :
	the path from tissue2cells directory to the data
	the format in which the data is saved (replace the frame num by ’t’ or ‘f’)
	the name s and path to which you want the plots to be saved

=======

For row-by-row analysis:
	Need cell ids belonging to every cell group/ cell row as a list. Enter it in 	the notebook 
