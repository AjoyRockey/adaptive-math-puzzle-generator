"""
Configuration Constants for Math Adaptive Learning System
"""

# Difficulty Levels
DIFFICULTY_LEVELS = {
    'Easy': 0,
    'Medium': 1,
    'Hard': 2
}

# Operand Ranges by Difficulty
OPERAND_RANGES = {
    'Easy': {'min': 1, 'max': 10},
    'Medium': {'min': 5, 'max': 50},
    'Hard': {'min': 10, 'max': 100}
}

# Operations
OPERATIONS = ['+', '-', '*', '/']
OPERATION_WEIGHTS = [0.25, 0.25, 0.25, 0.25]

# Thresholds
RESPONSE_TIME_THRESHOLD = 10.0  # seconds
ACCURACY_THRESHOLD_HIGH = 80
ACCURACY_THRESHOLD_LOW = 50
STREAK_THRESHOLD = 2

# Adaptation Parameters
EARLY_SESSION_MINIMUM = 3  # Don't adapt in first N questions
PERFORMANCE_WINDOW = 5  # Use last N questions for metrics
HYSTERESIS_ENABLED = True  # Prevent oscillation

# Display Settings
SHOW_RESPONSE_TIME = True
SHOW_METRICS_AFTER_QUESTION = True
DECIMAL_PLACES = 2
