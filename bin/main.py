from __future__ import division
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import matplotlib.pyplot as plt
from src import params, model as WE, additions as JA

from src import plotting as pl
pl.MasterFormatter()

def PLOT_HEATCAPACITY(lowres=False):
    x = np.arange(0.0, 1.001, 0.01)
    xdeg = np.degrees(np.arcsin(x))
    c = JA.HeatCapacity(x)
    ttl=(r'$H_\mathrm{\mathrm{ml}} = \frac{H_{\mathrm{ml}}^i+H_{\mathrm{ml}}^o}{2}+\frac{H_{\mathrm{ml}}^i-H_{\mathrm{ml}}^o}{2}\mathrm{erf}\left(\frac{x-x_\mathrm{APFZ}}{\delta}\right)$')
    f, a = plt.subplots(); a = pl.add_plot(a, xdeg, c/params.CwRho, col='r')
    a.axvline(np.degrees(np.arcsin(params.XAPFZ)), color='k', linestyle='--')
    a2 = a.twinx()
    f, a = pl.FormatAxis(f, a, ttl, r'Latitude, $\phi$ (deg)',
        r'Mixed-layer depth, $H_\mathrm{ml}$ (m)', ylim=[0,80])
    f, a2 = pl.FormatAxis(f, a2, ylab=r'Heat capacity, $c_\mathrm{w}$ (W yr m$^{-2}$ K$^{-1}$)',
        ylim=np.array(a.get_ylim())*params.CwRho)
    a2.grid(False, which='both')
    f.show()
    pass


def PLOT_BASALFLUX(lowres=False):
    x = np.arange(0.0, 1.001, 0.01)
    xdeg = np.degrees(np.arcsin(x))
    fb = JA.BasalFlux(x)
    ttl=(r'$F_\mathrm{b}=F_\mathrm{b}^\mathrm{i}$ + $\frac{\Delta F_\mathrm{b}}{2}\left(1-\mathrm{erf}\left( \frac{x-x_\mathrm{APFZ}}{\delta} \right) \right)$')
    f, a = plt.subplots()
    a.axhline(params.FB_ICE, linestyle='--', color='k', linewidth=1.5, label=r'$F_\mathrm{b}^\mathrm{i}$')
    a.axvline(np.degrees(np.arcsin(params.XAPFZ)), color='k', linestyle=':', label=r'$\phi_\mathrm{APFZ}$')
    a = pl.add_plot(a, xdeg, fb, col='b', lab=r'$F_\mathrm{b}$')
    f, a = pl.FormatAxis(f, a, ttl, r'Latitude, $\phi$ (deg)',
        r'Ocean basal heat-flux, $F_\mathrm{b}$ (Wm$^{-2}$)', ylim=[0,np.ceil(max(fb)+1.1)], leg=True)
    a.annotate(s='', xy=(0.6*np.degrees(np.arcsin(params.XAPFZ)),params.FB_ICE+params.DELTA_FB), xytext=(0.6*np.degrees(np.arcsin(params.XAPFZ)),params.FB_ICE), arrowprops=dict(arrowstyle='<->'))
    a.text(0.6*np.degrees(np.arcsin(params.XAPFZ))+0.01, 0.5*(2*params.FB_ICE+params.DELTA_FB), r'$\Delta F_\mathrm{b} = %.1f$ Wm$^{-2}$'%params.DELTA_FB, fontsize=16)
    f.show()
    pass


