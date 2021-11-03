#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 14:47:52 2021

@author: Mathew
"""

import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from skimage import filters,measure
from PIL import Image
import pandas as pd
import os
from skimage import io
root_path=r"/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/"
pathlist=[]     
Pixel_size=103
scale=8
# Add paths below



pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Lys_2021-09-07_13-04-11/1/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Lys_2021-09-07_13-04-11/2/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Lys_2021-09-07_13-04-11/3/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Lys_2021-09-07_13-04-11/4/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Lys_2021-09-07_13-04-11/5/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Lys_2021-09-07_13-04-11/6/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Sup_2021-09-07_12-32-26/1/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Sup_2021-09-07_12-32-26/2/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Sup_2021-09-07_12-32-26/3/")
pathlist.append("/Volumes/chem-mh-store/Members/Mathew Horrocks/20210907_Wren/Sup_2021-09-07_12-32-26/4/")

DL_filename="Green_Binary_scaled_shifted.tif"
SR_image="SR_fwhm_python_clustered.tif"
SR_stats_file="Metrics.csv"


# Look for coincidence

def feature_coincidence(labelled_image1,binary_image2):
    coincident_image=labelled_image1&binary_image2        # Find pixel overlap between the two images
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



Output_all_cases = pd.DataFrame(columns=['Path','Total_clusters','Coinc_clusters','Coinc_fraction','Coinc_Points_per_cluster_mean','Coinc_Points_per_cluster_SD','Coinc_Points_per_cluster_med',
                                       'Coinc_Area_mean','Coinc_Area_sd','Coinc_Area_med','Coinc_Length_mean','Coinc_Length_sd','Coinc_Length_med','Coinc_Ratio_mean','Coinc_Ratio_sd','Coinc_Ratio_med','non_coinc_Number_of_clusters','non_coinc_Points_per_cluster_mean','non_coinc_Points_per_cluster_SD','non_coinc_Points_per_cluster_med',
                                       'non_coinc_Area_mean','non_coinc_Area_sd','non_coinc_Area_med','non_coinc_Length_mean','non_coinc_Length_sd','non_coinc_Length_med','non_coinc_Ratio_mean','non_coinc_Ratio_sd','non_coinc_Ratio_med'])

for path in pathlist:
    path=path.replace("/Volumes/VERBATIM HD/210812_1nM590_timecourse/","/Users/Mathew/Documents/Current analysis/20210816_RRM_agg_ThT_added/")
    # First of all, load the images and the metrics
    
    DL=io.imread(path+DL_filename).astype('int')
    SR=io.imread(path+SR_image).astype('int')
    SR_stats=pd.read_csv(path+SR_stats_file,sep='\t')
    
    SR_coinc_list,SR_coinc_pixels,SR_fraction_coinc,SR_coincident_features_image,SR_noncoincident_features_image,SR_fraction_pixels_overlap=feature_coincidence(SR,DL)
    
    coinc_or_not=np.zeros(len(SR_stats))
    
    for i in SR_coinc_list:
        coinc_or_not[i-1]=1
        
    
    SR_stats['Coincident']=coinc_or_not
    
    SR_stats.to_csv(path + 'Metrics_all_with_coinc.csv', sep = '\t')
    
    
    coinc_metrics=SR_stats.copy()
    
    index_names = coinc_metrics[coinc_metrics['Coincident']==0].index
    coinc_metrics.drop(index_names, inplace = True)
    
    non_coinc_metrics=SR_stats.copy()
    
    index_names = non_coinc_metrics[non_coinc_metrics['Coincident']==1].index
    non_coinc_metrics.drop(index_names, inplace = True)
    
    coinc_metrics.to_csv(path + 'Metrics_Coinc.csv', sep = '\t')
    non_coinc_metrics.to_csv(path + 'Metrics_Non_Coinc.csv', sep = '\t')
    
    
    # Output plots
    coinc_clusters=coinc_metrics['Number_of_locs']
    
    plt.hist(coinc_clusters, bins = 20,range=[0,200], rwidth=0.9,color='#607c8e') # Plot a histogram. 
    plt.xlabel('Localisations per cluster')
    plt.ylabel('Number of clusters')
    plt.savefig(path+'/'+'Coinc_Localisations.pdf')
    plt.show()
    
    coinc_median_locs=np.median(coinc_clusters)
    coinc_mean_locs=coinc_clusters.mean()
    coinc_std_locs=coinc_clusters.std()
    
    
    non_coinc_clusters=non_coinc_metrics['Number_of_locs']
    
    plt.hist(non_coinc_clusters, bins = 20,range=[0,200], rwidth=0.9,color='#607c8e') # Plot a histogram. 
    plt.xlabel('Localisations per cluster')
    plt.ylabel('Number of clusters')
    plt.savefig(path+'/'+'Non_Coinc_Localisations.pdf')
    plt.show()
    
    non_coinc_median_locs=np.median(non_coinc_clusters)
    non_coinc_mean_locs=non_coinc_clusters.mean()
    non_coinc_std_locs=non_coinc_clusters.std()
    
    coinc_areas=coinc_metrics['area']*((Pixel_size/(scale*1000))**2)
    plt.hist(coinc_areas, bins = 20,range=[0,0.1], rwidth=0.9,color='#ff0000')
    plt.xlabel('Area (\u03bcm$^2$)',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster area',size=20)
    plt.savefig(path+"Coinc_Area.pdf")
    plt.show()
    
    coinc_median_area=coinc_areas.median()
    coinc_mean_area=coinc_areas.mean()
    coinc_std_area=coinc_areas.std()
    
    
    coinc_length=coinc_metrics['major_axis_length']*((Pixel_size/8))
    plt.hist(coinc_length, bins = 20,range=[0,1000], rwidth=0.9,color='#ff0000')
    plt.xlabel('Length (nm)',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster lengths',size=20)
    plt.savefig(path+"Coinc_Lengths.pdf")
    plt.show()

    coinc_median_length=coinc_length.median()
    coinc_mean_length=coinc_length.mean()
    coinc_std_length=coinc_length.std()

    non_coinc_areas=non_coinc_metrics['area']*((Pixel_size/(scale*1000))**2)
    plt.hist(non_coinc_areas, bins = 20,range=[0,0.1], rwidth=0.9,color='#ff0000')
    plt.xlabel('Area (\u03bcm$^2$)',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster area',size=20)
    plt.savefig(path+"non_coinc_Area.pdf")
    plt.show()
    
    non_coinc_median_area=non_coinc_areas.median()
    non_coinc_mean_area=non_coinc_areas.mean()
    non_coinc_std_area=non_coinc_areas.std()
    
    
    non_coinc_length=non_coinc_metrics['major_axis_length']*((Pixel_size/8))
    plt.hist(non_coinc_length, bins = 20,range=[0,1000], rwidth=0.9,color='#ff0000')
    plt.xlabel('Length (nm)',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster lengths',size=20)
    plt.savefig(path+"non_coinc_Lengths.pdf")
    plt.show()

    non_coinc_median_length=non_coinc_length.median()
    non_coinc_mean_length=non_coinc_length.mean()
    non_coinc_std_length=non_coinc_length.std()

    coinc_ratio=coinc_metrics['minor_axis_length']/coinc_metrics['major_axis_length']
    plt.hist(coinc_ratio, bins = 50,range=[0,1], rwidth=0.9,color='#ff0000')
    plt.xlabel('Eccentricity',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster Eccentricity',size=20)
    plt.savefig(path+"Coinc_Ecc.pdf")
    plt.show()
    
    coinc_median_ratio=coinc_ratio.median()
    coinc_mean_ratio=coinc_ratio.mean()
    coinc_std_ratio=coinc_ratio.std()
    
    non_coinc_ratio=non_coinc_metrics['minor_axis_length']/non_coinc_metrics['major_axis_length']
    plt.hist(non_coinc_ratio, bins = 50,range=[0,1], rwidth=0.9,color='#ff0000')
    plt.xlabel('Eccentricity',size=20)
    plt.ylabel('Number of Features',size=20)
    plt.title('Cluster Eccentricity',size=20)
    plt.savefig(path+"non_coinc_Ecc.pdf")
    plt.show()
    
    non_coinc_median_ratio=non_coinc_ratio.median()
    non_coinc_mean_ratio=non_coinc_ratio.mean()
    non_coinc_std_ratio=non_coinc_ratio.std()
    
    total=len(SR_stats)
    coinc_num=len(SR_coinc_list)
    coinc_frac=coinc_num/total
    
    Output_all_cases = Output_all_cases.append({'Path':path,'Total_clusters':total,'Coinc_clusters':coinc_num,'Coinc_fraction':coinc_frac,'Coinc_Points_per_cluster_mean':coinc_mean_locs,'Coinc_Points_per_cluster_SD':coinc_std_locs,'Coinc_Points_per_cluster_med':coinc_median_locs,
                                       'Coinc_Area_mean':coinc_mean_area,'Coinc_Area_sd':coinc_std_area,'Coinc_Area_med':coinc_median_area,'Coinc_Length_mean':coinc_mean_length,'Coinc_Length_sd':coinc_std_length,'Coinc_Length_med':coinc_median_length,'Coinc_Ratio_mean':coinc_mean_ratio,'Coinc_Ratio_sd':coinc_std_ratio,'Coinc_Ratio_med':coinc_median_ratio,'non_coinc_Points_per_cluster_mean':non_coinc_mean_locs,'non_coinc_Points_per_cluster_SD':non_coinc_std_locs,'non_coinc_Points_per_cluster_med':non_coinc_median_locs,
                                       'non_coinc_Area_mean':non_coinc_mean_area,'non_coinc_Area_sd':non_coinc_std_area,'non_coinc_Area_med':non_coinc_median_area,'non_coinc_Length_mean':non_coinc_mean_length,'non_coinc_Length_sd':non_coinc_std_length,'non_coinc_Length_med':non_coinc_median_length,'non_coinc_Ratio_mean':non_coinc_mean_ratio,'non_coinc_Ratio_sd':non_coinc_std_ratio,'non_coinc_Ratio_med':non_coinc_median_ratio},ignore_index=True)
    
    
    Output_all_cases.to_csv(root_path + 'GDSCSMLM_all_metrics_with_ThT.csv', sep = '\t')
    
    