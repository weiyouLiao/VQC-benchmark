from qiskit import Aer, QuantumCircuit
from qiskit.compiler import transpile
import pytest
import numpy as np

import mkl
nthread = 1
mkl.set_num_threads(nthread)

mark = "qiskit"
nqubit_list = range(14, 27)

def build_circuit(nqubits):
	depth = 10
	circ = QuantumCircuit(nqubits)
	for i in range(nqubits):
		circ.rz(np.random.rand()*np.pi*2, i)
		circ.ry(np.random.rand()*np.pi*2, i)
		circ.rz(np.random.rand()*np.pi*2, i)
	for i in range(depth):
		if (i+1)%2 == 1:
			for j in range(nqubits-1):
				circ.cx(j,j+1)
		else:
			for j in list(range(nqubits-1))[::-1]:
				circ.cx(j,j+1)
		for j in range(nqubits):
			circ.rz(np.random.rand()*np.pi*2, j)
			circ.ry(np.random.rand()*np.pi*2, j)
			circ.rz(np.random.rand()*np.pi*2, j)
	return circ


def sim_excute(benchmark, circuit):
	backend = Aer.get_backend("statevector_simulator")
	cirucit_opt = transpile(circuit, backend)
	# circuit.save_statevector()
	backend.set_options(max_parallel_threads=1,max_parallel_experiments =1,device ='CPU',method="statevector")
	def excute(backend, circuit):
		qobj_aer = backend.run(circuit).result().get_statevector(circuit)
	benchmark(excute, backend, cirucit_opt)


@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_H(benchmark, nqubits):
    benchmark.group = 'vqc'
    circuit = build_circuit(nqubits)
    sim_excute(benchmark, circuit)


