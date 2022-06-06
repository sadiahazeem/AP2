import matplotlib
matplotlib.use('MacOSX', force=True)
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import matplotlib.ticker as plticker#
try:
    from PIL import Image
except ImportError:
    import Image

image = Image.open('us2/content/bscan_oben.pdf')
my_dpi=300.
fig=plt.figure(figsize=(float(image.size[0])/my_dpi,float(image.size[1])/my_dpi),dpi=my_dpi)
ax=fig.add_subplot(111)

# Remove whitespace from around the image
fig.subplots_adjust(left=0,right=1,bottom=0,top=1)

# Set the gridding interval: here we use the major tick interval
myInterval=100.
loc = plticker.MultipleLocator(base=myInterval)
ax.xaxis.set_major_locator(loc)
ax.yaxis.set_major_locator(loc)

# Add the grid
ax.grid(which='major', axis='both', linestyle='-')

# Add the image
ax.imshow(image)

# Find number of gridsquares in x and y direction
nx=abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(myInterval)))
ny=abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(myInterval)))



s = 0.5 * 10**-2
t = 1.8 *10**-6

print("v = ", s/t)


########## brusttumor ##########

print("durchmesser der beiden kleinen löcher zusammen: ", 2/7 * 13.8)
print("durchmesser des festen tumors: ", 1.5 * 13.8)
print("tiefe des festen tumors: ", 1.4 * 13.8)
print("tiefe des flüssigen tumors: ", 1.8 * 13.8)

