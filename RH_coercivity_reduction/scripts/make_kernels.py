
#!/usr/bin/env python3
import os, json
import numpy as np, pandas as pd

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

params = {}
pp = os.path.join(ROOT, "params.json")
if os.path.exists(pp):
    params = json.load(open(pp, "r"))
Xi0  = float(params.get("Xi0", 16.0))
c0   = float(params.get("c0", 0.5))
Lstar= float(params.get("Lstar", 0.0))

xi = np.linspace(-64.0, 64.0, 4097)
Khat = Lstar + c0 * (xi**2)/(xi**2 + Xi0**2)

out = os.path.join(DATA, "kernel_profile.csv")
pd.DataFrame({"xi": xi, "Khat": Khat}).to_csv(out, index=False)
print("[make_kernels] wrote", out)
