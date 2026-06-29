"""
Accuracy Tracking Service - Monitors AI prediction performance for student outcomes.
Inspired by FORMULA_1_PREDICTOR_STREAMLIT_2026 accuracy tracking system.
"""
import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import os

logger = logging.getLogger(__name__)


@dataclass
class PredictionRecord:
    """Represents a single prediction and its actual outcome."""
    id: Optional[int] = None
    timestamp: str = ""
    student_id: int = 0
    prediction_type: str = ""  # 'difficulty', 'success_rate', 'mastery', 'engagement'
    predicted_value: float = 0.0
    actual_value: float = 0.0
    confidence_score: float = 0.0
    context: str = "{}"  # JSON string with additional context
    is_accurate: bool = False
    error_margin: float = 0.0
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class AccuracyMetrics:
    """Aggregated accuracy metrics over a time period."""
    period_start: str = ""
    period_end: str = ""
    total_predictions: int = 0
    accurate_predictions: int = 0
    accuracy_rate: float = 0.0
    mean_absolute_error: float = 0.0
    mean_squared_error: float = 0.0
    predictions_by_type: Dict[str, int] = None
    accuracy_by_type: Dict[str, float] = None
    
    def __post_init__(self):
        if self.predictions_by_type is None:
            self.predictions_by_type = {}
        if self.accuracy_by_type is None:
            self.accuracy_by_type = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)


