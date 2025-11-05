# backend/utils.py
from __future__ import annotations
from pathlib import Path
import typing as t
import pandas as pd
import joblib
import pickle

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "model_saved"

_cache: dict[str, t.Any] = {}

def _file(name: str) -> Path:
    p = DATA_DIR / name
    if not p.exists():
        raise FileNotFoundError(f"Missing required file: {p}")
    return p

def _smart_load(path: Path):
    """
    Prefer joblib (how your artifacts were saved), fall back to pickle.
    This avoids `_pickle.UnpicklingError: STACK_GLOBAL requires str`.
    """
    # Try joblib first
    try:
        return joblib.load(path)
    except Exception as e_joblib:
        # Fallback to raw pickle
        try:
            with open(path, "rb") as f:
                return pickle.load(f)
        except Exception as e_pickle:
            raise RuntimeError(
                f"Failed to load {path.name} with joblib ({e_joblib}) and pickle ({e_pickle})."
            )

def load_pickle(name: str):
    """Cache-aware loader using _smart_load under the hood."""
    if name in _cache:
        return _cache[name]
    obj = _smart_load(_file(name))
    _cache[name] = obj
    return obj

def load_scaler():
    return load_pickle("scaler.pkl")

def load_selector():
    return load_pickle("feature_selector.pkl")

def load_model():
    return load_pickle("lr_model.pkl")

def try_load_feature_names_from_csv() -> list[str] | None:
    csv_path = _file("selected_features1.csv")
    try:
        df = pd.read_csv(csv_path)
        if df.shape[1] == 1:
            return df.iloc[:, 0].astype(str).tolist()
        return list(df.columns)
    except Exception:
        return None
