#!/usr/bin/env python
import sys
from crew import CrewaiVideoStudyGuideCrew

def run():
    """
    Run the crew.
    """
    inputs = {
        'youtube_url': 'https://youtu.be/kNcPTdiDwkI'
    }
    CrewaiVideoStudyGuideCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()