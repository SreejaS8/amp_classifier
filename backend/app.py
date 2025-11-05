# backend/app.py
from __future__ import annotations
import os
from typing import List, Any, Dict

import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
import protpy  # <- your feature lib

from utils import load_scaler, load_selector, load_model, try_load_feature_names_from_csv

# ---------------------- Config & app ----------------------
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ALLOW_ORIGINS}})

SCALER = load_scaler()
SELECTOR = load_selector()
MODEL = load_model()

# Use the exact training order the scaler was fit on
if hasattr(SCALER, "feature_names_in_"):
    FULL_FEATURE_NAMES: List[str] = SCALER.feature_names_in_.tolist()
else:
    names = try_load_feature_names_from_csv()
    if not names:
        raise RuntimeError(
            "Need feature order: scaler.feature_names_in_ not found and CSV fallback missing."
        )
    FULL_FEATURE_NAMES = names

VALID_AA = set("ACDEFGHIKLMNPQRSTVWY")

# ---------------------- Helpers ----------------------
def clean_seq(s: str) -> str:
    if not isinstance(s, str):
        return ""
    return "".join([aa for aa in s.upper() if aa in VALID_AA])

# Use YOUR exact extractor calls (AAC, DPC, TPC via protpy.*_composition)
def make_features_df(seqs: List[str]) -> pd.DataFrame:
    aac_list, dpc_list, tpc_list = [], [], []

    for seq in seqs:
        # AAC
        aac = protpy.amino_acid_composition(seq)
        aac_list.append(np.array(aac).flatten())

        # DPC
        dpc = protpy.dipeptide_composition(seq)
        dpc_list.append(np.array(dpc).flatten())

        # TPC
        tpc = protpy.tripeptide_composition(seq)
        tpc_list.append(np.array(tpc).flatten())

    aac_df = pd.DataFrame(aac_list).add_prefix("AAC_")
    dpc_df = pd.DataFrame(dpc_list).add_prefix("DPC_")
    tpc_df = pd.DataFrame(tpc_list).add_prefix("TPC_")
    raw_df = pd.concat([aac_df, dpc_df, tpc_df], axis=1)

    # Align to the training feature order; fill missing with 0.0
    X = raw_df.reindex(columns=FULL_FEATURE_NAMES, fill_value=0.0).astype(float)
    return X

def pipeline_predict(cleaned_seqs: List[str]):
    X = make_features_df(cleaned_seqs)
    Xs = SCALER.transform(X)
    Xsel = SELECTOR.transform(Xs)
    preds = MODEL.predict(Xsel)
    probas = MODEL.predict_proba(Xsel) if hasattr(MODEL, "predict_proba") else None
    return preds, probas

# ---------------------- Routes ----------------------
@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "features_in": len(FULL_FEATURE_NAMES),
        "has_proba": hasattr(MODEL, "predict_proba"),
        "allow_origins": ALLOW_ORIGINS
    }), 200

@app.post("/predict")
def predict():
    """
    Body:
      { "seq": "FLPLIL" }
      or
      { "sequences": ["FLPLIL", "ILPWKWPWWP", ...] }
    """
    data = request.get_json(silent=True) or {}

    if "seq" in data:
        raw = [data["seq"]]
        ids = ["Seq1"]
    elif isinstance(data.get("sequences"), list):
        raw = data["sequences"]
        ids = [f"Seq{i+1}" for i in range(len(raw))]
    else:
        return jsonify({"error": "Provide 'seq' (string) or 'sequences' (list of strings)."}), 400

    cleaned = [clean_seq(s) for s in raw]
    if any(len(c) == 0 for c in cleaned):
        return jsonify({"error": "One or more sequences are empty or contain no valid amino acids (ACDEFGHIKLMNPQRSTVWY)."}), 400

    try:
        preds, probas = pipeline_predict(cleaned)
    except Exception as e:
        return jsonify({"error": "Inference failed", "detail": str(e)}), 500

    results = []
    for i, (r, c, y) in enumerate(zip(raw, cleaned, preds)):
        conf = None
        if probas is not None:
            conf = float(np.max(probas[i]))
        results.append({
            "id": ids[i],
            "input": r,
            "cleaned": c,
            "prediction": "AMP" if int(y) == 1 else "Non-AMP",
            "confidence": None if conf is None else round(conf, 4)
        })

    return jsonify({"results": results}), 200

if __name__ == "__main__":
    # Dev only; Render will use gunicorn
    app.run(host="0.0.0.0", port=8000, debug=True)
