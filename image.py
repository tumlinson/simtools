from __future__ import division
import numpy as np
from bokeh.plotting import figure, show, output_file
import os, sys 
from PIL import Image, ImageFilter


N = 20
img = np.empty((N,N), dtype=np.uint32)
view = img.view(dtype=np.uint8).reshape((N, N, 4))
for i in range(N):
    for j in range(N):
        view[i, j, 0] = int(i/N*255)
        view[i, j, 1] = 158
        view[i, j, 2] = int(j/N*255)
        view[i, j, 3] = 255

jpgfile = Image.open("HDST_source_z2.jpg")
r,g,b = np.array(jpgfile.split()) 

print 'img', np.size(img)
print 'img', np.shape(img) 

print 'm', np.size(m)
print 'm', np.shape(m) 

p = figure(x_range=(0,10), y_range=(0,10))

# must give a vector of images
p.image_rgba(image=[img], x=0, y=0, dw=10, dh=10)
print 'right before' 
p.image(image=[r], x=0, y=0, dw=10, dh=10)
print 'right after' 

output_file("image_rgba.html", title="image_rgba.py example")

show(p)  # open a browser
