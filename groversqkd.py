import time
from qiskit import QuantumCircuit, Aer, execute
from qiskit.circuit.library import GroverOperator
from qiskit.quantum_info import random_unitary

def create_oracle(key_size, target_state):
    unitary_matrix = random_unitary(2**key_size)

    qc_unitary = QuantumCircuit(key_size)
    qc_unitary.unitary(unitary_matrix, range(key_size))

    updated_target_state = unitary_matrix @ target_state

    oracle_circuit = QuantumCircuit(key_size)
    oracle_circuit.unitary(updated_target_state, range(key_size), label="Oracle")
    return oracle_circuit

def simulate_grovers_qkd_attack(key_size, data_type):
    if data_type == 'binary':
        target_key_state = random_unitary(2**key_size)
    elif data_type == 'integers':
        target_key_state = random_unitary(2**key_size, seed=0)
    else:
        raise ValueError("Invalid data type. Supported types are 'binary' and 'integers'.")

    oracle_circuit = create_oracle(key_size, target_key_state)
    grover_operator = GroverOperator(oracle_circuit)

    grover_circuit = QuantumCircuit(key_size, key_size)
    grover_circuit.h(range(key_size))
    grover_circuit.append(grover_operator, range(key_size))
    grover_circuit.measure(range(key_size), range(key_size))

    backend = Aer.get_backend('aer_simulator')
    
    start_time = time.time()
    result = execute(grover_circuit, backend, shots=1).result()
    end_time = time.time()
    
    counts = result.get_counts(grover_circuit)
    execution_time = end_time - start_time
    
    match_found = any(state == target_key_state for state in counts.keys())
    
    return counts, execution_time, match_found

key_size = 3
data_type = 'binary'

qkd_attack_result, execution_time, match_found = simulate_grovers_qkd_attack(key_size, data_type)
print(f"Grover's attack on QKD result: {qkd_attack_result}")
print(f"Execution time: {execution_time} seconds")
print(f"Match found: {match_found}")
