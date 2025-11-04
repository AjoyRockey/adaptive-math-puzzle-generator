"""
Performance Tracker Module
Tracks and aggregates user performance metrics
"""

from typing import Dict, List
from datetime import datetime
from config import PERFORMANCE_WINDOW

class PerformanceTracker:
    """Tracks user performance metrics throughout session"""

    def __init__(self, user_name: str):
        self.user_name = user_name
        self.session_start = datetime.now()
        self.attempts: List[Dict] = []
        self.difficulty_history: List[str] = []

    def record_attempt(self, puzzle_id: int, difficulty: str, 
                      was_correct: bool, response_time: float,
                      operand1: int, operand2: int, operation: str) -> None:
        """Record a single attempt"""
        attempt = {
            'puzzle_id': puzzle_id,
            'timestamp': datetime.now(),
            'difficulty': difficulty,
            'was_correct': was_correct,
            'response_time': response_time,
            'operand1': operand1,
            'operand2': operand2,
            'operation': operation
        }
        self.attempts.append(attempt)

    def record_difficulty_change(self, new_difficulty: str) -> None:
        """Log difficulty transition"""
        self.difficulty_history.append(new_difficulty)

    def get_accuracy(self, window_size: int = None) -> float:
        """Calculate accuracy percentage"""
        if not self.attempts:
            return 0.0

        attempts = self.attempts if window_size is None else self.attempts[-window_size:]

        if not attempts:
            return 0.0

        correct = sum(1 for a in attempts if a['was_correct'])
        return (correct / len(attempts)) * 100

    def get_streak(self) -> int:
        """Get current streak of consecutive correct answers"""
        if not self.attempts:
            return 0

        streak = 0
        for attempt in reversed(self.attempts):
            if attempt['was_correct']:
                streak += 1
            else:
                break

        return streak

    def get_avg_response_time(self, window_size: int = None) -> float:
        """Get average response time in seconds"""
        if not self.attempts:
            return 0.0

        attempts = self.attempts if window_size is None else self.attempts[-window_size:]

        if not attempts:
            return 0.0

        total_time = sum(a['response_time'] for a in attempts)
        return total_time / len(attempts)

    def get_recent_accuracy(self, window_size: int = PERFORMANCE_WINDOW) -> float:
        """Get accuracy over recent attempts"""
        return self.get_accuracy(window_size)

    def get_statistics(self) -> Dict:
        """Generate comprehensive session statistics"""
        total_attempts = len(self.attempts)
        correct_attempts = sum(1 for a in self.attempts if a['was_correct'])

        return {
            'user_name': self.user_name,
            'total_questions': total_attempts,
            'correct_answers': correct_attempts,
            'incorrect_answers': total_attempts - correct_attempts,
            'accuracy': self.get_accuracy(),
            'recent_accuracy': self.get_recent_accuracy(),
            'avg_response_time': self.get_avg_response_time(),
            'current_streak': self.get_streak(),
            'max_streak': self._get_max_streak(),
            'difficulty_transitions': len(self.difficulty_history),
            'final_difficulty': self.difficulty_history[-1] if self.difficulty_history else 'Unknown',
            'session_duration': (datetime.now() - self.session_start).total_seconds()
        }

    def _get_max_streak(self) -> int:
        """Calculate maximum streak achieved in session"""
        if not self.attempts:
            return 0

        max_streak = 0
        current_streak = 0

        for attempt in self.attempts:
            if attempt['was_correct']:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0

        return max_streak

    def get_attempt_log(self) -> List[Dict]:
        """Get detailed log of all attempts"""
        return self.attempts.copy()
