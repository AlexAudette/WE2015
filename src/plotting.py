from __future__ import division
import sys, os
import params, model
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


def FillInEndValues(lats, var):
    # This is because WE original numerical method uses centred grid points
    # and when converting back to degrees, misses a large chunk at the pole and
    # a small amount at the equator:
    var = np.append(np.array([var[0]]), var, axis=0)
    var = np.append(var, np.array([var[-1]]), axis=0)
    lats = np.append(0.0, lats)
    lats = np.append(lats, 90.0)
    return lats, var


def add_plot(ax, X, Y, col='k', lwid=1.5, lstyle='-', lab='', z=1,
    giveline=False):
    """Simple plot of Y vs X"""
    if lab == '':
        if z == np.nan:
            line = ax.plot(X, Y, color=col, linestyle=lstyle, linewidth=lwid)
        else:
            line = ax.plot(X, Y, color=col, linestyle=lstyle, linewidth=lwid,
                zorder=z)
    else:
        if z == np.nan:
            line = ax.plot(X, Y, color=col, linestyle=lstyle, linewidth=lwid,
                label=lab)
        else:
            line = ax.plot(X, Y, color=col, linestyle=lstyle, linewidth=lwid,
                label=lab, zorder=z)
    if giveline:
        return ax, line
    else:
        return ax


def PlotIceEdge(time, latitude, label='', col='k', details=''):
    """"""
    fig, ax = plt.subplots()
    ax.plot(time, latitude, color=col, label=label)
    ax.set_xlabel(r'Time, $t$ (yr)')
    ax.set_ylabel(r'Ice-edge latitude, $\phi_\mathrm{i}$ ($^\circ$)')
    title = r'Seasonal cycle of ice-edge latitude $\phi_\mathrm{i}$'
    ax.set_title(title + '\n' + details, y=1.02)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 90])
    fig.canvas.set_window_title('Ice-edge latitude')
    fig.tight_layout()
    return fig, ax


def PlotContour(time, latitude, variable, type='E'):
    """"""
    if type=='T':
        cont_levs=np.arange(-30, 45, 5)
    elif type=='E':
        cont_levs=np.arange(-50, 400, 50)
    
    latitude, variable = FillInEndValues(latitude, variable)
    fig, ax = plt.subplots()
    cs = ax.contourf(time, latitude, variable, levels=cont_levs)
    cbar = fig.colorbar(cs, ax=ax)
    cbar.ax.tick_params('both', length=0, which='both')
    
    if type=='E':
        ax.set_title(r'Surface enthalpy, $E$', fontsize=20, y=1.02)
        cbar.ax.set_ylabel(r'$E$ (W yr m$^{-2}$)', fontsize=16)
        ax.contour(time, latitude, variable, levels=[0], colors=('k',),
            linestyles=('-',))
        fig.canvas.set_window_title('E(x,t) contours')
    elif type=='T':
        ax.set_title(r'Surface temperature, $T$', y=1.02)
        cbar.ax.set_ylabel(r'$T$ ($^\circ$C)', fontsize=16)
        ax.contour(time, latitude, variable, levels=[params.Tm], colors=('k',),
            linestyles=('-',), linewidths=(1.5,))
        fig.canvas.set_window_title('T(x,t) contours')
    
    # Fake grid:
    for x in [0.2,0.4,0.6,0.8]:
        ax.axvline(x, color=[1,1,1], linewidth=0.5)
    for y in np.arange(10,90,10):
        ax.axhline(y, color=[1,1,1], linewidth=0.5)
    
    ax.set_xlabel(r'Time, $t$ (yr)')
    ax.set_ylabel(r'Latitude, $\phi$ ($^\circ$)')
    ax.set_xlim([0,1])
    ax.set_ylim([0,90])
    fig.tight_layout()
    return fig, ax


