#!/usr/bin/env python3
"""Produce placeholder figures and CSVs used by the article.

Outputs:
  - out/fig_energy.png
  - out/fig_localization.png
  - out/spectrum.csv
"""
import csv, math
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    outdir = Path("out")
    outdir.mkdir(exist_ok=True)
    # spectrum
    spec_path = outdir / "spectrum.csv"
    with spec_path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["k", "lambda_k"])
        for k in range(1, 101):
            lam = 1.0 + 0.5*math.sin(0.1*k) + 0.1/k
            w.writerow([k, f"{lam:.8f}"])
    # figure 1
    xs = [i/100.0 for i in range(0, 1000)]
    ys = [math.exp(-((x-5.0)**2)/2.0) for x in xs]
    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("Energy density (toy)")
    plt.title("Toy energy profile")
    plt.tight_layout()
    plt.savefig(outdir / "fig_energy.png", dpi=200)
    plt.close()
    # figure 2
    xs = [i/50.0 for i in range(-200, 201)]
    ys = [math.exp(-(x**2)/2.0) * (1.0/(1.0+x*x)) for x in xs]
    plt.figure()
    plt.plot(xs, ys)
    plt.xlabel("x")
    plt.ylabel("Localized kernel (toy)")
    plt.title("Toy localization")
    plt.tight_layout()
    plt.savefig(outdir / "fig_localization.png", dpi=200)
    plt.close()

if __name__ == "__main__":
    main()
