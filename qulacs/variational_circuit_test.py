import os
os.environ["QULACS_NUM_THREADS"]="1"
import numpy as np
from qulacs import ParametricQuantumCircuit, Observable,QuantumState, QuantumCircuit, QuantumCircuitSimulator
from qulacs.circuit import QuantumCircuitOptimizer
import pytest
import mkl
nthread = 1
mkl.set_num_threads(nthread)
mark = "qulacs"
nqubit_list = range(14, 27)
simulator_type = "backpp"

def build_circuit(nqubits):
	depth = 10
	circ = QuantumCircuit(nqubits)

	for i in range(nqubits):
		circ.add_RZ_gate(i, np.random.rand()*np.pi*2)
		circ.add_RY_gate(i, np.random.rand()*np.pi*2)
		circ.add_RZ_gate(i, np.random.rand()*np.pi*2)
	for i in range(depth):
		if (i+1)%2 == 1:
			for j in range(nqubits-1):
				circ.add_CNOT_gate(j, j+1)
		else:
			for j in list(range(nqubits-1))[::-1]:
				circ.add_CNOT_gate(j, j+1)
		for j in range(nqubits):
			circ.add_RZ_gate(j, np.random.rand()*np.pi*2)
			circ.add_RY_gate(j, np.random.rand()*np.pi*2)
			circ.add_RZ_gate(j, np.random.rand()*np.pi*2)
	return circ




def build_circuit_parametrized(nqubits):
	depth = 10
	circ = ParametricQuantumCircuit(nqubits)
	n_params_count = (depth+1)*nqubits*3
	theta = [np.random.rand()*np.pi*2 for i in range(n_params_count)]
	ncount = 0
	for i in range(nqubits):
		circ.add_parametric_RZ_gate(i, -theta[ncount])
		ncount += 1
		circ.add_parametric_RY_gate(i, -theta[ncount])
		ncount += 1
		circ.add_parametric_RZ_gate(i, -theta[ncount])
		ncount += 1
	for i in range(depth):
		if (i+1)%2 == 1:
			for j in range(nqubits-1):
				circ.add_CNOT_gate(j, j+1)
		else:
			for j in list(range(nqubits-1))[::-1]:
				circ.add_CNOT_gate(j, j+1)
		for j in range(nqubits):
			circ.add_parametric_RZ_gate(j, -theta[ncount])
			ncount += 1
			circ.add_parametric_RY_gate(j, -theta[ncount])
			ncount += 1
			circ.add_parametric_RZ_gate(j, -theta[ncount])
			ncount += 1
	return circ
	

def heisenberg_1d(n,hz=0,J=1,Jzz=1):
	observable = Observable(n)
	for i in range(n):
		observable.add_operator(hz, "Z {}".format(i))
	for i in range(n-1):
		observable.add_operator(J, "X {} X {}".format(i,i+1))
		observable.add_operator(J, "Y {} Y {}".format(i,i+1))
		observable.add_operator(Jzz, "Z {} Z {}".format(i,i+1))
	return observable



def sim_excute(benchmark, circuit, state):
	sim = QuantumCircuitSimulator(circuit, state)
	sim.initialize_state(0)
	def excute(sim):
		sim.simulate()
	benchmark(excute, sim)

def ad_excute(benchmark, circuit, ham):
	def excute(circuit, ham):
		grads = circuit.backprop(ham)
	benchmark(excute, circuit, ham)

# def noiseless_derivation_performance(n,depth):
# 	state = QuantumState(n)
# 	state.set_zero_state()
# 	variational_circuit = vqc_circuit(n,depth)
# 	optimizer = QuantumCircuitOptimizer()
# 	optimizer.optimize(variational_circuit, block_size =2)
# 	ham = heisenberg_1d(n)
# 	ta = time.time() 
# 	grads = variational_circuit.backprop(ham)
# 	tb = time.time()
# 	t = tb-ta
# 	#print(grads)
# 	print("t:{}".format(t))
# 	return t

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_vqc(benchmark, nqubits):
	benchmark.group = 'vqc'
	state = QuantumState(nqubits)
	state.set_zero_state()
	circuit = build_circuit(nqubits)
	optimizer = QuantumCircuitOptimizer()
	optimizer.optimize(circuit, block_size = 2)
	sim_excute(benchmark, circuit, state)



@pytest.mark.parametrize('nqubits', nqubit_list)
def test_vqc_ad(benchmark, nqubits):
	benchmark.group = 'ad'
	circuit = build_circuit_parametrized(nqubits)
	optimizer = QuantumCircuitOptimizer()
	optimizer.optimize(circuit, block_size =2)
	ham = heisenberg_1d(nqubits)
	ad_excute(benchmark, circuit, ham)