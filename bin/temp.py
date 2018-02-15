from __future__ import division
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src import params, model as WE, additions as JA

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


def main3(xi=0.8):
    """Animate the form of F_b with (crude) seasonal cycle."""
    x = np.arange(0.0, 1.0001, 0.001)
    xdeg = np.degrees(np.arcsin(x))
    t = np.arange(0.0, 1.0001, 0.01)
    FB = np.zeros( (len(t), len(x)) )
    for i in xrange(len(t)):
        FB[i] = JA.BasalFluxTimeDependent(x, t[i], xi)
    print FB
    
    fig, ax = plt.subplots()
    
    ### Fixed plot elements:
    ax.axvline(np.degrees(np.arcsin(xi)), color='k', linestyle='--')
    ax.set_xlabel(r'$\phi$ (deg)')
    ax.set_ylabel(r'$F_\mathrm{b}(x,t)$ (Wm$^{-2}$)')
    ax.set_title(r'$t = %.2f$' % t[0])
    ax.set_xlim([0,90])
    ax.set_ylim([0,10])
    fig, ax = pl.FormatAxis(fig, ax)
    
    ### Initial frame plot:
    line, = ax.plot(xdeg, FB[0], color='k', linewidth=1.5,
        label=r'$t=%.2f$ yr' % t[0])
    
    def animate(i):
        line.set_ydata(FB[i])
        ax.set_title(r'$t=%.2f$ yr' % t[i])
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
