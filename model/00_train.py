import pandas as pd
import numpy as np
import warnings
import re

warnings.filterwarnings("ignore")

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
import xgboost as xgb
import lightgbm as lgb
import joblib

# ─────────────────────────────────────────────
# 1.  VERİ YÜKLEME & TEMİZLEME
# ─────────────────────────────────────────────

def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)

    # Fiyat: sayıya çevir
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    df = df[df["price"] > 0]

    # RAM GB sayısına çevir
    def parse_gb(val):
        if pd.isna(val):
            return np.nan
        m = re.search(r"(\d+)", str(val))
        return float(m.group(1)) if m else np.nan

    df["ram_gb"]     = df["ram"].apply(parse_gb)
    df["storage_gb"] = df["storage"].apply(parse_gb)

    # CPU generation sayıya çevir
    def parse_cpugen(val):
        if pd.isna(val):
            return np.nan
        m = re.search(r"(\d{2})", str(val))
        return float(m.group(1)) if m else np.nan

    df["cpu_gen_num"] = df["cpu_gen"].apply(parse_cpugen)

    # Sayısal serileri çevir
    df["cpu_ryzen_series"]  = pd.to_numeric(df["cpu_ryzen_series"], errors="coerce")
    df["intel_core_series"] = pd.to_numeric(df["intel_core_series"], errors="coerce")
    df["cpu_priority"]      = pd.to_numeric(df["cpu_priority"],      errors="coerce")
    df["gpu_priority"]      = pd.to_numeric(df["gpu_priority"],      errors="coerce")
    df["ram_priority"]      = pd.to_numeric(df["ram_priority"],      errors="coerce")
    df["storage_priority"]  = pd.to_numeric(df["storage_priority"],  errors="coerce")
    df["os_priority"]       = pd.to_numeric(df["os_priority"],       errors="coerce")

    # Kategorik temizlik
    for col in ["extract_cpu_brand", "os", "usage_purpose", "brand"]:
        df[col] = df[col].fillna("unknown").str.strip().str.lower()

    # GPU: NaN → "none"
    df["gpu"] = df["gpu"].fillna("none").str.strip().str.lower()
    df["gpu_has"] = (df["gpu"] != "none").astype(int)

    return df

# ─────────────────────────────────────────────
# 2.  ÖZELLİK MÜHENDİSLİĞİ
# ─────────────────────────────────────────────

PRICE_FEATURES_NUM = [
    "ram_gb", "storage_gb",
    "cpu_priority", "gpu_priority", "ram_priority",
    "storage_priority", "os_priority",
    "cpu_ryzen_series", "intel_core_series", "cpu_gen_num",
    "gpu_has",
]

PRICE_FEATURES_CAT = [
    "extract_cpu_brand", "os", "brand", 
    "usage_purpose"
]

TARGET_PRICE = "price"

def build_preprocessor(num_cols, cat_cols):
    num_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler",  StandardScaler()),
    ])
    cat_pipe = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value="unknown")),
        ("ohe",     OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])
    return ColumnTransformer([
        ("num", num_pipe, num_cols),
        ("cat", cat_pipe, cat_cols),
    ])

# ─────────────────────────────────────────────
# 3.  MODEL TANIMI
# ─────────────────────────────────────────────

def get_models():
    return {
        "Random Forest": RandomForestRegressor(
            n_estimators=300, max_depth=12, min_samples_leaf=3,
            n_jobs=-1, random_state=42
        ),
        "XGBoost": xgb.XGBRegressor(
            n_estimators=400, learning_rate=0.06, max_depth=6,
            subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=1.0,
            n_jobs=-1, random_state=42, verbosity=0
        ),
        "LightGBM": lgb.LGBMRegressor(
            n_estimators=400, learning_rate=0.06, max_depth=7,
            num_leaves=63, subsample=0.8, colsample_bytree=0.8,
            reg_alpha=0.1, reg_lambda=1.0,
            n_jobs=-1, random_state=42, verbose=-1
        ),
    }

# ─────────────────────────────────────────────
# 4.  EĞİTİM & DEĞERLENDİRME
# ─────────────────────────────────────────────

def evaluate(y_true, y_pred, label=""):
    mae   = mean_absolute_error(y_true, y_pred)
    rmse  = np.sqrt(mean_squared_error(y_true, y_pred))
    r2    = r2_score(y_true, y_pred)
    mape  = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-9))) * 100
    print(f"  {label:20s}  MAE={mae:10.1f}  RMSE={rmse:10.1f}  R²={r2:.4f}  MAPE={mape:.2f}%")
    return {"mae": mae, "rmse": rmse, "r2": r2, "mape": mape}

def train_problem(df, num_cols, cat_cols, target_col):
    print(f"\n{'='*60}")

    all_cols = num_cols + cat_cols
    sub = df[all_cols + [target_col]].dropna(subset=[target_col])
    print(f"  Kullanılan satır: {len(sub):,}")

    X = sub[all_cols]
    y = sub[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    preprocessor = build_preprocessor(num_cols, cat_cols)
    results = {}
    trained = {}

    for name, model in get_models().items():
        pipe = Pipeline([
            ("prep",  preprocessor),
            ("model", model),
        ])
        pipe.fit(X_train, y_train)
        preds = pipe.predict(X_test)
        metrics = evaluate(y_test, preds, label=name)
        results[name] = metrics
        trained[name] = pipe

    # En iyi model (R² ile)
    best_name = max(results, key=lambda k: results[k]["r2"])
    print(f"\n En iyi model: {best_name}  (R²={results[best_name]['r2']:.4f})")

    return trained, results, best_name, preprocessor

# ─────────────────────────────────────────────
# 5.  ANA AKIŞ
# ─────────────────────────────────────────────

def run_pipeline(csv_path: str):
    df = load_and_clean(csv_path)

    # Problem 1 – Fiyat Tahmini
    trained_p1, results_p1, best_p1, _ = train_problem(
        df,
        num_cols=PRICE_FEATURES_NUM,
        cat_cols=PRICE_FEATURES_CAT,
        target_col=TARGET_PRICE,
    )
    
    # EKLENDİ: En iyi modeli Pipeline (Preprocessor + Model) olarak komple kaydediyoruz.
    best_model_pipeline = trained_p1[best_p1]
    joblib.dump(best_model_pipeline, "/work/model/best_laptop_model.joblib")
    print(f"\n  [BİLGİ] En iyi model ({best_p1}) '/work/model/best_laptop_model.joblib' olarak kaydedildi!")
if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "data/processed/05_extract_usage_purpose_features.csv"
    run_pipeline(path)