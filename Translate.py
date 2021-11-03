#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 15:40:26 2021

@author: Mathew
"""

import matplotlib.image as mpimg
import numpy as np
import os
from skimage import io
import imreg_dft as ird
from PIL import Image
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
import cv2
from numpy import unravel_index
from skimage.io import imread

pathlist=[]


pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/a-syn/200nM/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/a-syn/200nM/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/a-syn/200nM/2/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/1/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/1/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/1/2/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/3/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/3/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/3/2/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/2/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/2/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/72h/2/2/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/1/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/1/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/1/2/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/3/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/3/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/3/2/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/2/1/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/2/3/")
pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/4h/2/2/")
# pathlist.append(r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/48h/3/2/")
# 
file1="Green_Binary_scaled.tif"
file2="SR_points_python_clustered.tif"
to_plot=0


for path in pathlist:
    greenSlice = io.imread(path+file1).astype('uint8')
    redSlice = io.imread(path+file2).astype('uint8')
    
    binary_ch1=(greenSlice>0).astype('uint8')
    binary_ch2=(redSlice>0).astype('uint8')
    

    if to_plot==1:
        imRGB = np.zeros((greenSlice.shape[0],greenSlice.shape[1],3))
        imRGB[:,:,0] = binary_ch1
        imRGB[:,:,1] = binary_ch2
        
        fig, ax = plt.subplots(1,3, figsize=(14, 4))
        
        ax[0].imshow(greenSlice,cmap='Greens_r')
        ax[0].set_title('Green')
        ax[1].imshow(redSlice,cmap='Reds_r');
        ax[1].set_title('Red')
        ax[2].imshow(imRGB)
        ax[2].set_title('Overlay')
    
    
    coinc=binary_ch1&binary_ch2
    
    total=coinc.sum()
    
    print("Orginal total: %d"%total)
    
    coincident_pixels=np.zeros([20,20])
    
    for i in range(0,20):
        for j in range(0,20):
            y=(i-10)*5
            x=(j-10)*5
            
            M = np.float32([
            	[1, 0, y],
            	[0, 1, x]
            ])
        
        
            shifted = cv2.warpAffine(binary_ch1, M, (greenSlice.shape[1], greenSlice.shape[0]))
           
            coincshift=shifted&binary_ch2
            
            total=coincshift.sum()
            
            
            coincident_pixels[i][j]=total
            
    plt.imshow(coincident_pixels)
    plt.show()
    maximum=coincident_pixels.max()
    
    maxpos=unravel_index(coincident_pixels.argmax(), coincident_pixels.shape)
    
    ymove=(maxpos[0]-10)*5
    xmove=(maxpos[1]-10)*5  
    
    print("Maximum coincidence was %d with x shifted %d and y shifted %d"%(maximum,xmove,ymove))   
    
    final_M=np.float32([
            	[1, 0, ymove],
            	[0, 1, xmove]
            ])
    final_shift = cv2.warpAffine(binary_ch1, final_M, (greenSlice.shape[1], greenSlice.shape[0]))
    coincshift=final_shift&binary_ch2
    total=coincshift.sum()
    
    # print(total)
    # Shift and save files:
    file_zproj="Green_flat_scaled.tif"
    flat = io.imread(path+file_zproj).astype('uint16')
    flat_shift=cv2.warpAffine(flat, final_M, (flat.shape[1], flat.shape[0]))
    im3 = Image.fromarray(flat_shift)
    im3.save(path+'Green_flat_scaled_shifted.tif')
    
    file_filt="Green_flat.tif"
    filt = imread(path+file_filt)
    filtim=Image.fromarray(filt)
    filtl=filtim.resize((4096, 4096),resample=0)
    filt_arr=np.array(filtl).astype('uint16')
    filt_shift=cv2.warpAffine(filt_arr, final_M, (flat.shape[1], flat.shape[0]))
    im3 = Image.fromarray(filt_shift)
    im3.save(path+'Green_for_coinc.tif')
    
    im3 = Image.fromarray(final_shift)
    im3.save(path+'Green_Binary_scaled_shifted.tif')


