import numpy as np
import pennylane as qml
import mkl
import pytest
nthread = 1
mkl.set_num_threads(nthread)
mark = "pennylane"
nqubit_list = range(14, 31)

def build_operation_H(nqubits):
    operation = [qml.Hadamard(wires=[0])]
    return operation
def build_operation_RX(nqubits):
    operation = [qml.RX(np.pi/4, wires=[0])]
    return operation
def build_operation_CNOT(nqubits):
    operation = [qml.CNOT(wires=[0, 1])]
    return operation
def build_operation_Toffoli(nqubits):
    operation = [qml.Toffoli(wires=[0, 1, 2])]
    return operation


def sim_excute(benchmark, device, operation):
    def excute(device, operation):
        device.apply(operation)
    benchmark(excute, device, operation)




    
@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_H(benchmark, nqubits):
    benchmark.group = 'H'
    device = qml.device("lightning.qubit", wires=nqubits)
    operation = build_operation_H(nqubits)
    sim_excute(benchmark, device, operation)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_RX(benchmark, nqubits):
    benchmark.group = 'RX'
    device = qml.device("lightning.qubit", wires=nqubits)
    operation = build_operation_RX(nqubits)
    sim_excute(benchmark, device, operation)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_CNOT(benchmark, nqubits):
    benchmark.group = 'CNOT'
    device = qml.device("lightning.qubit", wires=nqubits)
    operation = build_operation_CNOT(nqubits)
    sim_excute(benchmark, device, operation)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_Toffoli(benchmark, nqubits):
    benchmark.group = 'Toffoli'
    device = qml.device("lightning.qubit", wires=nqubits)
    operation = build_operation_Toffoli(nqubits)
    sim_excute(benchmark, device, operation)


