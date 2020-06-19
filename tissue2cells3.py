# The code was generated by Sourabh Bhide (sourabh.j.bhide)
#!/usr/bin/env python
# coding: utf-8

# In[4]:


import numpy as np
import pandas as pd
import scipy
from scipy import ndimage
import scipy.misc
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from PIL import Image
from scipy.signal import find_peaks
import skimage.feature
from scipy import misc, ndimage, spatial
from skimage import feature
import imageio
from skimage import io
from PIL import Image as pilimage
from sklearn.metrics import pairwise_distances
from sklearn import cluster
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.metrics.pairwise import euclidean_distances
np.set_printoptions(threshold=np.inf)
from skimage.segmentation import watershed
import math 
import os
import os.path
from sklearn.cluster import OPTICS, cluster_optics_dbscan
import matplotlib.gridspec as gridspec
from skimage import filters
from skimage import exposure
from skimage import util 
from skimage import measure
import matplotlib.cm as cm

###########
t=0
basepath='img5out_9_25_32bit/'
suffix = '_pixel_26May'
master_data = pd.read_csv('img5out_9_25_32bit_fromscratch.csv', sep='\t',engine='python')


def measure_props(start,stop,master_data):
    measured_data = pd.DataFrame()
    df = pd.DataFrame()
    for t in range (start,stop):
        cell_identity = f'SUM_9_25_merged_img5out_T{t}/cell_identity.tif'#SUM_9_25_merged_img5out_T0
        myosin = f'Img5_SUM_9_25_16bit_T{t:02d}.tif' # Img5_SUM_9_25_16bit_T25
        myo_threshold = f'Img5_SUM_9_25_32bit_40pc_Huang_T{t:02d}.tif' # Img5_SUM_9_25_32bit_40pc_Huang_T29.tif
        a = os.path.join(basepath, cell_identity)
        b = os.path.join(basepath, myosin)
        c = os.path.join(basepath, myo_threshold)
        
        mask = np.array(Image.open(str(a)))
        myosin = np.array(Image.open(str(b)))
        if os.path.isfile(c): myo_seg = np.array(Image.open(str(c)))
        else :myo_seg = np.array(Image.open(str(a)))
        
        number_of_cells = master_data.frame_nb[master_data.frame_nb == t].count()
        
        df = measure_area (mask,myosin,number_of_cells,myo_seg)
        measured_data= measured_data.append(df)
        print("Frame number "+str(t)+" is imported")
    measured_data.to_csv('measured_data.csv', sep=';', decimal=',')
    print('DONE')

