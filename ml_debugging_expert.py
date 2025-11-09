"""
ML Debugging Expert System
Core expert system with rules for diagnosing ML training issues
"""

# Ensure backwards compatibility for older packages that reference
# `collections.Mapping` on newer Python versions (Mapping moved to
# `collections.abc`). The `compat` module provides aliases when
# necessary and must be imported before importing `experta`.
import compat  # noqa: F401 (module side-effects)
from experta import *
import json

class MLMetrics(Fact):
    """Fact to store ML training metrics"""
    pass

class MLDebugExpert(KnowledgeEngine):
    """Expert system for diagnosing ML training issues"""
    
    def __init__(self):
        super().__init__()
        self.diagnoses = []
        self.recommendations = []
    
    # Rule 1: Overfitting Detection
    @Rule(MLMetrics(train_accuracy=MATCH.ta, test_accuracy=MATCH.tea),
          TEST(lambda ta, tea: ta - tea > 15))
    def overfitting(self, ta, tea):
        diagnosis = f"OVERFITTING DETECTED: Train accuracy ({ta}%) significantly higher than test accuracy ({tea}%)"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Add regularization (L1/L2)",
            "Increase dropout rate (try 0.3-0.5)",
            "Use data augmentation",
            "Reduce model complexity",
            "Get more training data"
        ])
        self.declare(Fact(issue="overfitting"))
    
    # Rule 2: Underfitting Detection
    @Rule(MLMetrics(train_accuracy=MATCH.ta, test_accuracy=MATCH.tea),
          TEST(lambda ta, tea: ta < 70 and abs(ta - tea) < 10))
    def underfitting(self, ta, tea):
        diagnosis = f"UNDERFITTING DETECTED: Both train ({ta}%) and test ({tea}%) accuracy are low"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Increase model complexity",
            "Add more features",
            "Train for more epochs",
            "Reduce regularization",
            "Check if data preprocessing is correct"
        ])
        self.declare(Fact(issue="underfitting"))
    
    # Rule 3: Learning Rate Too High
    @Rule(MLMetrics(loss_oscillation=MATCH.osc),
          TEST(lambda osc: osc == "high"))
    def lr_too_high(self):
        diagnosis = "LEARNING RATE TOO HIGH: Loss is oscillating significantly"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Reduce learning rate by factor of 10 (e.g., 0.01 -> 0.001)",
            "Use learning rate scheduler",
            "Try Adam optimizer with default LR (0.001)"
        ])
        self.declare(Fact(issue="lr_high"))
    
    # Rule 4: Learning Rate Too Low
    @Rule(MLMetrics(convergence_speed=MATCH.speed),
          TEST(lambda speed: speed == "very_slow"))
    def lr_too_low(self):
        diagnosis = "LEARNING RATE TOO LOW: Model is converging very slowly"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Increase learning rate gradually",
            "Try learning rate finder",
            "Use cyclic learning rate"
        ])
        self.declare(Fact(issue="lr_low"))
    
    # Rule 5: Small Dataset Issue
    @Rule(MLMetrics(dataset_size=MATCH.size),
          TEST(lambda size: size < 1000))
    def small_dataset(self, size):
        diagnosis = f"SMALL DATASET WARNING: Only {size} samples may not be sufficient"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Use data augmentation heavily",
            "Consider transfer learning",
            "Use simpler model architecture",
            "Collect more data if possible"
        ])
        self.declare(Fact(issue="small_data"))
    
    # Rule 6: Batch Size Issue (Too Small)
    @Rule(MLMetrics(batch_size=MATCH.bs, dataset_size=MATCH.ds),
          TEST(lambda bs, ds: bs < 16 and ds > 1000))
    def batch_too_small(self, bs):
        diagnosis = f"BATCH SIZE TOO SMALL: Batch size of {bs} may cause noisy gradients"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Increase batch size to 32-128",
            "Use gradient accumulation if memory limited",
            "Adjust learning rate proportionally"
        ])
        self.declare(Fact(issue="small_batch"))
    
    # Rule 7: Good Performance
    @Rule(MLMetrics(train_accuracy=MATCH.ta, test_accuracy=MATCH.tea),
          TEST(lambda ta, tea: ta >= 85 and tea >= 80 and abs(ta - tea) <= 10))
    def good_performance(self, ta, tea):
        diagnosis = f"GOOD MODEL: Train ({ta}%) and test ({tea}%) accuracy are both high and balanced"
        self.diagnoses.append(diagnosis)
        self.recommendations.extend([
            "Model is performing well!",
            "Consider fine-tuning hyperparameters for marginal improvements",
            "Monitor for overfitting with more epochs"
        ])
        self.declare(Fact(issue="good"))
    
    def get_results(self):
        """Return diagnosis and recommendations"""
        return {
            "diagnoses": self.diagnoses,
            "recommendations": list(set(self.recommendations)),  # Remove duplicates
            "issues_found": len(self.diagnoses)
        }
    
    def reset_results(self):
        """Reset diagnosis and recommendations"""
        self.diagnoses = []
        self.recommendations = []


def run_diagnosis(metrics):
    """
    Run expert system diagnosis on given metrics
    
    Args:
        metrics (dict): Dictionary containing ML training metrics
        
    Returns:
        dict: Diagnosis results and recommendations
    """
    engine = MLDebugExpert()
    engine.reset()
    engine.reset_results()
    
    # Declare facts
    engine.declare(MLMetrics(**metrics))
    
    # Run inference
    engine.run()
    
    return engine.get_results()


# Example usage
if __name__ == "__main__":
    # Test Case 1: Overfitting
    print("=" * 60)
    print("TEST CASE 1: Overfitting Scenario")
    print("=" * 60)
    metrics1 = {
        "train_accuracy": 95,
        "test_accuracy": 68,
        "dataset_size": 5000,
        "batch_size": 32
    }
    result1 = run_diagnosis(metrics1)
    print(json.dumps(result1, indent=2))
    
    print("\n" + "=" * 60)
    print("TEST CASE 2: Underfitting Scenario")
    print("=" * 60)
    metrics2 = {
        "train_accuracy": 65,
        "test_accuracy": 63,
        "dataset_size": 5000,
        "batch_size": 32
    }
    result2 = run_diagnosis(metrics2)
    print(json.dumps(result2, indent=2))
    
    print("\n" + "=" * 60)
    print("TEST CASE 3: Good Model")
    print("=" * 60)
    metrics3 = {
        "train_accuracy": 92,
        "test_accuracy": 88,
        "dataset_size": 5000,
        "batch_size": 64
    }
    result3 = run_diagnosis(metrics3)
    print(json.dumps(result3, indent=2))