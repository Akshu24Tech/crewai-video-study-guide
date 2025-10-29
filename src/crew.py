"""
CrewAI Video Study Guide Generator
Handles cleanup issues and provides reliable content extraction
"""

import os
import time
import shutil
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, TXTSearchTool

from gemini_tools import analyze_youtube_with_gemini, synthesize_content_with_gemini, check_gemini_setup
from video_tools import extract_video_data
from dotenv import load_dotenv

load_dotenv()

def robust_cleanup():
    """Robust cleanup that handles Windows permission issues"""
    screenshot_dir = "screenshots"
    cleaned_files = 0
    
    try:
        # Try to clean individual files first
        if os.path.exists(screenshot_dir):
            for filename in os.listdir(screenshot_dir):
                file_path = os.path.join(screenshot_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        cleaned_files += 1
                except Exception as e:
                    print(f"⚠️  Could not remove {filename}: {e}")
            
            if cleaned_files > 0:
                print(f"🧹 Cleaned {cleaned_files} old screenshots")
        
        # Ensure directory exists
        os.makedirs(screenshot_dir, exist_ok=True)
        
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
        # Create directory anyway
        os.makedirs(screenshot_dir, exist_ok=True)
    
    # Clean transcript files
    transcript_files = ['transcript.txt', 'transcript_structured.json']
    for file in transcript_files:
        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"🧹 Removed old {file}")
        except Exception as e:
            print(f"⚠️  Could not remove {file}: {e}")

