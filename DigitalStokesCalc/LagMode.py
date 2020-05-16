import math
import numpy as np
import scipy
from scipy import special

#########################################
# Laguerré-Gaussian generating function #
#########################################

# Takes azimuthal index, radial index, radial co-ordinate, azimuthal co-ordinate and beam waist as inputs


def LagMode(l_idx, p_idx, R, TH, w0):
    out = np.sqrt((2 * math.factorial(p_idx)) / (math.pi * math.factorial(abs(l_idx) + p_idx))) * \
                   ((np.sqrt(2) * R) / w0) ** abs(l_idx) * \
                   np.exp(-(R / w0) ** 2) * \
                   np.exp(1j * l_idx * TH) * \
                   scipy.special.assoc_laguerre(2 * (R ** 2 / w0 ** 2), p_idx, abs(l_idx))

    return out

# This expression of the Laguerré-Gaussian mode ignores any propagation dependence
