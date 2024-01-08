# https://www.qcoder.jp/contests/demo/problems/B
from qiskit import QuantumCircuit

def solve() -> QuantumCircuit:
    qc = QuantumCircuit(1)
    qc.x(0)
    qc.h(0)
    return qc

def check(backend):
    qc = solve()
    qc.h(0)
    qc.measure_all()
    result = backend.run(qc).result()

    max_value = None
    max_count = 0
    for v, c in result.get_counts().items():
        if max_count < c:
            max_value = v
            max_count = c
    return max_value == '1'
