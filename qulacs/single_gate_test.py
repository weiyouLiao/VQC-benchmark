from qulacs import QuantumState, QuantumCircuit,QuantumCircuitSimulator
import pytest
import numpy as np
import mkl
nthread = 1
mkl.set_num_threads(nthread)
mark = "qulacs"
nqubit_list = range(14, 31)

def build_circuit_H(nqubits):
    circ = QuantumCircuit(nqubits)
    circ.add_H_gate(0)
    return circ
def build_circuit_RX(nqubits):
    circ = QuantumCircuit(nqubits)
    circ.add_RX_gate(0, np.pi/4)
    return circ
def build_circuit_CNOT(nqubits):
    circ = QuantumCircuit(nqubits)
    circ.add_CNOT_gate(0,1)
    return circ
# def build_circuit_Toffoli(nqubits):
#     circ = QuantumCircuit(nqubits)
#     circ.add_
#     return circ

def sim_excute(benchmark, circcuit, state):
    sim = QuantumCircuitSimulator(circcuit, state)
    sim.initialize_state(0)
    def excute(sim):
        sim.simulate()
    benchmark(excute, sim)


@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_H(benchmark, nqubits):
    benchmark.group = 'H'
    circuit = build_circuit_H(nqubits)
    state = QuantumState(nqubits)
    sim_excute(benchmark, circuit, state)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_RX(benchmark, nqubits):
    benchmark.group = 'RX'
    circuit = build_circuit_RX(nqubits)
    state = QuantumState(nqubits)
    sim_excute(benchmark, circuit, state)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_CNOT(benchmark, nqubits):
    benchmark.group = 'CNOT'
    circuit = build_circuit_CNOT(nqubits)
    state = QuantumState(nqubits)
    sim_excute(benchmark, circuit, state)

# @pytest.mark.parametrize('nqubits', nqubit_list)
# def test_single_Toffoli(benchmark, nqubits):
#     benchmark.group = 'Toffoli'
#     circuit = build_circuit_Toffoli(nqubits)
#     sim_excute(benchmark, circuit)

# def cnot_performance(n):
#     state = QuantumState(n)
#     # state.set_zero_state()
#     circ = QuantumCircuit(n)
#     # circ.add_gate(H(0))
#     circ.add_CNOT_gate(0,1)
#     sim = QuantumCircuitSimulator(circ, state)
#     sim.initialize_state(0)
#     epoch = 100.0
#     ta = time.time_ns() / (10 ** 9)
#     for i in range(int(epoch)):
#         sim.simulate()
#     tb = time.time_ns() / (10 ** 9)
#     t = tb-ta
#     t = t/epoch
#     # print("t:{}".format(t))
#     return t
