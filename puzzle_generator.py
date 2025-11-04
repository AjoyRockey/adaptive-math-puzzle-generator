"""
Puzzle Generator Module
Generates math puzzles of varying difficulty
"""

import random
from typing import Dict, List
from config import OPERAND_RANGES, OPERATIONS, OPERATION_WEIGHTS

class PuzzleGenerator:
    """Generates math puzzles based on difficulty level"""

    def __init__(self, seed: int = None):
        if seed:
            random.seed(seed)
        self.recent_puzzles: List[Dict] = []
        self.puzzle_counter = 0

    def generate_puzzle(self, difficulty: str) -> Dict:
        """
        Generate a math puzzle for given difficulty level

        Args:
            difficulty: 'Easy', 'Medium', or 'Hard'

        Returns:
            Dictionary with puzzle details and correct answer
        """
        if difficulty not in OPERAND_RANGES:
            raise ValueError(f"Invalid difficulty: {difficulty}")

        self.puzzle_counter += 1
        ranges = OPERAND_RANGES[difficulty]

        operand1 = random.randint(ranges['min'], ranges['max'])
        operand2 = random.randint(ranges['min'], ranges['max'])
        operation = random.choices(OPERATIONS, weights=OPERATION_WEIGHTS)[0]
        correct_answer = self._calculate_answer(operand1, operand2, operation)

        puzzle = {
            'puzzle_id': self.puzzle_counter,
            'difficulty': difficulty,
            'operand1': operand1,
            'operand2': operand2,
            'operation': operation,
            'correct_answer': correct_answer,
            'question_text': self._format_question(operand1, operation, operand2)
        }

        self.recent_puzzles.append(puzzle)
        if len(self.recent_puzzles) > 20:
            self.recent_puzzles.pop(0)

        return puzzle

    def _calculate_answer(self, op1: float, op2: float, operation: str) -> float:
        """Calculate correct answer for puzzle"""
        if operation == '+':
            return op1 + op2
        elif operation == '-':
            return op1 - op2
        elif operation == '*':
            return op1 * op2
        elif operation == '/':
            return round(op1 / op2, 2) if op2 != 0 else 0
        else:
            raise ValueError(f"Unknown operation: {operation}")

    def _format_question(self, op1: float, operation: str, op2: float) -> str:
        """Format puzzle as readable question"""
        return f"{op1} {operation} {op2} = ?"

    def get_recent_puzzles(self, count: int = 5) -> List[Dict]:
        """Get last N puzzles generated"""
        return self.recent_puzzles[-count:]
