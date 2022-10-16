#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
import numpy as np
import astropy.io.fits as fits
from astropy.wcs import WCS as WCS
#import aplpy,pdb
#import matplotlib.pyplot as mpl
import sys,glob,os,pdb
#import matplotlib.gridspec as gridspec
#import pandas as pd

# read in the big fits image
filein = fits.open('C:/Users/wensu/Documents/research/goodsn_epoch1_v0.9_F275W_60mas_sci.fits')
hf,df = filein[0].header,filein[0].data
# eventually you'll add in other images to read in  -- this is going to ultimately take about 5 gb's of memory to operatre

#read in the catalog which has magnitudes
rdpos_cat = fits.open('C:/Users/wensu/Documents/research/hlsp_UVcandels_hst_wfc3_goodsn_multi_v3-0.5_photometry-cat.fits')
data = rdpos_cat[1].data
x_image,y_image = np.array(data['X_IMAGE']),np.array(data['Y_IMAGE'])

#read in the redshift catalog
zpos_cat = np.genfromtxt('C:/Users/wensu/Documents/research/uvcandels_photz_eazy.txt',dtype=[('field',"|U8"),('objnoo',int),('redshift',float)],usecols=[0,1,2])
field,objnoo,redshift = zpos_cat['field'],zpos_cat['objnoo'],zpos_cat['redshift']
gn_ = np.logical_and(field == "goodsn",redshift < 1)
field,objnoo,redshift = np.array(field[gn_]),np.array(objnoo[gn_]),np.array(redshift[gn_])
print(objnoo,redshift)




# #convert ra/dec positions into pixels for cutout
#
sci='C:/Users/wensu/Documents/research/goodsn_epoch1_v0.9_F275W_60mas_sci.fits'
wcs_sol = WCS(sci)
ra,dec =  wcs_sol.wcs_pix2world(x_image,y_image,0)
#print(ra,dec)

# ### convert the ra, dec from the 275 to the x,y positions for your other wavelength images
# ### newx,newy =  wcs_sol.wcs_world2pix(ra,dec,0)

# # In the case of the UVCANDELS catalogs ONLY, the inputs will be pixels.
# # You'll need to take these pixel positions and convert to ra/dec and THEN convert back to pixels in the other fields.
# #loop over the positions:

for j in range(0,10):
	xlow,xhigh = np.int(y_image[j]-50),np.int(y_image[j]+50)
	ylow,yhigh = np.int(x_image[j]-50),np.int(x_image[j]+50)
	w = WCS(hf)
	newarr = df[xlow:xhigh,ylow:yhigh]
	#save cut-out objects as fits file
	newf = fits.PrimaryHDU()
	newf.data =  newarr
	newf.header = hf
	newf.header.update(w[xlow:xhigh,ylow:yhigh].to_header())
    ## good name: the name of the field _ object number _ wavelength/filter/redshift
	newf.writeto("{0}_{1}_{2}.fits".format(field[j],objnoo[j],redshift[j]),overwrite=True)

