from __future__ import division
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
    return FormatAxis(fig, ax)


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
    fig, ax = FormatAxis(fig, ax, minorgrid=False)
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
    ax.legend(loc=0)
    return FormatAxis(fig, ax)


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
    return FormatAxis(fig, ax, minorgrid=False)


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
    return FormatAxis(fig, ax)


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
    return FormatAxis(fig, ax, minorgrid=False)


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
    ax1.legend(ls, labs, loc=0)
    ax1.set_xlim([time[0], time[-1]])
    fig, ax1 = FormatAxis(fig, ax1, gridon=False)
    fig, ax2 = FormatAxis(fig, ax2, gridon=False)
    return fig, ax1, ax2


###############################################################################
###############################################################################

def MasterFormatter():
    """Set the default plotting styles for various MatPlotLib properties."""
    mpl.rcParams['font.sans-serif'] = 'Calibri' #font for sans-serif style
    mpl.rcParams['font.family'] = 'sans-serif' #choose sans-serif font style
    mpl.rcParams['mathtext.fontset'] = 'custom' #allow customising maths font
    mpl.rcParams['mathtext.rm'] = 'sans' #maths roman font in sans-serif format
    mpl.rcParams['mathtext.it'] = 'sans:italic' #maths italic font
    mpl.rcParams['mathtext.default'] = 'it' #maths in italic by default
    mpl.rcParams['axes.titlesize'] = 20 #font-size of plot titles
    mpl.rcParams['axes.labelsize'] = 18 #font-size of plot axes labels
    mpl.rcParams['lines.linewidth'] = 1.5 #default plot linewidth
    mpl.rcParams['savefig.format'] = 'pdf' #default save file format.
    pass


def FormatAxis(fig, ax, ticksize=18, tickpad=8, gridon=True, minorgrid=True):
    """Set the layout and formatting of the plot on axis ax belonging to figure
    object fig.
    
    --Args--
    fig        : MatPlotLib figure object.
    ax         : MatPlotLib axis object associated with fig.
    (ticksize) : int, font-size for axis tick labels.
    (tickpad)  : int, padding for the axis tick labels (see MatPlotLib).
    (gridon)   : bool, whether to set the grid on or not.
    (minorgrid): bool, whether to show minor grid-lines or not.
    """
    ax.minorticks_on()
    
    ax.tick_params(axis='both', which='both', direction='out')
    ax.tick_params(axis='both', which='major', labelsize=ticksize, pad=tickpad)
    
    if gridon:
        if minorgrid:
            ax.grid(which='minor', linestyle='-', color=[.92, .92, .92])
        ax.grid(which='major', linestyle='-', color=[.75, .75, .75])
    ax.set_axisbelow(True)
    fig.tight_layout()
    return fig, ax
