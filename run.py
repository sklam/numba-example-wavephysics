import sys
import common
import physics_numba, physics_numpy


if __name__ == '__main__':
    try:
        choice = sys.argv[1]

        backend=  {'numba': physics_numba.physics,
                   'numpy': physics_numpy.physics}[choice]

        filename = sys.argv[2]
    except:
        print("Usage: python %s <numba|numpy> <recorded_file>" % sys.argv[0])
    else:
        print "Click on the screen to plunk the string."
        print "Y-axis: top -- lighter; bottom -- heavier"
        print "X-axis: position"
        common.main(backend, filename)
