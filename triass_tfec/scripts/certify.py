"""
TFEC v3.1 Certification Suite
Runs 17 deterministic test cases
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from triass_tfec.core.engine import compress_packet, decompress_packet
import time


def run_certification():
    print("TFEC CORE v3.1 - CERTIFICATION TEST SUITE")
    print("-" * 45)
    
    test_cases = [
        ("Empty", b""),
        ("Small Text", b"Hello World!" * 10),
        ("Repeated Pattern", b"ABCD" * 1000),
        ("JSON-like", b'{"key":"value","array":[1,2,3]}' * 100),
        ("Telecom Pattern", b"ATATATATAT" * 500),
        ("Random Small", bytes(range(256))),
        ("Zeros", b"\x00" * 10000),
        ("Ones", b"\xff" * 10000),
        ("Alternating", b"\xaa\x55" * 5000),
        ("Sequential", bytes(i % 256 for i in range(10000))),
        ("CSV-like", b"name,age,city\nJohn,30,NYC\n" * 200),
        ("XML-like", b"<tag>value</tag>" * 500),
        ("Log Pattern", b"[INFO] Application started\n" * 300),
        ("Binary Counter", bytes(i % 256 for i in range(5000))),
        ("Mixed Text", b"The quick brown fox jumps over the lazy dog. " * 200),
        ("Sparse Data", b"\x00\x00\x00\x01" * 2500),
        ("High Entropy", bytes((i * 157 + 73) % 256 for i in range(10000))),
    ]
    
    passed = 0
    failed = 0
    
    for name, data in test_cases:
        try:
            start = time.time()
            compressed = compress_packet(data)
            restored = decompress_packet(compressed)
            elapsed = (time.time() - start) * 1000
            
            if restored == data:
                ratio = len(data) / len(compressed) if len(compressed) > 0 else 1.0
                print(f"  Testing: {name:20s} [✅]  Ratio: {ratio:.2f}x   Latency: {elapsed:.2f}ms")
                passed += 1
            else:
                print(f"  Testing: {name:20s} [❌]  Decompression mismatch")
                failed += 1
        except Exception as e:
            print(f"  Testing: {name:20s} [❌]  Error: {e}")
            failed += 1
    
    print()
    print(f"  CERTIFICATION RESULT: {'PASSED' if failed == 0 else 'FAILED'}")
    print(f"  Passed: {passed}/{passed + failed}")
    
    return failed == 0


if __name__ == "__main__":
    success = run_certification()
    sys.exit(0 if success else 1)
