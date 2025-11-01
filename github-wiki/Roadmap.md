# Roadmap: Toward a Fully FP-Ethos Assembly Library

Check [[Home]] for context or [[Publishing Tips]] to put this plan live on GitHub.

## Near-Term Milestones

1. **System V ABI Port** – Rework prologues/epilogues and calling conventions so every kernel exports cleanly on Linux and other UNIX-like systems while preserving the FP-first API.
2. **Foundation Utilities (Weeks 1–2)** – Add reusable building blocks such as enhanced matrix math, sliding-window helpers, and generalized distance metrics to unlock higher-level features.
3. **Tier A Algorithms (Weeks 3–8)**
   - Statistical suite hardening and extensions
   - Financial analytics kernels (windowed indicators, risk metrics)
   - Machine-learning primitives (K-means, KNN, gradient-based optimizers)
   - Signal-processing operators (convolution, correlation, peak detection)
4. **Tier B Algorithms (Weeks 9–11)** – Numerical methods (integration, roots, polynomial ops, matrix routines) and data-quality tools (hashing, profiling, dedupe, validation, anomaly detection).
5. **Stabilization (Week 12)** – Comprehensive verification, benchmarking against established C/NumPy/SciPy stacks, enriched documentation, and scenario demos.

## Vision

Deliver a complete, FP-ethos-compliant x86-64 assembly library whose entire API is callable from C and—after the port—both Microsoft and System V ABIs, covering advanced analytics domains with the same functional-programming ergonomics already achieved in the core library.
