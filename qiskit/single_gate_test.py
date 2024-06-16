from qiskit import Aer, QuantumCircuit
import pandas as pd
import numpy as np
import mkl
import pytest
nthread = 1
mkl.set_num_threads(nthread)
nqubit_list = range(14, 31)

def build_circuit_H(nqubits):
    circ = QuantumCircuit(nqubits)
    circ.h(0)
    return circ
def build_circuit_RX(nqubits):
    circ = QuantumCircuit(nqubits)
    circ.rx(np.pi/4,0)
    return circ
def build_circuit_CNOT(nqubits):
    circ = QuantumCircuit(nqubits)
    circ.cx(0,1)
    return circ
# def build_circuit_Toffoli(nqubits):
#     circ = QuantumCircuit(nqubits)
#     circ.ccx(0, 1, 2)
#     return circ

def sim_excute(benchmark, circuit):
    backend = Aer.get_backend("statevector_simulator")
    backend.set_options(max_parallel_threads=1,max_parallel_experiments =1,device ='CPU')
    def excute(backend, circuit):
        backend.run(circuit)
        result = backend.run(circuit).result()
        statevector = result.get_statevector(circuit)
    benchmark(excute, backend, circuit)



    
@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_H(benchmark, nqubits):
    benchmark.group = 'H'
    circuit = build_circuit_H(nqubits)
    sim_excute(benchmark, circuit)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_RX(benchmark, nqubits):
    benchmark.group = 'RX'
    circuit = build_circuit_RX(nqubits)
    sim_excute(benchmark, circuit)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_CNOT(benchmark, nqubits):
    benchmark.group = 'CNOT'
    circuit = build_circuit_CNOT(nqubits)
    sim_excute(benchmark, circuit)

# @pytest.mark.parametrize('nqubits', nqubit_list)
# def test_single_Toffoli(benchmark, nqubits):
#     benchmark.group = 'Toffoli'
#     circuit = build_circuit_Toffoli(nqubits)
#     sim_excute(benchmark, circuit)

