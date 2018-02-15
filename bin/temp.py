from __future__ import division
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
import matplotlib.pyplot as plt
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


def repeat(id=2):
    if id==1:
        main()
    else
        main2()
    pass


if __name__ == '__main__':
    main2()
