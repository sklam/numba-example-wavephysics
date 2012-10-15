import sys, time
try:
    import pygame
except ImportError:
    pass

try:
    from cPickle import pickle
except ImportError:
    import pickle
import numpy as np
from math import ceil
import contextlib


RADIUS = 1
MASS = .01
HOOKE_K = 2100000.
#HOOKE_K = 1125000.
#SUBDIVISION = 184
SUBDIVISION = 300
FRAMERATE = 60
DAMPING = 0.0001
PLUNK_MULTIPLIER = 20000.
#PARTICLE_COUNT = 64
PARTICLE_COUNT = 200

class Recorder:
    def __init__(self, filename):
        self.buf = []
        self.filename = filename

    @contextlib.contextmanager
    def auto_write(self):
        yield
        self.close()

    def add(self, sample):
        self.buf.append(sample)

    def close(self):
        print 'write recorded data'
        with open(self.filename, 'wb') as fout:
            pickle.dump(self.buf, fout)

def calc_impulse(strength):
    duration = 1./250.
    period = 1. / (4 * duration * FRAMERATE * SUBDIVISION)
    x = np.arange(duration * FRAMERATE * SUBDIVISION) * period
    return (strength * np.sin(2 * np.pi * x)).tolist()

class Plunk:
    def __init__(self):
        self.buf = None

    def plunk(self, strength):
        self.buf = iter(calc_impulse(strength))

    def next(self):
        try:
            if self.buf:
                return self.buf.next()
        except StopIteration:
            pass
        return 0.

def main(physics, filename):
    pygame.init()

    size = width, height = 600, 200
    white = 255, 255, 255
    red = 255, 0, 0
    blue = 0, 0, 255

    screen = pygame.display.set_mode(size)

    clock = pygame.time.Clock()

    count = PARTICLE_COUNT

    masspoints = np.empty((2, count, 2), dtype=np.float64)
    initpos = np.zeros(count, dtype=np.float64)
    for i in range(1, count):
        initpos[i] = initpos[i - 1] + float(width) / count
    masspoints[:, :, 0] = initpos
    masspoints[:, :, 1] = height / 2

    print('strides %s' % str(masspoints.strides))

    plunk_pos = count // 2.
    plunk = Plunk()

    rec = Recorder(filename)
    with rec.auto_write():
        while True:
            for event in pygame.event.get():  # process events
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONUP: # press & released
                    mx, my = pygame.mouse.get_pos()
                    plunk_pos = max(1, min(count-2, mx * count // width))
                    plunk.plunk(calc_impulse(my * PLUNK_MULTIPLIER))

            screen.fill(white)              # clear screen


            for _ in xrange(SUBDIVISION):
                f = plunk.next()
                physics(masspoints, 1./(SUBDIVISION * FRAMERATE), f, plunk_pos)
                pos = masspoints[0, count // 2]   # where to listen to
                normalized = (pos[1] - height/2.) / (height/2.)
                rec.add(normalized)

            pygame.draw.lines(screen, red, False, masspoints[0])
            pygame.draw.circle(screen, blue, map(int, masspoints[0, plunk_pos]), RADIUS)

            pygame.display.flip()

            measured_fps = clock.get_fps()
            pygame.display.set_caption("fps %.1f" % measured_fps)

            clock.tick(FRAMERATE)


def main_headless(physics, filename, dtype=np.float64):
    size = width, height = 600, 200
    count = PARTICLE_COUNT

    masspoints = np.empty((2, count, 2), dtype=dtype)
    initpos = np.zeros(count, dtype=dtype)
    for i in range(1, count):
        initpos[i] = initpos[i - 1] + float(width) / count
    masspoints[:, :, 0] = initpos
    masspoints[:, :, 1] = height / 2

    plunk_pos = count // 2.
    plunk = Plunk()

    rec = Recorder(filename)
    t_start = time.time()
    with rec.auto_write():
        # plunk once at the start
        plunk.plunk(calc_impulse(height * PLUNK_MULTIPLIER))

        for _ in xrange(10 * FRAMERATE):
            for _ in xrange(SUBDIVISION):
                f = plunk.next()
                physics(masspoints, 1./(SUBDIVISION * FRAMERATE), f, plunk_pos)
                pos = masspoints[0, count // 2]   # where to listen to
                normalized = (pos[1] - height/2.) / (height/2.)
                rec.add(normalized)


    t_end = time.time()
    print("Completed in %ss" % round(t_end - t_start, 2))


def choose_backend(choice):
    if choice == 'numba':
        import physics_numba
        return physics_numba
    elif choice == 'numbapro':
        import physics_numbapro
        return physics_numbapro
    elif choice == 'numba':
        import physics_numpy
        return physics_numpy
    else:
        raise KeyError('Invalid backend "%s"' % choice)

