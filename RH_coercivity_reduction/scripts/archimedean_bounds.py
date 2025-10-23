"""
Archimedean bounds for Re ψ(1/4 + i ξ/(4π)).
We construct explicit grid-verified constants C_lower, C_upper such that for all sampled ξ:
    Reψ(ξ) >= log|z(ξ)| - C_lower/(1+ξ^2)
    Reψ(ξ) <= log|z(ξ)| + C_upper/(1+ξ^2)
where z(ξ) = 1/4 + i ξ/(4π).
Outputs:
  - arch_bounds_scan.csv : grid values (ξ, Reψ, log_mod_z, resid)
  - arch_bounds_constants.json : constants and grid meta
"""
import os, json, math
from pathlib import Path

import numpy as np
import pandas as pd

try:
    import mpmath as mp
except Exception as e:
    raise SystemExit("mpmath is required: " + str(e))

def re_digamma_of_xi(xi: float) -> float:
    # z = 1/4 + i * xi/(4π)
    z = mp.mpf('0.25') + 1j * (mp.mpf(xi) / (4*mp.pi))
    return float(mp.re(mp.digamma(z)))

def log_mod_z_of_xi(xi: float) -> float:
    # |z| = sqrt( (1/4)^2 + (xi/(4π))^2 )
    val = math.sqrt( (0.25**2) + ( (xi/(4*math.pi))**2 ) )
    return math.log(val)

def main():
    here = Path(__file__).resolve().parent
    root = here  # write beside script by default
    # load optional params.json from BASE or script dir
    params = {}
    for pp in [root/"params.json", Path(root).parent/"params.json", Path("/mnt/data")/"params.json"]:
        if pp.exists():
            try:
                params = json.load(open(pp, "r", encoding="utf-8"))
                break
            except Exception:
                pass

    # grid config
    xi_max = float(params.get("arch_xi_max", 256.0))
    xi_step = float(params.get("arch_xi_step", 0.25))
    xis = np.arange(-xi_max, xi_max + 1e-12, xi_step, dtype=float)

    rows = []
    # compute Reψ and baseline log term
    for xi in xis:
        Repsi = re_digamma_of_xi(xi)
        logz  = log_mod_z_of_xi(xi)
        resid = Repsi - logz
        rows.append((xi, Repsi, logz, resid))

    df = pd.DataFrame(rows, columns=["xi","Repsi","log_mod_z","resid"])
    out_scan = root / "arch_bounds_scan.csv"
    df.to_csv(out_scan, index=False)

    # Find minimal C_lower and C_upper on the grid
    # We want Repsi >= log_mod_z - C/(1+xi^2)  <=> resid >= -C/(1+xi^2)
    # So C_lower >= max_xi ( ( -resid ) * (1+xi^2) )_+
    w = 1.0 + df["xi"].to_numpy()**2
    resid = df["resid"].to_numpy()
    lower_needed = np.maximum(0.0, (-resid) * w).max()
    upper_needed = np.maximum(0.0, ( resid) * w).max()

    consts = {
        "xi_max": xi_max,
        "xi_step": xi_step,
        "grid_points": int(len(df)),
        "C_lower": float(lower_needed),
        "C_upper": float(upper_needed),
        "inequalities": {
            "lower": "Reψ >= log|z| - C_lower/(1+xi^2)",
            "upper": "Reψ <= log|z| + C_upper/(1+xi^2)"
        },
        "notes": [
            "Bounds are grid-verified; increase xi_max / refine xi_step to tighten.",
            "These constants are for the specific archimedean term used in the paper."
        ]
    }
    out_consts = root / "arch_bounds_constants.json"
    json.dump(consts, open(out_consts, "w"), indent=2)
    print("[archimedean_bounds] wrote", out_scan, "and", out_consts)
    print("[archimedean_bounds] C_lower≈", consts["C_lower"], " C_upper≈", consts["C_upper"], " (grid:", len(df), "pts)")

if __name__ == "__main__":
    main()