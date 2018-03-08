from __future__ import division
import params
import numpy as np
import scipy.special as sp

def HeatCapacity(x):
    """Form of heat-capacity based on an erf(x) smoothed by an amount HC_WIDTH 
    about x=XAPFZ, the position of the antarctic polar frontal zone."""
    return .5*(params.CwRho*params.HML_ICE+params.CwRho*params.HML_OCEAN)+.5*(
        params.CwRho*params.HML_ICE-params.CwRho*params.HML_OCEAN)*sp.erf((
        x-params.XAPFZ)/params.HC_WIDTH)


def HeatCapacityInteractive(x, xi):
    """Form of heat-capacity based on an erf(x) smoothed by and amount HC_WIDTH
    about the current position of the ice-edge (this must be set dynamically in
    the main program i.e. calculated after every time step)."""
    return .5*(params.CwRho*params.HML_ICE+params.CwRho*params.HML_OCEAN)+.5*(
        params.CwRho*params.HML_ICE-params.CwRho*params.HML_OCEAN)*sp.erf((x-xi
        +params.HC_WIDTH)/params.HC_WIDTH)


def BasalFlux(x):
    """Form of basal heat flux based on erf(x) smoothed by an amount FB_X_WIDTH
    about x=XAPFZ, the position of the antarctic polar frontal zone."""
    return .5*(2*params.FB_ICE + params.DELTA_FB) - .5*params.DELTA_FB*sp.erf((
        x-params.XAPFZ)/params.FB_X_WIDTH)


def BasalFluxInteractive(x, xi):
    """Form of basal heat flux based on erf(x) smoothed by an amount FB_X_WIDTH
    about the current position of the ice-edge (this must be set dynamically in
    the main program i.e. calculated after every time time step)."""
    return params.FB_ICE + .5*params.DELTA_FB*(1-sp.erf(
        (x-xi)/params.FB_X_WIDTH))
