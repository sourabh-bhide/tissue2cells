#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import matplotlib.pyplot as plt
import tissue2cells as tc
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

def Fill_Error(df,col_name,color):
    df_mean = df.set_index('filename').groupby('frame_nb').agg(['mean'])
    df_std = df.set_index('filename').groupby('frame_nb').agg(['std'])
    error_down = (df_mean[str(col_name)].values)-(df_std[str(col_name)].values)
    error_up = (df_std[str(col_name)].values)+(df_mean[str(col_name)].values)
    Y_down = error_down.flatten()
    Y_up = error_up.flatten()
    Xaxis    = range(0,len(df_mean)*25,25)#this number depends upon the time resolution
    ax_df = plt.plot(Xaxis,df_mean[col_name],color=str(color))
    return plt.fill_between(Xaxis, Y_up, Y_down, alpha=0.1, color= str(color))


def RowAnalysis(AcrossRows,Colors1,label_rows):
    path_plots = 'Results/RowAnalysis_plots/'
    os.makedirs(path_plots, exist_ok=True)

    for i,j in zip(AcrossRows,Colors1):
        Fill_Error(i,'Area',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('cell area ($\mu$m$^{2}$)', fontsize=12)
    plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'all_rows_cell_area.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        Fill_Error(i,'sum_myosin_cells',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('sum_myosin_cells', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'all_rows_sum_myosin_cells.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        Fill_Error(i,'concentration_myo',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('concentration_myo', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'all_rows_concentration_myo.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        Fill_Error(i,'eccentricity',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('eccentricity', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'all_rows_eccentricity.png', transparent=True)
    plt.show()

    for i,j in zip(AcrossRows,Colors1):
        Fill_Error(i,'Offset_myo',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('Offset_myo', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'all_rows_Offset_myo.png', transparent=True)
    plt.show()


    for i,j in zip(AcrossRows,Colors1):
        Fill_Error(i,'DV_asymmetry',j)
    plt.xlabel('Time(sec)', fontsize=10)
    plt.ylabel('DV_asymmetry', fontsize=12)
    #plt.ylim(0,110)
    #plt.xlim(0,700)
    plt.legend(label_rows, loc='upper left', fontsize=11)
    plt.savefig(path_plots+'all_rows_DV_assymetry_roi.png', transparent=True)
    plt.show()
