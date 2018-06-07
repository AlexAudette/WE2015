# WE2015
Combined Energy Balance (EB) and Single Column (SC) models, based on the model of Till J. W. Wagner and Ian Eisenman (University of California).

## Overview

This repository contains some Python code to solve and plot solutions of an extended Energy Balance Model (EBM) of climate which has been presented and explored by Till Wagner and Ian Eisenman. The model describes the time evolution of the zonally- averaged surface enthalpy (equivalently surface temperature) in a single hemisphere which transports heat in the meridional direction, and sea ice grows/melts according to the local surface temperature and balance of heat fluxes. See the following reference for a full description of the physical processes represented in the model and insights into sea ice stability gained from it:

Wagner and Eisenman (2015). _How climate model complexity influences sea ice stability_. J Climate 28, 3998-4014.

which can be found [here](https://journals.ametsoc.org/doi/abs/10.1175/JCLI-D-14-00654.1) and their original source code which the present code is adapted from can be found [here](http://eisenman.ucsd.edu/code.html).

## Dependencies
  * Python 2.7.14
  * MatPlotLib 1.4.3
  * NumPy 1.14.3
