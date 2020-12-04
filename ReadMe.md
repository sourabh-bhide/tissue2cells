## Tissue To Cells

This repository contains methods used for discribing spatial distribution of myosin within and outside a cell in 2D epithelial tissue. [[Bhide et al.](https://doi.org/10.1101/2020.10.15.333963)]

![analysis_illustration](https://github.com/sourabh-bhide/tissue2cells/blob/master/Data/analysis_illustration.png)

These scripts/notebooks use output files from tissue analyzer.

=======

Requirements:
* Membrane segmentation results
* If tracking information is available then need the `track_id_cells` and `local_id_cells` information 	represented in the segmentation result

=======

Things to keep in mind and change in the tissue2cells.py file :
* the path from tissue2cells directory to the data
* the format in which the data is saved (replace the frame num by ’t’ or ‘f’)
* the name s and path to which you want the plots to be saved

=======

For row-by-row analysis:
* Need cell ids belonging to every cell group/ cell row as a list. Enter it in 	the notebook tissues2Cells.ipynb


=======

For myosin inside vs myosin outside analysis (Figures 2K and 2L in the manuscript):
* Raw data (intensities) named as Img{i}_SUM.tif (e.g. Img5_SUM.tif)
* Membrane segmentation results as a folder Img{i}_segmentation with each segmented frame stored as a separate file cell_identity_T{i}.tif (e.g. cell_identity_T0.tif)
* Cell tracking results named img{i}.csv necessarily containing columns `frame_nb`, `track_id_cells` and `local_id_cells`
