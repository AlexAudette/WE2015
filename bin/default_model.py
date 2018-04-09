from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params, model as WE, additions as JA, plotting as pl
from src import file_io as filing

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


def Vary_Constant_Fb(quickly=False, lowres=True, times=[22, 73], savedata=True,
    usesaved=False):
    """"""
    if quickly:
        fb = np.array([0.0, 4.0, 10.0])
    else:
        fb = np.arange(0.0, 10.001, 1.0)
    
    if usesaved:
        datadir = os.path.join(os.path.dirname(__file__), '..', 'data_out')
        filename = 'default_vary_const_fb' + ('_lowres' if lowres else '') + (
            '_quickly' if quickly else '')
        array = np.genfromtxt(os.path.join(datadir, filename + '.txt'))
        fb = array[0]
        phi_i_summer = array[1]
        phi_i_mean = array[2]
        phi_i_winter = array[3]
    
    else:
        phi_i_winter = np.zeros(len(fb))
        phi_i_summer = np.zeros(len(fb))
        phi_i_mean = np.zeros(len(fb))
        for i in xrange(len(fb)):
            print "Calculating %i of %i..." % (i+1, len(fb))
            params.Fb = fb[i]
            t, x, E, T = WE.Integration(lowres, varyHML=False, varyFB=False)
            phi_i_t = np.degrees(np.arcsin(WE.xi_seasonal(E, x)))
            phi_i_winter[i] = phi_i_t[times[0]]
            phi_i_summer[i] = phi_i_t[times[1]]
            phi_i_mean[i] = np.mean(phi_i_t)
        
        if savedata:
            array_to_save = np.array([fb, phi_i_summer, phi_i_mean, phi_i_winter])
            datadir = os.path.join(os.path.dirname(__file__), '..', 'data_out')
            filename = 'default_vary_const_fb' + ('_lowres' if lowres else '') + (
                '_quickly' if quickly else '')
            np.savetxt(os.path.join(datadir, filename + '.txt'), array_to_save)
    
    fig, ax = plt.subplots()
    ax.fill_between(fb, phi_i_summer, phi_i_winter, color=[.9,.9,.9]) 
    ax.plot(fb, phi_i_summer, color='r', linewidth=1.5, label='Summer')
    ax.plot(fb, phi_i_mean, color=[.5,.5,.5], linestyle=':', linewidth=1.5,
        label='Annual mean')
    ax.plot(fb, phi_i_winter, color='b', linewidth=1.5, label='Winter')
    ax.axvline(4.0, linestyle='--', linewidth=1.5, color='k')
    ax.set_xlabel(r'Ocean upward heat flux, $F_\mathrm{b}$ (W m$^{-2}$)')
    ax.set_ylabel(r'Ice-edge latitude, $\phi_\mathrm{i}$ (deg)')
    ax.legend(loc='upper left', fontsize=14)
    
    ax2 = ax.twinx()
    ax2.set_yticks(np.linspace(0, (2-np.sqrt(2))*np.pi*params.RE**2, 10))
    ax2.set_yticklabels(np.rint((1-np.sin(np.pi*np.array(ax.get_yticks())/180))*2E-12*np.pi*params.RE**2).astype(int))
    ax2.set_ylabel(r'Equivalent extent ($10^6$ km$^2$)')
    
    fig, ax = pl.FormatAxis(fig, ax, minorgrid=False)
    fig, ax2 = pl.FormatAxis(fig, ax2, minorgrid=False)
    
    fig.show()
    
    pass


if __name__ == '__main__':
    pl.MasterFormatter()
    if 'Vary_Constant_Fb' in sys.argv:
        Vary_Constant_Fb(quickly=('quickly' in sys.argv),
            lowres=('lowres' in sys.argv), savedata=('savedata' in sys.argv),
            usesaved=('usesaved' in sys.argv))
    else:
        main(lowres=('lowres' in sys.argv), usesaved=('usesaved' in sys.argv),
            savefigs=('savefigs' in sys.argv))
