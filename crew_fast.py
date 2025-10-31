#!/usr/bin/env python
"""
Fast Demo CrewAI Video Study Guide - Optimized for deployment timeouts
"""
import os
import sys
import logging
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a fast demo tool that doesn't actually download videos
@tool("Fast Demo Video Analyzer")
def demo_video_analyzer(youtube_url: str) -> str:
    """Fast demo tool that simulates video analysis without downloading"""
    logger.info(f"🎬 Analyzing video: {youtube_url}")
    
    # Simulate quick analysis
    return f"""
    📹 Video Analysis Complete for: {youtube_url}
    
    🎯 Key Findings:
    - Video Duration: ~15 minutes (estimated)
    - Content Type: Educational/Tutorial
    - Main Topics: Technology, Programming, AI
    - Screenshots: 5 key frames identified
    - Transcript: Available and processed
    
    📝 Ready for study guide generation!
    """

def create_fast_crew():
    """Create a fast demo crew with minimal processing"""
    
    # Fast analyzer agent
    analyzer = Agent(
        role='Fast Video Analyzer',
        goal='Quickly analyze video content and provide key insights',
        backstory='You are a speed-optimized video analyst that provides quick summaries.',
        tools=[demo_video_analyzer],
        verbose=True,
        allow_delegation=False,
        max_iter=1,  # Limit iterations
        max_execution_time=30  # 30 second timeout
    )
    
    # Fast note creator
    note_creator = Agent(
        role='Quick Note Creator',
        goal='Create study notes from video analysis',
        backstory='You create concise, well-structured study guides quickly.',
        verbose=False,
        allow_delegation=False,
        max_iter=1,  # Limit iterations
        max_execution_time=30  # 30 second timeout
    )
    
    # Fast analysis task
    analyze_task = Task(
        description="Quickly analyze the video at {youtube_url} and provide key insights about the content, topics, and structure.",
        expected_output="A summary of video content with key topics and insights",
        agent=analyzer
    )
    
    # Fast note creation task
    notes_task = Task(
        description="Create a concise study guide based on the video analysis. Include main topics, key points, and learning objectives.",
        expected_output="A well-structured study guide in markdown format",
        agent=note_creator,
        context=[analyze_task],
        output_file='demo_study_guide.md'
    )
    
    # Create fast crew
    return Crew(
        agents=[analyzer, note_creator],
        tasks=[analyze_task, notes_task],
        process=Process.sequential,
        verbose=True,
        full_output=True,
        max_rpm=30,  # Higher rate limit
        memory=False
    )

def run_fast():
    """Run the fast demo crew"""
    try:
        logger.info("🚀 Starting Fast Demo CrewAI...")
        
        # Check API keys
        if not os.getenv('OPENAI_API_KEY') and not os.getenv('GEMINI_API_KEY'):
            return "❌ Error: No API keys configured. Please set OPENAI_API_KEY or GEMINI_API_KEY"
        
        inputs = {
            'youtube_url': 'https://youtu.be/kNcPTdiDwkI'
        }
        
        logger.info("📝 Creating fast crew...")
        crew = create_fast_crew()
        
        logger.info("⚡ Running fast analysis...")
        result = crew.kickoff(inputs=inputs)
        
        logger.info("✅ Fast demo completed!")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return f"Error: {e}"

def health_check():
    """Quick health check"""
    try:
        logger.info("🔍 Health check...")
        
        # Check CrewAI
        from crewai import Agent
        logger.info("✅ CrewAI working")
        
        # Check API keys
        has_openai = bool(os.getenv('OPENAI_API_KEY'))
        has_gemini = bool(os.getenv('GEMINI_API_KEY'))
        
        if has_openai or has_gemini:
            logger.info("✅ API keys configured")
            return "✅ Ready to run"
        else:
            logger.warning("⚠️ No API keys found")
            return "⚠️ Missing API keys"
            
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return f"❌ Health check failed: {e}"

if __name__ == "__main__":
    print("🎯 Fast Demo CrewAI Video Study Guide")
    print("=" * 50)
    
    # Health check
    health = health_check()
    print(f"Health: {health}")
    
    if "Ready" in health:
        # Run fast demo
        result = run_fast()
        print("\n🎉 Demo Result:")
        print(result)
    else:
        print("❌ Cannot run - check API keys")