import os
import random
import pickle
import logging
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import IsolationForest
from sklearn.feature_selection import SelectKBest, f_regression
from scipy import stats

# Seed for reproducibility
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# Constants for dashboard and other modules
TIME_COL = "Measurement_Timestamp"
TARGET_COL = "Health_Score"
GROUP_COL = "Truck_Id"

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Export SENSORS config for dashboard
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

def load_data(path=None):
    """Basic data loading for dashboard visualization."""
    if path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "Train_Test_FleetData.xlsx")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at: {path}")
        
    df = pd.read_excel(path)
    # The format is DDMMMYY:HH:MM:SS, e.g., 22FEB16:16:03:07
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], format="%d%b%y:%H:%M:%S")
    
    # Calculate Health Score for visualization
    processor = AdvancedDataProcessor()
    
    def _calc(row):
        total_penalty = 0.0
        for sensor, params in SENSORS.items():
            actual = row.get(sensor, np.nan)
            if pd.isna(actual): continue
            r = params['upper'] - params['lower']
            deviation = max(0, actual - params['upper']) / r + max(0, params['lower'] - actual) / r
            total_penalty += params['weight'] * deviation * 100
        return max(0.0, min(100.0, 100.0 - total_penalty))
    
    logger.info("Computing health scores for dashboard...")
    df[TARGET_COL] = df.apply(_calc, axis=1)
    return df

