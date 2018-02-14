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

    x = np.arange(0.0, 1.0001, 0.001)
    E = np.cos(np.pi*x+0.2)
    
    xi = WE.xi_seasonal(np.array([[i] for i in E]), x)
    print xi
    
    y = JA.BasalFluxInteractive(x, xi[0])
    
    fig, ax = plt.subplots()
    ax.plot(np.degrees(np.arcsin(x)), y, color='k', linewidth=1.5)
    ax.set_xlabel(r'$\phi$ (deg)', fontsize=18)
    ax.set_ylabel(r'Ocean basal heat-flux, $F_\mathrm{b}$ (Wm$^{-2}$)',
        fontsize=18)
    ax.set_xlim([0,90])
    ax.set_ylim([0,16])
    fig, ax = pl.FormatAxis(fig, ax)
    fig.show()
    pass

if __name__ == '__main__':
    main()
