"""
Adaptive Engine Module
Implements rule-based and ML-driven difficulty adaptation
"""

from typing import Tuple
from config import (DIFFICULTY_LEVELS, ACCURACY_THRESHOLD_HIGH, 
                   ACCURACY_THRESHOLD_LOW, STREAK_THRESHOLD,
                   EARLY_SESSION_MINIMUM, PERFORMANCE_WINDOW)

class AdaptiveEngine:
    """Adaptive engine that decides next difficulty level"""

    def __init__(self, enable_ml: bool = True):
        self.enable_ml = enable_ml
        self.last_decision_reason = ""

    def decide_next_difficulty(self, current_difficulty: str, 
                             tracker) -> Tuple[str, str]:
        """Decide next difficulty level based on performance"""
        total_attempts = len(tracker.attempts)

        if total_attempts < EARLY_SESSION_MINIMUM:
            return current_difficulty, "Early session - maintaining difficulty"

        if self.enable_ml:
            next_diff, reason = self._ml_based_decision(current_difficulty, tracker)
        else:
            next_diff, reason = self._rule_based_decision(current_difficulty, tracker)

        self.last_decision_reason = reason
        return next_diff, reason

    def _rule_based_decision(self, current_difficulty: str, tracker) -> Tuple[str, str]:
        """Rule-based adaptation logic"""
        accuracy = tracker.get_recent_accuracy(PERFORMANCE_WINDOW)
        streak = tracker.get_streak()

        if (accuracy >= ACCURACY_THRESHOLD_HIGH and 
            streak >= STREAK_THRESHOLD and 
            current_difficulty != 'Hard'):
            return self._get_next_level(current_difficulty, +1), \
                   f"Strong performance: {accuracy:.1f}% accuracy, {streak} streak"

        elif (accuracy <= ACCURACY_THRESHOLD_LOW or streak == 0) and \
             current_difficulty != 'Easy':
            return self._get_next_level(current_difficulty, -1), \
                   f"Struggling: {accuracy:.1f}% accuracy"

        else:
            return current_difficulty, \
                   f"Maintaining level: {accuracy:.1f}% accuracy in optimal zone"

    def _ml_based_decision(self, current_difficulty: str, tracker) -> Tuple[str, str]:
        """ML-based adaptation using simple decision tree"""
        accuracy = tracker.get_recent_accuracy(PERFORMANCE_WINDOW)
        streak = tracker.get_streak()

        if accuracy < 50:
            if current_difficulty != 'Easy':
                decision = -1
                reason = f"Accuracy {accuracy:.1f}% below 50% threshold"
            else:
                decision = 0
                reason = "Already at Easy level"

        elif accuracy >= 80 and streak >= 2:
            if current_difficulty != 'Hard':
                decision = +1
                reason = f"High accuracy {accuracy:.1f}% + streak {streak}"
            else:
                decision = 0
                reason = "Already at Hard level"

        elif 60 <= accuracy < 80 and streak >= 1:
            if current_difficulty == 'Easy':
                decision = +1
                reason = f"Solid performance: {accuracy:.1f}% accuracy ready for challenge"
            else:
                decision = 0
                reason = f"Solid performance: {accuracy:.1f}% maintaining level"

        else:
            decision = 0
            reason = f"Balanced performance: {accuracy:.1f}% accuracy, maintaining level"

        next_difficulty = self._get_next_level(current_difficulty, decision)
        return next_difficulty, reason

    def _get_next_level(self, current: str, change: int) -> str:
        """Get next difficulty level"""
        levels = ['Easy', 'Medium', 'Hard']
        current_idx = levels.index(current)
        next_idx = max(0, min(2, current_idx + change))
        return levels[next_idx]

    def get_confidence_score(self, tracker) -> float:
        """Get confidence in current adaptation decision (0-1)"""
        if len(tracker.attempts) < 3:
            return 0.0

        accuracy = tracker.get_recent_accuracy(PERFORMANCE_WINDOW)
        consistency = 1.0 - (abs(accuracy - 75) / 100)

        return max(0, min(1, consistency))
