from __future__ import division
import numpy as np
import params

def ForwardEulerOnE(dt, E, T, Tg, a, S, Fb):
    """Uses the forward-Euler scheme to solve for E(x, t+dt).
    
    ---Arguments---
    dt : time-step.
    E  : np.array containing E(x, t).
    T  : np.array containing T(x, t).
    Tg : np.array containing Tg(x, t).
    a  : np.array containing a(x).
    S  : np.array containing S(x, t).
    Fb : np.array containing Fb(x, t).
    """
    return E + dt*(a*S - params.A - params.B*(T-params.Tm)
        - params.cg/params.tau*(T-Tg) + Fb + params.F)


def ImplicitEulerOnTg():
    pass