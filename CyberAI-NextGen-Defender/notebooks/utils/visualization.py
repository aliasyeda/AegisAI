import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_threat_distribution_chart(df):
    """Create threat type distribution chart"""
    if df.empty:
        return create_empty_chart("No threat data available")
    
    threat_counts = df['threat_type'].value_counts()
    fig = px.pie(
        values=threat_counts.values, 
        names=threat_counts.index,
        title="Threat Type Distribution"
    )
    return fig

def create_defense_actions_chart(df):
    """Create defense actions distribution chart"""
    if df.empty:
        return create_empty_chart("No defense data available")
    
    action_counts = df['defense_action'].value_counts()
    colors = ['#ff4b4b', '#ffa500', '#ffff00', '#00ff00']  # Red, Orange, Yellow, Green
    
    fig = go.Figure(data=[go.Bar(
        x=action_counts.index,
        y=action_counts.values,
        marker_color=colors[:len(action_counts)]
    )])
    
    fig.update_layout(title="Defense Actions Distribution")
    return fig

def create_timeline_chart(action_log):
    """Create threat timeline chart"""
    if action_log.empty or 'timestamp' not in action_log.columns:
        return create_empty_chart("No timeline data available")
    
    timeline = action_log.groupby(pd.Grouper(key='timestamp', freq='H')).size()
    fig = px.line(timeline, title='Threat Activity Timeline')
    return fig

def create_risk_heatmap(df):
    """Create risk heatmap"""
    if df.empty:
        return create_empty_chart("No risk data available")
    
    # Sample heatmap data
    fig = go.Figure(data=go.Heatmap(
        z=[[1, 2, 3], [2, 3, 4], [3, 4, 5]],
        x=['Low', 'Medium', 'High'],
        y=['Spam', 'Phishing', 'DDoS'],
        colorscale='Viridis'
    ))
    
    fig.update_layout(title="Threat Risk Heatmap")
    return fig

def create_empty_chart(message):
    """Create an empty chart with message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16)
    )
    return fig