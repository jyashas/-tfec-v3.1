"""
Benchmark TFEC vs Zstandard
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from triass_tfec.core.engine import compress_packet, decompress_packet
import zstandard as zstd
import time


def benchmark():
    print("TFEC vs Zstandard Benchmark")
    print("=" * 50)
    
    # Test data
    test_data = b"The quick brown fox jumps over the lazy dog. " * 1000
    
    # TFEC
    start = time.time()
    tfec_compressed = compress_packet(test_data)
    tfec_enc_time = (time.time() - start) * 1000
    
    start = time.time()
    tfec_restored = decompress_packet(tfec_compressed)
    tfec_dec_time = (time.time() - start) * 1000
    
    tfec_ratio = len(test_data) / len(tfec_compressed)
    
    # Zstandard
    start = time.time()
    zstd_compressed = zstd.compress(test_data, level=3)
    zstd_enc_time = (time.time() - start) * 1000
    
    start = time.time()
    zstd_restored = zstd.decompress(zstd_compressed)
    zstd_dec_time = (time.time() - start) * 1000
    
    zstd_ratio = len(test_data) / len(zstd_compressed)
    
    # Results
    print(f"\nTFEC: {tfec_ratio:.2f}x  enc {tfec_enc_time:.1f}ms  dec {tfec_dec_time:.1f}ms")
    print(f"Zstd: {zstd_ratio:.2f}x  enc {zstd_enc_time:.1f}ms  dec {zstd_dec_time:.1f}ms")
    print(f"\nTFEC vs Zstd size: {len(tfec_compressed) / len(zstd_compressed):.2f}x")
    print(f"TFEC vs Zstd speed: {zstd_enc_time / tfec_enc_time:.2f}x")
    
    # Verify correctness
    assert tfec_restored == test_data, "TFEC verification failed"
    assert zstd_restored == test_data, "Zstd verification failed"
    print("\n✅ All verifications passed")


if __name__ == "__main__":
    benchmark()
