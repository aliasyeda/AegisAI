# convert_json_to_pkl.py
import os, glob, joblib
import xgboost as xgb
from xgboost import XGBClassifier

MODELS_DIR = "models"

def convert_json_to_pkl(models_dir=MODELS_DIR):
    os.makedirs(models_dir, exist_ok=True)
    json_files = glob.glob(os.path.join(models_dir, "*_xgb.json")) + glob.glob(os.path.join(models_dir, "*_xgb.JSON")) + glob.glob(os.path.join(models_dir, "*_xgb.*json"))
    for j in json_files:
        base = os.path.basename(j)
        prefix = base.split("_")[0]
        pkl_target = os.path.join(models_dir, f"{prefix}_xgboost_model.pkl")
        try:
            booster = xgb.Booster()
            booster.load_model(j)
            clf = XGBClassifier()
            clf._Booster = booster
            clf._le = None
            joblib.dump(clf, pkl_target)
            print(f"Converted {j} -> {pkl_target}")
        except Exception as e:
            print(f"Failed to convert {j}: {e}")

if __name__ == "__main__":
    convert_json_to_pkl()
