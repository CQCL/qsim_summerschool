from pytket.circuit import Circuit, Qubit, CircBox, Pauli
from sympy import Symbol
from typing import List

class ControlledPauliExpBox(CircBox):

    def __init__(
        self,
        paulis: List[Pauli],
        qubits_idx: List[Qubit],
        rotation: Symbol
        ):
        r"""
        Create a unitary circuit encapsulated inside a pytket.circuit.CircBox, 
        which encodes an ancilla-controlled pauli-exponential acting over N-qubits.
        Args:
            paulis: List of Pauli operators to be applied to each qubit
            qubits_idx: List of qubits to apply the paulis to
            rotation: Symbolic rotation angle
        """
        if len(qubits_idx) != len(paulis):
            raise RuntimeError("Qubits should be same length as pauli")
        n_qubits = len(paulis)
        circuit_a = Circuit()
        circuit_a.add_q_register('q', n_qubits)
        
        # SINGLE PAULI GADGET
        # - Appropriate pauli gates
        for qubit, pauli in zip(qubits_idx, paulis):
            if pauli == Pauli.X:
                circuit_a.H(qubit)
            elif pauli == Pauli.Y:
                circuit_a.V(qubit)
            else:
                continue
        # - CNOT cascade
        for q0, q1 in zip(qubits_idx[:-1], qubits_idx[1:]):
            circuit_a.CX(q0, q1)
        
        # - Reverse of cascade and pauli gates
        circuit_b = circuit_a.dagger()

        # - Controlled Rotation in the middle
        circuit_rot = Circuit()
        q = circuit_rot.add_q_register('q', n_qubits)
        a = circuit_rot.add_q_register('a', 1)

        circuit_rot.CRz(rotation, a[0], qubits_idx[-1])
        
        circuit = Circuit()
        circuit.append(circuit_a)
        circuit.append(circuit_rot)
        circuit.append(circuit_b)
        circuit.flatten_registers() # Must be flattened to re index so DecomposeBoxes works
        super().__init__(circuit)