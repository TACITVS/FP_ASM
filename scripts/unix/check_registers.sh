#!/bin/bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$REPO_ROOT"

ASM_DIR="src/asm"

echo "=== CHECKING REGISTER PRESERVATION ==="
echo

for file in fp_core_reductions.asm fp_core_fused_folds.asm fp_core_fused_maps.asm; do
    echo "File: $file"
    echo "----------------------"

    # Check for YMM register saves (vmovdqa [rsp...], ymm)
    echo "YMM saves:"
    grep -n "vmovdqa \[.*\], ymm" "$ASM_DIR/$file" | head -5 || true

    # Check for YMM register restores (vmovdqa ymm, [rsp...])
    echo "YMM restores:"
    grep -n "vmovdqa ymm.*, \[.*\]" "$ASM_DIR/$file" | head -5 || true

    # Check for vzeroupper
    echo "vzeroupper calls:"
    grep -n "vzeroupper" "$ASM_DIR/$file" || true

    echo
done
