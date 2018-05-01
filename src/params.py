from __future__ import division
import numpy as np

##### CONSTANTS / PARAMETERS -- ORIGINAL BY WAGNER AND EISENMAN #####
D = 0.6 #diffusivity for heat transport (W m^-2 K^-1)
A = 193.0 #OLR when T = 0 (W m^-2)
B = 2.1 #OLR temperature dependence (W m^-2 K^-1)
cw = 9.8 #ocean mixed-layer heat capacity (W yr m^-2 K^-1)
S0 = 420.0 #insolation at equator (W m^-2)
S1 = 180#338.0 #insolation seasonal dependence (W m^-2)
S2 = 240.0 #insolation spatial dependence (W m^-2)
a0 = 0.7 #ice-free co-albedo at equator
a2 = 0.1 #ice-free co-albedo spatial dependence
ai = 0.4 #co-albedo where there is sea ice
Fb = 4.0 #heat flux from ocean below (W m^-2)
F = 0.0 #prescribed forcing (W m^-2)
k = 2.0 #sea ice thermal conductivity (W m^-2 K^-1)
Lf = 9.0 #sea ice latent heat of fusion (W yr m^-3)
cg = 0.01*cw #ghost layer heat capacity(W yr m^-2 K^-1)
tau = 1.0E-5 #ghost layer coupling timescale (yr)
Tm = 0.0 #melting temperature of ice (deg C)


##### NUMERICAL SOLUTION DEFAULTS #####
NX_LOWRES = 100 #number of x-grid points for low-resolution run
NX_HIGHRES = 600 # "" "" for high-resolution run (default model takes 10min)
NT_LOWRES = 1000 #number of time-steps for low-resolution run
NT_HIGHRES = 1000 # "" "" for high-resolution run
DURATION_LOWRES = 30 #no. of years to integrate forward (low resolution run)
DURATION_HIGHRES = 30 # "" "" (high resolution run)


##### NEW PARAMETERS BY JAKE AYLMER #####
#---For the variable heat-capacity:
HML_OCEAN = 75.0 # (m)
HML_ICE = 40.0 # (m)
CwRho = cw/HML_OCEAN #mixed-layer heat-capacity per unit volume (W yr m^-3 K^-1)
XAPFZ = .5*np.sqrt(3.) # = sin(60 deg)
HC_WIDTH = 0.05 # (dimensionless)

#---For the variable basal heat flux (erf(x) form):
DELTA_FB = 10.0 # Wm^-2
FB_ICE = 4.0 # Wm^-2
FB_X_WIDTH = 0.02 # (dimensionless)

custom_filename = 'WE2015_DEFAULT_DATA_'
