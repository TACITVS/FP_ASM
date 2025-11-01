# Core API (Modules 1–10)

Return to [[Home]] or explore [[API – Advanced Algorithms]].

Each module groups related functional kernels. All routines follow the Microsoft x64 calling convention and export C-friendly symbols.

## Category 1 – Simple Folds (Module 1)

- `fp_reduce_add_i64(const int64_t* in, size_t n)` sums `n` signed 64-bit integers and returns the total.
- `fp_reduce_add_f64(const double* in, size_t n)` sums `n` doubles with AVX2 reduction.
- `fp_reduce_max_i64(const int64_t* in, size_t n)` returns the maximum integer found in the input span.
- `fp_reduce_max_f64(const double* in, size_t n)` returns the maximum double in the buffer.

## Category 2 – Fused Folds (Module 2)

- `fp_fold_sumsq_i64(const int64_t* in, size_t n)` fuses squaring with accumulation to produce a sum of squares in one pass.
- `fp_fold_dotp_i64(const int64_t* a, const int64_t* b, size_t n)` multiplies and accumulates integer pairs for a dot product.
- `fp_fold_dotp_f64(const double* a, const double* b, size_t n)` is the floating-point dot product using FMA on AVX2 hardware.
- `fp_fold_sad_i64(const int64_t* a, const int64_t* b, size_t n)` sums absolute differences between two integer arrays.

## Category 3 – Fused Maps (Module 3)

- `fp_map_axpy_f64(const double* x, const double* y, double* out, size_t n, double c)` evaluates `out[i] = c * x[i] + y[i]` with AVX2 FMA.
- `fp_map_axpy_i64(const int64_t* x, const int64_t* y, int64_t* out, size_t n, int64_t c)` performs the integer AXPY analogue with scalar unrolling.
- `fp_map_scale_i64(const int64_t* in, int64_t* out, size_t n, int64_t c)` multiplies each integer by `c` using unrolled scalar loops.
- `fp_map_scale_f64(const double* in, double* out, size_t n, double c)` scales doubles with guaranteed SIMD coverage.
- `fp_map_offset_i64(const int64_t* in, int64_t* out, size_t n, int64_t c)` adds a constant to each integer element.
- `fp_map_offset_f64(const double* in, double* out, size_t n, double c)` adds `c` to each double in SIMD lanes.
- `fp_zip_add_i64(const int64_t* a, const int64_t* b, int64_t* out, size_t n)` sums two integer arrays element-wise.
- `fp_zip_add_f64(const double* a, const double* b, double* out, size_t n)` performs the floating-point zip-and-add variant.

## Category 4 – Simple Maps (Module 4)

- `fp_map_abs_i64(const int64_t* in, int64_t* out, size_t n)` writes absolute values using bit tricks for integers.
- `fp_map_abs_f64(const double* in, double* out, size_t n)` applies absolute-value masks to doubles.
- `fp_map_sqrt_f64(const double* in, double* out, size_t n)` computes vectorized square roots for each element.
- `fp_map_clamp_i64(const int64_t* in, int64_t* out, size_t n, int64_t min_val, int64_t max_val)` clamps integers to `[min_val, max_val]` via scalar logic.
- `fp_map_clamp_f64(const double* in, double* out, size_t n, double min_val, double max_val)` clamps doubles with SIMD compare/min/max sequences.

## Category 5 – Scans (Module 5)

- `fp_scan_add_i64(const int64_t* in, int64_t* out, size_t n)` emits the inclusive prefix sum over integers with unrolled scalar loops.
- `fp_scan_add_f64(const double* in, double* out, size_t n)` produces the inclusive prefix sum of doubles.

## Category 6 – Predicates (Module 6)

- `fp_pred_all_eq_const_i64(const int64_t* arr, size_t n, int64_t value)` returns `true` only if every entry equals `value`.
- `fp_pred_any_gt_const_i64(const int64_t* arr, size_t n, int64_t value)` flags whether any element exceeds the threshold.
- `fp_pred_all_gt_zip_i64(const int64_t* a, const int64_t* b, size_t n)` requires all `a[i] > b[i]` comparisons to pass.

## Category 7 – Stream Compaction (Module 7)

