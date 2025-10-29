"""
CrewAI Video Study Guide Generator - Main Crew Definition
Fast, AI-powered study guide generation from YouTube videos
"""

import os
import time
import shutil
from crewai import Agent, Task, Crew, Process
from crewai_tools import FileReadTool, TXTSearchTool

from .tools import (
    extract_video_data,
    analyze_youtube_with_gemini,
    synthesize_content_with_gemini,
    check_gemini_setup
)
from .config import Config

class VideoStudyGuideCrew:
    """CrewAI Video Study Guide Generator"""
    
    def __init__(self):
        self.config = Config()
        self.setup_tools()
        self.setup_agents()
        
    def setup_tools(self):
        """Initialize tools"""
        self.file_read_tool = FileReadTool()
        self.txt_search_tool = TXTSearchTool()
        
    def robust_cleanup(self):
        """Clean previous video data to prevent content mixing"""
        screenshot_dir = "screenshots"
        cleaned_files = 0
        
        try:
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
            
            os.makedirs(screenshot_dir, exist_ok=True)
            
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
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

    def get_video_info(self, youtube_url):
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

    def setup_agents(self):
        """Setup CrewAI agents"""
        self.video_analyzer = Agent(
            role='Video Content Analyzer',
            goal='Extract and analyze content from YouTube videos and create comprehensive study guides.',
            backstory="""You are an expert at analyzing educational video content and extracting key information.
                         You work with available data - screenshots, video metadata, or title information to
                         create meaningful study guides. You focus on the educational topic and create
                         comprehensive learning materials.""",
            tools=[
                extract_video_data,
                analyze_youtube_with_gemini,
                synthesize_content_with_gemini,
                self.file_read_tool,
                self.txt_search_tool
            ],
            verbose=False,
            allow_delegation=False,
            max_iter=2,
            max_execution_time=200
        )

    def create_tasks(self, youtube_url, video_info, output_file):
        """Create CrewAI tasks"""
        return [
            Task(
                description=(
                    f"Create a comprehensive study guide for the YouTube video: {youtube_url} "
                    f"Title: '{video_info['title']}' "
                    f"Channel: {video_info['uploader']} "
                    f"Duration: {video_info['duration']:.1f} minutes "
                    ""
                    "Work with available data to create educational content: "
                    "1. Extract video screenshots and any available transcript "
                    "2. Identify the educational topic and subject from the title "
                    "3. Create a study guide with: "
                    "   - Clear identification of the educational topic "
                    "   - Key concepts related to the subject "
                    "   - Learning objectives appropriate for the topic "
                    "   - Study recommendations and strategies "
                    "   - Practice questions relevant to the subject "
                    "   - Beautiful formatting with emojis and structure "
                    ""
                    "Create educational content appropriate for the topic based on available data."
                ),
                expected_output=f"A comprehensive study guide for '{video_info['title']}' with educational content based on available data and topic analysis.",
                agent=self.video_analyzer,
                output_file=output_file
            )
        ]

    def run(self, youtube_url: str = None, output_file: str = None):
        """Run the crew to generate study guide"""
        
        # Use config defaults if not provided
        if not youtube_url:
            youtube_url = self.config.VIDEO_URL
        if not output_file:
            output_file = self.config.OUTPUT_FILE
            
        print(f"🎯 Analyzing video: {youtube_url}")
        
        # Check Gemini setup
        print("🔍 Checking Gemini configuration...")
        gemini_ready, gemini_message = check_gemini_setup()
        print(f"{'✅' if gemini_ready else '❌'} {gemini_message}")
        
        if not gemini_ready:
            print("\n🚀 QUICK SETUP FOR GEMINI:")
            print("1. Get API key: https://makersuite.google.com/app/apikey")
            print("2. Add to .env: GEMINI_API_KEY=your_key_here")
            return None
        
        # Cleanup and setup
        print("🧹 Performing cleanup...")
        self.robust_cleanup()
        print("✅ Cleanup completed!")
        
        # Get video info
        print("📹 Getting video information...")
        video_info = self.get_video_info(youtube_url)
        print(f"📺 Title: {video_info['title']}")
        print(f"⏱️  Duration: {video_info['duration']:.1f} minutes")
        print(f"👤 Channel: {video_info['uploader']}")
        
        # Create crew
        tasks = self.create_tasks(youtube_url, video_info, output_file)
        
        crew = Crew(
            agents=[self.video_analyzer],
            tasks=tasks,
            process=Process.sequential,
            verbose=False,
            max_rpm=60,
            memory=False,
            max_execution_time=200
        )
        
        print(f"\n🚀 Starting content analysis...")
        print(f"🎯 Target: Create study guide for '{video_info['title']}'")
        
        start_time = time.time()
        
        try:
            result = crew.kickoff(inputs={
                'youtube_url': youtube_url,
                'video_title': video_info['title'],
                'video_duration': video_info['duration'],
                'video_uploader': video_info['uploader']
            })
            
            processing_time = time.time() - start_time
            print(f"\n✅ Analysis completed in {processing_time:.1f} seconds!")
            print(f"📄 Study guide saved to: {output_file}")
            
            # Show results
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    word_count = len(content.split())
                    
                    if word_count > 100:
                        print("✅ SUCCESS: Generated comprehensive study guide!")
                    else:
                        print("⚠️  WARNING: Study guide may be incomplete")
                    
                    print(f"📊 Generated {word_count} words")
            
            # Show time savings
            manual_time_estimate = video_info['duration'] * 2.5 + 60
            time_saved = manual_time_estimate - (processing_time / 60)
            efficiency_gain = (time_saved / manual_time_estimate) * 100
            
            print(f"\n⚡ Time Savings:")
            print(f"   • Manual process: ~{manual_time_estimate:.0f} minutes")
            print(f"   • AI processing: {processing_time/60:.1f} minutes") 
            print(f"   • Time saved: {time_saved:.0f} minutes ({efficiency_gain:.0f}%)")
            
            return result
            
        except Exception as e:
            print(f"❌ Error during processing: {e}")
            return None

def main():
    """Main entry point"""
    crew = VideoStudyGuideCrew()
    return crew.run()

if __name__ == "__main__":
    main()