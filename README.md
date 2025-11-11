# -tfec-v3.1
Certifiable lossless compression with Zstandard fallback and EBTA receipts. Built and maintained by Syntriass Labs · MIT License · 2025.

# TFEC v3.1 — Certifiable Lossless Compression  
**Production-ready core, CLI, and certification harness**

> Certifiable lossless compression with Zstandard fallback and EBTA receipts.  
> Built and maintained by **Syntriass Labs** · MIT License · 2025

---

## 📦 Features
- Rolling-hash FEE (pattern replacement with 2-byte refs, base64-safe metadata)
- Temporal prefilter (Δ / Δ²) for sequential entropy reduction
- 32-bit arithmetic coder (stable & precise)
- EBTA receipts (Shannon bit estimate + SHA3-256 integrity)
- Zstandard fallback (guarantees never worse than zstd)
- Certification suite (17/17 deterministic tests) with tabular output
- Clean, audit-friendly CLI

---

## ⚙️ Quickstart
```bash
# 1. Create and activate a virtual environment
python -m venv .venv
. .venv/bin/activate

# 2. Install TFEC in editable mode
pip install -e .[test] -r requirements.txt


🧰 Command-Line Interface
Compress
tfec compress input.bin output.tfec

Decompress
tfec decompress output.tfec restored.bin

Verify
diff input.bin restored.bin   # should be empty → bit-perfect match

Typical output:
🚀 TFEC v3.1 — Compress
📥 Input: 32,768 bytes
🗜️  Output: 9,512 bytes
🎯 Ratio: 3.44x   ⏱ 12.7 ms
📈 EBTA Receipt
   H_in:  261,680 bits
   H_out: 76,096 bits
   ΔH:   +185,584 bits


🧪 Certification Suite
Run the full test suite
python scripts/certify.py > certify.log 2>&1
tail -n +1 certify.log

What it does
Runs 17 deterministic test cases (text, logs, random, JSON-like, telecom, etc.)
Verifies bit-exact decompression for each case
Compares compression ratios vs Zstandard
Flags any case where TFEC is more than 1% worse than Zstd
Prints a summary table and final PASS/FAIL result
Example excerpt:
TFEC CORE v3.1 - CERTIFICATION TEST SUITE
-----------------------------------------
  Testing: JSON-like              [✅]  Ratio: 4.22x   Latency: 11.55ms
  Testing: Telecom Pattern        [✅]  Ratio: 5.38x   Latency: 15.03ms
  Testing: Random Small           [✅]  Ratio: 1.00x   Latency:  7.44ms
  ...
  CERTIFICATION RESULT: PASSED


⚖️ Benchmarks vs Zstd
Compare TFEC compression speed and ratio against Zstandard:
python scripts/bench_vs_zstd.py

Typical result:
TFEC: 3.41x  enc 13.5ms  dec 3.8ms
Zstd: 3.35x  size 9,764 bytes
TFEC vs Zstd: 1.02x


🧩 Python API Example
from triass_tfec.core.engine import compress_packet, decompress_packet

data = b"The quick brown fox jumps over the lazy dog." * 1000
compressed = compress_packet(data)
restored   = decompress_packet(compressed)
assert restored == data


📜 EBTA Receipts & Fallback Logic
EBTA Receipts — What they are
Each TFEC payload carries a small JSON “receipt” recording:
FieldMeaning
H_in
Shannon entropy estimate (bits) of the input
H_out
Exact output bit length (len(payload)*8)
delta
Difference H_in - H_out (positive = effective compression)
sha3
SHA3-256 hash of the encoded payload (integrity check)
Purpose
Quantifies compression efficiency (delta)
Ensures integrity — corruption is immediately detected
Provides audit evidence for certification and reproducibility
Verification
from triass_tfec.core.ebta import verify_receipt
ok = verify_receipt(payload, receipt)
assert ok, "Integrity mismatch"


Fallback Logic — Guardrails to Zstandard
TFEC pipeline:
Input → Temporal Prefilter → Rolling FEE → Arithmetic Coder → Output

Compute TFEC output.
If encoded size ≥ 95% of original (no meaningful gain):
Compress original with Zstandard (zstd_compress()).
Mark container as {"fallback": True, "zstd": True}.
During decompression:
If meta["fallback"] and meta["zstd"] → use zstd_decompress().
Always yields bit-exact restoration.
Guarantee:
TFEC is never worse than Zstd and always lossless.

Certification Guarantees
✅ Lossless: All tests must roundtrip exactly.
✅ Integrity: EBTA receipts verified via SHA3-256.
✅ Performance: Never worse than Zstandard (enforced by guardrail).
✅ Transparency: Ratios, timing, and EBTA deltas logged per case.

🗂️ What to Attach for TEC Submission
certify.log — full certification output (redirect stdout to file)
python scripts/certify.py > certify.log 2>&1

requirements_frozen.txt — environment capture
pip freeze > requirements_frozen.txt

Sample input/output pairs
tfec compress sample1.bin sample1.tfec

PDF summary (1 page) explaining EBTA receipts & fallback (see “EBTA Receipts & Fallback Logic” section).

🧾 Environment Reproducibility
CommandPurpose
python -m venv .venv && . .venv/bin/activate
isolate environment
pip install -e .[test] -r requirements.txt
install dependencies
pip freeze > requirements_frozen.txt
snapshot versions
pytest
run all tests (unit + certification)

🔍 License
MIT License © 2025 Syntriass Labs

✉️ Contact
Syntriass Labs
📧 [dev@syntriass.org](mailto:dev@syntriass.org)
🌐 [https://github.com/syntriass-labs/tfec](https://github.com/syntriass-labs/tfec)

 

create a github repository
