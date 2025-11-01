# FP-ASM

Welcome to the FP-ASM wiki. This site mirrors what you would create through GitHub's own wiki editor at https://github.com/TACITVS/FP_ASM/wiki/_new. Use the sidebar or the quick links below to explore every functional kernel, roadmap milestone, and publishing tip.

- [[API – Core Modules]]
- [[API – Advanced Algorithms]]
- [[Generic Functional Interface]]
- [[Roadmap]]
- [[Publishing Tips]]

## Overview

FP-ASM is a production-grade functional-programming toolkit for C, implemented in hand-optimized x86-64 assembly with AVX2 acceleration. The current distribution targets the Microsoft x64 calling convention; a System V port is planned next.

## Key Features

* Coverage of 36 functional-programming staples (map, fold, filter, group, unfold, etc.)
* 1.0–4.0× speedups against GCC `-O3` via fused kernels and SIMD code generation
* Zero external dependencies—include the supplied headers and link the objects
* Distinct entry points for `int64_t` and `double` primitives

## Quick Start

```c
#include <stdio.h>
#include "fp_core.h"

int main(void) {
    int64_t numbers[] = {1, 2, 3, 4, 5};
    int64_t sum = fp_reduce_add_i64(numbers, 5);
    printf("Sum: %lld\n", sum);

    double data[] = {25.3, 19.2, 28.5, 21.8};
    fp_sort_f64(data, 4);
    printf("Median: %.1f\n", data[2]);

    int64_t input[] = {1, 1, 2, 2, 2, 3};
    int64_t groups[6], counts[6];
    size_t ng = fp_group_i64(input, groups, counts, 6);

    int64_t checks[] = {1, 5, -3, 10};
    bool all_pos = fp_reduce_and_bool(checks, 4);

    return 0;
}
```

Compile with:

```bash
gcc your_program.c fp_core_*.o -o your_program.exe
```

## Repository Layout

* `bin/` – demo, benchmark, and regression executables
* `build/obj/` – NASM outputs ready for linking
* `docs/` – user guides, API deep dives, verification reports, and generated HTML
* `include/` – public headers (`fp_core.h`, `fp.h`)
* `logs/`, `scripts/`, `src/asm/`, `src/c/` – build tooling, sources, and tests

## Performance Snapshot

| Metric | Value |
| --- | --- |
| Operations | 36 |
| Assembly modules | 10 (~4,800 LOC) |
| Object size | ~27 KB |
| FP completeness | 100 % |
| Speedup vs GCC `-O3` | 1.0–4.0× |
| Types | `int64_t`, `double` |
| ISA | AVX2 |

## Next Steps

Jump to [[Roadmap]] for milestone planning or [[Publishing Tips]] if you are ready to synchronize this content to GitHub's hosted wiki.
