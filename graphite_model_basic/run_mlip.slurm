#!/bin/bash
#SBATCH --job-name=train_LiC6_graphite
#SBATCH --account=ddp381
#SBATCH --nodes=1
#SBATCH --partition=shared
#SBATCH --ntasks-per-node=64
#SBATCH --time=6:0:0
#SBATCH --mail-type=ALL

cd /home/rramji/test_mlip

train_data=train_LiC6_graphite.short.cfg
test_data=test_LiC6_graphite.short.cfg

srun -n 64 mlp train init.mtp $train_data --trained-pot-name=pot.mtp --valid-cfgs=$test_data
