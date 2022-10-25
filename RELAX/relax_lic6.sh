#!/bin/bash

export OMP_NUM_THREADS=1

in="../CFG/test_structures/lic6_high_eng.cfg"
out="lic6_relaxed.cfg"

mpirun -n 1 mlp relax relax.ini --cfg-filename=$in --save-relaxed=$out --force-tolerance=1e-4 --stress-tolerance=1e-3
