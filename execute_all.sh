#Single Gate Operation Benchmarks
./0_single_gate_test.sh VQC
./0_single_gate_test.sh yao
./0_single_gate_test.sh pennylane
./0_single_gate_test.sh qulacs
./0_single_gate_test.sh qiskit
./0_single_gate_test.sh projectq

# Quantum Circuit and Variational Quantum Circuit Benchmarks
./1_variational_circuit_test.sh VQC
./1_variational_circuit_test.sh yao
./1_variational_circuit_test.sh pennylane
./1_variational_circuit_test.sh qulacs
./1_variational_circuit_test.sh qiskit
./1_variational_circuit_test.sh projectq

# VQC Parallelization test
./2_parallelization_performance.sh VQC

# VQC Noisy Automatic Differentiation test
./3_noisy_ad_performance.sh VQC
