"""
EBTA (Entropy-Based Transparency Audit) Receipt System
Provides Shannon entropy estimates and SHA3-256 integrity checks
"""
import hashlib
import json
from typing import Dict
from collections import Counter
import math


def calculate_shannon_entropy(data: bytes) -> float:
    """
    Calculate Shannon entropy of data in bits.
    
    Args:
        data: Input bytes
        
    Returns:
        Entropy in bits
    """
    if len(data) == 0:
        return 0.0
    
    # Count byte frequencies
    frequencies = Counter(data)
    length = len(data)
    
    # Calculate Shannon entropy
    entropy = 0.0
    for count in frequencies.values():
        probability = count / length
        entropy -= probability * math.log2(probability)
    
    return entropy * length * 8  # Return in bits


def generate_receipt(input_data: bytes, output_data: bytes) -> Dict:
    """
    Generate EBTA receipt for compression operation.
    
    Args:
        input_data: Original uncompressed data
        output_data: Compressed data
        
    Returns:
        Receipt dictionary with H_in, H_out, delta, and sha3
    """
    h_in = calculate_shannon_entropy(input_data)
    h_out = len(output_data) * 8  # Exact bit length
    
    receipt = {
        "H_in": int(h_in),
        "H_out": h_out,
        "delta": int(h_in - h_out),
        "sha3": hashlib.sha3_256(output_data).hexdigest()
    }
    
    return receipt


def verify_receipt(payload: bytes, receipt: Dict) -> bool:
    """
    Verify integrity of payload against receipt.
    
    Args:
        payload: Compressed data
        receipt: EBTA receipt dictionary
        
    Returns:
        True if integrity check passes
    """
    computed_hash = hashlib.sha3_256(payload).hexdigest()
    return computed_hash == receipt.get("sha3")