def PlotContourWS(time, latitude, variable, time_index, type='E', title=''):
    """"""
    fig, ax = plt.subplots()
    ax.axhline(0.0, color=[.6, .6, .6])
    ax.plot(latitude, variable[:,time_index[0]], color='k',
        label=r'Winter ($t=%.2f$ yr)' % time[time_index[0]])
    ax.plot(latitude, variable[:,time_index[1]], color='k',
        label=r'Summer ($t=%.2f$ yr)' % time[time_index[1]], linestyle='--')
    ax.set_xlabel(r'Latitude, $\phi$ ($^\circ$)')
    if type == 'E':
        ax.set_ylabel(r'Surface enthalpy, $E$ (W yr m$^{-2}$)')
        fig.canvas.set_window_title('E(x,t) profiles')
    elif type == 'T':
        ax.set_ylabel(r'Surface temperature, $T$ ($^\circ$C)')
        fig.canvas.set_window_title('T(x,t) profiles')
    ax.set_title(title, fontsize=17, y=1.02)
    ax.set_xlim([0,90])
    ax.legend()
    fig.tight_layout()
    return fig, ax


def PlotIceThickness(time, latitude, enthalpy, time_index, title='', col='k'):
    """"""
    icethickness_winter = enthalpy[:,time_index[0]] / (-params.Lf)
    icethickness_summer = enthalpy[:,time_index[1]] / (-params.Lf)
    icethickness_winter = [h if h>=0 else 0 for h in icethickness_winter]
    icethickness_summer = [h if h>=0 else 0 for h in icethickness_summer]
    
    fig, ax = plt.subplots()
    ax.plot(latitude, icethickness_winter, color=col,
        label=r'Winter ($t=%.2f$ yr)' % time[time_index[0]])
    ax.plot(latitude, icethickness_summer, color=col,
        label=r'Summer ($t=%.2f$ yr)' % time[time_index[1]], linestyle='--')
    ax.set_xlabel(r'Latitude, $\phi$ ($^\circ$)')
    ax.set_ylabel(r'Ice thickness, $H_\mathrm{i}$ (m)')
    ax.set_title(title, fontsize=17, y=1.02)
    ax.set_xlim([50, 90])
    ax.set_ylim(ymin=0)
    ax.legend(loc=0)
    fig.canvas.set_window_title('Ice thickness')
    fig.tight_layout()
    return fig, ax


def PlotHeatTransport(time, X, T, time_index, plotdeg=True, title=''):
    """"""
    xb = np.arange(1.0/len(X), 1.0, 1.0/len(X))
    DiffOp = model.DiffOp(len(X), 1.0/len(X), xb)
    heat_transport = params.D*DiffOp.dot(T)
    
    latitude = np.degrees(np.arcsin(X)) if plotdeg else X
    
    fig, ax = plt.subplots()
    ax.axhline(0.0, color=[.6, .6, .6])
    ax.plot(latitude, heat_transport[:,time_index[0]], color='k',
        label=r'Winter ($t=%.2f$ yr)' % time[time_index[0]])
    ax.plot(latitude, heat_transport[:,time_index[1]], color='k',
        label=r'Summer ($t=%.2f$ yr)' % time[time_index[1]], linestyle='--')
    ax.set_xlabel(r'Latitude, $\phi$ ($^\circ$)')
    ax.set_ylabel(r'Heat transport, $D\nabla^{2}T$ (W m$^{-2}$)')
    ax.set_title(title, fontsize=17, y=1.02)
    ax.set_xlim([0, 90])
    ax.set_ylim([-200, 200])
    ax.legend(loc='upper left')
    fig.canvas.set_window_title('Heat transport')
    fig.tight_layout()
    return fig, ax


def PlotEnergyDiagnostic1(time, delta_E):
    """"""
    fig, ax = plt.subplots()
    ax.axhline(0, linewidth=1.0, color='#777777')
    ax.plot(time, delta_E, color='k', label=r'$\Delta F(t)$')
    ax.axhline(np.mean(delta_E), color='k', linestyle='--',
        linewidth=1.2, label=r'$\overline{\Delta F}$')
    ax.set_xlabel(r'Time, $t$ (yr)')
    ax.set_ylabel(r'Heat lost, $\Delta F$ (W m$^{-2}$)')
    ax.legend(loc='upper left', fontsize=18)
    fig.tight_layout()
    return fig, ax


