from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as filing


def main(lowres=False, usesaved=False, interactive=False, times=[22, 73],
    savefigs=False):
    """--Args--
    lowres:      boolean; if True, uses low resolution numerical parameters.
    usesaved:    boolean; if True, attempts to load relevant saved data rather
                 than calculating from scratch.
    interactive: boolean; whether to use the interactive form Hml(x, xi).
    times:       len-2 array; time *indexes* for winter and summer plots,
                 respectively.
    savefigs:    boolean; if True, saves figures (*.pdf) to the plots sub-
                 directory (will check before over-writing).
    """
    if usesaved:
        t, x, E, T = filing.OpenData('DAT_constant_Fb=%.1f_%.1f_Hml_%.1f' % (
            params.Fb, params.HML_ICE, params.HML_OCEAN) +
            ('_LR' if lowres else '_HR') +
            ('_interactiveHml' if interactive else ''))
    else:
        t, x, E, T = WE.Integration(lowres, varyHML=True, varyFB=False,
            interactiveHML=interactive)
        filing.SaveData(t, x, E, T, 'DAT_constant_Fb=%.1f_%.1f_Hml_%.1f' % (
            params.Fb, params.HML_ICE, params.HML_OCEAN) +
            ('_LR' if lowres else '_HR') +
            ('_interactiveHml' if interactive else ''))
    
    tdef,xdef, Edef, Tdef = filing.OpenData('DAT_constFb=4.0_constHML=75.0_HR')
    
    xi_deg = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
    xidef_deg = np.degrees(np.arcsin(WE.xi_seasonal(Edef, xdef)))
    
    # Plot the ice-edge seasonal cycle:
    details = r'(variable $H_\mathrm{ml}$, constant'
    details += r' $F_\mathrm{b}=%.1f$ m)' % params.Fb
    f1, a1 = pl.PlotIceEdge(t, xi_deg, label=r'Variable $H_\mathrm{ml}$',
        details=details)
    a1.plot(tdef, xidef_deg, color='grey', label='Constant $H_\mathrm{ml}$',
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
    title = r'$%.1f<H_\mathrm{ml}(x,t)$ /m $<%.1f$, $F_\mathrm{b}(x,t)=%.1f$ Wm$^{-2}$' %(
        params.HML_ICE, params.HML_OCEAN, params.Fb)
    f4, a4 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), E, times, 'E', title)
    
    # Plot T(x) for winter and summer:
    f5, a5 = pl.PlotContourWS(t, np.degrees(np.arcsin(x)), T, times, 'T', title)
    
    # Plot h(x) for winter and summer:
    f6, a6 = pl.PlotIceThickness(t, np.degrees(np.arcsin(x)), E, times, title)
    #### Add plot for constant Fb and constant Hml model manually:
    h_def_win = Edef[:,times[0]]/-params.Lf
    h_def_sum = Edef[:,times[1]]/-params.Lf
    h_def_win = [h if h>=0 else 0 for h in h_def_win]
    h_def_sum = [h if h>=0 else 0 for h in h_def_sum]
    a6.plot(np.degrees(np.arcsin(xdef)), h_def_win, color='grey', linewidth=1.5)
    a6.plot(np.degrees(np.arcsin(xdef)), h_def_sum, color='grey', linewidth=1.5,
        linestyle='--')
    
    # Plot the heat transport D(del^2)T(x,t) for winter and summer:
    f7, a7 = pl.PlotHeatTransport(t, x, T, times, title=title)
    
    figures = [f1, f2, f3, f4, f5, f6, f7]
    if savefigs:
        dirname = '%.1f_Hml_%.1f_constant_Fb=%.1f'%(params.HML_ICE,
            params.HML_OCEAN, params.Fb) + (
            '_interactive' if interactive else '')
        filing.SaveFigures(figures, dirname)
    for fig in figures:
        fig.show()
    pass


if __name__ == '__main__':
    pl.SetRCParams()
    main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
        savefigs=('savefigs' in sys.argv),
        interactive=('interactive' in sys.argv))
