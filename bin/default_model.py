from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
pl.MasterFormatter()

def main(lowres=False, usesaved=False, times=[22, 73]):
    
    basefilename = os.path.join(os.path.dirname(__file__), '..', 'data_out',
        r'DEFAULT_PLOT_DATA_' + (r'LR' if lowres else r'HR'))
    
    if usesaved:
        E = np.genfromtxt(basefilename + r'_E.txt')
        T = np.genfromtxt(basefilename + r'_T.txt')
        t = E[0,1:] # first row is t-coords,
        x = E[1:,0] # first col is x-coords,
        E = E[1:,1:] # rest is E(x,t).
    else:
        x, t, E, T = WE.Integration(lowres)
        np.savetxt(basefilename + r'_T.txt', T)
        array_to_save = np.zeros( (len(x)+1, len(t)+1) )
        array_to_save[1:,1:] = E
        array_to_save[0,1:] = t
        array_to_save[1:,0] = x
        np.savetxt(basefilename+ r'_E.txt', array_to_save)
    
    xi_deg = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
    
    # Plot the ice-edge seasonal cycle:
    f1, a1 = pl.PlotIceEdge(t, xi_deg, label='Default model')
    a1.axvline(t[times[0]], color='k')
    a1.axvline(t[times[1]], color='k', linestyle='--')
    a1.set_title('Seasonal ice-edge latitude \n(default model and parameters)',
        fontsize=20, y=1.02)
    f1.tight_layout()
    
    # Plot E(x, t) contour map:
    if lowres:
        f2, a2 = pl.PlotContour(t, np.degrees(np.arcsin(x)), E, 
            cont_levs=np.append(np.arange(-40,20,20), np.arange(50,350,50)))
    else:
        f2, a2 = pl.PlotContour(t, np.degrees(np.arcsin(x)), E)
    
    # Plot T(x, t) contour map:
    f3, a3 = pl.PlotContour(t, np.degrees(np.arcsin(x)), T, type='T',
        cont_levs=np.arange(-30,35,5) )
    f3.tight_layout()
    
    # Plot T(x) for winter and summer:
    f4, a4 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), T, times, 'T')
    
    # Plot E(x) for winter and summer:
    f5, a5 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), E, times, 'E')
    
    # Plot h(x) for winter and summer:
    f6, a6 = pl.PlotIceThickness(t, np.degrees(np.arcsin(x)), E, times)
    
    # Plot the heat transport D(del^2)T(x,t) for winter and summer:
    f7, a7 = pl.PlotHeatTransport(t, x, T, times)
    
    for fig in [f1, f2, f3, f4, f5, f6, f7]:
        fig.show()
    pass


if __name__ == '__main__':
    # sys.argv[0] == r'\..\bin\default_model.py'
    # sys.argv[1] == lowres
    # sys.argv[2] == usesaved
    if len(sys.argv) == 2:
        main(lowres=sys.argv[1]=='lowres')
    elif len(sys.argv) == 3:
        main(lowres=sys.argv[1]=='lowres', usesaved=sys.argv[2]=='usesaved')
    else:
        main()
