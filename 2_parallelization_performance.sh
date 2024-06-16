source activate benchmark-env

cd $1

threads_list=($(seq 1 64))
for threads in "${threads_list[@]}"
do
  export JULIA_NUM_THREADS=$threads
  julia parallelization_performance.jl
done

cd ../


