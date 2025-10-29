#!/usr/bin/env python3
"""
CrewAI Video Study Guide Generator - Main Entry Point
"""

from .crew import VideoStudyGuideCrew

def main():
    """Main function to run the crew"""
    crew = VideoStudyGuideCrew()
    result = crew.run()
    return result

if __name__ == "__main__":
    main()