#!/usr/bin/env python
import sys
import warnings
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from crewai_video_study_guide.main import run

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

if __name__ == "__main__":
    run()