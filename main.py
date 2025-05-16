#!/usr/bin/env python3

# MIT/X Consortium License
# © 2025 mahmoudElshimi <mahmoudelshimi@protonmail.ch>

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from typing import Optional
import math

app = FastAPI(title="QRNG API")


def generate_quantum_random_bits(total_bits: int, chunk_size: int = 29) -> str:
    """
    Generate a quantum random bits of length total_bits.
    
    Args:
        total_bits: Total number of bits to generate
        chunk_size: Number of qubits to use per circuit (default 29, max for AerSimulator)
    
    Returns:
        String of random bits
    """
    
    bits = ""
    while len(bits) < total_bits:
        n_bits = min(chunk_size, total_bits - len(bits))
        qc = QuantumCircuit(n_bits, n_bits)
        # Put all qubits in superposition
        qc.h(range(n_bits))
        qc.measure(range(n_bits), range(n_bits))

        backend = AerSimulator()
        transpiled = transpile(qc, backend)
        job = backend.run(transpiled, shots=1)
        result = job.result()
        counts = result.get_counts()
        bits += list(counts.keys())[0]

    return bits


@app.get("/", summary="Generate a 256-bit quantum random number")
def get_256bit_random():
    """
    Generate a 256-bit quantum random number using chunked bit generation.
    
    Returns:
        Dictionary containing:
            - bits: binary string representation
            - as_num: integer representation
            - bits_length: length of bit string
    """

    random_bits = generate_quantum_random_bits(256)
    random_number = int(random_bits, 2)
    return {
        "bits": random_bits,
        "as_num": random_number,
        "bits_length": len(random_bits)
    }


@app.get("/random", summary="Generate quantum random number between [min] and [max] with length")
def get_random_number(
    length: int = Query(..., description="Bit length of the random number to generate, e.g. 8, 16, 32"),
    min_val: Optional[int] = Query(None, description="Minimum value (inclusive)", alias="min"),
    max_val: Optional[int] = Query(None, description="Maximum value (inclusive)", alias="max")
):
    """
    Generate a quantum random number.
    
    Args:
        length: Bit length of random number
        min_val: Minimum value (inclusive)
        max_val: Maximum value (inclusive)
    
    Returns:
        Dictionary containing random number in different formats.
    """

    if (min_val is not None and max_val is None) or (min_val is None and max_val is not None):
        return JSONResponse(
            status_code=400,
            content={"error": "Both 'min' and 'max' must be provided together."}
        )

    if min_val is not None and max_val is not None:
        if min_val > max_val:
            return JSONResponse(
                status_code=400,
                content={"error": "'min' must be less than or equal to 'max'."}
            )
        range_size = max_val - min_val + 1
        n_bits = math.ceil(math.log2(range_size))
        if n_bits > length:
            return JSONResponse(
                status_code=400,
                content={"error": f"'length' is too small for the given range; minimum required bits: {n_bits}"}
            )
        while True:
            random_bits = generate_quantum_random_bits(n_bits)
            random_number = int(random_bits, 2)
            if random_number < range_size:
                break
        final_number = random_number + min_val
        final_bits = format(final_number, f'0{n_bits}b')
        return {
            "bits": final_bits,
            "as_num": final_number,
            "bits_length": len(final_bits),
            "min": min_val,
            "max": max_val
        }

    # generate random bits of specified length
    random_bits = generate_quantum_random_bits(length)
    random_number = int(random_bits, 2)
    return {
        "bits": random_bits,
        "as_num": random_number,
        "bits_length": length
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
