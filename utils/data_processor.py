import pandas as pd
import numpy as np

def process_health_data(df):
    """
    Process and validate health data
    """
    required_columns = [
        'date', 'sleep_hours', 'steps', 
        'exercise_minutes', 'heart_rate'
    ]
    
    # Validate columns
    if not all(col in df.columns for col in required_columns):
        raise ValueError(
            f"Missing required columns. Required: {required_columns}"
        )

    # Convert date column
    df['date'] = pd.to_datetime(df['date'])

    # Basic data cleaning
    df = df.dropna()  # Remove rows with missing values
    
    # Remove outliers using IQR method
    for col in ['sleep_hours', 'steps', 'exercise_minutes', 'heart_rate']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[
            (df[col] >= Q1 - 1.5 * IQR) & 
            (df[col] <= Q3 + 1.5 * IQR)
        ]

    # Sort by date
    df = df.sort_values('date')

    return df