def PlotEnergyDiagnostic2(time, E_stored, F_leave):
    """"""
    fig, ax1 = plt.subplots()
    l1 = ax1.plot(time, E_stored, color='purple', label=r'Net stored energy')
    ax2 = ax1.twinx()
    l2 = ax2.plot(time, F_leave, color='k', label=r'Net outgoing flux')
    ax1.set_xlabel(r'Time, $t$ (yr)')
    ax1.set_ylabel(r'Energy stored (W yr m$^{-2}$)')
    ax2.set_ylabel(r'Net flux leaving system (W m$^{-2}$)')
    ax2.axhline(0, linestyle='--', color='#777777')
    ax1.scatter(time[np.argmax(E_stored)], max(E_stored), color='purple')
    ax1.scatter(time[np.argmin(E_stored)], min(E_stored), color='purple')
    ax1.axvline(time[np.argmax(E_stored)], color='grey', linestyle='--')
    ax1.axvline(time[np.argmin(E_stored)], color='grey', linestyle='--')
    ls = l1+l2
    labs = [l.get_label() for l in ls]
    ax1.legend(ls, labs)
    ax1.set_xlim([time[0], time[-1]])
    fig.tight_layout()
    return fig, ax1, ax2


###############################################################################
###############################################################################

def SetRCParams():
    """Set default MatPlotLib formatting styles (rcParams) which will be set
    automatically for any plotting method.
    """
    # FONTS (NOTE: SOME OF THESE ARE SET-ORDER DEPENDENT):
    mpl.rcParams['font.sans-serif'] = 'Calibri' #Set font for sans-serif style
    mpl.rcParams['font.family'] = 'sans-serif' #Choose sans-serif font style
    mpl.rcParams['mathtext.fontset'] = 'custom' #Allow customising maths fonts
    mpl.rcParams['mathtext.rm'] = 'sans' #Maths roman font in sans-serif format
    mpl.rcParams['mathtext.it'] = 'sans:italic' #Maths italic font
    mpl.rcParams['mathtext.default'] = 'it' #Maths in italic by default
    
    # PLOT ELEMENT PROPERTIES:
    mpl.rcParams['lines.linewidth'] = 1.5 #Default plot linewidth (thickness)
    mpl.rcParams['lines.markersize'] = 4 #Default marker size (pts)
    mpl.rcParams['lines.markeredgewidth'] = 0 #Default marker edge width (pts)
    
    # LABEL PROPERTIES:
    mpl.rcParams['axes.titlesize'] = 20 #Title font size (pts)
    mpl.rcParams['axes.labelsize'] = 19 #Axis label font sizes (pts)
    mpl.rcParams['xtick.labelsize'] = 18 #X-tick label font size (pts)
    mpl.rcParams['ytick.labelsize'] = 18 #Y-tick label font size (pts)
    
    # GRID PROPERTIES:
    mpl.rcParams['axes.grid'] = True #Major grid on by default
    mpl.rcParams['grid.color'] = 'bfbfbf' #Grid line color
    mpl.rcParams['xtick.minor.visible'] = True #X-minor ticks on by default
    mpl.rcParams['ytick.minor.visible'] = True #Y-minor ticks on by default
    mpl.rcParams['xtick.major.pad'] = 8 #X-major tick padding
    mpl.rcParams['ytick.major.pad'] = 8 #Y-major tick padding
    mpl.rcParams['axes.axisbelow'] = True
    
    # LEGEND PROPERTIES:
    mpl.rcParams['legend.fancybox'] = False #Whether to use a rounded box
    mpl.rcParams['legend.fontsize'] = 16 #Legend label font size (pts)
    mpl.rcParams['legend.framealpha'] = 1 #Legend alpha (transparency)
    mpl.rcParams['legend.edgecolor'] = '#000000' #
    
    # GENERAL FIGURE PROPERTIES
    mpl.rcParams['figure.figsize'] = 8, 6 #Figure window size (inches)
    mpl.rcParams['savefig.format'] = 'pdf' #Default format to save to
    
    # ANIMATION PARAMETERS
    if os.path.isdir('N:\\ffmpeg\\bin'): #path to ffmpeg
        mpl.rcParams['animation.ffmpeg_path'] = 'N:\\ffmpeg\\bin\\ffmpeg.exe'
    elif os.path.isdir('C:\\Program Files (x86)\Ffmpeg For Audacity\\'):
        mpl.rcParams['animation.ffmpeg_path'] = \
            'C:\\Program Files (x86)\Ffmpeg For Audacity\\ffmpeg.exe'
    else:
        print "WARNING: FFMPEG not found."
    
    pass