def all_plots(cell_groups,track_id,df,start,stop):
    basepath = 'img5out_9_25_32bit/' ############################################################################
    path_cells = '/Users/saubhi/Desktop/tissues2cells_version2/Cells_tracked_'+str(cell_groups)+'/'
    os.makedirs(path_cells, exist_ok=True)
    
    for f in range(start,stop): # frame_nb
        a = f'SUM_9_25_merged_img5out_T{f}/cell_identity.tif' ##################################
        b = f'Img5_SUM_9_25_16bit_T{f:02d}.tif' ####################################################
        myo = f'Img5_SUM_9_25_32bit_40pc_Huang_T{f:02d}.tif' #######################################
        c = os.path.join(basepath, a)
        d = os.path.join(basepath, b)
        myos_seg = os.path.join(basepath, myo)
        myo_seg = np.array(Image.open(str(myos_seg)))
        mask = np.array(Image.open(str(c)))
        myosin = np.array(Image.open(str(d)))

        color=cm.viridis(np.linspace(0,1,len(track_id)))

        for i,c in zip(track_id,color):
            
            local_id = df.loc[(df["frame_nb"]==f) & (df["track_id_cells"]==i)].local_id_cells
            if local_id.size == 0:
                print(f'frame:{f}, cell_id:{i}')
                continue
            a= int(local_id)
            cell = np.array(mask)[:,:,2] == a
            
            labels, number_of_objects = ndimage.label(cell)
            m = (labels==1)*np.array(myosin)
            binary = (labels==1)*np.array(myo_seg)
            slice_x, slice_y = ndimage.find_objects(labels==1)[0]
            box = cell[slice_x, slice_y]
            roi = m[slice_x, slice_y]
            roi_binary = binary[slice_x, slice_y]
            
            
            plt.contour(box)
            plt.imshow(roi)
            plt.title(str(i)+'_frame_'+str(f))
            plt.xlim(0,110)
            plt.ylim(0,150)
            plt.savefig(path_cells+'Cell_'+str(i)+'_frame_'+str(f)+'.png',format='png',transparent=True)
            plt.show()

            polar_plots_traced_pixels(box,roi_binary,c)
            plt.title(str(i)+'_frame_'+str(f))
            plt.savefig(path_cells+'Polar_plot_cell_'+str(i)+'_frame_'+str(f)+'.png',format='png',transparent=True)
            plt.show()

        #plt.title(str(i)+'_frame_'+str(f))
        #plt.savefig(path+'frame_'+str(f)+'_'+str(n)+'.png',format='png',transparent=True)
        plt.show()

    for id in track_id : 
        images = []
        for t in range(start,stop):
            filename = f'Cell_{id}_frame_{t}.png' #Cell_543104_frame_5.png
            I = os.path.join(path_cells, filename)
            if os.path.exists(I):
                img = Image.open(str(I))
                images.append(img)
        get_concat_h_multi_blank(images).save(path_cells+'test_montage_cell_'+str(id)+'.png')
    # In[40]:


def cart2pol(x, y):
    rho = np.sqrt((x)**2 + (y)**2)
    phi = np.arctan2(y,x)
    return(rho,phi)

def polar_plots_traced_pixels(box,roi,color):
    a,b = ndimage.measurements.center_of_mass(box)
    shifyx = a-a
    shiftyy = b-b
    j,k=cart2pol(shiftyy, shifyx)
    plt.polar(k,j,'ro')
    for x,y in np.column_stack(np.where(roi > 200)):##################################################
        shiftx =(x-a)#/g
        shifty =(y-b)#/h
        c,d=cart2pol(shiftx,shifty)
        plt.polar(-d+1.5708,c,'o',color=color,alpha=0.1) #d-1.5708
    plt.ylim(0,100)


# In[41]:

# In[ ]:

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
# In[42]:


def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample)
                      for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst

def get_concat_h_blank(im1, im2, color=(0, 0, 0)):
    dst = Image.new('RGB', (im1.width + im2.width, max(im1.height, im2.height)), color)
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst

def get_concat_h_multi_blank(im_list):
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_h_blank(_im, im)
    return _im

def Mon(im_list):
    _im = im_list.pop(0)
    for im in im_list:
        _im = get_concat_h_blank(_im, im)
    return _im
# In[25]:

def skewness_cells(image,mask):
    from scipy.stats import skew
    indices = np.where(image)
    coordinates = zip(indices[0], indices[1])
    y_coord = np.asarray(indices[0])
    return skew(y_coord)

def V_fraction(roi,box):
    D=0
    V=0
    R=0
    a,b = ndimage.measurements.center_of_mass(box)
    for x,y in np.column_stack(np.where(roi > 200)):
        shiftx =(x-a)#/g
        shifty =(y-b)#/h
        c,d=cart2pol(shiftx,shifty)
        if d < 0.2618 or d > 5.4978:V = V+1
        elif d < 3.927 and d > 2.356:D = D+1
        else: R = R+1
            
    if ((V+D+R)==0): Vfrac = 0
    else : Vfrac = V/(D+V+R)
         
    return Vfrac

