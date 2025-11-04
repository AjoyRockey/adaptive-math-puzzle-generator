"""
Main Entry Point - Command-Line Interface
Math Adventures: Adaptive Learning Prototype
"""

import sys
import time
from puzzle_generator import PuzzleGenerator
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

class MathAdventuresSession:
    """Orchestrates the interactive learning session"""

    def __init__(self):
        self.generator = None
        self.tracker = None
        self.engine = None
        self.current_difficulty = 'Easy'
        self.session_active = False

    def start_session(self) -> None:
        """Initialize and start learning session"""
        print("\n" + "="*60)
        print("🎯 Welcome to Math Adventures!")
        print("AI-Powered Adaptive Learning Prototype")
        print("="*60 + "\n")

        user_name = input("📝 Enter your name: ").strip()
        if not user_name:
            user_name = "Learner"

        print("\n🎯 Choose starting difficulty:")
        print("   [1] Easy   [2] Medium   [3] Hard")

        choice = input("Your choice (1-3): ").strip()
        difficulty_map = {'1': 'Easy', '2': 'Medium', '3': 'Hard'}
        self.current_difficulty = difficulty_map.get(choice, 'Easy')

        self.generator = PuzzleGenerator()
        self.tracker = PerformanceTracker(user_name)
        self.engine = AdaptiveEngine(enable_ml=True)
        self.tracker.record_difficulty_change(self.current_difficulty)

        print(f"\n✅ Starting at {self.current_difficulty} level\n")
        self.session_active = True

        self._run_question_loop()

    def _run_question_loop(self) -> None:
        """Main loop for question presentation and answering"""
        question_number = 0

        while self.session_active:
            question_number += 1

            puzzle = self.generator.generate_puzzle(self.current_difficulty)

            print(f"\n🧮 Question {question_number} ({self.current_difficulty}):")
            print(f"   {puzzle['question_text']}")

            start_time = time.time()
            try:
                user_answer = input("Your answer: ").strip()
                if user_answer.lower() in ['quit', 'exit', 'q']:
                    self.session_active = False
                    break

                user_answer = float(user_answer)
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
                continue

            response_time = time.time() - start_time
            is_correct = abs(user_answer - puzzle['correct_answer']) < 0.01

            self.tracker.record_attempt(
                puzzle['puzzle_id'],
                self.current_difficulty,
                is_correct,
                response_time,
                puzzle['operand1'],
                puzzle['operand2'],
                puzzle['operation']
            )

            if is_correct:
                print(f"✅ Correct! (Time: {response_time:.1f}s)")
            else:
                print(f"❌ Incorrect. The answer is {puzzle['correct_answer']}")

            if question_number % 3 == 0:
                self._show_quick_stats()

            next_difficulty, reason = self.engine.decide_next_difficulty(
                self.current_difficulty, self.tracker
            )

            if next_difficulty != self.current_difficulty:
                if next_difficulty > self.current_difficulty:
                    print(f"⬆️  Level up! Reason: {reason}")
                else:
                    print(f"⬇️  Adjusted difficulty. Reason: {reason}")
                self.current_difficulty = next_difficulty
                self.tracker.record_difficulty_change(next_difficulty)

            if question_number >= 5:
                cont = input("\nContinue? (y/n): ").strip().lower()
                if cont != 'y':
                    self.session_active = False

    def _show_quick_stats(self) -> None:
        """Display quick performance statistics"""
        stats = self.tracker.get_statistics()
        print(f"\n📊 Quick Stats:")
        print(f"   Accuracy: {stats['accuracy']:.1f}%")
        print(f"   Avg Time: {stats['avg_response_time']:.1f}s")
        print(f"   Streak: {stats['current_streak']}")

    def end_session(self) -> None:
        """Generate final summary and end session"""
        print("\n" + "="*60)
        print("📊 Session Summary")
        print("="*60)

        stats = self.tracker.get_statistics()

        print(f"\n👤 Student: {stats['user_name']}")
        print(f"❓ Questions Answered: {stats['total_questions']}")
        print(f"✅ Correct: {stats['correct_answers']}")
        print(f"❌ Incorrect: {stats['incorrect_answers']}")
        print(f"\n📈 Performance Metrics:")
        print(f"   Overall Accuracy: {stats['accuracy']:.1f}%")
        print(f"   Recent Accuracy: {stats['recent_accuracy']:.1f}%")
        print(f"   Avg Response Time: {stats['avg_response_time']:.1f}s")
        print(f"   Current Streak: {stats['current_streak']}")
        print(f"   Max Streak: {stats['max_streak']}")
        print(f"\n📊 Learning Progress:")
        print(f"   Final Level: {stats['final_difficulty']}")
        print(f"   Difficulty Transitions: {stats['difficulty_transitions']}")
        print(f"   Session Duration: {stats['session_duration']:.1f}s")

        print(f"\n🎯 Recommendation for Next Session:")
        if stats['accuracy'] >= 80:
            print(f"   Try Hard level - You're doing great! 🌟")
        elif stats['accuracy'] >= 60:
            print(f"   Continue with Medium level - Good progress! 👍")
        else:
            print(f"   Practice Easy level more - Keep trying! 💪")

        print("\n" + "="*60)
        print("Thanks for using Math Adventures! 🎓")
        print("="*60 + "\n")

def main():
    """Main entry point"""
    session = MathAdventuresSession()
    try:
        session.start_session()
    except KeyboardInterrupt:
        print("\n\n⚠️  Session interrupted by user")
    finally:
        session.end_session()

if __name__ == '__main__':
    main()
