source activate benchmark-env
cd $1
threads_list=(1 4 8 16 32 64)
for threads in "${threads_list[@]}"
do
  export JULIA_NUM_THREADS=$threads
  julia noisy_ad_performance.jl
done


