#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import matplotlib.pyplot as plt
import tissue2cells3 as tc
import os
import os.path
import ipywidgets as widgets
w = widgets.Select(
    options=['Area','concentration_myo','DV_asymmetry', 'Ventral_fraction', 'offset',
       'sum_myosin_cells', 'eccentricity'],
    value='Area',
    # rows=10,
    description='Qyantity:',
    disabled=False)
def RowAnalysis(AcrossRows,Colors1,label_rows):
    path_plots = 'RowAnalysis_plots/'
    os.makedirs(path_plots, exist_ok=True)

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'Area',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('cell area ($\mu$m$^{2}$)', fontsize=12)
    plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_cell_area.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'sum_myosin_cells',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('sum_myosin_cells', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_sum_myosin_cells.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'concentration_myo',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('concentration_myo', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_concentration_myo.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'eccentricity',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('eccentricity', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_eccentricity.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'Offset_myo',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('Offset_myo', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_Offset_myo.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'Ventral_fraction',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('Ventral_fraction', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_Ventral_fractiont.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        tc.Fill_Error(i,'DV_asymmetry',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('DV_asymmetry', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'img5_all_rows_DV_assymetry_roi.png', transparent=True)
    plt.show()
