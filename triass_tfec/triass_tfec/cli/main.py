"""
TFEC v3.1 Command-Line Interface
"""
import sys
import argparse
import time
from pathlib import Path
from triass_tfec.core.engine import compress_packet, decompress_packet
from triass_tfec.core.ebta import generate_receipt


def main():
    parser = argparse.ArgumentParser(description="TFEC v3.1 - Certifiable Lossless Compression")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Compress command
    compress_parser = subparsers.add_parser("compress", help="Compress a file")
    compress_parser.add_argument("input", help="Input file path")
    compress_parser.add_argument("output", help="Output file path")
    
    # Decompress command
    decompress_parser = subparsers.add_parser("decompress", help="Decompress a file")
    decompress_parser.add_argument("input", help="Input file path")
    decompress_parser.add_argument("output", help="Output file path")
    
    args = parser.parse_args()
    
    if args.command == "compress":
        compress_file(args.input, args.output)
    elif args.command == "decompress":
        decompress_file(args.input, args.output)
    else:
        parser.print_help()
        sys.exit(1)


def compress_file(input_path: str, output_path: str):
    """Compress a file"""
    print(f"🚀 TFEC v3.1 — Compress")
    
    # Read input
    input_data = Path(input_path).read_bytes()
    print(f"📥 Input: {len(input_data):,} bytes")
    
    # Compress
    start = time.time()
    compressed = compress_packet(input_data)
    elapsed = (time.time() - start) * 1000
    
    # Generate receipt
    receipt = generate_receipt(input_data, compressed)
    
    # Write output
    Path(output_path).write_bytes(compressed)
    
    # Report
    ratio = len(input_data) / len(compressed) if len(compressed) > 0 else 0
    print(f"🗜️  Output: {len(compressed):,} bytes")
    print(f"🎯 Ratio: {ratio:.2f}x   ⏱ {elapsed:.1f} ms")
    print(f"📈 EBTA Receipt")
    print(f"   H_in:  {receipt['H_in']:,} bits")
    print(f"   H_out: {receipt['H_out']:,} bits")
    print(f"   ΔH:   {receipt['delta']:+,} bits")


def decompress_file(input_path: str, output_path: str):
    """Decompress a file"""
    print(f"🔓 TFEC v3.1 — Decompress")
    
    # Read input
    compressed = Path(input_path).read_bytes()
    print(f"📥 Input: {len(compressed):,} bytes")
    
    # Decompress
    start = time.time()
    restored = decompress_packet(compressed)
    elapsed = (time.time() - start) * 1000
    
    # Write output
    Path(output_path).write_bytes(restored)
    
    # Report
    print(f"📤 Output: {len(restored):,} bytes")
    print(f"⏱ {elapsed:.1f} ms")


if __name__ == "__main__":
    main()
