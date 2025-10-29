import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import VisionTool, FileReadTool
from video_tools import extract_video_data 
from dotenv import load_dotenv
import subprocess
import re

load_dotenv()

def get_video_duration(youtube_url):
    """Get video duration in minutes using yt-dlp"""
    try:
        cmd = ['yt-dlp', '--get-duration', '--no-playlist', youtube_url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            duration_str = result.stdout.strip()
            # Parse duration (format: HH:MM:SS or MM:SS)
            parts = duration_str.split(':')
            if len(parts) == 3:  # HH:MM:SS
                hours, minutes, seconds = map(int, parts)
                total_minutes = hours * 60 + minutes + seconds / 60
            elif len(parts) == 2:  # MM:SS
                minutes, seconds = map(int, parts)
                total_minutes = minutes + seconds / 60
            else:  # SS
                seconds = int(parts[0])
                total_minutes = seconds / 60
            return total_minutes
    except:
        pass
    return 30  # Default fallback

def get_optimal_crew_settings(duration_minutes):
    """Get optimal crew settings based on video duration - SPEED OPTIMIZED"""
    try:
        from config import FAST_MODE, MAX_CONCURRENT_REQUESTS
        if FAST_MODE:
            # Much more aggressive settings for speed
            if duration_minutes <= 5:        # Short videos
                return {'max_rpm': 60, 'memory': False, 'max_execution_time': 300}
            elif duration_minutes <= 15:     # Medium videos
                return {'max_rpm': 45, 'memory': False, 'max_execution_time': 600}
            elif duration_minutes <= 60:     # Long videos
                return {'max_rpm': 30, 'memory': True, 'max_execution_time': 900}
            elif duration_minutes <= 180:    # Very long videos
                return {'max_rpm': 20, 'memory': True, 'max_execution_time': 1200}
            else:                            # Ultra long videos
                return {'max_rpm': 15, 'memory': True, 'max_execution_time': 1800}
    except ImportError:
        pass
    
    # Fallback to original settings
    if duration_minutes <= 5:        # Short videos
        return {'max_rpm': 15, 'memory': False}
    elif duration_minutes <= 15:     # Medium videos
        return {'max_rpm': 12, 'memory': True}
    elif duration_minutes <= 60:     # Long videos
        return {'max_rpm': 8, 'memory': True}
    elif duration_minutes <= 180:    # Very long videos
        return {'max_rpm': 5, 'memory': True}
    else:                            # Ultra long videos
        return {'max_rpm': 3, 'memory': True}

# Agents
video_engineer = Agent(
    role='Video Content Engineer',
    goal='Download the video, extract screenshots at key intervals, and retrieve the full transcript.',
    backstory="""You are an expert in computer vision and media processing. Your job is to 
                 use your custom tools to cleanly break down the video data for the analysis agent.""",
    tools=[extract_video_data],
    verbose=True,
    allow_delegation=False
)

content_analyzer = Agent(
    role='Speed-Optimized Content Analyzer',
    goal='Rapidly analyze screenshots in batches and extract key visual information efficiently.',
    backstory="""You are an efficient visual analyst optimized for speed. You quickly identify important 
                 details, read text in images, and understand visual context. You work in batches to 
                 maximize processing speed while maintaining quality analysis.""",
    tools=[VisionTool()],
    verbose=False,  # Reduced verbosity for speed
    allow_delegation=False,
    max_iter=3,     # Limit iterations for speed
    max_execution_time=300  # 5 minute timeout per task
)

note_synthesizer = Agent(
    role='Speed-Optimized Note Synthesizer',
    goal='Rapidly create comprehensive study notes by efficiently combining visual analysis with transcript data.',
    backstory="""You are a highly efficient educational content creator optimized for speed and quality. 
                 You quickly synthesize information from multiple sources to create well-structured study 
                 guides. You work fast while maintaining educational value and clear organization.""",
    tools=[FileReadTool()],
    verbose=False,  # Reduced verbosity for speed
    allow_delegation=False,  # No delegation for speed
    max_iter=2,     # Limit iterations for speed
    max_execution_time=300  # 5 minute timeout per task
)

# Import configuration
try:
    from config import VIDEO_URL, FORCE_INTERVAL_SECONDS, FORCE_MAX_RPM, OUTPUT_FILE
    youtube_url = VIDEO_URL
    output_file = OUTPUT_FILE
except ImportError:
    # Fallback if config.py doesn't exist
    youtube_url = 'https://www.youtube.com/watch?v=GWnSsjT4V68'
    output_file = 'final_study_guide.md'

# Tasks
extract_task = Task(
    description=(
        "Use the 'Video Screenshot and Transcript Extractor' tool on the URL {youtube_url}. "
        "The tool will automatically determine the optimal screenshot interval based on the video length. "
        "Ensure the output clearly lists the file paths of all saved screenshots and the transcript file."
    ),
    expected_output='A clean summary listing the file paths and timestamps for all extracted screenshots and the transcript path.',
    agent=video_engineer,
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
    output_file=output_file
)

inputs = {
    'youtube_url': youtube_url,
}

# Auto-detect video duration and optimize settings
print("🔍 Analyzing video...")
video_duration = get_video_duration(inputs['youtube_url'])
crew_settings = get_optimal_crew_settings(video_duration)

# Apply any forced settings from config
try:
    if FORCE_MAX_RPM is not None:
        crew_settings['max_rpm'] = FORCE_MAX_RPM
except:
    pass

print(f"📹 Video duration: {video_duration:.1f} minutes")
print(f"⚙️  Optimized settings: {crew_settings}")

# Determine video category and provide recommendations
if video_duration <= 2:
    category = "Very Short"
    recommendation = "HIGH quality recommended for maximum detail"
elif video_duration <= 15:
    category = "Short"
    recommendation = "HIGH quality recommended for comprehensive coverage"
elif video_duration <= 60:
    category = "Medium"
    recommendation = "MEDIUM-HIGH quality recommended for balanced processing"
elif video_duration <= 180:
    category = "Long"
    recommendation = "MEDIUM quality recommended for efficient processing"
else:
    category = "Very Long"
    recommendation = "LOW-MEDIUM quality recommended for manageable processing time"

print(f"📊 Video category: {category}")
print(f"💡 Recommendation: {recommendation}")

# Show current settings
try:
    from config import SCREENSHOT_QUALITY, FAST_MODE
    print(f"🎯 Current quality: {SCREENSHOT_QUALITY}")
    print(f"⚡ Fast mode: {'ON' if FAST_MODE else 'OFF'}")
except ImportError:
    pass

print(f"💾 Output will be saved to: {output_file}")

note_taking_crew = Crew(
    agents=[video_engineer, content_analyzer, note_synthesizer],
    tasks=[extract_task, analysis_task, synthesis_task],
    process=Process.sequential,  # Keep sequential for now, but optimized
    verbose=False,  # Reduced verbosity for speed
    full_output=True,  # Get complete output
    **crew_settings  # Apply optimized settings
)

print("Starting the Note Taker Crew...")
result = note_taking_crew.kickoff(inputs=inputs)

print("\n\n################################")
print("###### CREW FINISHED WORK ######")
print("################################")
print(result)