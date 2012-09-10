from matplotlib import pyplot as plt
import pickle, sys

with open(sys.argv[1], "rb") as fin:
    rec = pickle.load(fin)

plt.plot(rec)
plt.show()
