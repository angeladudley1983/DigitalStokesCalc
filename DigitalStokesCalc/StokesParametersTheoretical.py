import matplotlib.pyplot as plt
import numpy as np
import math
from LagMode import LagMode

#######################################################################################################################
# Code for generating a theoretically simulated Stokes Parameters                                                     #
#######################################################################################################################

# Space Generation #

N = 1920

dx = 1.6*10**(-6)  # Real space per pixel (m)

x = np.linspace(-N/2, N/2, N)*dx  # Resolution (pixels)

y = np.linspace(-N/2, N/2, N)*dx

X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
TH = np.arctan2(Y, X)

# Intensity Simulation #

w0 = 0.75*10**(-3)  # Beam waist (m)
l_idx = 1  # Laguerré-Gaussian azimuthal index
p_idx = 0  # Laguerré-Gaussian radial index

zr = (math.pi*w0**2)/(633*10**(-9))  # Rayleigh range
z = 0.0003*zr  # Propagation distance
k = (2*math.pi)/(633*10**(-9))  # Wave-number
Rad = z*(1+(zr/z)**2)  # Radius of curvature
curvature = (-1j*k*R)/(2*Rad)*0   # If propagation is zero multiply this by 0 (setting z = 0 will result in an error)

UR = LagMode(l_idx, p_idx, R, TH, w0)*np.exp(curvature)  # Polarisation components (fields) utilises LagMode function
UL = LagMode(-l_idx, p_idx, R, TH, w0)*np.exp(-curvature)  # located in LagMode.py
UH = (1/np.sqrt(2))*(UR + UL)
UD = (1/np.sqrt(2))*(UR + 1j*UL)


R = abs(UR*np.conj(UR))  # Polarisation components (normalised intensities)
L = abs(UL*np.conj(UL))
TOT = R + L
R = abs(UR*np.conj(UR))
R = R/np.max(TOT)
L = abs(UL*np.conj(UL))
L = L/np.max(TOT)
D = abs(UD*np.conj(UD))
D = D/np.max(TOT)
H = abs(UH*np.conj(UH))
H = H/np.max(TOT)

# Stokes Parameters Calculation #

S0 = R + L
S1 = 2*H - S0
S2 = 2*D - S0
S3 = R - L

# Plotting and Saving #

plt.imshow(S0, cmap='gray')
plt.colorbar()
plt.savefig('S0Sim')
plt.show()

plt.imshow(S1, cmap='gray')
plt.colorbar()
plt.savefig('S1Sim')
plt.show()

plt.imshow(S2, cmap='gray')
plt.colorbar()
plt.savefig('S2Sim')
plt.show()

plt.imshow(S3, cmap='gray')
plt.colorbar()
plt.savefig('S3Sim')
plt.show()