def DV_Assymetry(box,myo_binary_cell):
    a,b = ndimage.measurements.center_of_mass(box)
    D=0
    V=0
    DV_ass=0
    for x,y in np.column_stack(np.where(myo_binary_cell > 254)):
        if y < int(a) :V = V+1
        else: D = D+1

    if (D==0 and V==0): DV_ass = 0
    else : DV_ass = V/(D+V)
            
    return DV_ass
           
# In[ ]:


def measure_area(mask,myosin,number_of_cells,myo_seg):
    centroid = []
    offset = []
    area_cells =[]
    sum_myosin_cells = []
    area_myo_seg_cells =[]
    background_area_cells= []
    concerntration=[]
    Ventral_fraction=[]
    skewness_cell = []
    DV_asymmetry= []
    eccentricity = []
    
    for i in range (1,number_of_cells+1):
        cell =np.array(mask)[:,:,2] == i
        labels, number_of_objects = ndimage.label(cell)
        myo2_seg_cell = (labels==1)*myo_seg # this step isolates myosinII signal for individual cells
        myo2_cell = (labels==1)*myosin # this step isolates myosinII signal for individual cells
        
        slice_x, slice_y = ndimage.find_objects(labels==1)[0]
        box = cell[slice_x, slice_y]
        roi = myo2_cell[slice_x, slice_y]
        
        props = skimage.measure.regionprops(box.astype(int),roi)
        weighted_cent = props[0].weighted_local_centroid
        weighted_cent = np.nan_to_num(weighted_cent)
        cent = props[0].centroid
        area = props[0].area
        cent = np.nan_to_num(cent)
        ecc = props[0].eccentricity
        ecc = np.nan_to_num(ecc)
        
        
        off_center = spatial.distance.euclidean(cent, weighted_cent)
        off_center = np.nan_to_num(off_center)
        
        #area = ndimage.measurements.sum(cell,labels==1)
        sum_myosin = ndimage.measurements.sum(myo2_cell)
        conc = sum_myosin/area
        area_myo_seg_blob = ndimage.measurements.sum(myo2_seg_cell)/255
        
        
        slice_x, slice_y = ndimage.find_objects(labels==1)[0]
        box = cell[slice_x, slice_y]
        a,b = ndimage.measurements.center_of_mass(box)
        myo_binary_cell = myo2_seg_cell[slice_x, slice_y]
       
        
        DV_assy = DV_Assymetry(box,myo_binary_cell)
        DV_asymmetry= np.append(DV_asymmetry,DV_assy)
        
        roi = myo2_cell[slice_x, slice_y]
        
        V_frac = V_fraction(roi,box)
        Ventral_fraction = np.append(Ventral_fraction,V_frac)
        
        skewness = skewness_cells(roi,box)
        skewness_cell=np.append(skewness_cell,skewness)
        
        
        area_cells = np.append(area_cells,area)
        centroid = np.append(centroid,cent,axis=0)
        offset = np.append(offset,off_center)
        sum_myosin_cells = np.append(sum_myosin_cells,sum_myosin)
        area_myo_seg_cells = np.append(area_myo_seg_cells,area_myo_seg_blob)
        concerntration = np.append(concerntration,conc)
        eccentricity = np.append(eccentricity,ecc)
    
    B = np.reshape(centroid, (-1, 2))
    C = pd.DataFrame(data=B, index=None, columns=["center_y_cells", "center_x_cells"])
    D = np.reshape(offset, (-1, 1))
    E = pd.DataFrame(data=D, index=None, columns=["offset"])
    F = np.reshape(area_cells, (-1, 1))
    G = pd.DataFrame(data=F, index=None, columns=["area_cells"])
    H = np.reshape(sum_myosin_cells, (-1, 1))
    I = pd.DataFrame(data=H, index=None, columns=["sum_myosin_cells"])

    J = np.reshape(eccentricity, (-1, 1))
    K = pd.DataFrame(data=J, index=None, columns=["eccentricity"])
    
    L = np.reshape(Ventral_fraction, (-1, 1))
    M = pd.DataFrame(data=L, index=None, columns=["Ventral_fraction"])
    
    N = np.reshape(concerntration, (-1, 1))
    O = pd.DataFrame(data=N, index=None, columns=["concerntration_cells"])
    
    P= np.reshape(DV_asymmetry, (-1, 1))
    Q= pd.DataFrame(data=P, index=None, columns=["DV_asymmetry"])
    
    R= np.reshape(skewness_cell, (-1, 1))
    S= pd.DataFrame(data=R, index=None, columns=["skewness_cell"])

    df1 = pd.concat([C,E,I,K,M,O,Q,S],axis=1, sort=True)
    df = pd.concat([G,df1],axis=1, sort=True)
    return df