- `fp_filter_gt_i64_simple(const int64_t* input, int64_t* output, size_t n, int64_t threshold)` copies values greater than `threshold` and returns the count emitted.
- `fp_partition_gt_i64(const int64_t* input, int64_t* output_pass, int64_t* output_fail, size_t n, int64_t threshold, size_t* out_pass_count, size_t* out_fail_count)` splits elements into “pass” and “fail” buffers and records their sizes.
- `fp_take_while_gt_i64(const int64_t* input, int64_t* output, size_t n, int64_t threshold)` copies prefix elements while the predicate holds, stopping at the first miss.
- `fp_drop_while_gt_i64(const int64_t* input, int64_t* output, size_t n, int64_t threshold)` skips the leading run satisfying the predicate and emits the remainder.

## Category 8 – Essential Operations (Module 8)

### Index-Based

- `fp_take_n_i64(const int64_t* input, int64_t* output, size_t array_len, size_t take_count)` copies the first `take_count` items (bounded by `array_len`) and returns how many were written.
- `fp_drop_n_i64(const int64_t* input, int64_t* output, size_t array_len, size_t drop_count)` skips `drop_count` entries and packs the remainder, returning the output length.
- `fp_slice_i64(const int64_t* input, int64_t* output, size_t array_len, size_t start, size_t end)` copies the half-open range `[start, end)` and reports its length.

### Additional Reductions

- `fp_reduce_product_i64(const int64_t* input, size_t n)` multiplies all integers (returns `1` for empty inputs).
- `fp_reduce_product_f64(const double* input, size_t n)` multiplies all doubles analogously.

### Search

- `fp_find_index_i64(const int64_t* input, size_t n, int64_t target)` returns the index of the first match or `-1` if absent.
- `fp_contains_i64(const int64_t* input, size_t n, int64_t target)` reports whether `target` exists (`true`) or not (`false`).

### Array Manipulation

- `fp_reverse_i64(const int64_t* input, int64_t* output, size_t n)` reverses the array into `output`.
- `fp_concat_i64(const int64_t* input_a, const int64_t* input_b, int64_t* output, size_t len_a, size_t len_b)` concatenates two inputs and returns the combined length.
- `fp_replicate_i64(int64_t* output, size_t n, int64_t value)` fills `output` with `value` repeated `n` times.

## Category 9 – Tier 2 (Module 9)

- `fp_sort_i64(int64_t* array, size_t n)` sorts integers in place using a tuned quicksort/insertion hybrid.
- `fp_sort_f64(double* array, size_t n)` sorts doubles in place with the same strategy.
- `fp_unique_i64(const int64_t* input, int64_t* output, size_t n)` removes consecutive duplicates (expects sorted input) and returns the unique count.
- `fp_union_i64(const int64_t* array_a, const int64_t* array_b, int64_t* output, size_t len_a, size_t len_b)` merges two sorted sets to form their union, returning its size.
- `fp_intersect_i64(const int64_t* array_a, const int64_t* array_b, int64_t* output, size_t len_a, size_t len_b)` computes the intersection of sorted inputs, returning the number of matches.

## Category 10 – Tier 3 (Module 10)

### Grouping & Encoding

- `fp_group_i64(const int64_t* input, int64_t* groups_out, int64_t* counts_out, size_t n)` groups consecutive equal values, filling parallel arrays and returning the number of groups.
- `fp_run_length_encode_i64(const int64_t* input, int64_t* output, size_t n)` emits `[value, count]` pairs for each run and returns twice the group count.

### Sequence Generation

- `fp_iterate_add_i64(int64_t* output, size_t n, int64_t start, int64_t step)` creates an arithmetic progression of length `n`.
- `fp_iterate_mul_i64(int64_t* output, size_t n, int64_t start, int64_t factor)` builds a geometric progression.
- `fp_range_i64(int64_t* output, int64_t start, int64_t end)` writes the range `[start, end)` and returns the number of elements.

### Boolean Reductions & Utilities

- `fp_reduce_and_bool(const int64_t* input, size_t n)` tests whether every value is non-zero (logical AND).
- `fp_reduce_or_bool(const int64_t* input, size_t n)` tests whether any value is non-zero (logical OR).
- `fp_zip_with_index_i64(const int64_t* input, int64_t* output, size_t n)` interleaves indices with values (`[0, x0, 1, x1, …]`) and returns the output length `2n`.
- `fp_replicate_f64(double* output, size_t n, double value)` broadcasts `value` across `n` doubles.
- `fp_count_i64(const int64_t* input, size_t n, int64_t target)` counts how many entries equal `target`.

Looking for higher-order helpers? Visit [[Generic Functional Interface]].
