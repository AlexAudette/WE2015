# Reference: "How Climate Model Complexity Influences Sea Ice Stability"
# T.J.W. Wagner & I. Eisenman, J Clim 28,10 (2015)
# 
# [Based on a version by Wagner and Eisenman, modified by Jake Aylmer to a 
# modular format].
#------------------------------------------------------------------------------
from __future__ import division
import numpy as np
import params, numerics, additions as JA


def DiffOp(nx, dx, xb):
    lam = 1.0/dx**2*(1-xb**2)
    L1=np.append(0, -lam); L2=np.append(-lam, 0); L3=-L1-L2
    return -np.diag(L3) - np.diag(L2[:nx-1],1) - np.diag(L1[1:nx],-1)


def KAPPA(dx, nx, xb, dt):
    diffop = params.D*DiffOp(nx, dx, xb)
    kappa = (1+dt/params.tau)*np.identity(nx)-dt*diffop/params.cg
    return kappa


def Insolation(x, nt, dt, nx, T):
    ty = np.arange(dt/2, 1+dt/2, dt)
    S = (np.tile(params.S0-params.S2*x**2, [nt,1]) -
        np.tile(params.S1*np.cos(2*np.pi*ty), [nx,1]).T*np.tile(x,[nt,1]))
    return S


def OceanAlbedo(x):
    return params.a0 - params.a2*x**2


def InitialConditions(x, varyHML=False):
    T = 7.5 + 20*(1 - 2*x**2)
    Tg = T
    if varyHML:
        xi = xi_seasonal(np.array([[t] for t in T]), x)[0]
        E = JA.HeatCapacityInteractive(x,xi)*T
    else:
        E = params.cw*T
    return T, Tg, E


def WE_A2(E, C, M, Fb, cw):
    T0 = C/(M - params.k*params.Lf/E) #WE15, eq.A3
    T = (E/cw)*(E>=0)+T0*(E<0)*(T0<0) #WE15, eq.9
    return C-M*T+Fb


def Integration(lowres=False, varyHML=False, varyFB=False):
    """Integration (see WE15_NumericIntegration.pdf)"""
    
    nx = params.NX_LOWRES if lowres else params.NX_HIGHRES
    nt = params.NT_LOWRES if lowres else params.NT_HIGHRES
    dur= params.DURATION_LOWRES if lowres else params.DURATION_HIGHRES
    
    dt = 1./nt #time-step size
    dx = 1./nx #grid-box width
    x = np.arange(dx/2., 1.+dx/2., dx) #native grid (JA: centre of grid-boxes?)
    xb = np.arange(dx, 1., dx) #JA: inner grid boundaries (excluding x=0, x=1)?
    
    T, Tg, E = InitialConditions(x, varyHML=varyHML)
    aw = OceanAlbedo(x)
    S = Insolation(x, nt, dt, nx, T)
    kappa = KAPPA(dx, nx, xb, dt)
    
    cg_tau = params.cg/params.tau
    dt_tau = dt/params.tau
    dc = dt_tau*cg_tau
    M = params.B + cg_tau
    kLf = params.k*params.Lf
    
    cw = JA.HeatCapacity(x) if varyHML else params.cw
    
    #Set up output arrays, saving 100 timesteps/year
    E100 = np.zeros([nx, dur*100]); T100 = np.zeros([nx, dur*100])
    p = -1
    m = -1
    
    #Loop over years:
    for years in range(0, dur):
        #Loop within one year:
        for i in range(0, int(nt)):
            m += 1
            #store 100 timesteps per year
            if (p+1)*10 == m:
                p = p+1; E100[:,p] = E; T100[:,p] = T
            
            alpha = aw*(E>0) + params.ai*(E<0) #WE15, eq.4
            C = alpha*S[i,:] + cg_tau*Tg-params.A
            
            xi = xi_seasonal(np.array([[e] for e in E]), x)[0]
            #cw = JA.HeatCapacityInteractive(x, xi) if varyHML else params.cw
            
            T0 = C/(M - kLf/E) #WE15, eq.A3
            T = (E/cw)*(E>=0)+T0*(E<0)*(T0<0) #WE15, eq.9
            
            Fb = JA.BasalFluxInteractive(x, xi) if varyFB else params.Fb
            
            E = E+dt*(C-M*T+Fb) #WE15, eq.A2
            
            #Implicit Euler on Tg:
            Tg = np.linalg.solve(kappa-np.diag(dc/(M-kLf/E)*(T0<0)*(E<0)),
            Tg+(dt_tau*((E/cw)*(E>=0)+(params.ai*S[i,:]-params.A)/(M-kLf/E)*(T0<0)*(E<0))))
        print 'YEAR %d/%d COMPLETE...\r' % (years+1, dur),
    
    #output only the final (converged) year
    #            t_final         x      E_final          T_final
    return np.linspace(0,1,100), x, E100[:,-101:-1], T100[:,-101:-1]


def xi_seasonal(E, x):
    """Compute seasonal ice edge from E."""
    xi = np.zeros(len(E[0]))
    for j in xrange(0,len(E[0])):
        if any(E[:,j]<0):
            ice = np.where(E[:,j]<0)[0]
            xi[j] = 0. if ice[0]==0 else x[ice[0]]
        else:
            xi[j] = 1. # JA: ice-free
    return xi
