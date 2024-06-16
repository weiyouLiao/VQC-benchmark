import os
os.environ['OMP_NUM_THREADS'] = '1'
import numpy as np
from projectq import MainEngine
from projectq.ops import Measure, CNOT,Rz,All,Ry
import pytest
import mkl
import argparse
import json
nthread = 1
mkl.set_num_threads(nthread)
mark = "projectq"
nqubit_list = range(14, 27)


def sim_excute(benchmark, nqubits):
	eng = MainEngine()
	Qureg=eng.allocate_qureg(nqubits)
	def excute(eng, Qureg):
		depth = 10
		for i in range(nqubits):
			Rz(np.random.rand()*np.pi*2)|Qureg[i]
			Ry(np.random.rand()*np.pi*2)|Qureg[i]
			Rz(np.random.rand()*np.pi*2)|Qureg[i]
		for i in range(depth):
			if (i+1)%2 == 1:
				for j in range(nqubits-1):
					CNOT|(Qureg[j],Qureg[j+1])
			else:
				for j in list(range(nqubits-1))[::-1]:
					CNOT|(Qureg[j],Qureg[j+1])
			for j in range(nqubits):
				Rz(np.random.rand()*np.pi*2)|Qureg[j]
				Ry(np.random.rand()*np.pi*2)|Qureg[j]
				Rz(np.random.rand()*np.pi*2)|Qureg[j]
		All(Measure)|Qureg
		eng.flush()
	benchmark(excute, eng, Qureg)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_H(benchmark, nqubits):
    benchmark.group = 'vqc'
    sim_excute(benchmark, nqubits)




	