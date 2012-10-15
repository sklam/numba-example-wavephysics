from numba import f4, f8
from numba.decorators import jit
from numbapro.vectorize import GUVectorize

from common import *

from physics_numba import hooke

def verlet_integrate(cpos, ppos, force, dt, npos):
    ax = force[0] / MASS
    ay = force[1] / MASS
    npos[0] = (2 - DAMPING) * cpos[0] - (1 - DAMPING) * ppos[0] + ax * (dt[0]**2)
    npos[1] = (2 - DAMPING) * cpos[1] - (1 - DAMPING) * ppos[1] + ay * (dt[0]**2)

gufunc = GUVectorize(verlet_integrate, '(m),(n),(p),(q)->(m)',
                     backend='ast', target='cpu')
gufunc.add(argtypes=[f8[:], f8[:], f8[:], f8[:], f8[:]])
guf_verlet_integrate = gufunc.build_ufunc()

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
    # NOTE: NumbaPro 0.6 GUFunc not taking scalar properly.
    #       Must convert to an array.
    dt = np.asarray(dt, dtype=cpos.dtype)
    guf_verlet_integrate(cpos, ppos, force, dt, npos)

    masspoints[1] = cpos
    masspoints[0] = npos

