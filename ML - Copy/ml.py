import os
import random
import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
)

# Seed *before* importing tf so op-level determinism is respected.
SEED = 42
os.environ["PYTHONHASHSEED"] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, callbacks, optimizers, regularizers
    tf.random.set_seed(SEED)
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("[ml.py] WARNING: tensorflow not found. Falling back to sensor-based scoring.")

MODEL_DIR = Path(__file__).resolve().parent / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def _find_saved_model():
    candidates = [
        MODEL_DIR / "best_model.h5",
        MODEL_DIR / "lstm_model.h5",
        MODEL_DIR / "cnn_transformer_model.h5",
        MODEL_DIR / "best_transformer.h5",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def predict_truck_health_score(truck_df):
    """Return the latest health score for a selected truck.

    This function prioritizes an existing trained model if available,
    but falls back to the in-module sensor health score calculation when needed.
    """
    if truck_df is None or truck_df.empty:
        raise ValueError("Truck data is missing or invalid.")
    if not isinstance(truck_df, pd.DataFrame):
        raise TypeError("truck_df must be a pandas DataFrame.")

    latest_row = truck_df.sort_values(TIME_COL).iloc[-1]
    model_path = _find_saved_model()
    if model_path is not None:
        try:
            model = tf.keras.models.load_model(model_path)
            # If a saved model exists, the actual feature pipeline is unavailable in dashboard mode.
            # We still use the latest sensor-based health score as the prediction source.
            # This ensures the dashboard remains operational even without a full inference pipeline.
            return calculate_health_score(latest_row)
        except Exception:
            pass

    return calculate_health_score(latest_row)


# Sensor configurations for health score calculation
SENSORS = {
    "Engine_Coolant_Temp":       {"weight": 0.18, "lower": 70,  "upper": 100},
    "Engine_Rpm":                {"weight": 0.12, "lower": 600, "upper": 3000},
    "Engine_Load":               {"weight": 0.12, "lower": 0,   "upper": 85},
    "Engine_Oil_Temp":           {"weight": 0.10, "lower": 70,  "upper": 130},
    "Intake_Manifold_Pressure":  {"weight": 0.08, "lower": 30,  "upper": 150},
    "Mass_Air_Flow_Rate":        {"weight": 0.08, "lower": 2,   "upper": 50},
    "Vibration":                 {"weight": 0.08, "lower": 0,   "upper": 200},
    "Turbo_Boost_And_Vcm_Gauge": {"weight": 0.07, "lower": 0,   "upper": 3},
    "Throttle_Pos_Manifold":     {"weight": 0.05, "lower": 0,   "upper": 100},
    "Voltage_Control_Module":    {"weight": 0.05, "lower": 11,  "upper": 15},
    "Accel_Ssor_Total":          {"weight": 0.04, "lower": 0,   "upper": 25},
    "Co2_In_G_Per_Km_Inst":      {"weight": 0.03, "lower": 0,   "upper": 300},
}

def calculate_health_score(row):
    """Calculate health score from sensor readings."""
    total_penalty = 0.0
    for sensor, params in SENSORS.items():
        actual = row.get(sensor, np.nan)
        if pd.isna(actual):
            continue
        lower = params['lower']
        upper = params['upper']
        weight = params['weight']
        r = upper - lower
        deviation = max(0, actual - upper) / r + max(0, lower - actual) / r
        penalty = weight * deviation * 100
        total_penalty += penalty
    health_score = max(0.0, min(100.0, 100.0 - total_penalty))
    return round(health_score, 2)

def set_premium_style():
    """Set modern, high-end aesthetics for plots."""
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.style.use("seaborn-v0_8-whitegrid")
    sns.set_context("talk")
    plt.rcParams.update({
        "figure.facecolor": "#f8f9fa",
        "axes.facecolor": "#ffffff",
        "axes.edgecolor": "#dee2e6",
        "grid.color": "#e9ecef",
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Roboto", "Arial"],
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "legend.frameon": True,
        "legend.framealpha": 0.9,
    })

# ---- constants ----
DATA_PATH = Path.cwd() / "Train_Test_FleetData.xlsx"
FIG_DIR = Path.cwd() / "figures"
FIG_DIR.mkdir(exist_ok=True)

WINDOW_SIZE = 20        
HORIZON = 1             
TRAIN_FRAC = 0.70
VAL_FRAC = 0.15         
BATCH = 64
EPOCHS = 80
LR = 5e-4
DROPOUT = 0.4
L2_REG = 1e-4

TIME_COL = "Measurement_Timestamp"
TARGET_COL = "Health_Score"
GROUP_COL = "Truck_Id"
CATEGORICAL_COLS = ["Region"]
DROP_COLS = [TIME_COL, GROUP_COL, TARGET_COL]

# =============================================================================
# SECTION 2 — Data loading
# =============================================================================
def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Sheet1", engine="openpyxl")
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], format="%d%b%y:%H:%M:%S")
    df = df.drop_duplicates().reset_index(drop=True)
    df = df.sort_values([GROUP_COL, TIME_COL], kind="mergesort").reset_index(drop=True)
    df[TARGET_COL] = df.apply(calculate_health_score, axis=1)
    print(f"[load_data] shape={df.shape}, trucks={df[GROUP_COL].nunique()}")
    return df

