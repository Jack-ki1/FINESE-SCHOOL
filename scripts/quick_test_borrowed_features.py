"""
Quick Test Script - Verify all borrowed features from F1 Predictor are working.
Inspired by FORMULA_1_PREDICTOR_STREAMLIT_2026's quick_test.py

Usage:
    python scripts/quick_test_borrowed_features.py
"""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_accuracy_tracker():
    """Test accuracy tracking service."""
    print("\n" + "="*80)
    print("Testing Accuracy Tracker Service")
    print("="*80)
    
    try:
        from services.accuracy_tracker import AccuracyTracker
        
        # Use a temporary file instead of in-memory for better compatibility
        import tempfile
        temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        temp_db.close()
        
        tracker = AccuracyTracker(db_path=temp_db.name)
        
        # Record some test predictions
        print("✓ Recording test predictions...")
        for i in range(5):
            tracker.record_prediction(
                student_id=1,
                prediction_type='mastery',
                predicted_value=0.7 + i*0.05,
                actual_value=0.75,
                confidence_score=0.8,
                context={'test': True}
            )
        
        print("✓ Calculating metrics...")
        metrics = tracker.calculate_metrics(days=7, student_id=1)
        print(f"  - Total predictions: {metrics.total_predictions}")
        print(f"  - Accuracy rate: {metrics.accuracy_rate:.2f}%")
        print(f"  - Mean absolute error: {metrics.mean_absolute_error:.4f}")
        
        print("✓ Getting trend analysis...")
        trend = tracker.get_trend_analysis(days=7)
        print(f"  - Trend direction: {trend['trend_direction']}")
        print(f"  - Days analyzed: {trend['total_days']}")
        
        print("✓ Checking thresholds...")
        alerts = tracker.check_accuracy_thresholds(threshold=70.0)
        print(f"  - Alerts generated: {len(alerts)}")
        
        print("✓ Exporting to JSON...")
        export_data = tracker.export_to_json(student_id=1)
        data = json.loads(export_data)
        print(f"  - Export size: {len(export_data)} bytes")
        
        # Clean up temp file
        import os
        os.unlink(temp_db.name)
        
        print("\n✅ Accuracy Tracker: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Accuracy Tracker: TEST FAILED")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_student_model():
    """Test probabilistic student modeling."""
    print("\n" + "="*80)
    print("Testing Probabilistic Student Model")
    print("="*80)
    
    try:
        from services.student_model import ProbabilisticStudentModel, StudentProfile
        
        model = ProbabilisticStudentModel(n_simulations=1000)  # Smaller for testing
        
        # Create test student profile
        print("✓ Creating student profile...")
        profile = StudentProfile(
            student_id=1,
            knowledge_retention=0.7,
            engagement_score=0.8,
            practice_frequency=0.6,
            concept_mastery=0.75,
            time_on_task=0.65,
            error_pattern_score=0.3,
            improvement_velocity=0.5,
            learning_style_match=0.8
        )
        
        print("✓ Running prediction simulation...")
        prediction = model.predict_success_probability(profile, difficulty_level=0.5)
        print(f"  - Success probability: {prediction.success_probability:.2%}")
        print(f"  - Confidence interval: {prediction.confidence_interval}")
        print(f"  - Expected outcome: {prediction.expected_outcome:.2f}")
        print(f"  - Risk assessment: {prediction.risk_assessment}")
        print(f"  - Simulations run: {prediction.simulations_run}")
        
        print("✓ Recommending difficulty level...")
        recommended = model.recommend_difficulty(profile, target_success_rate=0.75)
        print(f"  - Recommended difficulty: {recommended:.2f}")
        
        print("✓ Comparing scenarios...")
        scenarios = [
            {'difficulty': 0.3, 'name': 'Easy'},
            {'difficulty': 0.5, 'name': 'Medium'},
            {'difficulty': 0.7, 'name': 'Hard'}
        ]
        results = model.compare_scenarios(profile, scenarios)
        for i, result in enumerate(results):
            print(f"  - Scenario {i+1}: {result.success_probability:.2%} success")
        
        print("\n✅ Student Model: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Student Model: TEST FAILED")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_report_generator():
    """Test report generation service."""
    print("\n" + "="*80)
    print("Testing Report Generator Service")
    print("="*80)
    
    try:
        from services.report_generator import ReportGenerator
        
        reporter = ReportGenerator()
        
        # Prepare test data
        print("✓ Preparing test data...")
        student_data = {
            'name': 'Test Student',
            'overall_score': 75.5,
            'improvement_rate': 5.2,
            'knowledge_retention': 0.7,
            'engagement_score': 0.8,
            'practice_frequency': 0.6,
            'concept_mastery': 0.75,
            'time_on_task': 0.65,
            'error_pattern_score': 0.3,
            'improvement_velocity': 0.5,
            'learning_style_match': 0.8,
            'score_history': [50 + i*2.5 for i in range(10)]
        }
        
        accuracy_data = {
            'accuracy_rate': 78.5,
            'accuracy_by_type': {
                'mastery': 80.0,
                'engagement': 75.0,
                'difficulty': 82.0
            },
            'predictions_by_type': {
                'mastery': 50,
                'engagement': 45,
                'difficulty': 55
            }
        }
        
        predictions = [
            {
                'timestamp': '2026-06-29T10:00:00',
                'prediction_type': 'mastery',
                'predicted_value': 0.75,
                'actual_value': 0.80,
                'error_margin': 0.05,
                'is_accurate': True
            }
            for _ in range(10)
        ]
        
        print("✓ Generating student progress report...")
        html = reporter.generate_student_progress_report(
            student_data=student_data,
            accuracy_data=accuracy_data,
            predictions=predictions
        )
        
        print(f"  - Report size: {len(html)} characters")
        print(f"  - Contains Plotly charts: {'plotly' in html.lower()}")
        print(f"  - Contains metric cards: {'metric-card' in html.lower()}")
        print(f"  - Contains radar chart: {'scatterpolar' in html.lower()}")
        
        # Save test report with UTF-8 encoding
        output_file = "test_report.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"  - Saved to: {output_file}")
        
        print("\n✅ Report Generator: ALL TESTS PASSED")
        return True
        
    except Exception as e:
        print(f"\n❌ Report Generator: TEST FAILED")
        print(f"   Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_imports():
    """Test that all modules can be imported."""
    print("\n" + "="*80)
    print("Testing Module Imports")
    print("="*80)
    
    modules = [
        ('services.accuracy_tracker', 'AccuracyTracker'),
        ('services.student_model', 'ProbabilisticStudentModel'),
        ('services.report_generator', 'ReportGenerator'),
    ]
    
    all_passed = True
    
    for module_name, class_name in modules:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"✓ {module_name}.{class_name}")
        except Exception as e:
            print(f"❌ {module_name}.{class_name}: {e}")
            all_passed = False
    
    if all_passed:
        print("\n✅ All imports successful")
    else:
        print("\n❌ Some imports failed")
    
    return all_passed


def main():
    print("="*80)
    print("FINESE SCHOOL - Borrowed Features Quick Test")
    print("Inspired by FORMULA_1_PREDICTOR_STREAMLIT_2026")
    print("="*80)
    print(f"Started at: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Test imports first
    results.append(("Module Imports", test_imports()))
    
    # Test individual services
    results.append(("Accuracy Tracker", test_accuracy_tracker()))
    results.append(("Student Model", test_student_model()))
    results.append(("Report Generator", test_report_generator()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status:12s} - {name}")
    
    print("="*80)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Borrowed features are working correctly.")
        print("="*80)
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        print("="*80)
        return 1


if __name__ == '__main__':
    sys.exit(main())
