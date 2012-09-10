numba-example-wavephysics
=========================

A numba example that implements a wave physics simulation.  Just like plunking a rubberband.

Quick Run
---------

With GUI

    python run.py numba record.dat

Headless

    python run_headless.py numba record.dat

Generate .wav sound file

    python write_wave.py record.dat record.wav

Generate plot of the sound wave

    python plot.py record.dat


To use the numpy backend, which is VERY SLOW, replace "numba" with "numpy" in the above commands.
