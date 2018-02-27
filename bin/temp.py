from __future__ import division
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src import params, model as WE, additions as JA, file_io as filing

from src import plotting as pl
pl.MasterFormatter()

def main():
    """Plot the interactive form of the ocean basal heat-flux."""
    x = np.arange(0.0, 1.0001, 0.001)
    E = np.cos(np.pi*x+0.2)
    
    xi = WE.xi_seasonal(np.array([[i] for i in E]), x)
    print xi
    
    y = JA.BasalFluxInteractive(x, xi[0])
    
    fig, ax = plt.subplots()
    ax.plot(np.degrees(np.arcsin(x)), y, color='k', linewidth=1.5,
        label=r'$F_\mathrm{b}(\phi)$')
    ax.set_xlabel(r'$\phi$ (deg)', fontsize=18)
    ax.set_ylabel(r'Ocean basal heat-flux, $F_\mathrm{b}$ (Wm$^{-2}$)',
        fontsize=18)
    ax.axvline(np.degrees(np.arcsin(xi[0])), linestyle='--', color='k',
        label=r'$\phi=\phi_\mathrm{i}$')
    ax.set_xlim([0,90])
    ax.set_ylim([0,16])
    ax.legend(loc=0)
    fig, ax = pl.FormatAxis(fig, ax)
    fig.show()
    pass


def main2():
    """Plot the old non-interactive form of H_ml."""
    x = np.arange(0.0, 1.0001, 0.001)
    y = JA.HeatCapacity(x)
    
    fig, ax = plt.subplots()
    ax.plot(np.degrees(np.arcsin(x)), y, color='k', linewidth=1.5,
        label=r'$H_\mathrm{ml}(\phi)$')
    ax.set_xlabel(r'$\phi$ (deg)', fontsize=18)
    ax.set_ylabel(r'Mixed-layer depth, $H_\mathrm{ml}$ (m)',
        fontsize=18)
    ax.set_xlim([0,90])
    ax.set_ylim([0,10])
    ax.set_title(r'Old form of $H_\mathrm{ml}$', fontsize=18, y=1.02)
    fig, ax = pl.FormatAxis(fig, ax)
    fig.show()
    pass


def main3():
    """Animate the form of F_b with (crude) seasonal cycle."""
    
    ### Import data for ice-edge latitude:
    tdef, xdef, Edef = filing.OpenData('DAT_constFb=4.0_constHML=75.0_HR')[0:3]
    xideg_def = np.degrees(np.arcsin(WE.xi_seasonal(Edef, xdef)))
    
    t, x_coords, E = filing.OpenData('DAT_t_DEPENDENCE')[0:3]
    x = WE.xi_seasonal(E, x_coords)
    xdeg = np.degrees(np.arcsin(x))
    FB = np.zeros( (len(t), len(x_coords)) )
    for i in xrange(len(t)):
        FB[i] = JA.BasalFluxTimeDependent(x_coords, t[i], x[i])
    
    fig, (ax1, ax2) = plt.subplots(1,2)
    
    ### Fixed plot elements:
    ax1.set_xlabel(r'$\phi$ (deg)')
    ax1.set_ylabel(r'$F_\mathrm{b}(x,t)$ (Wm$^{-2}$)')
    ax1.set_xlim([0,90])
    ax1.set_ylim([0,10])
    fig, ax1 = pl.FormatAxis(fig, ax1)
    
    ax2.plot(tdef, xideg_def, color='grey', linewidth=1.5)
    ax2.plot(t, xdeg, color='k', linewidth=1.5)
    ax2.set_xlabel(r'Time, $t$ (yr)')
    ax2.set_ylabel(r'Ice-edge latitude, $\phi_\mathrm{i}$ (deg)')
    ax2.set_title(r'Seasonal ice-edge latitude')
    ax2.set_xlim([0,1])
    ax2.set_ylim([0,90])
    
    ### Initial frame plot:
    ax1.set_title(r'$t = %.2f$' % t[0])
    line, = ax1.plot(np.degrees(np.arcsin(x_coords)), FB[0], color='k',
        linewidth=1.5, label=r'$t=%.2f$ yr' % t[0])
    time, = ax2.plot(np.array([t[0],t[0]]), np.array([0,90]), color='k',
        linestyle='--')
    fig, ax1 = pl.FormatAxis(fig, ax1)
    fig, ax2 = pl.FormatAxis(fig, ax2)
    
    def animate(i):
        line.set_ydata(FB[i])
        time.set_xdata(np.array([t[i], t[i]]))
        ax1.set_title(r'$t=%.2f$ yr' % t[i])
        return line
    
    ani = animation.FuncAnimation(fig, animate, np.arange(1,len(t)),
        interval=100, blit=False)
    
    fig.show()
    return FB


if __name__ == '__main__':
    if "1" in sys.argv:
        main()
    elif "2" in sys.argv:
        main2()
    elif "3" in sys.argv:
        main3()
    else:
        main()
