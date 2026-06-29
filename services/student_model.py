"""
Probabilistic Student Modeling Service - Uses Monte Carlo simulation for adaptive learning.
Inspired by FORMULA_1_PREDICTOR_STREAMLIT_2026's Monte Carlo prediction system.
"""
import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class StudentProfile:
    """Represents a student's learning profile with multiple dimensions."""
    student_id: int
    knowledge_retention: float = 0.5  # 0-1, how well they retain information
    engagement_score: float = 0.5  # 0-1, current engagement level
    practice_frequency: float = 0.5  # 0-1, how often they practice
    concept_mastery: float = 0.5  # 0-1, overall mastery of current concepts
    time_on_task: float = 0.5  # 0-1, average time spent on tasks
    error_pattern_score: float = 0.5  # 0-1, frequency of errors (lower is better)
    improvement_velocity: float = 0.5  # 0-1, rate of improvement
    learning_style_match: float = 0.5  # 0-1, how well teaching style matches student
    
    def to_vector(self) -> np.ndarray:
        """Convert profile to feature vector."""
        return np.array([
            self.knowledge_retention,
            self.engagement_score,
            self.practice_frequency,
            self.concept_mastery,
            self.time_on_task,
            self.error_pattern_score,
            self.improvement_velocity,
            self.learning_style_match
        ])
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class PredictionResult:
    """Result from Monte Carlo simulation."""
    success_probability: float  # Overall probability of success
    confidence_interval: Tuple[float, float]  # 95% CI
    expected_outcome: float  # Expected score/outcome
    risk_assessment: str  # 'low', 'medium', 'high'
    simulations_run: int
    outcome_distribution: List[float]  # Distribution of possible outcomes
    key_factors: Dict[str, float]  # Impact of each factor
    
    def to_dict(self) -> Dict:
        result = asdict(self)
        result['confidence_interval'] = list(result['confidence_interval'])
        return result


