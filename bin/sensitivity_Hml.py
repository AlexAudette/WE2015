from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as f


def main(lowres=True, usesaved=False, savedata=True, filename='Hml_sensitivity.txt'):
    """"""
    if usesaved:
        Hml, xi_summer, xi_mean, xi_winter = f.OpenSensitivityData(filename)
    else:
        Hml = np.array([30, 40, 50, 60, 70, 80, 90, 100])
        xi_summer = np.zeros(len(Hml))
        xi_winter = np.zeros(len(Hml))
        xi_mean = np.zeros(len(Hml))
        
        for i in xrange(len(Hml)):
            params.cw = (9.8/75.0)*Hml[i]
            print "Calculating with Hml = %.2f m..." % (params.cw*75.0/9.8)
            t, x, E, T = WE.Integration(lowres=lowres)
            xi_of_t = WE.xi_seasonal(E, x)
            xi_summer[i] = np.max(xi_of_t)
            xi_winter[i] = np.min(xi_of_t)
            xi_mean[i] = np.mean(xi_of_t)
        print ""
        
        if savedata:
            f.SaveSensitivityData(Hml, xi_summer, xi_mean, xi_winter, filename)
    
    fig, ax = pl.PlotSensitivity(Hml, xi_summer, xi_mean, xi_winter)
    fig.show()


if __name__ == '__main__':
    pl.SetRCParams()
    main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
        savedata=('savedata' in sys.argv))