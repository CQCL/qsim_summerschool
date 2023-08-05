from pytket.utils import QubitPauliOperator
from pytket.pauli import Pauli, QubitPauliString
from pytket.circuit import Qubit

def ising_model(n_qubits: int, h: float, j: float):
    """ Returns a QubitPauliOperator representing the Ising model Hamiltonian
    Args:
        n_qubits: number of qubits
        h: strength of the transverse field
        j: strength of the coupling
        
    Returns:
        QubitPauliOperator representing the Ising model Hamiltonian"""
    qpo = QubitPauliOperator()
    for i in range(n_qubits - 1):
        qpo = qpo + QubitPauliOperator({QubitPauliString([Qubit(i), Qubit(i+1)], [Pauli.Z, Pauli.Z]): j})
    for i in range(n_qubits):
        qpo = qpo + QubitPauliOperator({QubitPauliString([Qubit(i)], [Pauli.X]): h})
    return qpo