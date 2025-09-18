
#!/usr/bin/env python3
import os, json
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
pp = os.path.join(ROOT,"params.json")
params = json.load(open(pp)) if os.path.exists(pp) else {}
Xi0  = float(params.get("Xi0", 16.0))
c0   = float(params.get("c0", 0.5))
Lstar= float(params.get("Lstar", 0.0))

ker = pd.read_csv(os.path.join(ROOT,"data","kernel_profile.csv"))
xi = ker["xi"].to_numpy(float)
Khat = ker["Khat"].to_numpy(float)
dxi = xi[1]-xi[0]

def Q_of_Ahat(Ahat):
    return (1.0/(2.0*np.pi))*np.sum(Khat * (np.abs(Ahat)**2)) * dxi

def weighted_grad(Ahat):
    w = (xi**2)/(xi**2 + Xi0**2)
    return np.sum(w * (np.abs(Ahat)**2)) * dxi

def gaussian(mu,s):
    return np.exp(-0.5*((xi-mu)/s)**2)

rng = np.random.default_rng(123)
rows=[]
kappa_bar = c0/(2.0*np.pi)
for i in range(64):
    mu1,mu2 = rng.uniform(-24,24,2)
    s1,s2 = rng.uniform(0.5,2.0,2)
    Ahat = gaussian(mu1,s1) + gaussian(mu2,s2)
    Q = Q_of_Ahat(Ahat)
    RHS = kappa_bar * weighted_grad(Ahat)
    rows.append({"i":i,"Q":Q,"rhs":RHS,"ok":Q>=RHS})
df = pd.DataFrame(rows)
df.to_csv(os.path.join(ROOT,"data","IU_check_random.csv"), index=False)

L = df["Q"].to_numpy(float)
R = df["rhs"].to_numpy(float)
margin = L - R
eps = max(1e-12, 1e-12 * float(np.median(np.abs(R)) or 1.0))
margin_tol = L - (R - eps)

ok_fraction = float((margin >= 0).mean())
min_margin = float(margin.min())
ok_fraction_tol = float((margin_tol >= 0).mean())
min_margin_tol = float(margin_tol.min())

stats = {
  "source_csv":"data/IU_check_random.csv",
  "lhs_col":"Q", "rhs_col":"rhs",
  "ok_fraction": ok_fraction, "min_margin": min_margin,
  "ok_fraction_tol": ok_fraction_tol, "min_margin_tol": min_margin_tol,
  "all_ok": bool(min_margin>=0), "all_ok_tol": bool(min_margin_tol>=0),
  "eps_used": eps,
  "note":"Sanity-check only; not part of the proof."
}
json.dump(stats, open(os.path.join(ROOT,"data","IU_stats.json"),"w"), indent=2)
print("IU exact:   ok_fraction=", ok_fraction, " min_margin=", min_margin)
print("IU toléré:  ok_fraction=", ok_fraction_tol, " min_margin=", min_margin_tol, " eps=", eps)
