# Advanced Algorithms (Module 11)

Return to [[Home]] or review [[API – Core Modules]].

## Data Structures

- `DescriptiveStats` stores mean, variance, standard deviation, skewness, and kurtosis for a dataset.
- `Quartiles` holds Q1, median (Q2), Q3, and the interquartile range.
- `LinearRegression` captures slope, intercept, R², and standard error for a fitted line.

## Functions

- `fp_descriptive_stats_f64(const double* data, size_t n, DescriptiveStats* stats)` computes all five descriptive moments in a single pass.
- `fp_moments_f64(const double* data, size_t n, double* moments)` emits raw sums, squared sums, cubes, and fourth powers for downstream analytics.
- `fp_percentile_f64(const double* sorted_data, size_t n, double p)` returns the `p`‑th percentile via linear interpolation on sorted input.
- `fp_percentiles_f64(const double* sorted_data, size_t n, const double* p_values, size_t n_percentiles, double* results)` batches percentile lookups for multiple probabilities.
- `fp_quartiles_f64(const double* sorted_data, size_t n, Quartiles* quartiles)` extracts Q1, median, Q3, and IQR together.
- `fp_covariance_f64(const double* x, const double* y, size_t n)` calculates covariance using a fused single-pass algorithm.
- `fp_correlation_f64(const double* x, const double* y, size_t n)` computes Pearson’s correlation coefficient, guarding edge cases (NaN for undefined).
- `fp_linear_regression_f64(const double* x, const double* y, size_t n, LinearRegression* result)` fits `y = mx + b`, calculates R² and standard error, and handles degenerate datasets explicitly.
- `fp_predict_f64(double x_value, const LinearRegression* model)` evaluates a fitted model at `x_value`.
- `fp_detect_outliers_zscore_f64(const double* data, size_t n, double threshold, uint8_t* is_outlier)` marks points whose Z-score exceeds `threshold` in a two-pass analysis.
- `fp_detect_outliers_iqr_f64(const double* sorted_data, size_t n, double k_factor, uint8_t* is_outlier)` labels outliers using the IQR rule on sorted inputs.

Need callback-style wrappers instead? Jump to [[Generic Functional Interface]].
