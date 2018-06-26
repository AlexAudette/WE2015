from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as f


def main(lowres=True, usesaved=False, savedata=True, filename='Fb_sensitivity'):
    """"""
    if usesaved:
        Fb, xi_summer, xi_mean, xi_winter = f.OpenSensitivityData(filename)
    else:
        Fb = np.linspace(0.5, 9.5, 10)
        xi_summer = np.zeros(len(Fb))
        xi_winter = np.zeros(len(Fb))
        xi_mean = np.zeros(len(Fb))
        
        for i in xrange(len(Fb)):
            params.Fb = Fb[i]
            print "Calculating with F_b = %.2f W/m^2..." % params.Fb
            t, x, E, T = WE.Integration(lowres=lowres)
            xi_of_t = WE.xi_seasonal(E, x)
            xi_summer[i] = np.max(xi_of_t)
            xi_winter[i] = np.min(xi_of_t)
            xi_mean[i] = np.mean(xi_of_t)
        print ""
        
        if savedata:
            f.SaveSensitivityData(Fb, xi_summer, xi_mean, xi_winter, filename)
    
    fig, ax = pl.PlotSensitivity(Fb, xi_summer, xi_mean, xi_winter, type='Fb',
                                 xlim=[0,10])
    fig.show()


if __name__ == '__main__':
    pl.SetRCParams()
    main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
        savedata=('savedata' in sys.argv))