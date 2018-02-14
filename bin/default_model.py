from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as filing
pl.MasterFormatter()

def main(lowres=False, usesaved=False, times=[22, 73], savefigs=False):
    """Run the model and generate all plots for the standard model as described
    by Wagner and Eisenman (2015), i.e. with constant ocean mixed-layer depth
    and constant ocean basal heat-flux (selects the parameter values in
    params.py)
    
    --Args--
    lowres:   boolean; if True, uses low resolution numerical parameters.
    usesaved: boolean; if True, attempts to load relevant saved data rather
              than calculating from scratch.
    times:    len-2 array; time *indexes* for winter and summer plots,
              respectively.
    savefigs: boolean; if True, saves figures (*.pdf) to the plots sub-
              directory (will check before over-writing).
    """
    if usesaved:
        t, x, E, T = filing.OpenData('DAT_constFb=%.1f_constHml=%.1f_' % (
            params.Fb, params.HML_OCEAN) + ('LR' if lowres else 'HR') )
    else:
        t, x, E, T = WE.Integration(lowres, varyHML=False, varyFB=False)
        filing.SaveData(t, x, E, T, 'DAT_constFb=%.1f_constHML=%.1f_' % (
            params.Fb, params.HML_OCEAN) + ('LR' if lowres else 'HR') )
    
    xi_deg = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
    
    # Plot the ice-edge seasonal cycle:
    details = r'(constant $F_\mathrm{b}=%.1f$ Wm$^{-2}$, constant' % params.Fb
    details += r' $H_\mathrm{ml}=%.1f$ m)' % params.HML_OCEAN
    f1, a1 = pl.PlotIceEdge(t, xi_deg, label='Default model', details=details)
    a1.axvline(t[times[0]], color='k')
    a1.axvline(t[times[1]], color='k', linestyle='--')
    f1.tight_layout()
    
    # Plot E(x, t) contour map:
    if lowres:
        f2, a2 = pl.PlotContour(t, np.degrees(np.arcsin(x)), E)
    else:
        f2, a2 = pl.PlotContour(t, np.degrees(np.arcsin(x)), E)
    
    # Plot T(x, t) contour map:
    f3, a3 = pl.PlotContour(t, np.degrees(np.arcsin(x)), T, type='T')
    f3.tight_layout()
    
    # Plot E(x) for winter and summer:
    title = r'$F_\mathrm{b}(x,t)=%.1f$ Wm$^{-2}$, $H_\mathrm{ml}(x,t)=%.1f$ m' %(
        params.Fb, params.HML_OCEAN)
    f4, a4 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), E, times, 'E', title)
    
    # Plot T(x) for winter and summer:
    f5, a5 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), T, times, 'T', title)
    
    # Plot h(x) for winter and summer:
    f6, a6 = pl.PlotIceThickness(t, np.degrees(np.arcsin(x)), E, times, title)
    
    # Plot the heat transport D(del^2)T(x,t) for winter and summer:
    f7, a7 = pl.PlotHeatTransport(t, x, T, times, title=title)
    
    figures = [f1, f2, f3, f4, f5, f6, f7]
    if savefigs:
        filing.SaveFigures(figures, 'constantFb=%.1f_constantHml=%.1f'%(
            params.Fb, params.HML_OCEAN))
    for fig in figures:
        fig.show()
    pass


if __name__ == '__main__':
    main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
        savefigs=('savefigs' in sys.argv))
