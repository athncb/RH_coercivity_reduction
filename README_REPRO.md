# PCPI ⇒ Coercivity of Q_η and Resonant Exclusion — Reproducibility Package

This directory mirrors the *companion code and data* for the published PDF **PCPI ⇒ coercivité de Q_η et exclusion des zéros hors-ligne**.

## Contents
- **Code (user-provided externally):** `make_kernels.py`, `check_IU.py`, `archimedean_bounds.py`, `resonant_test_bounds.py`, `figures.py`, `update_hashes.py`
- **Data & Results (here):**
  - `kernel_profile.csv` — sampled \hat K(ξ) over [-64,64] (4097 pts).
  - `IU_check_random.csv`, `IU_stats.json` — stochastic coercivity checks (Q ≥ κ̄∫w|Â|²).
  - `Hloc_constants_exact.csv`, `H_baseline_scan.csv` — local H_{{η,σ}} bounds & baseline calibration.
  - `Qeta_heatmap_min.csv`, `Qeta_lines_eta_R2.csv` — Q_η minima / resonant slices.
  - `prime_metrics.csv` — primary explicit-formula metrics.
  - `spectrum.csv` — toy spectrum for figure.
  - `iu_report.json` — aggregated (toy) bounds for the ratio R_Q.
  - Images: `fig_energy.png`, `fig_localization.png`.

## One-shot pipeline
1. **Build kernel**  
   ```bash
   python make_kernels.py
   ```
2. **Run coercivity sanity-check**  
   ```bash
   python check_IU.py
   ```
3. **(Optional) Figures & hashes**  
   ```bash
   python figures.py
   python update_hashes.py
   ```

## Parameters
Controlled by `params.json` (defaults shown):
```json
{
  "Xi0": 16.0,
  "c0": 0.5,
  "Lstar": 0.0,
  "eta": 0.2,
  "sigma": 1.0
}
```

## What the numbers show
- `IU_stats.json`: all tests are satisfied within machine tolerance (`ok_fraction_tol=1.0`, `min_margin_tol≈1e-12`).
- `kernel_profile.csv`: \hat K is positive with low-frequency baseline L_* and high-frequency growth c₀ · ξ²/(ξ²+Ξ₀²).
- Heatmaps/lines for Q_η illustrate the expected loss of coercivity under resonant localization (test function g_{{γ,R}}).

**Note.** These computations are *sanity checks* that numerically support the analytic claims; they are not a proof by themselves.

## Citation
If you reuse this package, please cite the published PDF and reference this directory as the companion reproducibility dataset.
