# Fleet Vehicle Health Monitoring System

A complete end-to-end time-series deep learning system for computing and visualizing a continuous Health Score for fleet vehicles based on real-time sensor readings.

## Architecture

This project is fully modularized into the following components:

1. **`data_processing.py`**: Handles feature engineering (calculating the `Health_Score` from sensor deviations), temporal splitting per truck to avoid data leakage, preprocessing (IQR outlier capping, log-transformations, encoding, scaling), and windowing sequences.
2. **`models.py`**: Defines the two deep learning architectures used for continuous regression:
   - **LSTM Model**: Bidirectional LSTMs with dropout and L2 regularization.
   - **CNN+Transformer Model**: 1D-CNN temporal feature extractor paired with a Transformer Encoder block and global pooling.
3. **`train.py`**: The orchestrator script that loads data, trains both models, evaluates them (MAE, RMSE, R²), produces an Ensemble average prediction, generates learning curves, and saves a time-series animation (GIF) of the Health Score evolution.
4. **`dashboard.py`**: An interactive Streamlit application that visualizes the raw sensor data alongside the computed Health Score for any selected truck in the fleet, utilizing interactive Plotly charts and threshold alerts.

## Requirements

Ensure you have the following packages installed:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn tensorflow openpyxl streamlit plotly pillow
```

## How to Run

### 1. Training the Models & Generating Animations
To train the neural networks and generate the evaluation plots + the GIF animation of the health score over time:
```bash
python train.py
```
*Outputs will be saved in the `models/` directory (for .h5 models and scalers) and the `figures/` directory (for PNG plots and the .gif animation).*

### 2. Launching the Interactive Dashboard
To monitor the health of the fleet interactively:
```bash
streamlit run dashboard.py
```
This will open a web browser tab where you can:
- Select a specific `Truck_Id`.
- View its overall Health KPIs (Latest, Average, Min, Max).
- See critical/warning alerts if the score drops below operational thresholds.
- Interact with detailed Plotly time-series graphs for every major sensor, complete with shaded "Normal Range" overlays to help you understand *why* a health score is degrading.