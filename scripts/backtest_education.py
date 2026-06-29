"""
Backtesting Script - Test educational prediction models against historical data.
Inspired by FORMULA_1_PREDICTOR_STREAMLIT_2026's backtesting framework.

Usage:
    python scripts/backtest_education.py --days 30
    python scripts/backtest_education.py --student-id 123
"""
import sys
import os
import argparse
import json
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.accuracy_tracker import AccuracyTracker
from services.student_model import ProbabilisticStudentModel, StudentProfile


def run_backtest(days: int = 30, student_id: int = None):
    """
    Run backtesting on historical student data.
    
    Args:
        days: Number of days to look back
        student_id: Optional specific student to test
    """
    print("=" * 80)
    print("FINESE SCHOOL - Educational Model Backtesting")
    print("=" * 80)
    print(f"Period: Last {days} days")
    if student_id:
        print(f"Student ID: {student_id}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Initialize services
    tracker = AccuracyTracker()
    model = ProbabilisticStudentModel(n_simulations=5000)
    
    # Get historical predictions
    predictions = tracker.get_recent_predictions(
        student_id=student_id,
        limit=1000
    )
    
    if not predictions:
        print("\n❌ No historical prediction data found.")
        return
    
    print(f"\n📊 Found {len(predictions)} historical predictions")
    
    # Calculate metrics
    metrics = tracker.calculate_metrics(days=days, student_id=student_id)
    
    print("\n" + "=" * 80)
    print("OVERALL METRICS")
    print("=" * 80)
    print(f"Total Predictions:     {metrics.total_predictions}")
    print(f"Accurate Predictions:  {metrics.accurate_predictions}")
    print(f"Accuracy Rate:         {metrics.accuracy_rate:.2f}%")
    print(f"Mean Absolute Error:   {metrics.mean_absolute_error:.4f}")
    print(f"Mean Squared Error:    {metrics.mean_squared_error:.4f}")
    
    print("\n" + "=" * 80)
    print("ACCURACY BY PREDICTION TYPE")
    print("=" * 80)
    for ptype, acc in metrics.accuracy_by_type.items():
        count = metrics.predictions_by_type.get(ptype, 0)
        status = "✅" if acc >= 70 else "⚠️" if acc >= 50 else "❌"
        print(f"{status} {ptype:20s}: {acc:6.2f}% ({count} predictions)")
    
    # Trend analysis
    trend = tracker.get_trend_analysis(days=days)
    
    print("\n" + "=" * 80)
    print("TREND ANALYSIS")
    print("=" * 80)
    print(f"Trend Direction:       {trend['trend_direction']}")
    print(f"Trend Magnitude:       {trend['trend_magnitude']:.2f}%")
    print(f"Overall Accuracy:      {trend['overall_accuracy']:.2f}%")
    print(f"Days Analyzed:         {trend['total_days']}")
    
    if trend['trend_direction'] == 'improving':
        print("\n✅ Model performance is IMPROVING over time")
    elif trend['trend_direction'] == 'declining':
        print("\n⚠️ WARNING: Model performance is DECLINING - recalibration needed")
    else:
        print("\n⚠️ Insufficient data for trend analysis")
    
    # Calibration recommendations
    print("\n" + "=" * 80)
    print("CALIBRATION RECOMMENDATIONS")
    print("=" * 80)
    
    for ptype in metrics.accuracy_by_type.keys():
        calibration = tracker.calibrate_model(ptype)
        if calibration.get('calibrated'):
            print(f"\n{ptype}:")
            print(f"  Correction Factor: {calibration['correction_factor']:+.4f}")
            print(f"  Sample Size: {calibration['sample_size']}")
            print(f"  Recommendation: {calibration['recommendation']}")
    
    # Export results
    export_data = tracker.export_to_json(student_id=student_id)
    output_file = f"backtest_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(output_file, 'w') as f:
        f.write(export_data)
    
    print(f"\n" + "=" * 80)
    print(f"📄 Results exported to: {output_file}")
    print("=" * 80)
    
    # Summary and recommendations
    print("\n" + "=" * 80)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    
    if metrics.accuracy_rate >= 80:
        print("✅ EXCELLENT: Model accuracy is above 80%")
        print("   → Continue current approach")
        print("   → Consider expanding to more prediction types")
    elif metrics.accuracy_rate >= 60:
        print("⚠️ GOOD: Model accuracy is acceptable (60-80%)")
        print("   → Monitor trends closely")
        print("   → Apply calibration corrections")
        print("   → Gather more training data")
    else:
        print("❌ NEEDS IMPROVEMENT: Model accuracy below 60%")
        print("   → Immediate recalibration required")
        print("   → Review feature weights")
        print("   → Collect more high-quality training data")
        print("   → Consider manual oversight until accuracy improves")
    
    print("\n" + "=" * 80)
    print("Backtesting completed successfully!")
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description='Backtest educational prediction models')
    parser.add_argument('--days', type=int, default=30, help='Number of days to look back (default: 30)')
    parser.add_argument('--student-id', type=int, default=None, help='Specific student ID to test')
    
    args = parser.parse_args()
    
    try:
        run_backtest(days=args.days, student_id=args.student_id)
    except Exception as e:
        print(f"\n❌ Error during backtesting: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
