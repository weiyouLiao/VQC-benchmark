from projectq import MainEngine
from projectq.backends import Simulator
from projectq import ops
import sys
import time
import pandas as pd
import numpy as np
import pytest
import mkl

mkl.set_num_threads(1)
mark = "projectq"
nqubit_list = range(14, 31)

def take_locs(qureg, locs):
    if isinstance(locs, int):
        return qureg[locs]
    elif isinstance(locs, tuple):
        return tuple(qureg[loc] for loc in locs)
    elif locs is None:
        return qureg
    else:
        raise

def sim_excute(benchmark, G, locs, nqubits):
    eng = MainEngine()
    reg = eng.allocate_qureg(nqubits)
    qi = take_locs(reg, locs)
    def excute(eng, G, qi):
        G | qi
        eng.flush()
    benchmark(excute, eng, G, qi)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_H(benchmark, nqubits):
    benchmark.group = "H"
    sim_excute(benchmark, ops.X, 0, nqubits)
    
@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_RX(benchmark, nqubits):
    benchmark.group = "RX"
    sim_excute(benchmark, ops.Rx(np.pi/4), 0, nqubits)

@pytest.mark.parametrize('nqubits', nqubit_list)
def test_single_CNOT(benchmark, nqubits):
    benchmark.group = "CNOT"
    sim_excute(benchmark, ops.CNOT, (0,1), nqubits)
    
# @pytest.mark.parametrize('nqubits', nqubit_list)
# def test_single_Tofflie(benchmark, nqubits):
#     benchmark.group = "Tofflie"
#     sim_excute(benchmark, ops.Rx(np.pi/4), 0, nqubits)





