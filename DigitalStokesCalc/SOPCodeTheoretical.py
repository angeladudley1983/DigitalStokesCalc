import matplotlib.pyplot as plt
import numpy as np
import math
from matplotlib.collections import EllipseCollection
from LagMode import LagMode

#######################################################################################################################
# Code for generating a theoretically simulated SOP for vector beams expressed as a superposition of Laguerré-Gaussian#
# beams in the circular polarisation basis                                                                            #
#######################################################################################################################

# Space Generation #

dx = 0.03*10**(-3)  # Pixel size (m)

x = np.linspace(-25, 25, 30)*dx  # Resolution of ellipses (30)

y = np.linspace(-25, 25, 30)*dx

X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)
TH = np.arctan2(Y, X)

# Intensity Simulation #

w0 = 0.55*10**(-3)  # Beam waist (m)
l_idx = 1  # Laguerré-Gaussian azimuthal index
p_idx = 0  # Laguerré-Gaussian radial index

zr = (math.pi*w0**2)/(633*10**(-9))  # Rayleigh range
z = 0.0017*zr  # Propagation distance 0.0017*zr
k = (2*math.pi)/(633*10**(-9))  # Wave-number
Rad = z*(1+(zr/z)**2)  # Radius of curvature
curvature = (-1j*k*R)/(2*Rad)*0  # If propagation is zero multiply this by 0 (setting z = 0 will result in an error)

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

# Ellipses Parameters Calculation #

L_hyp = np.hypot(S1, S2)
h = np.sqrt((np.sqrt(S1**2+S2**2+S3**2)-L_hyp)/2)*dx  # Ellipse semi-minor axis
w = np.sqrt((np.sqrt(S1**2+S2**2+S3**2)+L_hyp)/2)*dx  # Ellipse semi-major axis
Psi = np.angle(S1+1j*S2)/2  # Ellipse orientation angle
H = np.sign(np.average(S3))  # Circular polarisation handedness (assumes homogeneous handedness)

# Ellipses Plotting #

XY = np.column_stack((X.ravel(), Y.ravel()))  # Sets co-ordinates for ellipses centers

fig, ax = plt.subplots()  # Creates figure environment
ax.set_facecolor('white')  # Background colour


if H > 0:  # Loop for selecting colour based on averaged handedness H
    ec = EllipseCollection(w, h, np.rad2deg(Psi), units='xy', offsets=XY,
                           transOffset=ax.transData, cmap='Reds', facecolors='none')
    ec.set_array(S0.ravel())  # Scales ellipse colour to intensity (i.e. S0)
elif H < 0:
    ec = EllipseCollection(w, h, np.rad2deg(Psi), units='xy', offsets=XY,
                           transOffset=ax.transData, cmap='Blues', facecolors='none')
    ec.set_array(S0.ravel())
else:
    ec = EllipseCollection(w, h, np.rad2deg(Psi), units='xy', offsets=XY,
                           transOffset=ax.transData, cmap='Greens', facecolors='none')
    ec.set_array(S0.ravel())

ax.add_collection(ec)  # Plotting and labelling
ax.autoscale_view()
ax.set(xlim=(-25*dx, 25*dx), ylim=(-25*dx, 25*dx))
plt.axis('off')  # Remove this line to see the axes
c_bar = plt.colorbar(ec)
c_bar.set_label('Normalised $S_0$')
plt.show()