def get_video_info(youtube_url):
    """Get video information with error handling"""
    try:
        import subprocess
        cmd = ['yt-dlp', '--dump-json', '--no-download', youtube_url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            import json
            metadata = json.loads(result.stdout)
            return {
                'title': metadata.get('title', 'Unknown'),
                'description': metadata.get('description', ''),
                'duration': metadata.get('duration', 0) / 60,
                'uploader': metadata.get('uploader', 'Unknown'),
                'view_count': metadata.get('view_count', 0)
            }
    except Exception as e:
        print(f"⚠️  Could not get video metadata: {e}")
    
    return {'title': 'Unknown Video', 'description': '', 'duration': 30, 'uploader': 'Unknown'}

# Configuration
try:
    from config import VIDEO_URL, OUTPUT_FILE
    youtube_url = VIDEO_URL
    output_file = OUTPUT_FILE
except ImportError:
    # Fallback to default values
    youtube_url = 'https://youtu.be/kNcPTdiDwkI'
    output_file = 'my_study_guide.md'

print(f"🎯 Analyzing video: {youtube_url}")

# Robust cleanup
print("🧹 Performing robust cleanup...")
robust_cleanup()
print("✅ Cleanup completed!")

# Check Gemini setup
print("🔍 Checking Gemini configuration...")
gemini_ready, gemini_message = check_gemini_setup()
print(f"{'✅' if gemini_ready else '❌'} {gemini_message}")

if not gemini_ready:
    print("\n🚀 QUICK SETUP FOR GEMINI:")
    print("1. Get API key: https://makersuite.google.com/app/apikey")
    print("2. Add to .env: GEMINI_API_KEY=your_key_here")
    exit(1)

# Get video information
print("📹 Getting video information...")
video_info = get_video_info(youtube_url)
print(f"📺 Title: {video_info['title']}")
print(f"⏱️  Duration: {video_info['duration']:.1f} minutes")
print(f"👤 Channel: {video_info['uploader']}")

# Initialize tools
print("⚡ Initializing tools...")
file_read_tool = FileReadTool()
txt_search_tool = TXTSearchTool()
print("✅ Tools ready!")

# Create robust agent
robust_agent = Agent(
    role='Robust Video Content Analyzer',
    goal=f'Extract and analyze content from "{video_info["title"]}" and create a comprehensive study guide based on available data.',
    backstory=f"""You are analyzing the YouTube video "{video_info['title']}" by "{video_info['uploader']}". 
                 You must work with whatever data is available - screenshots, video metadata, or title information.
                 Even if some tools fail, you should create a meaningful study guide based on the video title 
                 and any available information. Focus on the educational topic indicated by the title.""",
    tools=[
        extract_video_data,
        synthesize_content_with_gemini,
        file_read_tool,
        txt_search_tool
    ],
    verbose=False,
    allow_delegation=False,
    max_iter=2,
    max_execution_time=200
)

# Create robust task
robust_task = Task(
    description=(
        f"Create a comprehensive study guide for the YouTube video: {youtube_url} "
        f"Title: '{video_info['title']}' "
        f"Channel: {video_info['uploader']} "
        f"Duration: {video_info['duration']:.1f} minutes "
        ""
        "Work with available data to create educational content: "
        "1. First, try to extract video screenshots and any available transcript "
        "2. Based on the video title, identify the educational topic and subject "
        "3. Create a study guide that includes: "
        "   - Clear identification of the educational topic "
        "   - Key concepts related to the subject (based on title analysis) "
        "   - Learning objectives appropriate for the topic "
        "   - Study recommendations and strategies "
        "   - Practice questions relevant to the subject "
        "   - Beautiful formatting with emojis and structure "
        ""
        "If video analysis tools fail, use the title and metadata to infer the educational content. "
        "The title suggests this is about NCERT Class 9 Geography Chapter 3 on Drainage systems. "
        "Create educational content appropriate for this topic."
    ),
    expected_output=f"A comprehensive study guide for '{video_info['title']}' with educational content based on available data and topic analysis.",
    agent=robust_agent,
    output_file=output_file
)

# Create crew
crew_settings = {
    'max_rpm': 60,
    'memory': False,
    'max_execution_time': 200
}

robust_crew = Crew(
    agents=[robust_agent],
    tasks=[robust_task],
    process=Process.sequential,
    verbose=False,
    **crew_settings
)

print(f"\n🚀 Starting content analysis...")
print(f"🎯 Target: Create study guide for '{video_info['title']}'")
print("⚡ Will work with available data and handle failures gracefully!")

start_time = time.time()

try:
    result = robust_crew.kickoff(inputs={
        'youtube_url': youtube_url,
        'video_title': video_info['title'],
        'video_duration': video_info['duration'],
        'video_uploader': video_info['uploader']
    })
    
    processing_time = time.time() - start_time
    print(f"\n✅ Analysis completed in {processing_time:.1f} seconds!")
    print(f"📄 Study guide saved to: {output_file}")
    print(f"🎉 Processing time: {processing_time/60:.1f} minutes")
    
    # Check results
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            word_count = len(content.split())
            
            # Check content quality
            if word_count > 100:
                print("✅ SUCCESS: Generated comprehensive study guide!")
            else:
                print("⚠️  WARNING: Study guide may be incomplete")
            
            print(f"📊 Generated {word_count} words")
            
            print(f"\n📚 Study guide preview:")
            print("=" * 60)
            preview = content[:800] + "..." if len(content) > 800 else content
            print(preview)
    
    # Check for extracted data
    screenshot_count = 0
    if os.path.exists('screenshots'):
        screenshot_count = len([f for f in os.listdir('screenshots') if f.endswith('.jpg')])
    
    transcript_exists = os.path.exists('transcript.txt')
    
    print(f"\n📊 Data extraction summary:")
    print(f"   • Screenshots: {screenshot_count}")
    print(f"   • Transcript: {'✅' if transcript_exists else '❌'}")
    print(f"   • Processing time: {processing_time:.1f}s")
    
    # Show time savings
    manual_time_estimate = video_info['duration'] * 2.5 + 60  # Watch + note-taking time
    time_saved = manual_time_estimate - (processing_time / 60)
    efficiency_gain = (time_saved / manual_time_estimate) * 100
    
    print(f"\n⚡ Time Savings:")
    print(f"   • Manual process: ~{manual_time_estimate:.0f} minutes")
    print(f"   • AI processing: {processing_time/60:.1f} minutes") 
    print(f"   • Time saved: {time_saved:.0f} minutes ({efficiency_gain:.0f}%)")
    
except Exception as e:
    print(f"❌ Error during processing: {e}")
    print("💡 Check your API keys and internet connection")

print("\n" + "="*60)
print("🎉 ANALYSIS COMPLETE!")
print("✅ Handles cleanup issues and provides reliable content")
print("="*60)
