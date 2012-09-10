import sys
try:
    from cPickle import pickle
except ImportError:
    import pickle
import scipy.io.wavfile as wavfile
import numpy as np

from common import FRAMERATE, SPEEDUP

def main(fin, fout, speedup):
    with open(fin, "rb") as fin:
        rec = np.array(pickle.load(fin))

    rate = 44100
    print("sample rate: %s" % rate)
    peak = 2**15 - 1
    # adjust speed
    orig_rate = FRAMERATE * SPEEDUP
    scaling = rate / orig_rate // speedup
    print("scaling: %s" % scaling)


    samples = np.zeros(len(rec) * scaling, dtype=np.int16)

    # normalize
    amp = peak * 1.0 / max(rec.max(), abs(rec.min()))

    for i in xrange(samples.shape[0]):
        samples[i] = amp * rec[i // scaling]

    wavfile.write(fout, rate, samples)

if __name__ == '__main__':

    fin = sys.argv[1]
    fout = sys.argv[2]
    try:
        speedup = float(sys.argv[3])
    except IndexError:
        speedup = 1.
    main(fin, fout, speedup)
