import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import EllipseCollection
from PIL import Image  # Note this may require the 'Pillow' package instead of 'PIL' depending on the Python IDE used
from matplotlib import image

#######################################################################################################################
# Code for reconstructing the SOP from experimental intensity measurements of the right (R), left (L), horizontal (H) #
# and diagonal (D) components                                                                                         #
#######################################################################################################################

# Loading experimental intensity images #

R = Image.open('MR.png')
L = Image.open('ML.png')
H = Image.open('MH.png')
D = Image.open('MD.png')

# Resizing intensity images to allow for a visible ellipse resolution (50 x 50 pixels) #

R.thumbnail((50, 50), Image.ANTIALIAS)
L.thumbnail((50, 50), Image.ANTIALIAS)
H.thumbnail((50, 50), Image.ANTIALIAS)
D.thumbnail((50, 50), Image.ANTIALIAS)

# Saving re-sized images #

R.save('R2.png')
L.save('L2.png')
H.save('H2.png')
D.save('D2.png')

# Reading re-sized images into arrays #

R3 = image.imread('R2.png')
L3 = image.imread('L2.png')
H3 = image.imread('H2.png')
D3 = image.imread('D2.png')

# Displays re-sized matrices and requires user to click the center of each intensity measurement for cropping #

plt.imshow(R3, cmap='gray')
plt.colorbar()
Rcenter = np.round(plt.ginput(n=1))
plt.close()

plt.imshow(L3, cmap='gray')
plt.colorbar()
Lcenter = np.round(plt.ginput(n=1))
plt.close()

plt.imshow(H3, cmap='gray')
plt.colorbar()
Hcenter = np.round(plt.ginput(n=1))
plt.close()
#
plt.imshow(D3, cmap='gray')
plt.colorbar()
Dcenter = np.round(plt.ginput(n=1))
plt.close()

size = 15  # Pixels to crop on each side of selected center (this may be of use for multiplexed intensity measurements)
# N.B. User should ensure that this does not extend beyond the edge of the image matrix

# Loop differentiates between Gray and RGB/RGBA images (takes only one colour matrix from the latter) then crops#

if len(R3.shape) > 2:
    R4 = R3[int(Rcenter[0, 1]) - size:int(Rcenter[0, 1]) + size, int(Rcenter[0, 0]) - size:int(Rcenter[0, 0]) + size, 1]
    L4 = L3[int(Lcenter[0, 1]) - size:int(Lcenter[0, 1]) + size, int(Lcenter[0, 0]) - size:int(Lcenter[0, 0]) + size, 1]
    H4 = H3[int(Hcenter[0, 1]) - size:int(Hcenter[0, 1]) + size, int(Hcenter[0, 0]) - size:int(Hcenter[0, 0]) + size, 1]
    D4 = D3[int(Dcenter[0, 1]) - size:int(Dcenter[0, 1]) + size, int(Dcenter[0, 0]) - size:int(Dcenter[0, 0]) + size, 1]
else:
    R4 = R3[int(Rcenter[0, 1])-size:int(Rcenter[0, 1])+size, int(Rcenter[0, 0])-size:int(Rcenter[0, 0])+size]
    L4 = L3[int(Lcenter[0, 1])-size:int(Lcenter[0, 1])+size, int(Lcenter[0, 0])-size:int(Lcenter[0, 0])+size]
    H4 = H3[int(Hcenter[0, 1])-size:int(Hcenter[0, 1])+size, int(Hcenter[0, 0])-size:int(Hcenter[0, 0])+size]
    D4 = D3[int(Dcenter[0, 1])-size:int(Dcenter[0, 1])+size, int(Dcenter[0, 0])-size:int(Dcenter[0, 0])+size]

# Stokes parameters calculation #

S0 = R4 + L4
S1 = 2*H4 - S0
S2 = 2*D4 - S0
S3 = (R4 - L4)

# Ellipses Parameters #

L_hyp = np.hypot(S1, S2)
h = np.sqrt((np.sqrt(S1**2+S2**2+S3**2)-L_hyp)/2)  # Semi-minor axis
w = np.sqrt((np.sqrt(S1**2+S2**2+S3**2)+L_hyp)/2)  # Semi-major axis
Psi = np.angle(S1+1j*S2)/2  # Ellipse orientation angle
H = np.sign(S3)  # Circular polarisation handedness (allows for inhomogeneous handedness)

x = np.linspace(0, 2*size, 2*size)
y = np.linspace(0, 2*size, 2*size)

X, Y = np.meshgrid(x, y)

# Ellipses Plotting #

XY = np.column_stack((X.ravel(), -Y.ravel()))

fig, ax = plt.subplots()
ax.set_facecolor('white')

ec = EllipseCollection(w, h, np.rad2deg(Psi), units='xy', offsets=XY,
                       transOffset=ax.transData, cmap='Greens', facecolors='none')
ec.set_array(S0.ravel())  # Scales ellipse colour to intensity (i.e. S0)
# ec.set_array(H.ravel()) This line may be used to allow for the scaling of the ellipse colour with the measured
# handedness (i.e. +/- 1 for right/left respectively)

ax.add_collection(ec)
ax.autoscale_view()
c_bar = plt.colorbar(ec)
c_bar.set_label('Measured $S_0$')
plt.axis('off')  # Remove this line to see the axes
plt.show()
