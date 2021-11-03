#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  9 12:57:38 2021

@author: Mathew
"""


from skimage.io import imread
import os
import pandas as pd
from picasso import render
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.cluster import DBSCAN
from skimage import filters,measure
from skimage.filters import threshold_local

# Change paths to the images:
    


Pixel_size=103.0
   

# Settings
image_width=512
image_height=512



filename_contains="405_0"

# Folders to analyse:
root_path=r"/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/"
pathlist=[]


pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/0h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/4h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/8h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/12h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/24h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/48h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/1/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/1/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/1/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/2/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/2/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/2/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/3/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/3/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/72h/3/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/a-syn/200nM/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/a-syn/200nM/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/a-syn/200nM/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/52h/100nM/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/52h/100nM/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/52h/100nM/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/52h/200nM/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/52h/200nM/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/52h/200nM/2/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/72h/3/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/72h/1/")
pathlist.append(r"/Volumes/VERBATIM HD/210812_1nM590_timecourse/AB42/72h/2/")




def load_image(toload):
    
    image=imread(toload)
    
    return image

def z_project(image):
    
    mean_int=np.mean(image,axis=0)
  
    return mean_int

# Subtract background:
def subtract_bg(image):
    background = threshold_local(image, 11, offset=np.percentile(image, 1), method='median')
    bg_corrected =image - background
    return bg_corrected

def threshold_image_otsu(input_image):
    # threshold_value=filters.threshold_otsu(input_image)  
    
    threshold_value=input_image.mean()+5*input_image.std()
    print(threshold_value)
    binary_image=input_image>threshold_value

    return threshold_value,binary_image

def threshold_image_standard(input_image,thresh):
     
    binary_image=input_image>thresh

    return binary_image

# Threshold image using otsu method and output the filtered image along with the threshold value applied:
    
def threshold_image_fixed(input_image,threshold_number):
    threshold_value=threshold_number   
    binary_image=input_image>threshold_value

    return threshold_value,binary_image

# Label and count the features in the thresholded image:
def label_image(input_image):
    labelled_image=measure.label(input_image)
    number_of_features=labelled_image.max()
 
    return number_of_features,labelled_image
    
# Function to show the particular image:
def show(input_image,color=''):
    if(color=='Red'):
        plt.imshow(input_image,cmap="Reds")
        plt.show()
    elif(color=='Blue'):
        plt.imshow(input_image,cmap="Blues")
        plt.show()
    elif(color=='Green'):
        plt.imshow(input_image,cmap="Greens")
        plt.show()
    else:
        plt.imshow(input_image)
        plt.show() 
    
        
# Take a labelled image and the original image and measure intensities, sizes etc.
def analyse_labelled_image(labelled_image,original_image):
    measure_image=measure.regionprops_table(labelled_image,intensity_image=original_image,properties=('area','perimeter','centroid','orientation','major_axis_length','minor_axis_length','mean_intensity','max_intensity'))
    measure_dataframe=pd.DataFrame.from_dict(measure_image)
    return measure_dataframe

# This is to look at coincidence purely in terms of pixels

def coincidence_analysis_pixels(binary_image1,binary_image2):
    pixel_overlap_image=binary_image1&binary_image2         
    pixel_overlap_count=pixel_overlap_image.sum()
    pixel_fraction=pixel_overlap_image.sum()/binary_image1.sum()
    
    return pixel_overlap_image,pixel_overlap_count,pixel_fraction

# Look at coincidence in terms of features. Needs binary image input 

def feature_coincidence(binary_image1,binary_image2):
    number_of_features,labelled_image1=label_image(binary_image1)          # Labelled image is required for this analysis
    coincident_image=binary_image1 & binary_image2        # Find pixel overlap between the two images
    coincident_labels=labelled_image1*coincident_image   # This gives a coincident image with the pixels being equal to label
    coinc_list, coinc_pixels = np.unique(coincident_labels, return_counts=True)     # This counts number of unique occureences in the image
    # Now for some statistics
    total_labels=labelled_image1.max()
    total_labels_coinc=len(coinc_list)
    fraction_coinc=total_labels_coinc/total_labels
    
    # Now look at the fraction of overlap in each feature
    # First of all, count the number of unique occurances in original image
    label_list, label_pixels = np.unique(labelled_image1, return_counts=True)
    fract_pixels_overlap=[]
    for i in range(len(coinc_list)):
        overlap_pixels=coinc_pixels[i]
        label=coinc_list[i]
        total_pixels=label_pixels[label]
        fract=1.0*overlap_pixels/total_pixels
        fract_pixels_overlap.append(fract)
    
    
    # Generate the images
    coinc_list[0]=1000000   # First value is zero- don't want to count these. 
    coincident_features_image=np.isin(labelled_image1,coinc_list)   # Generates binary image only from labels in coinc list
    coinc_list[0]=0
    non_coincident_features_image=~np.isin(labelled_image1,coinc_list)  # Generates image only from numbers not in coinc list.
    
    return coinc_list,coinc_pixels,fraction_coinc,coincident_features_image,non_coincident_features_image,fract_pixels_overlap

Output_all_cases = pd.DataFrame(columns=['Path','Number_of_events','Intensity_mean','Intensity_SD','Intensity_med',
                                       'Area_mean','Area_sd','Area_med','Length_mean','Length_sd','Length_med','Ratio_mean','Ratio_sd','Ratio_med'])



for path in pathlist:
    
    for root, dirs, files in os.walk(path):
            for name in files:
                    if filename_contains in name:
                        if ".tif" in name:
                            resultsname = name
                            print(resultsname)
     
    image_path=path+resultsname
    print(image_path)
        
        
        
    green=load_image(image_path)
   

    green_flat=z_project(green)


    green_filtered=subtract_bg(green_flat)


    imsr2 = Image.fromarray(green_flat)
    imsr2.save(path+'Green_flat.tif')
    larger=imsr2.resize((4096, 4096))
    larger.save(path+'Green_flat_scaled.tif')
    
    
    imsr2 = Image.fromarray(green_filtered)
    imsr2.save(path+'Green_filtered.tif')
    larger=imsr2.resize((4096, 4096))
    larger.save(path+'Green_filtered_scaled.tif')
    
    green_threshold,green_binary=threshold_image_otsu(green_filtered)
    im = Image.fromarray(green_binary)
    im.save(path+'Green_Binary.tif')
    larger=im.resize((4096, 4096))
    larger.save(path+'Green_Binary_scaled.tif')
    
    
    green_number,green_labelled=label_image(green_binary)
    print("%d feautres were detected in the green image."%green_number)
    measurements=analyse_labelled_image(green_labelled,green_filtered)
    
    
    labeltot=green_labelled.max()+1
        
    print('Total number of clusters in labelled image: %d'%labeltot)
    
    # Make and save histograms
            
    areas=measurements['area']*((Pixel_size/1000)**2)
    plt.hist(areas, bins = 20,range=[0,2], rwidth=0.9,color='#ff0000')
    plt.xlabel('Area (\u03bcm$^2$)',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster area',size=20)
    plt.savefig(path+"Area.pdf")
    plt.show()
    
    median_area=areas.median()
    mean_area=areas.mean()
    std_area=areas.std()
    
    
    length=measurements['major_axis_length']*((Pixel_size))
    plt.hist(length, bins = 20,range=[0,5000], rwidth=0.9,color='#ff0000')
    plt.xlabel('Length (nm)',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster lengths',size=20)
    plt.savefig(path+"Lengths.pdf")
    plt.show()

    median_length=length.median()
    mean_length=length.mean()
    std_length=length.std()
    
    ratio=measurements['minor_axis_length']/measurements['major_axis_length']
    plt.hist(ratio, bins = 50,range=[0,1], rwidth=0.9,color='#ff0000')
    plt.xlabel('Eccentricity',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster Eccentricity',size=20)
    plt.savefig(path+"Ecc.pdf")
    plt.show()
    
    
    intensities_all=measurements['max_intensity']
    mean_intensity=intensities_all.mean()
    std_intensity=intensities_all.std()
    median_intensity=intensities_all.median()
                            
    median_ratio=ratio.median()
    mean_ratio=ratio.mean()
    std_ratio=ratio.std()
    
    measurements['Eccentricity']=ratio
   
    
    measurements.to_csv(path + '/' + 'ThT_Metrics.csv', sep = '\t')
    

    
    Output_all_cases = Output_all_cases.append({'Path':path,'Number_of_events':labeltot,'Intensity_mean':mean_intensity,'Intensity_SD':std_intensity,'Intensity_med':median_intensity,
                                                'Area_mean':mean_area,'Area_sd':std_area,'Area_med':median_area,'Length_mean':mean_length,'Length_sd':std_length,'Length_med':median_length,
                                                'Ratio_mean':mean_ratio,'Ratio_sd':std_ratio,'Ratio_med':median_ratio},ignore_index=True)


    Output_all_cases.to_csv(root_path + 'all_ThT_metrics.csv', sep = '\t')