def all_plots_utr(cell_groups,track_id,df,start,stop):
    basepath = 'UtrGFP_sqhmCherry/' ############################################################################
    path_cells = '/Users/saubhi/Desktop/tissue2cells_version1/Cells_tracked_'+str(cell_groups)+'/'
    os.makedirs(path_cells, exist_ok=True)
    
    for f in range(start,stop): # frame_nb
        aa = f'img46_T{f:02d}/cell_identity.tif'# img46_T00
        aactin = f'Data_images/SUM_Actin_Image_46_Out_{f:04d}.tif' # SUM_Actin_Image_46_Out_0000
        amyo = f'Data_images/SUM_Myosin_Image_46_Out{f:04d}.tif' # SUM_Myosin_Image_46_Out0003.tif
        c2 = os.path.join(basepath, aa)
        act2 = os.path.join(basepath, aactin)
        myo2 = os.path.join(basepath, amyo)
        
        mask1 = np.array(Image.open(str(c2)))
        actin1 = np.array(Image.open(str(act2)))
        myosin1 = np.array(Image.open(str(myo2)))
    
        
        color=cm.viridis(np.linspace(0,1,len(track_id)))
        
        for i,c in zip(track_id,color):
            
            local_id = df.loc[(df["frame_nb"]==f) & (df["track_id_cells"]==i)].local_id_cells
            if local_id.size == 0:
                print(f'frame:{f}, cell_id:{i}')
                continue
            a= int(local_id)
            cell = np.array(mask1)[:,:,2] == a
            
            labels, number_of_objects = ndimage.label(cell)
            myosin_cell= (labels==1)*np.array(myosin1)
            actin_cell = (labels==1)*np.array(actin1)
            slice_x, slice_y = ndimage.find_objects(labels==1)[0]
            box = cell[slice_x, slice_y]
            roi_myosin = myosin_cell[slice_x, slice_y]
            roi_actin = actin_cell[slice_x, slice_y]
            
            
            plt.contour(box)
            plt.imshow(roi_myosin)
            plt.title(str(i)+'_frame_'+str(f))
            plt.savefig(path_cells+'Cell_myosin_'+str(i)+'_frame_'+str(f)+'.png',format='png',transparent=True)
            plt.show()
            
            plt.contour(box)
            plt.imshow(roi_actin)
            plt.title(str(i)+'_frame_'+str(f))
            plt.savefig(path_cells+'Cell_actin_'+str(i)+'_frame_'+str(f)+'.png',format='png',transparent=True)
            plt.show()

        plt.show()

        #plt.title(str(i)+'_frame_'+str(f))
        #plt.savefig(path+'frame_'+str(f)+'_'+str(n)+'.png',format='png',transparent=True)
    plt.show()


def make_montage_cells(name,track_id_list,signal,start,stop,suffix=suffix):
    for track_id in track_id_list :
            images = []
            for t in range(start,stop):
                filename = f'Cells_tracked_{name}/Cell_{signal}_{track_id}_frame_{t}.png'##########actin or myosin
                if os.path.exists(filename):
                    img = Image.open(str(filename))
                    images.append(img)
                    
            get_concat_h_multi_blank(images).save(f'Cells_tracked_{name}/Montage_Cell_{signal}_{track_id}.png')
