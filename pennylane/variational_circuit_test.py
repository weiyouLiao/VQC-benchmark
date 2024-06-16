import os
import pytest
import time
import pandas as pd
import pennylane as qml
import argparse
import json
import jax
from jax import numpy as np
import numpy
import mkl
nthread = 1
mkl.set_num_threads(nthread)
mark = "pennylane"
nqubit_list = range(14, 27)

def heisenberg_hamiltonian(n):
	coeffs = []
	obs = []
	for i in range(n-1):
		coeffs.extend([1, 1, 1])  # J_i = 1
		obs.extend([qml.PauliX(i) @ qml.PauliX(i+1), qml.PauliY(i) @ qml.PauliY(i+1), qml.PauliZ(i) @ qml.PauliZ(i+1)])
	for i in range(n):
		coeffs.append(1)  # h_i = 1
		obs.append(qml.PauliZ(i))
	O = qml.Hamiltonian(coeffs, obs)
	return O


def build_operations(nqubits):
	depth = 10
	operations = []
	for i in range(nqubits):
		operations.append(qml.RZ(numpy.random.rand()*np.pi*2, wires=i))
		operations.append(qml.RY(numpy.random.rand()*np.pi*2, wires=i))
		operations.append(qml.RZ(numpy.random.rand()*np.pi*2, wires=i))
	
	for i in range(depth):
		if (i+1)%2 == 1:
			for j in range(nqubits-1):
				operations.append(qml.CNOT(wires=[j, j+1]))
		else:
			for j in list(range(nqubits-1))[::-1]:
				operations.append(qml.CNOT(wires=[j, j+1]))
		for j in range(nqubits):
			operations.append(qml.RZ(numpy.random.rand()*np.pi*2, wires=j))
			operations.append(qml.RY(numpy.random.rand()*np.pi*2, wires=j))
			operations.append(qml.RZ(numpy.random.rand()*np.pi*2, wires=j))
	return operations


def sim_excute(benchmark, device, operation):
	def excute(device, operation):
		device.apply(operation)
	benchmark(excute, device, operation)	


def ad_excute(benchmark, circuit_adjoint, paralist):
	def excute(circuit_adjoint, paralist):
		jax.grad(circuit_adjoint)(paralist)
	benchmark(excute, circuit_adjoint, paralist)



@pytest.mark.parametrize('nqubits', nqubit_list)
def test_vqc(benchmark, nqubits):
	benchmark.group = 'vqc'
	device = qml.device("lightning.qubit", wires=nqubits)
	operation = build_operations(nqubits)
	sim_excute(benchmark, device, operation)
	
@pytest.mark.parametrize('nqubits', nqubit_list)
def test_vqc_ad(benchmark, nqubits):
	benchmark.group = 'ad'
	depth = 10
	n_params_count = (depth+1)*nqubits*3
	paralist = [numpy.random.rand()*np.pi*2 for i in range(n_params_count)]
	paralist = np.array(paralist)
	
	dev_lightning = qml.device('lightning.qubit', wires=nqubits)
	@qml.qnode(dev_lightning, diff_method="adjoint")
	def circuit_adjoint(paralist):
			depth = 10
			O = heisenberg_hamiltonian(nqubits)
			count = 0
			for i in range(nqubits):
				qml.RZ(paralist[count], wires=i)
				count+=1
				qml.RY(paralist[count], wires=i)
				count+=1
				qml.RZ(paralist[count], wires=i)
				count+=1
			for i in range(depth):
				if (i+1)%2 == 1:
					for j in range(nqubits-1):
						qml.CNOT(wires=[j, j+1])
				else:
					for j in list(range(nqubits-1))[::-1]:
						qml.CNOT(wires=[j, j+1])
				for j in range(nqubits):
					qml.RZ(paralist[count], wires=j)
					count+=1
					qml.RY(paralist[count], wires=j)
					count+=1
					qml.RZ(paralist[count], wires=j)
					count+=1
			return qml.expval(O)

	ad_excute(benchmark, circuit_adjoint, paralist)







	
