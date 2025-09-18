
#!/usr/bin/env python3
import os, hashlib, pathlib

HERE = os.path.dirname(__file__)
ROOT = os.path.abspath(os.path.join(HERE, ".."))
targets = [os.path.join(ROOT, "data"), os.path.join(ROOT, "figures")]
hashes = []
for tgt in targets:
    if os.path.isdir(tgt):
        for p in sorted(pathlib.Path(tgt).rglob("*")):
            if p.is_file():
                h = hashlib.sha256(p.read_bytes()).hexdigest()
                rel = str(p.relative_to(ROOT))
                hashes.append(f"{h}  {rel}")
out = os.path.join(ROOT, "hashes.sha256")
with open(out, "a", encoding="utf-8") as f:
    f.write("\n".join(hashes) + ("\n" if hashes else ""))
print("[update_hashes] appended hashes for data/ and figures/")
