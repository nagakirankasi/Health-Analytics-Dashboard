import streamlit as st
import pandas as pd
from utils.data_processor import process_health_data
from utils.predictor import predict_weight_change
from utils.visualizer import (
    plot_sleep_patterns,
    plot_step_count,
    plot_exercise_minutes,
    plot_heart_rate
)
from utils.apple_health import AppleHealthConnector
#from utils.report_generator import generate_health_report

def main():
    st.set_page_config(
        page_title="Health Analytics Dashboard",
        page_icon="❤️",
        layout="wide"
    )

    st.title("Health Analytics Dashboard")

    # Data source selection
    data_source = st.radio(
        "Choose your data source",
        ["Sample Health Data", "CSV Upload"],
        help="Use sample data or upload your own CSV file"
    )

    data = None

    if data_source == "Sample Health Data":
        st.info("🔬 Using sample health data to demonstrate the analytics")
        if st.button("Load Sample Data"):
            with st.spinner("Loading sample health data..."):
                try:
                    health_connector = AppleHealthConnector()
                    data = pd.DataFrame(health_connector.get_last_month_data())
                    st.success("Successfully loaded sample health data!")
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")

    else:
        st.markdown("""
        Upload your health data to get insights and weight change predictions.
        The data should include sleep, steps, exercise, and heart rate information.
        """)

        uploaded_file = st.file_uploader(
            "Upload your health data (CSV)",
            type=['csv'],
            help="Upload a CSV file containing your health metrics"
        )

        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")

    if data is not None:
        try:
            processed_data = process_health_data(data)

            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Avg. Sleep (hours)", 
                         f"{processed_data['sleep_hours'].mean():.1f}")
            with col2:
                st.metric("Avg. Steps", 
                         f"{processed_data['steps'].mean():.0f}")
            with col3:
                st.metric("Avg. Exercise (mins)", 
                         f"{processed_data['exercise_minutes'].mean():.0f}")
            with col4:
                st.metric("Avg. Heart Rate", 
                         f"{processed_data['heart_rate'].mean():.0f}")

            # Visualizations
            st.subheader("Health Metrics Analysis")
            tab1, tab2, tab3, tab4 = st.tabs([
                "Sleep Patterns", "Step Count", 
                "Exercise Minutes", "Heart Rate"
            ])

            with tab1:
                st.plotly_chart(plot_sleep_patterns(processed_data))
            with tab2:
                st.plotly_chart(plot_step_count(processed_data))
            with tab3:
                st.plotly_chart(plot_exercise_minutes(processed_data))
            with tab4:
                st.plotly_chart(plot_heart_rate(processed_data))

            # Weight Prediction
            st.subheader("Weight Change Prediction")
            weight_change = predict_weight_change(processed_data)

            if weight_change > 0:
                st.warning(f"Predicted weight gain: {abs(weight_change):.1f} lbs")
            else:
                st.success(f"Predicted weight loss: {abs(weight_change):.1f} lbs")

            # Add explanation of the prediction
            with st.expander("How is the prediction calculated?"):
                st.markdown("""
                The weight change prediction is based on several factors:
                - Sleep quality (optimal is 7-8 hours)
                - Daily steps (target: 10,000 steps)
                - Exercise duration (recommended: 30+ minutes)
                - Heart rate patterns

                The model analyzes these patterns over time to estimate potential weight changes.
                """)
            

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
    else:
        if data_source == "CSV Upload":
            st.info("Please upload your health data to begin analysis")

if __name__ == "__main__":
    main()