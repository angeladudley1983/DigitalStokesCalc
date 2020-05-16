import matplotlib.pyplot as plt
import numpy as np
from matplotlib import image

#######################################################################################################################
# Code for calculating the Stokes parameters from experimental intensity measurements of the right (R), left (L),     #
# horizontal (H) and diagonal (D) components                                                                          #
#######################################################################################################################

# Reading experimental intensity images into array #

R = image.imread('MR.png')
L = image.imread('ML.png')
H = image.imread('MH.png')
D = image.imread('MD.png')

# Displays image matrices and requires user to click the center of each intensity measurement for cropping #

plt.imshow(R, cmap='gray')
plt.colorbar()
Rcenter = np.round(plt.ginput(n=1))
plt.close()

plt.imshow(L, cmap='gray')
plt.colorbar()
Lcenter = np.round(plt.ginput(n=1))
plt.close()

plt.imshow(H, cmap='gray')
plt.colorbar()
Hcenter = np.round(plt.ginput(n=1))
plt.close()
#
plt.imshow(D, cmap='gray')
plt.colorbar()
Dcenter = np.round(plt.ginput(n=1))
plt.close()

size = 30  # Pixels to crop on each side of selected center (this may be of use for multiplexed intensity measurements)
# N.B. User should ensure that this does not extend beyond the edge of the image matrix from center

# Loop differentiates between Gray and RGB/RGBA images (takes only one colour matrix from the latter) then crops#

if len(R.shape) > 2:
    R2 = R[int(Rcenter[0, 1]) - size:int(Rcenter[0, 1]) + size, int(Rcenter[0, 0]) - size:int(Rcenter[0, 0]) + size, 1]
    L2 = L[int(Lcenter[0, 1]) - size:int(Lcenter[0, 1]) + size, int(Lcenter[0, 0]) - size:int(Lcenter[0, 0]) + size, 1]
    H2 = H[int(Hcenter[0, 1]) - size:int(Hcenter[0, 1]) + size, int(Hcenter[0, 0]) - size:int(Hcenter[0, 0]) + size, 1]
    D2 = D[int(Dcenter[0, 1]) - size:int(Dcenter[0, 1]) + size, int(Dcenter[0, 0]) - size:int(Dcenter[0, 0]) + size, 1]
else:
    R2 = R[int(Rcenter[0, 1])-size:int(Rcenter[0, 1])+size, int(Rcenter[0, 0])-size:int(Rcenter[0, 0])+size]
    L2 = L[int(Lcenter[0, 1])-size:int(Lcenter[0, 1])+size, int(Lcenter[0, 0])-size:int(Lcenter[0, 0])+size]
    H2 = H[int(Hcenter[0, 1])-size:int(Hcenter[0, 1])+size, int(Hcenter[0, 0])-size:int(Hcenter[0, 0])+size]
    D2 = D[int(Dcenter[0, 1])-size:int(Dcenter[0, 1])+size, int(Dcenter[0, 0])-size:int(Dcenter[0, 0])+size]

# Stokes parameters calculation #

S0 = R2 + L2
S1 = 2*H2 - S0
S2 = 2*D2 - S0
S3 = (R2 - L2)

# Plotting and Saving #

plt.imshow(S0, cmap='gray')
plt.colorbar()
plt.savefig('S0')
plt.show()

plt.imshow(S1, cmap='gray')
plt.colorbar()
plt.savefig('S1')
plt.show()

plt.imshow(S2, cmap='gray')
plt.colorbar()
plt.savefig('S2')
plt.show()

plt.imshow(S3, cmap='gray')
plt.colorbar()
plt.savefig('S3')
plt.show()
