[![DOI](https://zenodo.org/badge/1059098901.svg)](https://doi.org/10.5281/zenodo.17149032)
# Paquet reproductible PCPI–RH

- Scripts: dossier `scripts/`
- Données: dossier `data/`
- Commandes: voir ci-dessous

## Empreintes
Au moment de l'archivage, les hachages SHA256 des CSV et figures sont listés dans `hashes.sha256`.

## Étapes
1. Préparer l'environnement Python (numpy, mpmath, sympy, pandas).
2. Exécuter `scripts/make_kernels.py` pour générer `Hb_eta_sigma.npy`.
3. Exécuter `scripts/check_IU.py` pour les tests de positivité.
4. Exécuter `scripts/figures.py` pour (re)produire FIG.1–FIG.4.



## Quick reproducibility

```bash
python scripts/make_kernels.py
python scripts/check_IU.py
python scripts/figures.py
```

Artifacts are written under `out/`. After generation, recompute hashes:

```bash
python scripts/update_hashes.py
```
