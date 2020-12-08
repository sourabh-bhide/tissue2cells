## Tissue To Cells

This repository contains methods used for discribing spatial distribution of myosin within and outside a cell in 2D epithelial tissue. [[Bhide et al.](https://doi.org/10.1101/2020.10.15.333963)]

![analysis_illustration](https://github.com/sourabh-bhide/tissue2cells/blob/master/Data/analysis_illustration.png)

These scripts/notebooks use output files from tissue analyzer.

=======

Requirements:
* Membrane segmentation results
* If tracking information is available then need the `track_id_cells` and `local_id_cells` information 	represented in the segmentation result

=======

For row-by-row analysis:
* Need cell ids belonging to every cell group/ cell row as a list. Enter it in 	the notebook tissues2Cells.ipynb


=======

For myosin inside vs myosin outside analysis (Figures 2K and 2L in the manuscript):
* Raw data (intensities) named as Img{i}_SUM.tif (e.g. Img5_SUM.tif)
* Membrane segmentation results as a folder Img{i}_segmentation with each segmented frame stored as a separate file cell_identity_T{i}.tif (e.g. cell_identity_T0.tif)
* Cell tracking results named img{i}.csv necessarily containing columns `frame_nb`, `track_id_cells` and `local_id_cells`

=======

Usage:
* Combine the datafile into HDF5 file using 'convert_tiffs.py'
* Run the notebook tissue2cells.ipynb and plot_myo_in_out.ipynb for analysis and measurement of myosin signal