class ProbabilisticStudentModel:
    """
    Uses Monte Carlo simulation to predict student outcomes and adapt difficulty.
    Inspired by F1 Predictor's probabilistic approach with 50,000+ simulations.
    """
    
    def __init__(self, n_simulations: int = 10000):
        """
        Initialize the model.
        
        Args:
            n_simulations: Number of Monte Carlo simulations to run
        """
        self.n_simulations = n_simulations
        
        # Feature weights (can be calibrated over time)
        self.feature_weights = np.array([
            0.20,  # knowledge_retention
            0.15,  # engagement_score
            0.15,  # practice_frequency
            0.20,  # concept_mastery
            0.10,  # time_on_task
            0.10,  # error_pattern_score (inverted)
            0.05,  # improvement_velocity
            0.05   # learning_style_match
        ])
    
    def predict_success_probability(self, student_profile: StudentProfile,
                                   difficulty_level: float = 0.5) -> PredictionResult:
        """
        Predict probability of student success at given difficulty level.
        
        Args:
            student_profile: Student's learning profile
            difficulty_level: Difficulty level (0=easy, 1=hard)
            
        Returns:
            PredictionResult with probabilities and confidence intervals
        """
        # Convert student profile to feature vector
        features = student_profile.to_vector()
        
        # Adjust for difficulty (higher difficulty reduces success probability)
        difficulty_factor = 1.0 - (difficulty_level * 0.3)
        
        # Run Monte Carlo simulation
        outcomes = self._run_simulation(features, difficulty_factor)
        
        # Calculate statistics
        success_threshold = 0.6  # Outcomes above this are considered "success"
        success_count = np.sum(outcomes >= success_threshold)
        success_probability = success_count / len(outcomes)
        
        # Confidence interval (95%)
        ci_lower = np.percentile(outcomes, 2.5)
        ci_upper = np.percentile(outcomes, 97.5)
        
        # Expected outcome
        expected_outcome = np.mean(outcomes)
        
        # Risk assessment
        if success_probability >= 0.8:
            risk = 'low'
        elif success_probability >= 0.5:
            risk = 'medium'
        else:
            risk = 'high'
        
        # Factor importance (sensitivity analysis)
        key_factors = self._calculate_factor_importance(features, difficulty_factor)
        
        result = PredictionResult(
            success_probability=float(success_probability),
            confidence_interval=(float(ci_lower), float(ci_upper)),
            expected_outcome=float(expected_outcome),
            risk_assessment=risk,
            simulations_run=self.n_simulations,
            outcome_distribution=outcomes.tolist()[:100],  # Sample for visualization
            key_factors=key_factors
        )
        
        logger.info(f"Prediction: success_prob={success_probability:.2f}, risk={risk}")
        return result
    
    def recommend_difficulty(self, student_profile: StudentProfile,
                            target_success_rate: float = 0.75) -> float:
        """
        Recommend optimal difficulty level for student.
        Uses binary search to find difficulty that achieves target success rate.
        
        Args:
            student_profile: Student's learning profile
            target_success_rate: Desired probability of success (0-1)
            
        Returns:
            Recommended difficulty level (0-1)
        """
        # Binary search for optimal difficulty
        low, high = 0.0, 1.0
        best_difficulty = 0.5
        
        for _ in range(20):  # 20 iterations gives sufficient precision
            mid = (low + high) / 2
            prediction = self.predict_success_probability(student_profile, mid)
            
            if abs(prediction.success_probability - target_success_rate) < 0.02:
                best_difficulty = mid
                break
            elif prediction.success_probability > target_success_rate:
                low = mid  # Can increase difficulty
                best_difficulty = mid
            else:
                high = mid  # Need to decrease difficulty
        
        logger.info(f"Recommended difficulty: {best_difficulty:.2f} for target {target_success_rate}")
        return best_difficulty
    
    def _run_simulation(self, features: np.ndarray, difficulty_factor: float) -> np.ndarray:
        """
        Run Monte Carlo simulation using vectorized NumPy operations.
        Completes 10,000+ simulations in <1 second.
        
        Args:
            features: Student feature vector
            difficulty_factor: Difficulty adjustment factor
            
        Returns:
            Array of simulated outcomes
        """
        # Generate random variations for each feature (simulating uncertainty)
        # Use normal distribution with std dev based on feature values
        feature_variations = np.random.normal(
            loc=features,
            scale=features * 0.1 + 0.05,  # 10% variation + base noise
            size=(self.n_simulations, len(features))
        )
        
        # Clip to valid range [0, 1]
        feature_variations = np.clip(feature_variations, 0, 1)
        
        # Calculate weighted score for each simulation
        weighted_scores = feature_variations @ self.feature_weights
        
        # Apply difficulty factor
        adjusted_scores = weighted_scores * difficulty_factor
        
        # Add some randomness (unpredictable factors)
        noise = np.random.normal(0, 0.05, size=self.n_simulations)
        final_outcomes = np.clip(adjusted_scores + noise, 0, 1)
        
        return final_outcomes
    
    def _calculate_factor_importance(self, features: np.ndarray, 
                                    difficulty_factor: float) -> Dict[str, float]:
        """
        Calculate importance of each factor using sensitivity analysis.
        
        Args:
            features: Student feature vector
            difficulty_factor: Difficulty adjustment factor
            
        Returns:
            Dictionary mapping factor names to importance scores
        """
        factor_names = [
            'knowledge_retention',
            'engagement_score',
            'practice_frequency',
            'concept_mastery',
            'time_on_task',
            'error_pattern_score',
            'improvement_velocity',
            'learning_style_match'
        ]
        
        importance = {}
        baseline = np.mean(self._run_simulation(features, difficulty_factor))
        
        # Test impact of varying each factor
        for i, name in enumerate(factor_names):
            perturbed_features = features.copy()
            perturbed_features[i] *= 1.1  # Increase by 10%
            
            perturbed_outcome = np.mean(self._run_simulation(perturbed_features, difficulty_factor))
            importance[name] = abs(perturbed_outcome - baseline) / baseline if baseline > 0 else 0
        
        # Normalize importance scores
        total = sum(importance.values())
        if total > 0:
            importance = {k: v/total for k, v in importance.items()}
        
        return importance
    
    def compare_scenarios(self, student_profile: StudentProfile,
                         scenarios: List[Dict]) -> List[PredictionResult]:
        """
        Compare multiple learning scenarios (e.g., different teaching approaches).
        
        Args:
            student_profile: Student's learning profile
            scenarios: List of scenario configurations with difficulty levels
            
        Returns:
            List of predictions for each scenario
        """
        results = []
        for scenario in scenarios:
            difficulty = scenario.get('difficulty', 0.5)
            prediction = self.predict_success_probability(student_profile, difficulty)
            results.append(prediction)
        
        return results
    
    def update_weights_from_data(self, historical_data: List[Dict]):
        """
        Update feature weights based on historical outcome data.
        Simple calibration mechanism.
        
        Args:
            historical_data: List of dicts with features and actual outcomes
        """
        if not historical_data:
            return
        
        # This is a simplified weight update mechanism
        # In production, would use more sophisticated ML techniques
        logger.info(f"Updating weights based on {len(historical_data)} historical records")
        
        # For now, just log that calibration happened
        # Real implementation would use gradient descent or similar


# Global instance
student_model = ProbabilisticStudentModel(n_simulations=10000)


def get_student_model() -> ProbabilisticStudentModel:
    """Get the global student model instance."""
    return student_model
