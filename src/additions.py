from __future__ import division
import params
import scipy.special as sp

def HeatCapacity(x):
    """Form of heat-capacity (mixed-layer depth) based on an erf(x) smoothed
    by an amount HC_WIDTH about x=XAPFZ, the position of the antarctic polar
    frontal zone."""
    return .5*(params.CwRho*params.HML_ICE+params.CwRho*params.HML_OCEAN)+.5*(
        params.CwRho*params.HML_ICE-params.CwRho*params.HML_OCEAN)*sp.erf((
        x-params.XAPFZ)/params.HC_WIDTH)


def HeatCapacityInteractive(x, xi):
    """"""
    return .5*(params.CwRho*params.HML_ICE+params.CwRho*params.HML_OCEAN)+.5*(
        params.CwRho*params.HML_ICE-params.CwRho*params.HML_OCEAN)*sp.erf((x-xi
        +params.HC_WIDTH)/params.HC_WIDTH)


def BasalFluxInteractive(x, xi):
    """"""
    return params.FB_ICE + .5*params.DELTA_FB*(1-sp.erf((x-xi)/params.FB_X_WIDTH))


def BasalFlux(x):
    """Form of basal heat flux based on erf(x) smoothed by an amount HFC_WIDTH
    about x=XAPFZ, the position of the anarctic polar frontal zone."""
    return .5*(2*params.FB_ICE + params.DELTA_FB) - .5*params.DELTA_FB*sp.erf((x-params.XAPFZ)/params.HC_WIDTH)
