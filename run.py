import sys
import common

if __name__ == '__main__':
    try:
        backend = common.choose_backend(sys.argv[1])
        filename = sys.argv[2]
    except (KeyError, IndexError) as e:
        print(e)
        print("Usage: python %s <numba|numbapro|numpy> <recorded_file>" % sys.argv[0])
    else:
        print("Click on the screen to plunk the string.")
        print("Y-axis: top -- lighter; bottom -- heavier")
        print("X-axis: position")
        common.main(backend.physics, filename)
