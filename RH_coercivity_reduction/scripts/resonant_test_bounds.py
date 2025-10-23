"""
Resonant test bounds for Q given a hypothetical off-line zero.
We model the "bump" induced by an off-line zero at ±2γ by a negative Gaussian
in the spectral kernel and study when the quadratic form becomes negative on
resonant packets.

Model:
  K_eff(ξ) = Khat(ξ) + Zhat(ξ; γ, amp, sigma_z)
  Zhat(ξ)  = -amp * [exp(-((ξ-2γ)^2)/(2σ_z^2)) + exp(-((ξ+2γ)^2)/(2σ_z^2))]

Resonant packet (Fourier side of the test function):
  Â(ξ; γ, R, σ_a) = exp(-((ξ-2γ)^2)/(2σ_a^2)) + exp(-((ξ+2γ)^2)/(2σ_a^2)),
  where σ_a = 1/R (narrowing with R).

We compute:
  Q(γ,R,amp) = (1/2π) ∫ K_eff(ξ) |Â(ξ)|^2 dξ  (Riemann sum on provided grid)

Outputs:
  - resonant_Q_scan.csv        : grid of (gamma, R, amp, Q)
  - resonant_amp_threshold.csv : minimal amp making Q<0 for each (gamma,R)
  - resonant_summary.json      : min Q observed and the argmin
"""
import os, json, math
from pathlib import Path
import numpy as np, pandas as pd

def load_kernel_profile(root: Path):
    # Try several locations
    candidates = [
        root/"kernel_profile.csv",
        root/"data"/"kernel_profile.csv",
        root.parent/"data"/"kernel_profile.csv"
    ]
    for c in candidates:
        if c.exists():
            df = pd.read_csv(c)
            xi = df["xi"].to_numpy(float)
            Khat = df["Khat"].to_numpy(float)
            dxi = float(xi[1] - xi[0])
            return xi, Khat, dxi
    raise FileNotFoundError("kernel_profile.csv not found in expected locations.")

def gaussian(x, mu, s):
    return np.exp(-0.5*((x-mu)/s)**2)

def Ahat(xi, gamma, R):
    sigma_a = 1.0 / max(R, 1e-6)
    return gaussian(xi,  2.0*gamma, sigma_a) + gaussian(xi, -2.0*gamma, sigma_a)

def Zhat(xi, gamma, amp, sigma_z):
    return -amp * ( gaussian(xi,  2.0*gamma, sigma_z) + gaussian(xi, -2.0*gamma, sigma_z) )

def Q_value(xi, Khat_eff, Ahat_vec, dxi):
    return (1.0/(2.0*math.pi)) * float(np.sum(Khat_eff * (np.abs(Ahat_vec)**2)) * dxi)

def main():
    here = Path(__file__).resolve().parent
    root = here  # data expected alongside script by default

    # params
    params = {}
    for pp in [root/"params.json", root.parent/"params.json", Path("/mnt/data")/"params.json"]:
        if pp.exists():
            try:
                params = json.load(open(pp,"r",encoding="utf-8"))
                break
            except Exception:
                pass

    xi, Khat, dxi = load_kernel_profile(root)

    # scan configuration
    gammas = params.get("res_gammas", [4.0, 6.0, 8.0, 12.0, 16.0])
    Rs     = params.get("res_Rs",     [2.0, 4.0, 8.0, 12.0, 16.0, 24.0, 32.0])
    sigma_z= float(params.get("res_sigma_z", 0.75))
    amp_list = params.get("res_amp_list", [0.0, 0.05, 0.1, 0.2, 0.3])

    rows = []
    thr_rows = []  # thresholds per (gamma,R)

    for gamma in gammas:
        for R in Rs:
            A = Ahat(xi, gamma, R)
            Q0 = Q_value(xi, Khat, A, dxi)
            # bump contribution: linear in amp
            Z_unit = Zhat(xi, gamma, 1.0, sigma_z)
            Qb = Q_value(xi, Khat + Z_unit, A, dxi) - Q0  # effect of amp=1
            # if Qb < 0, we can find amp* = Q0 / (-Qb) to flip sign
            amp_star = float(Q0 / (-Qb)) if Qb < 0 else float("inf")
            thr_rows.append({"gamma":gamma, "R":R, "Q0":Q0, "Qb_unit":Qb, "amp_threshold": amp_star})

            for amp in amp_list:
                K_eff = Khat + Zhat(xi, gamma, amp, sigma_z)
                Q = Q_value(xi, K_eff, A, dxi)
                rows.append({"gamma":gamma, "R":R, "amp":amp, "Q":Q})

    df = pd.DataFrame(rows)
    thr = pd.DataFrame(thr_rows)

    out1 = root/"resonant_Q_scan.csv"
    out2 = root/"resonant_amp_threshold.csv"
    df.to_csv(out1, index=False)
    thr.to_csv(out2, index=False)

    # summary
    idxmin = int(df["Q"].idxmin())
    summary = {
        "min_Q": float(df.loc[idxmin,"Q"]),
        "at": {
            "gamma": float(df.loc[idxmin,"gamma"]),
            "R": float(df.loc[idxmin,"R"]),
            "amp": float(df.loc[idxmin,"amp"]),
        },
        "sigma_z": sigma_z,
        "notes": [
            "This is a model-based negative bump; amp encodes the hypothetical off-line zero strength.",
            "If amp_threshold is small across (gamma,R), resonance is an efficient detector."
        ]
    }
    out3 = root/"resonant_summary.json"
    json.dump(summary, open(out3, "w"), indent=2)

    print("[resonant_test_bounds] wrote:", out1, out2, out3)
    print("[resonant_test_bounds] min Q ~", summary["min_Q"], "at", summary["at"])

if __name__ == "__main__":
    main()