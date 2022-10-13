#!/bin/bash

export OMP_NUM_THREADS=1

in="../CFG/test_structures/graphite_high_eng.cfg"
out="graphite_relaxed.cfg"

mlp relax relax.ini --cfg-filename=$in --save-relaxed=$out --force-tolerance=1e-4 --stress-tolerance=1e-3
