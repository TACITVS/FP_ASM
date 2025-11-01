# Callback-Oriented Helpers

The lightweight `fp.h` header provides higher-order wrappers for rapid prototyping alongside specialized fast paths.

- `fp_map_i64(const int64_t* in, int64_t* out, size_t n, fp_unary_i64 f)` applies user-supplied unary callbacks across `n` integers.
- `fp_reduce_i64(const int64_t* a, size_t n, int64_t init, fp_binary_i64 op)` folds integers with a custom binary operator, starting from `init`.
- `fp_map_square_i64(const int64_t* in, int64_t* out, size_t n)` offers a specialized callback-free squaring path.
- `fp_reduce_add_i64(const int64_t* a, size_t n, int64_t init)` sums integers while honoring an initial accumulator (distinct from the zero-init core variant).
- `fp_foldmap_sumsq_i64(const int64_t* in, size_t n, int64_t init)` performs a fused square-and-sum with an initial bias term.
