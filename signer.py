#!/usr/bin/env python3
"""Signe catalogue-contrats.json et ecrit manifeste.json.

La cle privee reste hors du depot : ~/Developer/.cles/aloiconseil-catalogue-signing.key
Usage : python3 signer.py [chemin-de-la-cle]
"""
import base64, hashlib, json, os, sys
from cryptography.hazmat.primitives import serialization

ici = os.path.dirname(os.path.abspath(__file__))
cle = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ici, "..", ".cles", "aloiconseil-catalogue-signing.key")
fichier = open(os.path.join(ici, "catalogue-contrats.json"), "rb").read()
cat = json.loads(fichier)
empreinte = hashlib.sha256(fichier).hexdigest()
k = serialization.load_pem_private_key(open(cle, "rb").read(), None)
signature = base64.b64encode(k.sign(empreinte.encode())).decode()
manifeste = {
    "catalogVersion": cat.get("catalogVersion") or str(cat.get("version")),
    "dataUpdatedAt": cat.get("dataUpdatedAt") or "",
    "sha256": empreinte,
    "signature": signature,
    "url": "https://kanjalex-dev.github.io/aloiconseil-catalogue/catalogue-contrats.json",
}
json.dump(manifeste, open(os.path.join(ici, "manifeste.json"), "w"), indent=1, ensure_ascii=False)
print("manifeste.json :", manifeste["catalogVersion"], empreinte[:12])
