import sys, pygame, numpy as np
from math import ceil

from common import *

def physics(masspoints, dt, plunk, which):
    ppos = masspoints[1]
    cpos = masspoints[0]
    N = cpos.shape[0]

    # apply hooke's law
    force = np.zeros((N, 2), dtype=cpos.dtype)
    for i in range(1, N):
        dx, dy = cpos[i] - cpos[i - 1]
        dist = np.sqrt(dx**2 + dy**2)
        assert dist != 0
        fmag = -HOOKE_K * dist
        cosine = dx / dist
        sine = dy / dist
        fvec = np.array([fmag * cosine, fmag * sine])
        force[i - 1] -= fvec
        force[i] += fvec

    force[0] = force[-1] = 0, 0
    force[which][1] += plunk

    accel = force / MASS

    # verlet integration
    npos = (2 - DAMPING) * cpos - (1 - DAMPING) * ppos + accel * (dt**2)

    masspoints[1] = cpos
    masspoints[0] = npos


