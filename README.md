Code used to analyse Owen's data. In vitro time-course with aptamer and ThT. 

1) SR.ijm

This runs GDSCSMLM to generate fitresults.txt file (localisations).

2) Cluster.py

This needs to be run after the super-resolution fitting step. Generates images and 
runs DBSCAN for clustering. The clusters then have number of locs and lengths etc. calculated. 

3) ThT.py

This analyses the diffraction limited images and generates data on size of aggregates etc. It also generates the binary images required for the colocalisation steo. 

4) Translate.py 

Since ThT and SR images are not perfectly overlaid, due to ThT being added post-SR imaging, then there's a slight drift. This script accounts for this. 

5) Coincidence.py

Analyses coincidence between SR and ThT images. 
