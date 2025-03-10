"""
Apple Health integration module for fetching health data
"""
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import streamlit as st
import numpy as np

class AppleHealthConnector:
    """Handles connection and data fetching from Apple Health"""

    def __init__(self):
        """Initialize with sample data for testing"""
        self.is_demo = True

    def authenticate(self) -> bool:
        """
        Mock authentication for demo purposes
        Returns: bool indicating success
        """
        return True

    def generate_sample_data(self, days: int = 30) -> dict:
        """
        Generate realistic sample health data
        """
        np.random.seed(42)  # For reproducible results

        # Generate somewhat realistic data with some patterns
        sleep_hours = np.clip(np.random.normal(7.5, 0.8, days), 5, 10)
        steps = np.clip(np.random.normal(8000, 2000, days), 3000, 15000)
        exercise_minutes = np.clip(np.random.normal(40, 15, days), 10, 90)
        heart_rate = np.clip(np.random.normal(72, 5, days), 60, 100)

        return {
            'sleep_hours': sleep_hours.tolist(),
            'steps': steps.tolist(),
            'exercise_minutes': exercise_minutes.tolist(),
            'heart_rate': heart_rate.tolist()
        }

    def get_last_month_data(self) -> dict:
        """
        Get sample health data for the last month
        Returns:
            Dictionary with processed health metrics
        """
        try:
            # Generate sample data
            raw_data = self.generate_sample_data()

            # Create date range
            end_date = datetime.date.today()
            start_date = end_date - relativedelta(months=1)
            date_range = pd.date_range(start=start_date, end=end_date, periods=len(raw_data['sleep_hours']))

            # Format the data
            processed_data = {
                'date': date_range,
                'sleep_hours': raw_data['sleep_hours'],
                'steps': raw_data['steps'],
                'exercise_minutes': raw_data['exercise_minutes'],
                'heart_rate': raw_data['heart_rate']
            }

            return processed_data

        except Exception as e:
            st.error(f"Error generating sample data: {str(e)}")
            return {}