# Supplementary Note — Mapping code/data to the article

**Goal.** Link every data artifact to a specific statement/figure in the paper.

- **(IU) Inequality (coercivity):** `kernel_profile.csv` → kernel definition; `IU_check_random.csv` + `IU_stats.json` → stochastic verification (Section: Coercivité unique).  
- **Local Archimedean bounds (H_loc):** `Hloc_constants_exact.csv` + `H_baseline_scan.csv` → numerical envelopes for \widehat H_{{η,σ}} (Section: Bornes archimédiennes & base-line).  
- **Resonant test:** `Qeta_heatmap_min.csv` / `Qeta_lines_eta_R2.csv` → empirical trends showing how resonant packets break coercivity if an off-line zero existed (Section: Test résonant).  
- **Figures (illustrative):** `spectrum.csv`, `fig_energy.png`, `fig_localization.png` (Annexes/illustrations).

**Machine precision remark.** Margins at the level 1e-16…1e-12 should be interpreted as numerical noise, not genuine violations.

**Reproducibility.** The files are hashed via `update_hashes.py` (SHA-256) for integrity tracking.