class AccuracyTracker:
    """
    Tracks and analyzes AI prediction accuracy for student learning outcomes.
    Inspired by F1 Predictor's real-time accuracy monitoring system.
    """
    
    def __init__(self, db_path: str = "finese_school.db"):
        self.db_path = db_path
        self._ensure_tables_exist()
    
    def _get_connection(self):
        """Get database connection."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")  # Enable WAL mode for better concurrency
        return conn
    
    def _ensure_tables_exist(self):
        """Create accuracy tracking tables if they don't exist."""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            logger.info(f"Creating accuracy tracking tables in {self.db_path}")
            
            # Main predictions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accuracy_predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    student_id INTEGER NOT NULL,
                    prediction_type TEXT NOT NULL,
                    predicted_value REAL NOT NULL,
                    actual_value REAL NOT NULL,
                    confidence_score REAL DEFAULT 0.5,
                    context TEXT DEFAULT '{}',
                    is_accurate BOOLEAN DEFAULT 0,
                    error_margin REAL DEFAULT 0.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Aggregated metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accuracy_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    period_start TEXT NOT NULL,
                    period_end TEXT NOT NULL,
                    metric_type TEXT NOT NULL,
                    total_predictions INTEGER DEFAULT 0,
                    accurate_predictions INTEGER DEFAULT 0,
                    accuracy_rate REAL DEFAULT 0.0,
                    mean_absolute_error REAL DEFAULT 0.0,
                    mean_squared_error REAL DEFAULT 0.0,
                    predictions_by_type TEXT DEFAULT '{}',
                    accuracy_by_type TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS accuracy_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    alert_type TEXT NOT NULL,
                    severity TEXT NOT NULL,
                    message TEXT NOT NULL,
                    metric_value REAL DEFAULT 0.0,
                    threshold REAL DEFAULT 0.0,
                    is_resolved BOOLEAN DEFAULT 0,
                    resolved_at TEXT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Accuracy tracking tables created successfully")
        except Exception as e:
            logger.error(f"Error creating accuracy tracking tables: {e}")
            raise
    
    def record_prediction(self, student_id: int, prediction_type: str, 
                         predicted_value: float, actual_value: float,
                         confidence_score: float = 0.5, context: Dict = None) -> int:
        """
        Record a prediction and its actual outcome.
        
        Args:
            student_id: ID of the student
            prediction_type: Type of prediction ('difficulty', 'success_rate', 'mastery', 'engagement')
            predicted_value: The predicted value (0-1 scale)
            actual_value: The actual observed value (0-1 scale)
            confidence_score: Model's confidence in the prediction (0-1)
            context: Additional context information
            
        Returns:
            ID of the recorded prediction
        """
        if context is None:
            context = {}
        
        # Calculate accuracy (within 10% margin is considered accurate)
        error_margin = abs(predicted_value - actual_value)
        is_accurate = error_margin <= 0.1
        
        record = PredictionRecord(
            timestamp=datetime.now().isoformat(),
            student_id=student_id,
            prediction_type=prediction_type,
            predicted_value=predicted_value,
            actual_value=actual_value,
            confidence_score=confidence_score,
            context=json.dumps(context),
            is_accurate=is_accurate,
            error_margin=error_margin
        )
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO accuracy_predictions 
            (timestamp, student_id, prediction_type, predicted_value, actual_value,
             confidence_score, context, is_accurate, error_margin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (record.timestamp, record.student_id, record.prediction_type,
              record.predicted_value, record.actual_value, record.confidence_score,
              record.context, record.is_accurate, record.error_margin))
        
        prediction_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Recorded prediction #{prediction_id}: {prediction_type} for student {student_id}")
        return prediction_id
    
    def get_recent_predictions(self, student_id: Optional[int] = None,
                              prediction_type: Optional[str] = None,
                              limit: int = 100) -> List[PredictionRecord]:
        """
        Get recent prediction records with optional filtering.
        
        Args:
            student_id: Filter by specific student
            prediction_type: Filter by prediction type
            limit: Maximum number of records to return
            
        Returns:
            List of PredictionRecord objects
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM accuracy_predictions WHERE 1=1"
        params = []
        
        if student_id is not None:
            query += " AND student_id = ?"
            params.append(student_id)
        
        if prediction_type is not None:
            query += " AND prediction_type = ?"
            params.append(prediction_type)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        predictions = []
        for row in rows:
            pred = PredictionRecord(
                id=row['id'],
                timestamp=row['timestamp'],
                student_id=row['student_id'],
                prediction_type=row['prediction_type'],
                predicted_value=row['predicted_value'],
                actual_value=row['actual_value'],
                confidence_score=row['confidence_score'],
                context=row['context'],
                is_accurate=bool(row['is_accurate']),
                error_margin=row['error_margin']
            )
            predictions.append(pred)
        
        return predictions
    
    def calculate_metrics(self, days: int = 7, student_id: Optional[int] = None) -> AccuracyMetrics:
        """
        Calculate aggregated accuracy metrics over a time period.
        
        Args:
            days: Number of days to look back
            student_id: Optional filter for specific student
            
        Returns:
            AccuracyMetrics object with aggregated statistics
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        end_date = datetime.now().isoformat()
        
        # Base query
        query = '''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN is_accurate THEN 1 ELSE 0 END) as accurate,
                AVG(error_margin) as mae,
                AVG(error_margin * error_margin) as mse
            FROM accuracy_predictions
            WHERE timestamp >= ?
        '''
        params = [start_date]
        
        if student_id is not None:
            query += " AND student_id = ?"
            params.append(student_id)
        
        cursor.execute(query, params)
        row = cursor.fetchone()
        
        total = row['total'] or 0
        accurate = row['accurate'] or 0
        mae = row['mae'] or 0.0
        mse = row['mse'] or 0.0
        
        accuracy_rate = (accurate / total * 100) if total > 0 else 0.0
        
        # Get breakdown by prediction type
        type_query = '''
            SELECT prediction_type, 
                   COUNT(*) as count,
                   SUM(CASE WHEN is_accurate THEN 1 ELSE 0 END) as accurate_count
            FROM accuracy_predictions
            WHERE timestamp >= ?
        '''
        type_params = [start_date]
        
        if student_id is not None:
            type_query += " AND student_id = ?"
            type_params.append(student_id)
        
        type_query += " GROUP BY prediction_type"
        
        cursor.execute(type_query, type_params)
        type_rows = cursor.fetchall()
        
        predictions_by_type = {}
        accuracy_by_type = {}
        
        for type_row in type_rows:
            ptype = type_row['prediction_type']
            pcount = type_row['count']
            paccurate = type_row['accurate_count']
            
            predictions_by_type[ptype] = pcount
            accuracy_by_type[ptype] = (paccurate / pcount * 100) if pcount > 0 else 0.0
        
        conn.close()
        
        metrics = AccuracyMetrics(
            period_start=start_date,
            period_end=end_date,
            total_predictions=total,
            accurate_predictions=accurate,
            accuracy_rate=accuracy_rate,
            mean_absolute_error=mae,
            mean_squared_error=mse,
            predictions_by_type=predictions_by_type,
            accuracy_by_type=accuracy_by_type
        )
        
        # Save metrics to database
        self._save_metrics(metrics)
        
        return metrics
    
    def _save_metrics(self, metrics: AccuracyMetrics):
        """Save calculated metrics to database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO accuracy_metrics
            (period_start, period_end, metric_type, total_predictions,
             accurate_predictions, accuracy_rate, mean_absolute_error,
             mean_squared_error, predictions_by_type, accuracy_by_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.period_start,
            metrics.period_end,
            'weekly',
            metrics.total_predictions,
            metrics.accurate_predictions,
            metrics.accuracy_rate,
            metrics.mean_absolute_error,
            metrics.mean_squared_error,
            json.dumps(metrics.predictions_by_type),
            json.dumps(metrics.accuracy_by_type)
        ))
        
        conn.commit()
        conn.close()
    
    def check_accuracy_thresholds(self, threshold: float = 70.0) -> List[Dict]:
        """
        Check if accuracy has dropped below threshold and generate alerts.
        
        Args:
            threshold: Minimum acceptable accuracy percentage
            
        Returns:
            List of generated alerts
        """
        metrics = self.calculate_metrics(days=7)
        alerts = []
        
        if metrics.accuracy_rate < threshold:
            alert = self._create_alert(
                alert_type='low_accuracy',
                severity='warning',
                message=f'Prediction accuracy dropped to {metrics.accuracy_rate:.1f}% (threshold: {threshold}%)',
                metric_value=metrics.accuracy_rate,
                threshold=threshold
            )
            alerts.append(alert)
        
        # Check individual prediction types
        for ptype, acc in metrics.accuracy_by_type.items():
            if acc < threshold:
                alert = self._create_alert(
                    alert_type=f'low_accuracy_{ptype}',
                    severity='warning',
                    message=f'{ptype} prediction accuracy dropped to {acc:.1f}% (threshold: {threshold}%)',
                    metric_value=acc,
                    threshold=threshold
                )
                alerts.append(alert)
        
        return alerts
    
    def _create_alert(self, alert_type: str, severity: str, message: str,
                     metric_value: float, threshold: float) -> Dict:
        """Create and save an alert."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        
        cursor.execute('''
            INSERT INTO accuracy_alerts
            (timestamp, alert_type, severity, message, metric_value, threshold)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (timestamp, alert_type, severity, message, metric_value, threshold))
        
        alert_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        alert = {
            'id': alert_id,
            'timestamp': timestamp,
            'alert_type': alert_type,
            'severity': severity,
            'message': message,
            'metric_value': metric_value,
            'threshold': threshold,
            'is_resolved': False
        }
        
        logger.warning(f"Alert created: {message}")
        return alert
    
    def get_trend_analysis(self, days: int = 30) -> Dict:
        """
        Analyze accuracy trends over time to see if model is improving.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend analysis results
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get daily accuracy for the past N days
        cursor.execute('''
            SELECT DATE(timestamp) as day,
                   COUNT(*) as total,
                   SUM(CASE WHEN is_accurate THEN 1 ELSE 0 END) as accurate,
                   AVG(error_margin) as avg_error
            FROM accuracy_predictions
            WHERE timestamp >= datetime('now', ? || ' days')
            GROUP BY DATE(timestamp)
            ORDER BY day ASC
        ''', (f'-{days}',))
        
        rows = cursor.fetchall()
        conn.close()
        
        daily_data = []
        for row in rows:
            daily_data.append({
                'date': row['day'],
                'total_predictions': row['total'],
                'accurate_predictions': row['accurate'],
                'accuracy_rate': (row['accurate'] / row['total'] * 100) if row['total'] > 0 else 0,
                'avg_error': row['avg_error']
            })
        
        # Calculate trend
        if len(daily_data) >= 2:
            first_half = daily_data[:len(daily_data)//2]
            second_half = daily_data[len(daily_data)//2:]
            
            first_avg = sum(d['accuracy_rate'] for d in first_half) / len(first_half)
            second_avg = sum(d['accuracy_rate'] for d in second_half) / len(second_half)
            
            trend_direction = 'improving' if second_avg > first_avg else 'declining'
            trend_magnitude = abs(second_avg - first_avg)
        else:
            trend_direction = 'insufficient_data'
            trend_magnitude = 0.0
        
        return {
            'daily_data': daily_data,
            'trend_direction': trend_direction,
            'trend_magnitude': trend_magnitude,
            'overall_accuracy': sum(d['accuracy_rate'] for d in daily_data) / len(daily_data) if daily_data else 0,
            'total_days': len(daily_data)
        }
    
    def export_to_json(self, student_id: Optional[int] = None) -> str:
        """
        Export accuracy data to JSON format.
        
        Args:
            student_id: Optional filter for specific student
            
        Returns:
            JSON string with accuracy data
        """
        predictions = self.get_recent_predictions(student_id=student_id, limit=1000)
        metrics = self.calculate_metrics(days=30, student_id=student_id)
        trend = self.get_trend_analysis(days=30)
        
        export_data = {
            'exported_at': datetime.now().isoformat(),
            'metrics': metrics.to_dict(),
            'trend_analysis': trend,
            'recent_predictions': [p.to_dict() for p in predictions]
        }
        
        return json.dumps(export_data, indent=2)
    
    def calibrate_model(self, prediction_type: str) -> Dict:
        """
        Calibrate prediction model based on historical accuracy.
        Adjusts future predictions based on systematic biases.
        
        Args:
            prediction_type: Type of prediction to calibrate
            
        Returns:
            Calibration parameters
        """
        predictions = self.get_recent_predictions(
            prediction_type=prediction_type,
            limit=500
        )
        
        if not predictions:
            return {'calibrated': False, 'reason': 'No data available'}
        
        # Calculate systematic bias
        biases = [p.actual_value - p.predicted_value for p in predictions]
        avg_bias = sum(biases) / len(biases)
        
        # Calculate correction factor
        correction_factor = avg_bias
        
        # Calculate confidence adjustment
        high_conf = [p for p in predictions if p.confidence_score > 0.8]
        low_conf = [p for p in predictions if p.confidence_score < 0.5]
        
        high_conf_accuracy = sum(1 for p in high_conf if p.is_accurate) / len(high_conf) if high_conf else 0
        low_conf_accuracy = sum(1 for p in low_conf if p.is_accurate) / len(low_conf) if low_conf else 0
        
        calibration = {
            'calibrated': True,
            'prediction_type': prediction_type,
            'correction_factor': correction_factor,
            'avg_bias': avg_bias,
            'sample_size': len(predictions),
            'high_confidence_accuracy': high_conf_accuracy,
            'low_confidence_accuracy': low_conf_accuracy,
            'recommendation': 'Adjust predictions by adding correction_factor'
        }
        
        logger.info(f"Calibration complete for {prediction_type}: correction_factor={correction_factor:.3f}")
        return calibration


# Global instance
accuracy_tracker = AccuracyTracker()


def get_accuracy_tracker() -> AccuracyTracker:
    """Get the global accuracy tracker instance."""
    return accuracy_tracker
