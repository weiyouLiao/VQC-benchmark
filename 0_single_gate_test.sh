source activate benchmark-env
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export MKL_DOMAIN_NUM_THREADS=1
export JULIA_NUM_THREADS=1

cd $1
if [ "$1" = "VQC" ] || [ "$1" = "yao" ]; then
  julia ./single_gate_test.jl
else
  pytest ./single_gate_test.py --benchmark-save="single_gate_test" --benchmark-sort=name --benchmark-min-rounds=5
fi
cd ../