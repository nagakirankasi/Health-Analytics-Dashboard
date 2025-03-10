import plotly.graph_objects as go
import plotly.express as px

def plot_sleep_patterns(data):
    """Create sleep patterns visualization"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['sleep_hours'],
        mode='lines+markers',
        name='Sleep Hours',
        line=dict(color='#0066cc'),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title='Sleep Patterns Over Time',
        xaxis_title='Date',
        yaxis_title='Hours of Sleep',
        template='plotly_white',
        height=400
    )
    return fig

def plot_step_count(data):
    """Create step count visualization"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data['date'],
        y=data['steps'],
        marker_color='#00cc66'
    ))
    fig.update_layout(
        title='Daily Step Count',
        xaxis_title='Date',
        yaxis_title='Steps',
        template='plotly_white',
        height=400
    )
    return fig

def plot_exercise_minutes(data):
    """Create exercise minutes visualization"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['exercise_minutes'],
        fill='tozeroy',
        mode='lines',
        line=dict(color='#ff6666'),
        name='Exercise Minutes'
    ))
    fig.update_layout(
        title='Daily Exercise Minutes',
        xaxis_title='Date',
        yaxis_title='Minutes',
        template='plotly_white',
        height=400
    )
    return fig

def plot_heart_rate(data):
    """Create heart rate visualization"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['date'],
        y=data['heart_rate'],
        mode='lines',
        name='Heart Rate',
        line=dict(color='#ff3366')
    ))
    fig.update_layout(
        title='Heart Rate Trends',
        xaxis_title='Date',
        yaxis_title='BPM',
        template='plotly_white',
        height=400
    )
    return fig
