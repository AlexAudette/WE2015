from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as filing
pl.MasterFormatter()

def main(lowres=False, usesaved=False, times=[22, 73], savefigs=False):
    """Bla bla bla...
    
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
        t, x, E, T = filing.OpenData('DAT_%.1f_Fb_%.1f_constantHml=%.1f' % (
            params.FB_ICE, params.FB_ICE+params.DELTA_FB, params.HML_OCEAN) + (
            '_LR' if lowres else '_HR') )
    else:
        t, x, E, T = WE.Integration(lowres, varyHML=False, varyFB=True)
        filing.SaveData(t, x, E, T, 'DAT_%.1f_Fb_%.1f_constantHml=%.1f' % (
            params.FB_ICE, params.FB_ICE+params.DELTA_FB, params.HML_OCEAN) + (
            '_LR' if lowres else '_HR') )
    
    tdef,xdef, Edef, Tdef = filing.OpenData('DAT_constFb=4.0_constHML=75.0_HR')
    
    xi_deg = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
    xidef_deg = np.degrees(np.arcsin(WE.xi_seasonal(Edef, xdef)))
    
    # Plot the ice-edge seasonal cycle:
    details = r'(variable $F_\mathrm{b}$, constant'
    details += r' $H_\mathrm{ml}=%.1f$ m)' % params.HML_OCEAN
    f1, a1 = pl.PlotIceEdge(t, xi_deg, label=r'Variable $F_\mathrm{b}$',
        details=details)
    a1.plot(tdef, xidef_deg, color='grey', label='Constant $F_\mathrm{b}$',
        linewidth=1.5)
    a1.axvline(t[times[0]], color='k')
    a1.axvline(t[times[1]], color='k', linestyle='--')
    a1.legend(loc=0, fontsize=14)
    f1.tight_layout()
    
    # Plot E(x, t) contour map:
    f2, a2 = pl.PlotContour(t, np.degrees(np.arcsin(x)), E)
    
    # Plot T(x, t) contour map:
    f3, a3 = pl.PlotContour(t, np.degrees(np.arcsin(x)), T, type='T')
    
    # Plot E(x) for winter and summer:
    title = r'$%.1f<F_\mathrm{b}(x,t)$ /Wm$^{-2}<%.1f$, $H_\mathrm{ml}(x,t)=%.1f$ m' %(
        params.FB_ICE, params.FB_ICE+params.DELTA_FB, params.HML_OCEAN)
    f4, a4 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), E, times, 'E', title)
    
    # Plot T(x) for winter and summer:
    f5, a5 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), T, times, 'T', title)
    
    # Plot h(x) for winter and summer:
    f6, a6 = pl.PlotIceThickness(t, np.degrees(np.arcsin(x)), E, times, title)
    
    # Plot the heat transport D(del^2)T(x,t) for winter and summer:
    f7, a7 = pl.PlotHeatTransport(t, x, T, times, title=title)
    
    figures = [f1, f2, f3, f4, f5, f6, f7]
    if savefigs:
        filing.SaveFigures(figures, '%.1f_Fb_%.1f_constantHml=%.1f'%(
            params.FB_ICE, params.FB_ICE+params.DELTA_FB, params.HML_OCEAN))
    for fig in figures:
        fig.show()
    pass


if __name__ == '__main__':
    main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
        savefigs=('savefigs' in sys.argv))
