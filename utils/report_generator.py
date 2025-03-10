"""
Module for generating PDF health reports
"""
import io
from datetime import datetime
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.barcharts import VerticalBarChart

def create_chart(data, metric_name, width=400, height=200):
    """Create a chart for the PDF report"""
    drawing = Drawing(width, height)
    
    if metric_name == 'steps':
        # Bar chart for steps
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [data[metric_name].tolist()]
        chart.categoryAxis.categoryNames = [d.strftime('%Y-%m-%d') for d in data['date']]
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.angle = 45
    else:
        # Line chart for other metrics
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [data[metric_name].tolist()]
        chart.categoryAxis.categoryNames = [d.strftime('%Y-%m-%d') for d in data['date']]
        chart.categoryAxis.labels.boxAnchor = 'ne'
        chart.categoryAxis.labels.angle = 45
    
    drawing.add(chart)
    return drawing

def generate_health_report(data: pd.DataFrame, weight_change: float) -> bytes:
    """
    Generate a PDF report of health metrics and predictions
    
    Args:
        data: DataFrame containing health metrics
        weight_change: Predicted weight change in pounds
    
    Returns:
        PDF report as bytes
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    subtitle_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Content elements
    elements = []
    
    # Title
    elements.append(Paragraph("Health Analytics Report", title_style))
    elements.append(Paragraph(f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", normal_style))
    elements.append(Spacer(1, 12))
    
    # Summary Statistics
    elements.append(Paragraph("Summary Statistics", subtitle_style))
    summary_data = [
        ["Metric", "Average", "Minimum", "Maximum"],
        ["Sleep (hours)", f"{data['sleep_hours'].mean():.1f}", f"{data['sleep_hours'].min():.1f}", f"{data['sleep_hours'].max():.1f}"],
        ["Steps", f"{data['steps'].mean():.0f}", f"{data['steps'].min():.0f}", f"{data['steps'].max():.0f}"],
        ["Exercise (mins)", f"{data['exercise_minutes'].mean():.0f}", f"{data['exercise_minutes'].min():.0f}", f"{data['exercise_minutes'].max():.0f}"],
        ["Heart Rate (BPM)", f"{data['heart_rate'].mean():.0f}", f"{data['heart_rate'].min():.0f}", f"{data['heart_rate'].max():.0f}"]
    ]
    
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 20))
    
    # Trend Analysis
    elements.append(Paragraph("Trend Analysis", subtitle_style))
    
    # Add charts
    for metric in ['sleep_hours', 'steps', 'exercise_minutes', 'heart_rate']:
        elements.append(Paragraph(f"{metric.replace('_', ' ').title()} Trend", styles['Heading3']))
        elements.append(create_chart(data, metric))
        elements.append(Spacer(1, 20))
    
    # Weight Change Prediction
    elements.append(Paragraph("Weight Change Prediction", subtitle_style))
    prediction_text = (
        f"Based on your activity patterns, you are predicted to "
        f"{'gain' if weight_change > 0 else 'lose'} "
        f"{abs(weight_change):.1f} pounds."
    )
    elements.append(Paragraph(prediction_text, normal_style))
    elements.append(Spacer(1, 12))
    
    # Recommendations
    elements.append(Paragraph("Recommendations", subtitle_style))
    recommendations = [
        "Sleep: Aim for 7-8 hours of sleep per night for optimal health.",
        "Steps: Target 10,000 steps daily for good cardiovascular health.",
        "Exercise: Include at least 30 minutes of moderate exercise daily.",
        "Heart Rate: Monitor your resting heart rate for cardiovascular fitness."
    ]
    for rec in recommendations:
        elements.append(Paragraph(f"• {rec}", normal_style))
        elements.append(Spacer(1, 6))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
