"""
Tools for CrewAI Video Study Guide Generator
"""

# Import the existing tools from the root directory
import sys
import os

# Add the parent directory to the path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from video_tools import extract_video_data
    from gemini_tools import analyze_youtube_with_gemini, synthesize_content_with_gemini, check_gemini_setup
except ImportError:
    # Fallback imports if the modules are in the same directory
    try:
        from .video_tools import extract_video_data
        from .gemini_tools import analyze_youtube_with_gemini, synthesize_content_with_gemini, check_gemini_setup
    except ImportError:
        print("⚠️  Warning: Could not import tools. Make sure video_tools.py and gemini_tools.py are available.")
        
        # Create dummy functions as fallback
        def extract_video_data(*args, **kwargs):
            return "Tool not available"
            
        def analyze_youtube_with_gemini(*args, **kwargs):
            return "Tool not available"
            
        def synthesize_content_with_gemini(*args, **kwargs):
            return "Tool not available"
            
        def check_gemini_setup():
            return False, "Tools not properly imported"

__all__ = [
    'extract_video_data',
    'analyze_youtube_with_gemini', 
    'synthesize_content_with_gemini',
    'check_gemini_setup'
]