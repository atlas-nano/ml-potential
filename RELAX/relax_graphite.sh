#!/bin/bash

export OMP_NUM_THREADS=1

in="../CFG/test_structures/graphite_high_eng.cfg"
out="graphite_relaxed.cfg"

mpirun -n 1 mlp relax relax.ini --cfg-filename=$in --save-relaxed=$out --force-tolerance=1e-5 --stress-tolerance=1e-4
