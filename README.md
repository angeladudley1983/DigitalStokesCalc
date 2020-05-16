# DigitalStokesCalc

In this folder are Python codes allowing for SOP theoretical simulation (SOPCodeTheoretical.py) and experimental reconstruction (SOPCodeExperimental.py)
 - as well as the experimental calculation of Stokes parameters (StokesParametersExperimental.py) and the simulation of expected parameters (StokesParametersTheoretical.py).

All codes are currently set up to deal with TE vector vortex beams expressed using Laguerre-Gaussian modes in the right-left circular polarisation basis,
however appropriate changes to the R, L, H and D components in the relevant codes will allow for their use in a variety of cases.

In order to run these the user will need to install the following Python packages:

1. numpy
2. scipy
3. math
4. matplotlib.pyplot
5. PIL (or Pillow for certain IDEs - e.g. PyCharm)

N.B. The simulation '...Theoretical.py' codes have dependence on the Laguerre-Gaussian generating function 'LagMode.py'.

The handedness matrix H calculated by the SoP codes can be manipulated as the user requires,
possible ways to do this are presented in the comments of both the experimental and theoretical SOP codes.

Experimental images of Stokes intensities (.png files) obtained in the conventional manner are also given for the users convenience in testing the experimental codes.