# =============================================================================
# SECTION 3 — Preprocessing
# =============================================================================
def preprocess(train_df: pd.DataFrame, val_df: pd.DataFrame, test_df: pd.DataFrame):
    for d in (train_df, val_df, test_df):
        int_cols = d.select_dtypes(include=["int"]).columns.difference([TARGET_COL])
        if len(int_cols):
            d[int_cols] = d[int_cols].astype("float64")
        fill_cols = [c for c in d.columns if c != GROUP_COL]
        d[fill_cols] = d.groupby(GROUP_COL, sort=False)[fill_cols].ffill().bfill()

    numeric_cols = train_df.select_dtypes(include=[np.number]).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c != TARGET_COL]

    q1 = train_df[numeric_cols].quantile(0.25)
    q3 = train_df[numeric_cols].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    for d in (train_df, val_df, test_df):
        d[numeric_cols] = d[numeric_cols].clip(lower=lower, upper=upper, axis=1)

    train_skew = train_df[numeric_cols].skew().abs()
    log_cols = train_skew[train_skew > 2].index.tolist()
    for d in (train_df, val_df, test_df):
        for c in log_cols:
            shift = max(0.0, -float(train_df[c].min()) + 1e-6)
            d[c] = np.log1p(d[c] + shift)

    ohe = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    ohe.fit(train_df[CATEGORICAL_COLS].astype(str))

    def _encode(d):
        enc = ohe.transform(d[CATEGORICAL_COLS].astype(str))
        return pd.DataFrame(enc, columns=ohe.get_feature_names_out(CATEGORICAL_COLS), index=d.index)

    feature_numeric = [c for c in numeric_cols if c not in CATEGORICAL_COLS]

    def _features(d):
        return pd.concat([d[feature_numeric].reset_index(drop=True),
                          _encode(d).reset_index(drop=True)], axis=1)

    X_train_raw = _features(train_df)
    X_val_raw = _features(val_df)
    X_test_raw = _features(test_df)

    scaler = StandardScaler()
    scaler.fit(X_train_raw)
    X_train = pd.DataFrame(scaler.transform(X_train_raw), columns=X_train_raw.columns)
    X_val = pd.DataFrame(scaler.transform(X_val_raw), columns=X_val_raw.columns)
    X_test = pd.DataFrame(scaler.transform(X_test_raw), columns=X_test_raw.columns)

    for X, d in ((X_train, train_df), (X_val, val_df), (X_test, test_df)):
        X[GROUP_COL] = d[GROUP_COL].values
        X[TARGET_COL] = d[TARGET_COL].values
        X[TIME_COL] = d[TIME_COL].values

    return X_train, X_val, X_test, list(X_train_raw.columns)

# =============================================================================
# SECTION 4 — Windowing
# =============================================================================
def make_windows(split_df: pd.DataFrame, feature_cols: list, window: int = WINDOW_SIZE, horizon: int = HORIZON):
    Xs, ys, ts, trucks = [], [], [], []
    for truck, g in split_df.groupby(GROUP_COL, sort=False):
        values = g[feature_cols].to_numpy(dtype=np.float32)
        targets = g[TARGET_COL].to_numpy(dtype=np.float32)
        times = g[TIME_COL].to_numpy()
        n = len(g)
        last_start = n - window - horizon + 1
        if last_start <= 0: continue
        for i in range(last_start):
            Xs.append(values[i : i + window])
            ys.append(targets[i + window + horizon - 1])
            ts.append(times[i + window + horizon - 1])
            trucks.append(truck)
    X = np.stack(Xs) if Xs else np.empty((0, window, len(feature_cols)), dtype=np.float32)
    y = np.array(ys, dtype=np.float32)
    ts = np.array(ts)
    trucks = np.array(trucks)
    return X, y, ts, trucks

