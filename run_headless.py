import sys
import common

if __name__ == '__main__':
    try:
        backend = common.choose_backend(sys.argv[1])
        filename = sys.argv[2]
    except (KeyError, IndexError) as e:
        print(e)
        print("Usage: python %s <numba|numpy> <recorded_file>" % sys.argv[0])
    else:
        common.main_headless(backend.physics, filename)
