import sys
try:
    from cPickle import pickle
except ImportError:
    import pickle
import scipy.io.wavfile as wavfile
import numpy as np

from common import FRAMERATE, SUBDIVISION

def main(fin, fout, speedup):
    with open(fin, "rb") as fin:
        rec = np.array(pickle.load(fin))

    rate = 48000
    print("sample rate: %s" % rate)
    peak = 2**15 - 1
    # adjust speed
    orig_rate = FRAMERATE * SUBDIVISION
    scaling = int(round(rate / orig_rate / speedup))
    print("scaling: %s" % scaling)


    samples = np.zeros(rec.shape[0] * scaling, dtype=np.int16)

    # normalize
    amp = peak * 1.0 / max(rec.max(), abs(rec.min()))

    for i in xrange(rec.shape[0] - 1):
        for j in range(scaling):
            percent = float(j) / scaling
            pt = ((1 - percent) * rec[i] + percent * rec[i + 1])  # linear interpolate
            samples[i * scaling + j] = amp * pt

    wavfile.write(fout, rate, samples)

if __name__ == '__main__':

    fin = sys.argv[1]
    fout = sys.argv[2]
    try:
        speedup = float(sys.argv[3])
    except IndexError:
        speedup = 1.
    main(fin, fout, speedup)