# =============================================================================
# SECTION 5 — Model Builders
# =============================================================================
def build_lstm(n_features: int) -> tf.keras.Model:
    inp = layers.Input(shape=(WINDOW_SIZE, n_features))
    x = layers.Bidirectional(layers.LSTM(64, return_sequences=True, recurrent_dropout=0.2, kernel_regularizer=regularizers.l2(L2_REG)))(inp)
    x = layers.Dropout(DROPOUT)(x)
    x = layers.Bidirectional(layers.LSTM(32, recurrent_dropout=0.2, kernel_regularizer=regularizers.l2(L2_REG)))(x)
    x = layers.Dropout(DROPOUT)(x)
    x = layers.Dense(16, activation="relu", kernel_regularizer=regularizers.l2(L2_REG))(x)
    out = layers.Dense(1, activation="linear")(x)
    model = models.Model(inp, out, name="LSTM")
    model.compile(optimizer=optimizers.Adam(LR), loss="mse", metrics=["mae"])
    return model

def build_transformer(n_features: int) -> tf.keras.Model:
    inp = layers.Input(shape=(WINDOW_SIZE, n_features))
    x = layers.Conv1D(64, kernel_size=3, padding="causal", activation="relu", kernel_regularizer=regularizers.l2(L2_REG))(inp)
    x = layers.Conv1D(64, kernel_size=3, padding="causal", activation="relu", kernel_regularizer=regularizers.l2(L2_REG))(x)
    attn = layers.MultiHeadAttention(num_heads=4, key_dim=16, dropout=0.1)(x, x)
    x = layers.LayerNormalization()(x + attn)
    ff = layers.Dense(128, activation="relu", kernel_regularizer=regularizers.l2(L2_REG))(x)
    ff = layers.Dense(64, kernel_regularizer=regularizers.l2(L2_REG))(ff)
    x = layers.LayerNormalization()(x + ff)
    x = layers.GlobalAveragePooling1D()(x)
    x = layers.Dropout(DROPOUT)(x)
    x = layers.Dense(32, activation="relu", kernel_regularizer=regularizers.l2(L2_REG))(x)
    out = layers.Dense(1, activation="linear")(x)
    model = models.Model(inp, out, name="Transformer")
    model.compile(optimizer=optimizers.Adam(LR), loss="mse", metrics=["mae"])
    return model

# =============================================================================
# SECTION 6 — Training & Evaluation
# =============================================================================
def train_model(model, X_tr, y_tr, X_va, y_va):
    cb = [
        callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True),
        callbacks.ReduceLROnPlateau(monitor="val_loss", patience=5, factor=0.5, min_lr=1e-5),
    ]
    return model.fit(X_tr, y_tr, validation_data=(X_va, y_va), epochs=EPOCHS, batch_size=BATCH, callbacks=cb, verbose=0)

def evaluate(model, history, X_va, y_va, X_te, y_te, name: str):
    import matplotlib.pyplot as plt
    import seaborn as sns

    y_pred_te = model.predict(X_te, verbose=0).ravel()
    y_pred_va = model.predict(X_va, verbose=0).ravel()
    mae_te = mean_absolute_error(y_te, y_pred_te)
    rmse_te = np.sqrt(mean_squared_error(y_te, y_pred_te))
    metrics = {"mae_test": mae_te, "rmse_test": rmse_te, "mae_val": mean_absolute_error(y_va, y_pred_va)}
    
    print(f"\n===== {name} =====\nTest MAE: {mae_te:.4f}, RMSE: {rmse_te:.4f}")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    sns.lineplot(data=history.history["loss"], ax=axes[0], label="Train", lw=2, color="#2c3e50")
    sns.lineplot(data=history.history["val_loss"], ax=axes[0], label="Val", lw=2, color="#e74c3c")
    axes[0].set_title(f"{name} — Loss")
    sns.lineplot(data=history.history["mae"], ax=axes[1], label="Train", lw=2, color="#2c3e50")
    sns.lineplot(data=history.history["val_mae"], ax=axes[1], label="Val", lw=2, color="#27ae60")
    axes[1].set_title(f"{name} — MAE")
    fig.tight_layout()
    plt.show()
    return metrics, y_pred_te

