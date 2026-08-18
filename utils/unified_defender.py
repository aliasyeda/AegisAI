

# unified_defender.py
import os
import glob
import joblib
import json
import pandas as pd
import numpy as np
from typing import Optional
import warnings

# optional imports (shap/xgboost). We'll import lazily and handle missing packages.
try:
    import xgboost as xgb
    from xgboost import XGBClassifier
except Exception:
    xgb = None
    XGBClassifier = None

try:
    import shap
except Exception:
    shap = None

from sklearn.preprocessing import StandardScaler

class UnifiedDefender:
    """
    UnifiedDefender: loads models/artifacts from a models/ folder and exposes:
      - predict(threat_name, df): returns DataFrame with predictions, probs, defense_action, text, top_contributing_features
      - get_combined_log(): reads saved defense CSVs and returns combined DataFrame
    """

    def __init__(self, models_path: str = "models", default_thresholds=None):
        self.models_path = models_path
        os.makedirs(self.models_path, exist_ok=True)

        # default thresholds for defender actions (can be tuned)
        # block if prob >= block, quarantine if >= quarantine, monitor else allow
        self.thresholds = default_thresholds or {"block": 0.7, "quarantine": 0.4, "monitor": 0.2}



        # storage for loaded artifacts
        self.models = {}          # threat -> model object
        self.scalers = {}         # threat -> scaler
        self.encoders = {}        # threat -> label encoder / dict of encoders
        self.vectorizers = {}     # threat -> tfidf vectorizer (for text)
        self._load_available_artifacts()

    # -------------------------
    # helper artifact loading
    # -------------------------
    def _artifact_path(self, threat, suffix):
        return os.path.join(self.models_path, f"{threat}_{suffix}")

    def _find_file(self, pattern):
        files = glob.glob(pattern)
        return files[0] if files else None

    def _load_xgb_from_json(self, json_path):
        """
        If only XGBoost JSON exists, try wrapping into an XGBClassifier object and return it.
        Returns None if unable.
        """
        if xgb is None or XGBClassifier is None:
            return None
        try:
            booster = xgb.Booster()
            booster.load_model(json_path)
            clf = XGBClassifier()
            clf._Booster = booster
            clf._le = None
            return clf
        except Exception:
            return None

    def _load_available_artifacts(self):
        """
        Search models/ folder for *_xgboost_model.pkl, *_xgb.json, *_scaler.joblib, *_tfidf_vectorizer.pkl, *_label_encoders.joblib
        """
        for f in os.listdir(self.models_path):
            fname = os.path.basename(f)
            # parse threat prefix e.g., spam_xgboost_model.pkl
            parts = fname.split("_")
            if len(parts) < 2:
                continue
            threat = parts[0]
            full = os.path.join(self.models_path, fname)

            try:
                if fname.endswith("_xgboost_model.pkl") or fname.endswith("_xgboost_model.joblib") or fname.endswith("_xgboost_model.pkl"):
                    # load model
                    try:
                        self.models[threat] = joblib.load(full)
                    except Exception:
                        # try xgboost Booster load fallback
                        if xgb:
                            booster = xgb.Booster()
                            booster.load_model(full)
                            clf = XGBClassifier()
                            clf._Booster = booster
                            clf._le = None
                            self.models[threat] = clf
                elif fname.endswith("_xgb.json") or fname.endswith("_xgb.json") or fname.endswith("_xgb.json") or fname.endswith("_xgb.json"):
                    # some outputs named *_xgb.json or *_xgb.json or *_xgb.json
                    if threat not in self.models:
                        mdl = self._load_xgb_from_json(full)
                        if mdl is not None:
                            self.models[threat] = mdl
                elif fname.endswith("_xgb.json") or fname.endswith("_xgb.json"):
                    pass
            except Exception:
                # continue; keep scanning other artifacts
                pass

        # load scalers, vectorizers, encoders (joblib/pkl)
        for threat in set([f.split("_")[0] for f in os.listdir(self.models_path) if "_" in f]):
            # scaler
            candidate = self._find_file(os.path.join(self.models_path, f"{threat}_scaler.*"))
            if candidate:
                try:
                    self.scalers[threat] = joblib.load(candidate)
                except Exception:
                    pass

            # vectorizer (tfidf)
            candidate = self._find_file(os.path.join(self.models_path, f"{threat}_tfidf_vectorizer.*"))
            if candidate:
                try:
                    self.vectorizers[threat] = joblib.load(candidate)
                except Exception:
                    pass

            # label encoders or other encoders
            candidate = self._find_file(os.path.join(self.models_path, f"{threat}_label_encoders.*"))
            if candidate:
                try:
                    self.encoders[threat] = joblib.load(candidate)
                except Exception:
                    pass

        # if nothing found, that's fine - we will error gently later
        return

    # -------------------------
    # prediction + defense
    # -------------------------
    def _defense_decision(self, prob: float):
        """
        Map probability -> defense_action
        """
        if prob >= self.thresholds["block"]:
            return "block_ip"
        if prob >= self.thresholds["quarantine"]:
            return "quarantine"
        if prob >= self.thresholds["monitor"]:
            return "monitor"
        return "allow"

    def _model_predict_proba(self, model, X):
        """
        Return probability for positive class. Works for sklearn/xgboost/Keras-like models.
        """
        try:
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(X)
                # if binary, proba[:,1] is positive class
                if proba.ndim == 2 and proba.shape[1] >= 2:
                    return np.array(proba)[:, 1]
                # fallback to first column
                return np.array(proba)[:, 0]
            if hasattr(model, "predict"):
                preds = model.predict(X)
                # if predictions in [0,1] and are probabilities
                if np.issubdtype(np.array(preds).dtype, np.floating):
                    return np.array(preds)
                # else map ints to floats
                return np.array(preds).astype(float)
        except Exception:
            pass
        # final fallback: try booster.predict if xgboost booster present
        try:
            if xgb and isinstance(model, xgb.Booster):
                dmat = xgb.DMatrix(X)
                return model.predict(dmat)
        except Exception:
            pass
        # fallback zeros
        return np.zeros((X.shape[0],))

    def predict(self, threat_name: str, df_input: pd.DataFrame) -> pd.DataFrame:
        """
        threat_name: e.g., "spam","phishing","ddos","malware","iot","password"
        df_input: if text-based threat, single-column DataFrame with 'text' or 0 column
                  if numeric, DataFrame of features (already prepared)
        returns: DataFrame with columns ['index','predicted_label','prediction_prob','defense_action','text','top_contributing_features']
        """
        threat = threat_name.lower()
        model = self.models.get(threat)
        scaler = self.scalers.get(threat)
        vectorizer = self.vectorizers.get(threat)

        # Create output DF skeleton
        results = []
        df = df_input.copy().reset_index(drop=True)

        # normalize text column name if present
        text_col = None
        for possible in ["text", "text_sample", 0, "raw_text", "message"]:
            if possible in df.columns:
                text_col = possible
                break
        if text_col is None:
            # if single-column df (unnamed)
            if df.shape[1] == 1:
                text_col = df.columns[0]
            else:
                # no text column; we'll attempt to predict on numeric features
                text_col = None

        # Prepare X for model
        if text_col is not None and vectorizer is not None:
            # text pipeline
            texts = df[text_col].astype(str).fillna("").tolist()
            try:
                X_feat = vectorizer.transform(texts)
            except Exception:
                # vectorizer may not accept raw types; coerce to strings
                X_feat = vectorizer.transform([str(t) for t in texts])

            probs = None
            if model is not None:
                try:
                    probs = self._model_predict_proba(model, X_feat)
                except Exception:
                    probs = np.zeros((len(texts),))
            else:
                probs = np.zeros((len(texts),))

            # SHAP: compute per-sample top features if shap and model available
            top_features_list = ["" for _ in range(len(texts))]
            if shap is not None and model is not None:
                try:
                    # TreeExplainer works for tree models and returns shap_values array
                    explainer = shap.TreeExplainer(model)
                    shap_vals = explainer.shap_values(X_feat)
                    # shap_vals shape can vary; try to handle 2D arrays
                    # for binary classification shap_vals may be (n_samples, n_features) or list
                    if isinstance(shap_vals, list):
                        # take the last (or second) if returned list
                        arr = shap_vals[-1]
                    else:
                        arr = shap_vals
                    # arr should be 2D (n_samples, n_features)
                    feature_names = np.array(vectorizer.get_feature_names_out())
                    for i in range(min(len(texts), arr.shape[0])):
                        row = arr[i]
                        # row might be sparse or dense
                        if hasattr(row, "toarray"):
                            row = row.toarray().ravel()
                        # get top indices by absolute contribution
                        idxs = np.argsort(np.abs(row))[-10:][::-1]
                        top_names = feature_names[idxs]
                        top_vals = row[idxs]
                        pairs = [f"{n} ({float(np.round(v,4))})" for n, v in zip(top_names, top_vals)]
                        top_features_list[i] = ", ".join(pairs)
                except Exception:
                    # if SHAP fails, leave blank
                    top_features_list = ["" for _ in range(len(texts))]

            # build results rows
            for i, t in enumerate(texts):
                prob = float(probs[i]) if hasattr(probs, "__len__") else float(probs)
                action = self._defense_decision(prob)
                label = int(round(prob)) if prob <= 1.0 else int(prob)
                results.append({
                    "index": i,
                    "predicted_label": label,
                    "prediction_prob": prob,
                    "defense_action": action,
                    "text": t,
                    "top_contributing_features": top_features_list[i]
                })

        else:
            # numeric/features pipeline
            # assume df contains numeric features appropriate for the model
            X_numeric = df.select_dtypes(include=[np.number]).values
            if scaler is not None and hasattr(scaler, "transform"):
                try:
                    X_scaled = scaler.transform(X_numeric)
                except Exception:
                    X_scaled = X_numeric
            else:
                X_scaled = X_numeric

            if model is not None:
                probs = self._model_predict_proba(model, X_scaled)
            else:
                probs = np.zeros((X_scaled.shape[0],))

            # shap for numeric: if vectorizer not relevant, try shap on numeric model
            top_features_list = ["" for _ in range(len(probs))]
            if shap is not None and model is not None:
                try:
                    explainer = shap.TreeExplainer(model)
                    shap_vals = explainer.shap_values(X_scaled)
                    if isinstance(shap_vals, list):
                        arr = shap_vals[-1]
                    else:
                        arr = shap_vals
                    # feature names from df numeric
                    feature_names = df.select_dtypes(include=[np.number]).columns.to_numpy()
                    for i in range(min(len(probs), arr.shape[0])):
                        row = arr[i]
                        if hasattr(row, "toarray"):
                            row = row.toarray().ravel()
                        idxs = np.argsort(np.abs(row))[-10:][::-1]
                        top_names = feature_names[idxs]
                        top_vals = row[idxs]
                        pairs = [f"{n} ({float(np.round(v,4))})" for n, v in zip(top_names, top_vals)]
                        top_features_list[i] = ", ".join(pairs)
                except Exception:
                    top_features_list = ["" for _ in range(len(probs))]

            # create results
            for i in range(len(probs)):
                prob = float(probs[i]) if hasattr(probs, "__len__") else float(probs)
                action = self._defense_decision(prob)
                label = int(round(prob)) if prob <= 1.0 else int(prob)
                results.append({
                    "index": i,
                    "predicted_label": label,
                    "prediction_prob": prob,
                    "defense_action": action,
                    "text": str(df.iloc[i].to_dict()),
                    "top_contributing_features": top_features_list[i]
                })

        out = pd.DataFrame(results)
        # Save per-threat defense results for later aggregation
        try:
            os.makedirs(self.models_path, exist_ok=True)
            out_path = os.path.join(self.models_path, f"{threat}_defense_results.csv")
            out.to_csv(out_path, index=False)
        except Exception:
            pass

        return out

    # -------------------------
    # log aggregation
    # -------------------------
    def get_combined_log(self) -> pd.DataFrame:
        """
        Read all *_defense_results.csv in models/ and combine them into a single df with column 'threat'
        """
        paths = glob.glob(os.path.join(self.models_path, "*_defense_results.csv"))
        dfs = []
        for p in paths:
            try:
                df = pd.read_csv(p)
                # infer threat name
                base = os.path.basename(p)
                threat = base.split("_")[0]
                df["threat"] = threat
                # ensure consistent columns
                if "text" not in df.columns:
                    # try 'text_sample' or fall back to index
                    if "text_sample" in df.columns:
                        df = df.rename(columns={"text_sample": "text"})
                    else:
                        df["text"] = df.apply(lambda r: "", axis=1)
                dfs.append(df)
            except Exception:
                continue
        if dfs:
            combined = pd.concat(dfs, ignore_index=True)
            return combined
        return pd.DataFrame(columns=["threat", "index", "predicted_label", "prediction_prob", "defense_action", "text", "top_contributing_features"])
