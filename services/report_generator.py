"""
Report Generation Service - Creates professional HTML reports with interactive charts.
Inspired by FORMULA_1_PREDICTOR_STREAMLIT_2026's professional reporting system.
"""
import json
import logging
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generates professional HTML reports with interactive Plotly charts.
    Inspired by F1 Predictor's publication-quality report generation.
    """
    
    def __init__(self):
        self.template_path = "templates/reports/"
    
    def generate_student_progress_report(self, student_data: Dict,
                                        accuracy_data: Dict,
                                        predictions: List[Dict]) -> str:
        """
        Generate comprehensive student progress report.
        
        Args:
            student_data: Student profile and performance data
            accuracy_data: Prediction accuracy metrics
            predictions: Recent prediction records
            
        Returns:
            HTML report string
        """
        # Create charts
        progress_chart = self._create_progress_chart(student_data)
        accuracy_chart = self._create_accuracy_chart(accuracy_data)
        prediction_dist_chart = self._create_prediction_distribution(predictions)
        radar_chart = self._create_student_radar(student_data)
        
        # Build HTML report
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>FINESE SCHOOL - Student Progress Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    margin-top: 30px;
                }}
                .metric-card {{
                    display: inline-block;
                    width: 200px;
                    margin: 10px;
                    padding: 15px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border-radius: 8px;
                    text-align: center;
                }}
                .metric-value {{
                    font-size: 32px;
                    font-weight: bold;
                }}
                .metric-label {{
                    font-size: 14px;
                    opacity: 0.9;
                }}
                .chart-container {{
                    margin: 20px 0;
                    padding: 20px;
                    background: #fafafa;
                    border-radius: 8px;
                }}
                .summary {{
                    background: #e8f4f8;
                    padding: 15px;
                    border-left: 4px solid #3498db;
                    margin: 20px 0;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                th, td {{
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:hover {{
                    background-color: #f5f5f5;
                }}
                .footer {{
                    margin-top: 40px;
                    text-align: center;
                    color: #7f8c8d;
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📊 Student Progress Report</h1>
                <p><strong>Student:</strong> {student_data.get('name', 'N/A')} | 
                   <strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
                
                <h2>🎯 Key Metrics</h2>
                <div>
                    <div class="metric-card">
                        <div class="metric-value">{accuracy_data.get('accuracy_rate', 0):.1f}%</div>
                        <div class="metric-label">Prediction Accuracy</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{student_data.get('overall_score', 0):.1f}</div>
                        <div class="metric-label">Current Score</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{student_data.get('improvement_rate', 0):.1f}%</div>
                        <div class="metric-label">Improvement Rate</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{len(predictions)}</div>
                        <div class="metric-label">Total Predictions</div>
                    </div>
                </div>
                
                <div class="summary">
                    <h3>📈 Performance Summary</h3>
                    <p>{self._generate_summary_text(student_data, accuracy_data)}</p>
                </div>
                
                <h2>📉 Learning Progress Over Time</h2>
                <div class="chart-container">
                    {progress_chart}
                </div>
                
                <h2>🎯 Prediction Accuracy Analysis</h2>
                <div class="chart-container">
                    {accuracy_chart}
                </div>
                
                <h2>📊 Student Capability Radar</h2>
                <div class="chart-container">
                    {radar_chart}
                </div>
                
                <h2>🔮 Recent Predictions Distribution</h2>
                <div class="chart-container">
                    {prediction_dist_chart}
                </div>
                
                <h2>📋 Detailed Prediction History</h2>
                {self._create_predictions_table(predictions)}
                
                <div class="footer">
                    <p>Generated by FINESE SCHOOL AI Assistant | 
                    Report ID: {datetime.now().strftime('%Y%m%d%H%M%S')}</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        logger.info("Generated student progress report")
        return html
    
    def _create_progress_chart(self, student_data: Dict) -> str:
        """Create learning progress over time chart."""
        # Sample data - in real implementation, fetch from database
        dates = [f"Day {i}" for i in range(1, 11)]
        scores = student_data.get('score_history', [50 + i*3 + np.random.normal(0, 2) for i in range(10)])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=scores,
            mode='lines+markers',
            name='Score',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title='Learning Progress Over Time',
            xaxis_title='Time',
            yaxis_title='Score',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_accuracy_chart(self, accuracy_data: Dict) -> str:
        """Create prediction accuracy visualization."""
        # Prepare data
        categories = list(accuracy_data.get('accuracy_by_type', {}).keys())
        accuracies = list(accuracy_data.get('accuracy_by_type', {}).values())
        
        if not categories:
            categories = ['Overall']
            accuracies = [accuracy_data.get('accuracy_rate', 0)]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=accuracies,
                marker_color=['#2ecc71' if acc >= 70 else '#f39c12' if acc >= 50 else '#e74c3c' 
                             for acc in accuracies]
            )
        ])
        
        fig.update_layout(
            title='Prediction Accuracy by Type',
            xaxis_title='Prediction Type',
            yaxis_title='Accuracy (%)',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_prediction_distribution(self, predictions: List[Dict]) -> str:
        """Create distribution of predicted vs actual outcomes."""
        if not predictions:
            return "<p>No prediction data available</p>"
        
        predicted = [p.get('predicted_value', 0) for p in predictions[:50]]
        actual = [p.get('actual_value', 0) for p in predictions[:50]]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=predicted,
            y=actual,
            mode='markers',
            name='Predictions',
            marker=dict(size=10, color='#9b59b6', opacity=0.6)
        ))
        
        # Add perfect prediction line
        min_val = min(min(predicted), min(actual))
        max_val = max(max(predicted), max(actual))
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='#e74c3c', width=2, dash='dash')
        ))
        
        fig.update_layout(
            title='Predicted vs Actual Outcomes',
            xaxis_title='Predicted Value',
            yaxis_title='Actual Value',
            template='plotly_white',
            height=400
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_student_radar(self, student_data: Dict) -> str:
        """Create student capability radar chart."""
        categories = [
            'Knowledge<br>Retention',
            'Engagement',
            'Practice<br>Frequency',
            'Concept<br>Mastery',
            'Time on<br>Task',
            'Error<br>Pattern',
            'Improvement<br>Velocity',
            'Learning<br>Style Match'
        ]
        
        values = [
            student_data.get('knowledge_retention', 0.5) * 100,
            student_data.get('engagement_score', 0.5) * 100,
            student_data.get('practice_frequency', 0.5) * 100,
            student_data.get('concept_mastery', 0.5) * 100,
            student_data.get('time_on_task', 0.5) * 100,
            (1 - student_data.get('error_pattern_score', 0.5)) * 100,
            student_data.get('improvement_velocity', 0.5) * 100,
            student_data.get('learning_style_match', 0.5) * 100
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Student Profile',
            line=dict(color='#3498db', width=2)
        ))
        
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            title='Student Capability Radar',
            height=500
        )
        
        return fig.to_html(full_html=False, include_plotlyjs='cdn')
    
    def _create_predictions_table(self, predictions: List[Dict]) -> str:
        """Create HTML table of recent predictions."""
        if not predictions:
            return "<p>No prediction history available</p>"
        
        html = """
        <table>
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Predicted</th>
                    <th>Actual</th>
                    <th>Error</th>
                    <th>Accurate?</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for pred in predictions[:20]:  # Show last 20
            date = pred.get('timestamp', 'N/A')[:10]
            ptype = pred.get('prediction_type', 'N/A')
            predicted = f"{pred.get('predicted_value', 0):.2f}"
            actual = f"{pred.get('actual_value', 0):.2f}"
            error = f"{pred.get('error_margin', 0):.2f}"
            accurate = "✅ Yes" if pred.get('is_accurate', False) else "❌ No"
            
            html += f"""
                <tr>
                    <td>{date}</td>
                    <td>{ptype}</td>
                    <td>{predicted}</td>
                    <td>{actual}</td>
                    <td>{error}</td>
                    <td>{accurate}</td>
                </tr>
            """
        
        html += """
            </tbody>
        </table>
        """
        
        return html
    
    def _generate_summary_text(self, student_data: Dict, accuracy_data: Dict) -> str:
        """Generate human-readable summary text."""
        accuracy = accuracy_data.get('accuracy_rate', 0)
        score = student_data.get('overall_score', 0)
        improvement = student_data.get('improvement_rate', 0)
        
        summary = f"The student is currently performing at {score:.1f}% with an improvement rate of {improvement:.1f}%. "
        
        if accuracy >= 80:
            summary += "Our AI predictions are highly reliable (>80% accuracy), providing strong confidence in recommendations. "
        elif accuracy >= 60:
            summary += "AI predictions show moderate reliability (60-80%). Consider manual review of critical decisions. "
        else:
            summary += "AI prediction accuracy needs improvement (<60%). Manual oversight recommended. "
        
        if improvement > 5:
            summary += "The student shows strong positive momentum in their learning journey."
        elif improvement > 0:
            summary += "The student is making steady progress."
        else:
            summary += "Consider adjusting teaching strategies to boost engagement."
        
        return summary
    
    def generate_teacher_dashboard_report(self, class_data: Dict) -> str:
        """
        Generate comprehensive teacher dashboard report for entire class.
        
        Args:
            class_data: Aggregated class performance data
            
        Returns:
            HTML report string
        """
        # Implementation similar to student report but aggregated
        # Would include class-wide trends, at-risk students, etc.
        pass


# Global instance
report_generator = ReportGenerator()


def get_report_generator() -> ReportGenerator:
    """Get the global report generator instance."""
    return report_generator