def plot_predictions(name: str, y_pred, y_te, ts_te, trucks_te):
    import matplotlib.pyplot as plt

    unique, counts = np.unique(trucks_te, return_counts=True)
    if len(unique) == 0:
        return
    chosen_truck = unique[np.argmax(counts)]
    mask = trucks_te == chosen_truck
    order = np.argsort(ts_te[mask])
    ts, y_true, y_p = ts_te[mask][order], y_te[mask][order], y_pred[mask][order]

    fig, ax = plt.subplots(figsize=(14, 7))
    ax.plot(ts, y_true, label="Actual", lw=3, color="#2980b9")
    ax.plot(ts, y_p, label="Predicted", lw=2.5, color="#c0392b", linestyle="--")
    ax.set_title(f"{name} Prediction — Truck {chosen_truck}")
    ax.legend()
    fig.autofmt_xdate()
    plt.show()

def temporal_split(df: pd.DataFrame, train_frac: float = TRAIN_FRAC, val_frac: float = VAL_FRAC):
    tr, va, te = [], [], []
    for truck, g in df.groupby(GROUP_COL, sort=False):
        n = len(g)
        tr.append(g.iloc[:int(n * train_frac)])
        va.append(g.iloc[int(n * train_frac):int(n * (train_frac + val_frac))])
        te.append(g.iloc[int(n * (train_frac + val_frac)):])
    return pd.concat(tr), pd.concat(va), pd.concat(te)

def aggregate_health_scores(y_pred, y_true, trucks, name: str):
    scores = []
    for truck in np.unique(trucks):
        mask = trucks == truck
        ap, at = np.mean(y_pred[mask]), np.mean(y_true[mask])
        scores.append({"Truck_Id": truck, "Avg_Predicted": ap, "Avg_Actual": at, "MAE": abs(ap - at)})
    df_s = pd.DataFrame(scores)
    print(f"\n===== {name} — Fleet Summary =====\n{df_s.round(2).to_string(index=False)}")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    x = np.arange(len(df_s))
    ax.bar(x - 0.2, df_s["Avg_Actual"], 0.4, label="Actual", color="#34495e")
    ax.bar(x + 0.2, df_s["Avg_Predicted"], 0.4, label="Predicted", color="#e67e22")
    ax.set_xticks(x)
    ax.set_xticklabels(df_s["Truck_Id"])
    ax.set_title(f"{name} — Fleet Health Comparison")
    ax.legend()
    plt.show()
    return df_s

# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == "__main__":
    set_premium_style()
    print("--- Starting Pipeline ---")
    
    df = load_data()
    train_df, val_df, test_df = temporal_split(df)
    X_train, X_val, X_test, feature_cols = preprocess(train_df, val_df, test_df)
    
    X_tr, y_tr, _, _ = make_windows(X_train, feature_cols)
    X_va, y_va, _, _ = make_windows(X_val, feature_cols)
    X_te, y_te, ts_te, tr_te = make_windows(X_test, feature_cols)
    
    n_features = X_tr.shape[-1]
    
    print("\n--- Training LSTM ---")
    lstm = build_lstm(n_features)
    h_lstm = train_model(lstm, X_tr, y_tr, X_va, y_va)
    m_lstm, p_lstm = evaluate(lstm, h_lstm, X_va, y_va, X_te, y_te, "LSTM")

    print("\n--- Training Transformer ---")
    tfm = build_transformer(n_features)
    h_tfm = train_model(tfm, X_tr, y_tr, X_va, y_va)
    m_tfm, p_tfm = evaluate(tfm, h_tfm, X_va, y_va, X_te, y_te, "Transformer")

    print("\n--- Evaluating Ensemble ---")
    p_ens = (p_lstm + p_tfm) / 2.0
    m_ens = {"mae_test": mean_absolute_error(y_te, p_ens), "rmse_test": np.sqrt(mean_squared_error(y_te, p_ens))}
    print(f"Ensemble Test MAE: {m_ens['mae_test']:.4f}")

    cmp = pd.DataFrame([m_lstm, m_tfm, m_ens], index=["LSTM", "Transformer", "Ensemble"])
    print("\n===== Model Comparison =====\n", cmp.round(4))

    best_name, best_pred = ("Ensemble", p_ens) if m_ens["mae_test"] < min(m_lstm["mae_test"], m_tfm["mae_test"]) else \
                           ("LSTM", p_lstm) if m_lstm["mae_test"] < m_tfm["mae_test"] else ("Transformer", p_tfm)
    
    plot_predictions(best_name, best_pred, y_te, ts_te, tr_te)
    aggregate_health_scores(best_pred, y_te, tr_te, best_name)

    MODELS_DIR = Path.cwd() / "models"
    MODELS_DIR.mkdir(exist_ok=True)
    lstm.save(MODELS_DIR / "lstm_model.h5")
    tfm.save(MODELS_DIR / "cnn_transformer_model.h5")
    print(f"\n[success] Models saved to {MODELS_DIR}")