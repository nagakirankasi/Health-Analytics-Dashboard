import numpy as np
from sklearn.linear_model import LinearRegression

def predict_weight_change(data):
    """
    Predict weight change based on health metrics
    """
    # Calculate features
    features = np.column_stack((
        data['sleep_hours'],
        data['steps'] / 1000,  # normalize steps
        data['exercise_minutes'],
        data['heart_rate']
    ))

    # Simple trend calculation using linear regression
    days = np.arange(len(data)).reshape(-1, 1)
    
    # Calculate activity score
    activity_score = (
        (data['sleep_hours'] - 7) * 0.3 +  # optimal sleep difference
        (data['steps'] - 10000) * 0.00004 +  # steps difference from 10k
        (data['exercise_minutes'] - 30) * 0.02 +  # exercise difference from 30 mins
        (data['heart_rate'] - 70) * -0.01  # heart rate difference from 70
    ).mean()

    # Predict weight change
    # Negative score means weight loss, positive means gain
    weight_change = -activity_score * 2  # Scale factor for pounds

    return weight_change
