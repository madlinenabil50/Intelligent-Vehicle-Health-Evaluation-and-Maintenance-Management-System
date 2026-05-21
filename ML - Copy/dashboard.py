import os
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Important configuration for Plotly full width
st.set_page_config(page_title="Fleet Health Dashboard", layout="wide")

# Import logic from data_processing to compute the score directly
from data_processing import load_data, SENSORS, TARGET_COL, TIME_COL, GROUP_COL
from certificate_generator import generate_certificate


@st.cache_data
def get_fleet_data():
    """Load data and compute health scores once."""
    df = load_data()
    return df


def main():
    st.title("🚛 Fleet Vehicle Health Dashboard")
    st.markdown("Monitor real-time health scores and time-series sensor readings for all fleet vehicles.")

    # 1. Load Data
    with st.spinner("Loading fleet data..."):
        df = get_fleet_data()

    # 2. Truck Selection
    st.sidebar.header("Filter Options")
    truck_ids = sorted(df[GROUP_COL].unique())
    selected_truck = st.sidebar.selectbox("Select Truck ID:", truck_ids)

    # Filter dataset for the selected truck
    truck_df = df[df[GROUP_COL] == selected_truck].sort_values(TIME_COL)

    if truck_df.empty:
        st.warning("No data found for this truck.")
        return

    # 3. KPIs
    latest_score = truck_df[TARGET_COL].iloc[-1]
    avg_score = truck_df[TARGET_COL].mean()
    min_score = truck_df[TARGET_COL].min()
    max_score = truck_df[TARGET_COL].max()

    st.header(f"Health Overview: Truck {selected_truck}")

    # 4. Alerts
    if latest_score < 40:
        st.error(
            f"🚨 CRITICAL ALERT: Truck {selected_truck}'s latest health score is {latest_score:.2f} "
            "(Below 40). Immediate maintenance required!"
        )
    elif latest_score < 60:
        st.warning(
            f"⚠️ WARNING: Truck {selected_truck}'s latest health score is {latest_score:.2f} "
            "(Below 60). Schedule inspection soon."
        )
    else:
        st.success(f"✅ Truck {selected_truck} is operating normally. Latest score: {latest_score:.2f}")

    # Display KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Health Score", f"{latest_score:.2f}")
    col2.metric("Average Health Score", f"{avg_score:.2f}")
    col3.metric("Minimum Health Score", f"{min_score:.2f}")
    col4.metric("Maximum Health Score", f"{max_score:.2f}")

    st.markdown("---")

    # 5. Time-Series Visualization: Health Score
    st.subheader("Health Score Over Time")
    fig_health = px.line(
        truck_df,
        x=TIME_COL,
        y=TARGET_COL,
        title="Overall Health Score Trend",
        labels={TARGET_COL: "Health Score (0-100)", TIME_COL: "Time"},
    )
    fig_health.add_hline(
        y=40,
        line_dash="dash",
        line_color="red",
        annotation_text="Critical Threshold (40)",
    )
    fig_health.add_hline(
        y=60,
        line_dash="dash",
        line_color="orange",
        annotation_text="Warning Threshold (60)",
    )
    fig_health.update_layout(xaxis_title="", hovermode="x unified", margin=dict(t=30, b=0, l=0, r=0))
    fig_health.update_yaxes(range=[0, 105])
    st.plotly_chart(fig_health, use_container_width=True)

    st.markdown("---")

    # 6. Certificate generation
    st.subheader("Generate Vehicle Health Certificate")
    st.markdown("Use the selected Truck ID and the latest predicted health score to create a professional PDF certificate.")

    if st.button("Generate Certificate"):
        try:
            health_score = latest_score
            file_path = generate_certificate(selected_truck, health_score)
            st.success("Certificate generated successfully.")

            if Path(file_path).exists():
                with open(file_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download Certificate",
                        data=pdf_file,
                        file_name=Path(file_path).name,
                        mime="application/pdf",
                    )
        except Exception as exc:
            st.error(f"Certificate generation failed: {exc}")

    st.markdown("---")

    # 7. Multi-Graph Layout for Sensors
    st.subheader("Sensor Diagnostics")
    st.markdown("Detailed breakdown of key sensors used to calculate the Health Score.")

    sensors = list(SENSORS.keys())
    for i in range(0, len(sensors), 2):
        cols = st.columns(2)

        for j, col in enumerate(cols):
            if i + j < len(sensors):
                sensor = sensors[i + j]
                fig_sensor = px.line(truck_df, x=TIME_COL, y=sensor, title=sensor)
                upper = SENSORS[sensor]["upper"]
                lower = SENSORS[sensor]["lower"]
                fig_sensor.add_hrect(
                    y0=lower,
                    y1=upper,
                    line_width=0,
                    fillcolor="green",
                    opacity=0.1,
                    annotation_text="Normal Range",
                    annotation_position="top left",
                )
                fig_sensor.update_layout(xaxis_title="", hovermode="x unified", height=300, margin=dict(t=30, b=0, l=0, r=0))
                col.plotly_chart(fig_sensor, use_container_width=True)


if __name__ == "__main__":
    main()