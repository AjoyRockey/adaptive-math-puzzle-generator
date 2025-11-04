# Math Adventures - AI-Powered Adaptive Learning Prototype

## Overview
Math Adventures is an intelligent adaptive learning system for children ages 5-10 to practice basic mathematics through real-time difficulty adjustment.

## Features
- Dynamic puzzle generation
- Real-time performance tracking
- Intelligent adaptive difficulty
- Comprehensive session analytics

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application
```bash
# Command-line version
python main.py

# Or web version
streamlit run app.py
```

## System Requirements
- Python 3.8+
- ~100MB disk space
- Any OS (Windows, macOS, Linux)

## How It Works
1. Student enters name and selects starting difficulty
2. System generates math problems
3. Tracks accuracy, speed, and streaks
4. Automatically adjusts difficulty based on performance
5. Provides session summary and recommendations

## File Structure
- `config.py` - Configuration constants
- `puzzle_generator.py` - Puzzle creation
- `tracker.py` - Performance metrics
- `adaptive_engine.py` - Adaptive logic
- `main.py` - Command-line interface
- `app.py` - Web interface (optional)
- `requirements.txt` - Dependencies

## License
MIT License