class AdvancedDataProcessor:
    """
    Advanced Data Processing Pipeline for Truck Health Prediction.
    Handles cleaning, advanced outlier detection, feature engineering, and smart splitting.
    """
    def __init__(self, target_col='Health_Score', window_size=20, k_features=20):
        self.target_col = target_col
        self.window_size = window_size
        self.k_features = k_features
        self.scaler = StandardScaler()
        self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.feature_selector = SelectKBest(score_func=f_regression, k=self.k_features)
        self.isolation_forest = IsolationForest(contamination=0.02, random_state=SEED)
        self.feature_cols = []
        
        # Sensor ranges and weights (for potential recalculation if needed)
        self.SENSORS_CONFIG = {
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

    def clean_data(self, df):
        """
        Cleaning: Detect and remove NaN and duplicates.
        Apply interpolation per Truck_Id to avoid corrupting time-series patterns.
        """
        logger.info("Cleaning data: removing duplicates and interpolating NaNs per truck...")
        df = df.drop_duplicates().reset_index(drop=True)
        # Group-wise interpolation
        df = df.groupby(GROUP_COL).apply(lambda group: group.interpolate(method='linear').ffill().bfill()).reset_index(drop=True)
        return df

    def handle_outliers(self, df, fit=False):
        """
        Outlier handling using IQR and Isolation Forest.
        If fit=True, fit the Isolation Forest; else, use pre-fitted model.
        """
        logger.info(f"Handling outliers using hybrid method (fit={fit})...")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.difference([GROUP_COL, 'Record_Id', self.target_col])
        
        # IQR Capping (always applied)
        Q1 = df[numeric_cols].quantile(0.25)
        Q3 = df[numeric_cols].quantile(0.75)
        IQR = Q3 - Q1
        df[numeric_cols] = df[numeric_cols].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR, axis=1)
        
        # Isolation Forest
        if fit:
            self.isolation_forest.fit(df[numeric_cols].fillna(0))
        outliers = self.isolation_forest.predict(df[numeric_cols].fillna(0))
        df = df[outliers == 1].reset_index(drop=True)
        
        return df

    def engineer_features(self, df):
        """
        Feature Engineering: Lags, Rolling Stats, and Interaction features.
        Performed per truck to maintain time order.
        """
        logger.info("Engineering features: lags, rolling statistics, and interactions per truck...")
        
        # Sort by truck and time
        df = df.sort_values([GROUP_COL, TIME_COL])
        
        # 1. Lag Features (1, 3, 5 steps)
        for col in ["Vibration", "Engine_Load", "Engine_Coolant_Temp"]:
            if col in df.columns:
                df[f'{col}_lag1'] = df.groupby(GROUP_COL)[col].shift(1)
                df[f'{col}_lag3'] = df.groupby(GROUP_COL)[col].shift(3)
        
        # 2. Rolling Statistics (window=5)
        for col in ["Engine_Rpm", "Engine_Load"]:
            if col in df.columns:
                df[f'{col}_roll_mean'] = df.groupby(GROUP_COL)[col].transform(lambda x: x.rolling(window=5).mean())
                df[f'{col}_roll_std'] = df.groupby(GROUP_COL)[col].transform(lambda x: x.rolling(window=5).std())
        
        # 3. Interaction Features
        if 'Engine_Rpm' in df.columns and 'Engine_Load' in df.columns:
            df['RPM_Load_Interaction'] = df['Engine_Rpm'] * df['Engine_Load']
            
        # Handle new NaNs from lags/rolling
        df = df.fillna(0)
        return df

    def split_data(self, df):
        """
        Smart Splitting: 60/20/20 Time-Series Split per Truck.
        Returns train_df, val_df, test_df.
        """
        logger.info("Splitting data: 60% Train, 20% Val, 20% Test (Temporal Split per truck)...")
        
        train_dfs, val_dfs, test_dfs = [], [], []
        
        for truck, group in df.groupby(GROUP_COL):
            n = len(group)
            if n < self.window_size + 1:
                logger.warning(f"Skipping truck {truck} with insufficient data ({n} < {self.window_size + 1})")
                continue
            train_end = int(n * 0.6)
            val_end = int(n * 0.8)
            
            train_dfs.append(group.iloc[:train_end])
            val_dfs.append(group.iloc[train_end:val_end])
            test_dfs.append(group.iloc[val_end:])
            
        if not train_dfs:
            raise ValueError("No valid training data after splitting. Check data size.")
        
        train_df = pd.concat(train_dfs).reset_index(drop=True)
        val_df = pd.concat(val_dfs).reset_index(drop=True) if val_dfs else pd.DataFrame()
        test_df = pd.concat(test_dfs).reset_index(drop=True) if test_dfs else pd.DataFrame()
        
        return train_df, val_df, test_df

    def scale_and_select_features(self, train_df, val_df, test_df):
        """
        Normalization using StandardScaler and feature selection.
        Fit on train, transform all.
        """
        logger.info("Scaling features using StandardScaler and selecting top features...")
        
        # Identify features
        drop_cols = ['Record_Id', GROUP_COL, TIME_COL, 'Maintenance_Flag', self.target_col]
        self.feature_cols = [c for c in train_df.columns if c not in drop_cols]
        
        # Fit scaler on train
        self.scaler.fit(train_df[self.feature_cols])
        
        # Transform all
        X_train = self.scaler.transform(train_df[self.feature_cols])
        X_val = self.scaler.transform(val_df[self.feature_cols]) if not val_df.empty else np.array([])
        X_test = self.scaler.transform(test_df[self.feature_cols]) if not test_df.empty else np.array([])
        
        # Feature selection on train
        self.feature_selector.fit(X_train, train_df[self.target_col])
        selected_indices = self.feature_selector.get_support(indices=True)
        self.feature_cols = [self.feature_cols[i] for i in selected_indices]
        
        # Apply selection
        X_train = X_train[:, selected_indices]
        if X_val.size > 0:
            X_val = X_val[:, selected_indices]
        if X_test.size > 0:
            X_test = X_test[:, selected_indices]
        
        y_train = train_df[self.target_col].values
        y_val = val_df[self.target_col].values if not val_df.empty else np.array([])
        y_test = test_df[self.target_col].values if not test_df.empty else np.array([])
        
        return X_train, X_val, X_test, y_train, y_val, y_test

    def create_sequences_per_truck(self, df, X, y):
        """
        Create sequences per truck to prevent data leakage.
        Returns Xs, ys, and corresponding truck_ids.
        """
        logger.info("Creating sequences per truck...")
        Xs, ys, truck_ids = [], [], []
        for truck, group in df.groupby(GROUP_COL):
            indices = group.index
            X_truck = X[indices]
            y_truck = y[indices]
            for i in range(len(X_truck) - self.window_size):
                Xs.append(X_truck[i:(i + self.window_size)])
                ys.append(y_truck[i + self.window_size])
                truck_ids.append(truck)
        return np.array(Xs), np.array(ys), truck_ids

    def prepare_pipeline(self, df):
        """
        Full pipeline: Clean -> Features -> Split -> Outliers -> Scale -> Select -> Sequences.
        """
        df = self.clean_data(df)
        df = self.engineer_features(df)
        train_df, val_df, test_df = self.split_data(df)
        
        # Handle outliers: fit on train, apply to all
        train_df = self.handle_outliers(train_df, fit=True)
        if not val_df.empty:
            val_df = self.handle_outliers(val_df, fit=False)
        if not test_df.empty:
            test_df = self.handle_outliers(test_df, fit=False)
        
        X_train, X_val, X_test, y_train, y_val, y_test = self.scale_and_select_features(train_df, val_df, test_df)
        
        # Create sequences per truck
        X_train_seq, y_train_seq, _ = self.create_sequences_per_truck(train_df, X_train, y_train)
        X_val_seq, y_val_seq, _ = (self.create_sequences_per_truck(val_df, X_val, y_val) 
                                if X_val.size > 0 else (np.array([]), np.array([]), []))
        X_test_seq, y_test_seq, test_truck_ids = (self.create_sequences_per_truck(test_df, X_test, y_test) 
                                  if X_test.size > 0 else (np.array([]), np.array([]), []))
        
        # Final validation
        if self.target_col in df.columns:
            df[self.target_col] = df[self.target_col].clip(0, 100)
        
        return X_train_seq, X_val_seq, X_test_seq, y_train_seq, y_val_seq, y_test_seq, test_truck_ids

    def save_pipeline(self, path='models/processor.pkl'):
        """Save the full processor object."""
        os.makedirs('models', exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        logger.info(f"Pipeline saved to {path}")

def load_and_process_data(path):
    logger.info("="*80)
    logger.info("Initializing Advanced Preprocessing Pipeline")
    logger.info("="*80)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found at {path}")
        
    df = pd.read_excel(path)
    df[TIME_COL] = pd.to_datetime(df[TIME_COL], format="%d%b%y:%H:%M:%S")
    processor = AdvancedDataProcessor()
    X_train_seq, X_val_seq, X_test_seq, y_train_seq, y_val_seq, y_test_seq, test_truck_ids = processor.prepare_pipeline(df)
    processor.save_pipeline()
    
    logger.info(f"Data processed: Train={X_train_seq.shape if X_train_seq.size > 0 else 0}, "
                f"Val={X_val_seq.shape if X_val_seq.size > 0 else 0}, "
                f"Test={X_test_seq.shape if X_test_seq.size > 0 else 0}")
    return X_train_seq, X_val_seq, X_test_seq, y_train_seq, y_val_seq, y_test_seq, test_truck_ids