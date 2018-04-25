### EBM_SCM_MODEL (Wagner and Eisenman 2015)
### Modified and used by Jake Aylmer
###
### Some code to test whether the default model as outlined in the original
### paper is conserving energy. This would seem to be an important property for
### any model of climate to have and it is not obvious that equation (9) is
### not breaking that.
### ---------------------------------------------------------------------------

from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as filing


def EnergyDiagnostic(enth_prev, enth_current, enth_next, temperature, x, t, dt):
    """Calculate the residual energy stored in the system at time t, i.e.
    the integral of WE2015 eq. (2):
    
        integral{ dE/dt - aS + L - D*del^2 T - Fb - F } dx over [0,1]
    
    Note that the laplacian term drops out to zero.
    
    --Args--
    enth_prev    : NumPy array, shape (n_x, ); E(x) [W yr m^-2] at time t-dt [yr].
    enth_current : NumPy array, shape (n_x, ); E(x) [W yr m^-2] at time t [yr].
    enth_next    : NumPy array, shape (n_x, ); E(x) [W yr m^-2] at time t+dt [yr].
    temperature  : NumPy array, shape (n_x, ); T(x) [degC] at time t [yr].
    x            : NumPy array, shape (n_x, ); x-coordinates of cell centres.
    t            : float; current time [yr].
    dt           : float; time step [yr].
    """
    dx = x[1] - x[0] #assumes uniform grid spacing
    
    ddt_enth = (enth_next - enth_prev) / (2*dt)
    
    int_ddt_enth = np.sum(ddt_enth) * dx
    
    a =  WE.OceanAlbedo(x)*(enth_current>=0) + params.ai*(enth_current<0)
    S = params.S0 - params.S1*x*np.cos(2*np.pi*t) - params.S2*x**2
    int_aS = np.sum(a*S)*dx
    
    int_L = params.A + params.B*np.sum(temperature)*dx - params.B*params.Tm
    
    dE = int_ddt_enth - int_aS + int_L - params.Fb - params.F
    
    return dE


def EnergyDiagnostic2(x, t, enthalpy, temperature):
    """Alternative energy conservation diagnostic. Returns the total energy
    stored at time t and net flux leaving the system at time t.
    
    --Args--
    x           : NumPy array, x = sin(lat) coordinates.
    t           : float, current time [yr]
    enthalpy    : NumPy array, surface enthalpy profile at time t [W yr m^-2].
    temperature : NumPy array, temperature profile at time t [degC].
    """
    
    dx = x[1] - x[0] #grid spacing, assumed constant.
    
    E_stored_total = np.sum(enthalpy)*dx
    
    a =  WE.OceanAlbedo(x)*(enthalpy>=0) + params.ai*(enthalpy<0)
    S = params.S0 - params.S1*x*np.cos(2*np.pi*t) - params.S2*x**2
    int_aS = np.sum(a*S)*dx
    
    int_L = params.A + params.B*np.sum(temperature)*dx - params.B*params.Tm
    
    net_flux_leaving = int_L - int_aS - params.Fb - params.F
    
    return E_stored_total, net_flux_leaving


def main(lowres=False, usesaved=False, savefigs=True, custom=False):
    """For the standard model implementation by Wagner and Eisenman (WE2015),
    test whether it is conserving energy by calculating the integral over the
    hemisphere of their equation (2). By integrating, the D*laplacian(T) term
    drops out.
    """
    if usesaved:
        if custom:
            t, x, E, T = filing.OpenData(
                params.custom_filename + ('LR' if lowres else 'HR') )
        else:
            t, x, E, T = filing.OpenData(
                'WE2015_DEFAULT_DATA_' + ('LR' if lowres else 'HR') )
    else:
        t, x, E, T = WE.Integration(lowres, varyHML=False, varyFB=False)
        filing.SaveData(t, x, E, T, 'DAT_constFb=%.1f_constHML=%.1f_' % (
            params.Fb, params.HML_OCEAN) + ('LR' if lowres else 'HR') )
    
    # We now have an equilibrated seasonal cycle surface enthalpy E(x,t) and 
    # temperature profile T specified at certain times within the season.
    
    dx = x[1]-x[0]
    dt = t[1]-t[0]
    dE = np.zeros(len(t)-2)
    for i in xrange(1, len(t)-1):
        dE[i-1] = EnergyDiagnostic(np.array([enth[i-1] for enth in E]),
            np.array([enth[i] for enth in E]),
            np.array([enth[i+1] for enth in E]),
            np.array([temp[i] for temp in T]), x, t[i], dt=dt )
    
    # Return also the integral of this curve (if zero, net energy loss within
    # one seasonal cycle is zero so maybe okay...):
    int_dE = np.sum(dE)*dt
    print "The integral of dE over time = %.4f W yr m^-2" % int_dE
    
    # Now use the second diagnostic:
    E_stored = np.zeros(len(t))
    F_leave = np.zeros(len(t))
    for i in xrange(len(t)):
        E_stored[i], F_leave[i] = EnergyDiagnostic2(x, t[i],
            np.array([enth[i] for enth in E]),
            np.array([temp[i] for temp in T]))
    
    fig1, ax1 = pl.PlotEnergyDiagnostic1(t[1:len(t)-1], dE)
    fig1.canvas.set_window_title('cons_test_diag1_dx=%.2E_dt=%.2E' % (dx, dt))
    fig2, ax2a, ax2b = pl.PlotEnergyDiagnostic2(t, E_stored, F_leave)
    fig2.canvas.set_window_title('cons_test_diag2_dx=%.2E_dt=%.2E' % (dx, dt))
    if savefigs:
        filing.SaveFigures([fig1, fig2], 'conservation_tests')
        filing.SaveFigures([fig1, fig2], 'conservation_tests', '.svg')
    fig1.show()
    fig2.show()
    
    pass


if __name__ == '__main__':
    pl.MasterFormatter()
    main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
            savefigs=('savefigs' in sys.argv), custom=('custom' in sys.argv))