def VARY_HML(lowres=False):
    params.NX_HIGHRES = 120
    
    textname = r'DEFAULT_PLOT_DAT_HR.txt'
    datname = os.path.join(os.path.dirname(__file__), '..', 'data_out', textname)
    tdef, xidef_deg = filing.READDATA_TWOCOL(datname)
    
    x, t, E = WE.Integration(lowres=lowres, varyCW=True)[0:3]
    xi_deg = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
    f, a = plt.subplots()
    a = pl.add_plot(a,tdef, xidef_deg, col='grey', lab='Default model')
    a = pl.add_plot(a, t, xi_deg, col='r', lab=r'Variable $H_\mathrm{ml}$')
    f, a = pl.FormatAxis(f, a,
        r'Seasonal ice-edge latitude'+'\n'+r'(variable $H_\mathrm{ml}$, fixed $F_\mathrm{b}=%.1f$ Wm$^{-2}$)'%params.Fb,
        r'$t$ (yr)', r'Ice-edge latitude, $\phi_\mathrm{i}$ (deg)', ylim=[0,90], leg=True)
    PLOT_HEATCAPACITY()
    f.show()
    pass


def VARY_FB(lowres=True, DFB=params.DELTA_FB):
    params.DELTA_FB = DFB
    f, a = plt.subplots()
    
    textname = r'DEFAULT_PLOT_DAT_HR.txt'
    datname = os.path.join(os.path.dirname(__file__), '..', 'data_out', textname)
    tdef, xidef_deg = filing.READDATA_TWOCOL(datname)
    
    x, t, E = WE.Integration(lowres, varyFB=True)[0:3]
    xi_deg = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
    a = pl.add_plot(a, tdef, xidef_deg, col='grey', lab='Default model')
    a = pl.add_plot(a, t, xi_deg, col='b',
        lab=r'Variable $F_\mathrm{b}$ ($\Delta F_\mathrm{b} = %.1f$ Wm$^{-2}$)' % params.DELTA_FB)
    f, a = pl.FormatAxis(f, a,
        r'Seasonal ice-edge latitude'+'\n'+r'(variable $F_\mathrm{b}$, fixed $H_\mathrm{ml}=%.1f$ m)'%params.HML_OCEAN,
        r'$t$ (yr)', r'Ice-edge latitude, $\phi_\mathrm{i}$ (deg)', ylim=[0,90], leg=True)
    PLOT_BASALFLUX()
    f.show()
    pass


def VARY_BOTH(lowres=False, plotall=True, DFB=params.DELTA_FB):
    params.NX_HIGHRES = 120; params.DELTA_FB = DFB
    
    textname = r'DEFAULT_PLOT_DAT_HR.txt'
    datname = os.path.join(os.path.dirname(__file__), '..', 'data_out', textname)
    tdef, xidef_deg = filing.READDATA_TWOCOL(datname)
    
    xBOTH, tBOTH, EBOTH=WE.Integration(lowres=lowres,varyCW=True,varyFB=True)[0:3]
    xiBOTH_deg = np.degrees(np.arcsin(WE.xi_seasonal(EBOTH, xBOTH)))
    if plotall:
        xCW, tCW, ECW = WE.Integration(lowres=lowres, varyCW=True)[0:3]
        xFB, tFB, EFB = WE.Integration(lowres=lowres, varyFB=True)[0:3]
        xiCW_deg = np.degrees(np.arcsin(WE.xi_seasonal(ECW, xCW)))
        xiFB_deg = np.degrees(np.arcsin(WE.xi_seasonal(EFB, xFB)))
    f, a = plt.subplots()
    a = pl.add_plot(a, tdef, xidef_deg, col='grey', lab='Default model')
    if plotall:
        a = pl.add_plot(a, tCW, xiCW_deg, col='r', lab=r'Variable $H_\mathrm{ml}$')
        a = pl.add_plot(a, tFB, xiFB_deg, col='b',
            lab=r'Variable $F_\mathrm{b}$ ($\Delta F_\mathrm{b} = %.1f$ Wm$^{-2}$)'%params.DELTA_FB)
    a = pl.add_plot(a, tBOTH, xiBOTH_deg, col='purple',
        lab=r'Variable $H_\mathrm{ml}$ and $F_\mathrm{b}$')
    f,a = pl.FormatAxis(f, a, 'Seasonal ice-edge latitude', r'$t$ (yr)',
        r'Ice-edge latitude, $\phi_\mathrm{i}$', ylim=[0,90], leg=True)
    f.show()
    pass


if __name__ == '__main__':
    pass
