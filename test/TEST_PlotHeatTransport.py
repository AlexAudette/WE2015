### TEST FOR PlotHeatTransport()
from __future__ import division
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from src import params, plotting as pl
pl.MasterFormatter()

def DoTest():
    # Define some data which has an obvious solution in x-space.
    # Data is in format T = [ [T(x1, t1), T(x1, t2), ...] 
    #                         [T(x2, t1), T(x2, t2), ...]
    #                         [           ...           ]
    #                         [T(xn, t1), T(xn, t2), ...] ] 
    t = np.arange(0.0, 1.001, 0.01)
    x = np.arange(0.005, 1.001, 0.005)
    data = x**2 + 1
    T = np.array( [ [i]*len(t) for i in data ] )
    
    # Generate the del^2 T data and plot:
    fig, ax = pl.PlotHeatTransport(t, x, T, [0,-1], plotdeg=False)
    #analytic solution:
    ax.plot(x, params.D*(2-6*x**2), linestyle='--', color='b',label='Analytic')
    ax.set_xlim([0,1])
    ax.set_xlabel(r'$x=\sin \phi$', fontsize=18)
    ax.set_ylabel(r'$D\nabla^{2}f$', fontsize=18)
    ax.set_title(
        r'Testing $\nabla^{2}$ operator implementation on $f(x,t)=x^{2}+1$',
        fontsize=20, y=1.02)
    ax.legend(loc=0)
    fig.tight_layout()
    fig.show()
    pass


if __name__ == '__main__':
    DoTest()
