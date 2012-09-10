from numba import f, d
from numba.decorators import jit

from common import *

@jit(arg_types=[d[:,:], d[:,:]])
def hooke(cpos, force):
    N = cpos.shape[0]
    for i in range(1, N):
        dx = cpos[i, 0] - cpos[i - 1, 0]
        dy = cpos[i, 1] - cpos[i - 1, 1]
        dist = np.sqrt(dx**2 + dy**2)
        fmag = -HOOKE_K * dist

        cosine = dx / dist
        sine = dy / dist

        fx = fmag * cosine
        fy = fmag * sine

        force[i - 1, 0] -= fx
        force[i - 1, 1] -= fy
        force[i, 0] += fx
        force[i, 1] += fy

@jit(arg_types=[d[:,:], d[:,:], d[:,:], d[:,:], d])
def verlet_integrate(npos, cpos, ppos, force, dt):
    N = cpos.shape[0]
    for i in range(N):
        ax = force[i, 0] / MASS
        ay = force[i, 1] / MASS
        npos[i, 0] = (2 - DAMPING) * cpos[i, 0] - (1 - DAMPING) * ppos[i, 0] + ax * (dt**2)
        npos[i, 1] = (2 - DAMPING) * cpos[i, 1] - (1 - DAMPING) * ppos[i, 1] + ay * (dt**2)

def physics(masspoints, dt, plunk, which):
    ppos = masspoints[1]
    cpos = masspoints[0]
    N = cpos.shape[0]

    # apply hooke's law
    force = np.zeros((N, 2), dtype=cpos.dtype)
    hooke(cpos, force)

    force[0] = force[-1] = 0, 0
    force[which][1] += plunk

    # verlet integration
    npos = np.empty((N, 2), dtype=cpos.dtype)
    verlet_integrate(npos, cpos, ppos, force, dt)

    masspoints[1] = cpos
    masspoints[0] = npos

