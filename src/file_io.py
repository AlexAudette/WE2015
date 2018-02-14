from __future__ import division
import sys, os, numpy as np, matplotlib.pyplot as plt
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import params


def OpenData(filename, datlocation='data_out'):
    """"""
    datadir = os.path.join(os.path.dirname(__file__), '..', datlocation)
    print "Loading data from: %s" % filename+'_E.txt'
    E = np.genfromtxt(os.path.join(datadir, filename + '_E.txt'))
    print "Loading data from: %s" % filename+'_T.txt'
    T = np.genfromtxt(os.path.join(datadir, filename + '_T.txt'))
    t = E[0,1:] # first row is t-coords,
    x = E[1:,0] # first col is x-coords,
    E = E[1:,1:] # rest is E(x,t).
    return t, x, E, T


def SaveData(t, x, E, T, filename, datlocation='data_out'):
    """"""
    datadir = os.path.join(os.path.dirname(__file__), '..', datlocation)
    E_array_to_save = np.zeros( (len(x)+1, len(t)+1) )
    E_array_to_save[1:,1:] = E
    E_array_to_save[0,1:] = t
    E_array_to_save[1:,0] = x
    print "Saving data to: %s" % filename+'_E.txt'
    np.savetxt(os.path.join(datadir, filename + '_E.txt'), E_array_to_save)
    print "Saving data to: %s" % filename+'_T.txt'
    np.savetxt(os.path.join(datadir, filename + '_T.txt'), T)
    pass


def SaveFigures(figures, subdir):
    """Save several figures to plots\subdir with filenames given by their
    canvas window titles. Makes the directory if it does not exist and warns/
    aborts if about to over-write a file.
    
    --Args--
    figures: list of MatPlotLib figure objects.
    subdir:  string, name of sub-directory to which figures should be saved.
    """
    dirname = os.path.join(os.path.dirname(__file__), '..', 'plots', subdir)
    if not os.path.isdir(dirname):
        os.mkdir(dirname)
    passall = False
    for f in figures:
        filename_to_save = str(f.canvas.manager.window.windowTitle()) + '.pdf'
        if passall:
            f.savefig(os.path.join(dirname, filename_to_save))
        else:
            if os.path.isfile(os.path.join(dirname, filename_to_save)):
                prt='About to overwrite \"%s\"! Continue? [Y / Y-ALL / N] > '%(
                    filename_to_save)
                check = raw_input(prt)
                if not (check == 'Y' or check == 'Y-ALL'):
                    pass
                else:
                    f.savefig(os.path.join(dirname, filename_to_save))
                passall = check=='Y-ALL'
            else:
                f.savefig(os.path.join(dirname, filename_to_save))
    pass
