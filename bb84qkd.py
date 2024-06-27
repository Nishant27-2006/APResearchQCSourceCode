from qiskit import QuantumCircuit, Aer, execute
import random

# Function to simulate the BB84 protocol for QKD
def bb84_qkd_simulation(num_bits):
    alice_bits = [random.randint(0, 1) for _ in range(num_bits)]
    alice_bases = [random.randint(0, 1) for _ in range(num_bits)]
    bob_bases = [random.randint(0, 1) for _ in range(num_bits)]
    eve_bases = [random.randint(0, 1) for _ in range(num_bits)]
    
    alice_qubits = []
    for i in range(num_bits):
        qc = QuantumCircuit(1)
        if alice_bits[i] == 1:
            qc.x(0)
        if alice_bases[i] == 1:
            qc.h(0)
        alice_qubits.append(qc)
    
    eve_intercepted_bits = []
    for i in range(num_bits):
        qc = alice_qubits[i].copy()
        if eve_bases[i] == 1:
            qc.h(0)
        qc.measure_all()
        simulator = Aer.get_backend('aer_simulator')
        result = execute(qc, simulator, shots=1).result()
        measured_bit = int(list(result.get_counts().keys())[0])
        eve_intercepted_bits.append(measured_bit)
    
    bob_bits = []
    for i in range(num_bits):
        qc = alice_qubits[i].copy()
        if bob_bases[i] == 1:
            qc.h(0)
        qc.measure_all()
        simulator = Aer.get_backend('aer_simulator')
        result = execute(qc, simulator, shots=1).result()
        measured_bit = int(list(result.get_counts().keys())[0])
        bob_bits.append(measured_bit)
    
    alice_key = [alice_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    bob_key = [bob_bits[i] for i in range(num_bits) if alice_bases[i] == bob_bases[i]]
    eve_key = [eve_intercepted_bits[i] for i in range(num_bits) if alice_bases[i] == eve_bases[i]]

    return alice_key, bob_key, eve_key, alice_bits, bob_bits, eve_intercepted_bits

# Parameters for the simulation
num_bits = 100
alice_key, bob_key, eve_key, alice_bits, bob_bits, eve_intercepted_bits = bb84_qkd_simulation(num_bits)

print(f"Alice's original bits: {alice_bits[:10]}...")
print(f"Bob's measured bits: {bob_bits[:10]}...")
print(f"Eve's intercepted bits: {eve_intercepted_bits[:10]}...")
print(f"Alice's key: {alice_key[:10]}...")
print(f"Bob's key: {bob_key[:10]}...")
print(f"Eve's key: {eve_key[:10]}...")

# Analyze the results
matching_keys = alice_key == bob_key
eve_success_rate = sum([a == e for a, e in zip(alice_bits, eve_intercepted_bits)]) / num_bits

print(f"Keys match between Alice and Bob: {matching_keys}")
print(f"Eve's success rate in intercepting bits correctly: {eve_success_rate:.2%}")
