#!/usr/bin/env python
"""
Minimal CrewAI Video Study Guide - Direct approach for deployment
"""
import os
import sys
import logging
from crewai import Agent, Crew, Process, Task
from crewai_tools import VisionTool, FileReadTool

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import video tools from the existing file
sys.path.append('.')

try:
    from video_tools import extract_video_data
    logger.info("✅ Successfully imported video_tools")
except ImportError as e:
    logger.error(f"❌ Failed to import video_tools: {e}")
    # Create a fallback tool
    from crewai.tools import tool
    
    @tool("Video Screenshot and Transcript Extractor")
    def extract_video_data(youtube_url: str) -> str:
        """Fallback video extractor tool"""
        return f"Video processing for {youtube_url} - using fallback implementation"

# Check environment variables
required_env_vars = ['OPENAI_API_KEY', 'GEMINI_API_KEY']
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    logger.warning(f"⚠️ Missing environment variables: {missing_vars}")
else:
    logger.info("✅ Environment variables are set")

def create_crew():
    """Create the video study guide crew"""
    
    # Create agents
    video_engineer = Agent(
        role='Video Content Engineer',
        goal='Download the video, extract screenshots at key intervals, and retrieve the full transcript.',
        backstory='''You are an expert in computer vision and media processing. Your job is to 
                     use your custom tools to cleanly break down the video data for the analysis agent.''',
        tools=[extract_video_data],
        verbose=True,
        allow_delegation=False
    )
    
    content_analyzer = Agent(
        role='Speed-Optimized Content Analyzer',
        goal='Rapidly analyze screenshots in batches and extract key visual information efficiently.',
        backstory='''You are an efficient visual analyst optimized for speed. You quickly identify important 
                     details, read text in images, and understand visual context. You work in batches to 
                     maximize processing speed while maintaining quality analysis.''',
        tools=[VisionTool()],
        verbose=False,
        allow_delegation=False,
        max_iter=3,
        max_execution_time=300
    )
    
    note_synthesizer = Agent(
        role='Speed-Optimized Note Synthesizer',
        goal='Rapidly create comprehensive study notes by efficiently combining visual analysis with transcript data.',
        backstory='''You are a highly efficient educational content creator optimized for speed and quality. 
                     You quickly synthesize information from multiple sources to create well-structured study 
                     guides. You work fast while maintaining educational value and clear organization.''',
        tools=[FileReadTool()],
        verbose=False,
        allow_delegation=False,
        max_iter=2,
        max_execution_time=300
    )
    
    # Create tasks
    extract_task = Task(
        description=(
            "Use the 'Video Screenshot and Transcript Extractor' tool on the URL {youtube_url}. "
            "The tool will automatically determine the optimal screenshot interval based on the video length. "
            "Ensure the output clearly lists the file paths of all saved screenshots and the transcript file."
        ),
        expected_output='A clean summary listing the file paths and timestamps for all extracted screenshots and the transcript path.',
        agent=video_engineer
    )
    
    analysis_task = Task(
        description=(
            "SPEED-OPTIMIZED ANALYSIS: Rapidly analyze all screenshots from the Video Content Engineer. "
            "Work efficiently through each screenshot file: "
            "1. Quickly identify key visual elements, text, and educational content using VisionTool. "
            "2. Extract main concepts and themes without excessive detail. "
            "3. Note important text, titles, or data visible in images. "
            "4. Focus on educational value and learning objectives. "
            "5. Work through screenshots systematically and efficiently. "
            "Prioritize speed while maintaining quality. Provide concise but comprehensive analysis."
        ),
        expected_output="Efficient visual analysis for each screenshot with timestamps, focusing on key concepts and educational content.",
        agent=content_analyzer,
        context=[extract_task]
    )
    
    synthesis_task = Task(
        description=(
            "SPEED-OPTIMIZED SYNTHESIS: Rapidly create a comprehensive study guide using analysis and transcript data. "
            "Work efficiently to: "
            "1. Quickly read transcript file (if available) using FileReadTool. "
            "2. Efficiently match visual analysis with transcript content by timestamp. "
            "3. Create structured, informative notes combining visual and audio information. "
            "4. Extract key concepts and main points without excessive elaboration. "
            "5. Use clear headings, bullet points, and organized structure. "
            "6. Include relevant transcript quotes when they add educational value. "
            "7. Focus on learning objectives and practical study value. "
            "8. Maintain quality while prioritizing speed and efficiency. "
            "Generate a professional study guide optimized for both speed and educational value."
        ),
        expected_output="A well-structured study guide in Markdown format efficiently combining visual and audio information with key concepts and learning materials.",
        agent=note_synthesizer,
        context=[extract_task, analysis_task],
        output_file='final_study_guide.md'
    )
    
    # Create and return crew
    return Crew(
        agents=[video_engineer, content_analyzer, note_synthesizer],
        tasks=[extract_task, analysis_task, synthesis_task],
        process=Process.sequential,
        verbose=False,
        full_output=True,
        max_rpm=15,
        memory=False
    )

def run():
    """Run the crew with error handling"""
    try:
        logger.info("🚀 Starting CrewAI Video Study Guide...")
        
        # Check if we have the required environment
        if not os.getenv('OPENAI_API_KEY') and not os.getenv('GEMINI_API_KEY'):
            logger.error("❌ No API keys found. Please set OPENAI_API_KEY or GEMINI_API_KEY")
            return "Error: No API keys configured"
        
        inputs = {
            'youtube_url': 'https://youtu.be/kNcPTdiDwkI'
        }
        
        logger.info("📝 Creating crew...")
        crew = create_crew()
        
        logger.info("🎬 Processing video...")
        result = crew.kickoff(inputs=inputs)
        
        logger.info("✅ Crew completed successfully!")
        print(result)
        return result
        
    except Exception as e:
        logger.error(f"❌ Error running crew: {e}")
        print(f"Error: {e}")
        return f"Error: {e}"

def health_check():
    """Simple health check function"""
    try:
        logger.info("🔍 Running health check...")
        
        # Check imports
        from crewai import Agent
        logger.info("✅ CrewAI imports working")
        
        # Check environment
        api_key_status = "✅" if (os.getenv('OPENAI_API_KEY') or os.getenv('GEMINI_API_KEY')) else "❌"
        logger.info(f"{api_key_status} API keys status")
        
        return "Health check passed"
        
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        return f"Health check failed: {e}"

if __name__ == "__main__":
    # Run health check first
    health_status = health_check()
    print(f"Health Status: {health_status}")
    
    # Then run the crew
    run()