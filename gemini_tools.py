"""
Gemini-Powered Video Analysis Tools
Fast, efficient, and comprehensive video analysis using Google's Gemini API
"""

import os
import json
import requests
from typing import List, Dict, Any
from crewai.tools import tool

# Try to import Gemini SDK
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini SDK not installed. Run: pip install google-generativeai")

def setup_gemini():
    """Setup Gemini API"""
    if not GEMINI_AVAILABLE:
        return None
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("⚠️  GEMINI_API_KEY not found in environment variables")
        return None
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('models/gemini-2.5-flash')  # Latest fast model

@tool("Gemini YouTube Video Analyzer")
def analyze_youtube_with_gemini(youtube_url: str) -> str:
    """
    Analyze YouTube video directly using Gemini's video understanding capabilities.
    This is much faster than downloading and processing screenshots manually.
    """
    try:
        if not GEMINI_AVAILABLE:
            return "Gemini SDK not available. Please install: pip install google-generativeai"
        
        model = setup_gemini()
        if not model:
            return "Gemini API not configured. Please add GEMINI_API_KEY to environment."
        
        # Use Gemini's direct video analysis
        prompt = f"""
        Analyze this YouTube video comprehensively: {youtube_url}
        
        Please provide:
        1. 📋 **Overview**: What is this video about?
        2. 🎯 **Main Topics**: Key subjects covered
        3. 💡 **Key Insights**: Most important takeaways
        4. 📚 **Learning Points**: Educational content and concepts
        5. 🔍 **Details**: Specific information, data, or examples mentioned
        6. 🎨 **Visual Elements**: Important visual content, diagrams, or demonstrations
        7. 📝 **Summary**: Comprehensive summary for study purposes
        
        Format the response in beautiful markdown with emojis and clear sections.
        Focus on creating comprehensive study notes that would be valuable for learning.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # Fallback to screenshot analysis if direct video analysis fails
            return f"Direct video analysis failed: {e}. Falling back to screenshot analysis."
            
    except Exception as e:
        return f"Error in Gemini video analysis: {e}"

@tool("Gemini Vision Screenshot Analyzer")
def analyze_screenshots_with_gemini(screenshot_paths: List[str]) -> str:
    """
    Analyze multiple screenshots using Gemini Vision for fast, comprehensive analysis.
    """
    try:
        if not GEMINI_AVAILABLE:
            return "Gemini SDK not available. Please install: pip install google-generativeai"
        
        # Setup Gemini Vision model
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "GEMINI_API_KEY not found in environment variables"
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')  # Latest model with vision
        
        analysis_results = []
        
        for i, screenshot_path in enumerate(screenshot_paths[:10]):  # Limit to 10 for speed
            try:
                if os.path.exists(screenshot_path):
                    # Load and analyze image
                    import PIL.Image
                    image = PIL.Image.open(screenshot_path)
                    
                    prompt = f"""
                    Analyze this screenshot from a video (Screenshot {i+1}):
                    
                    Please identify:
                    - 🎯 Main subject or topic shown
                    - 📝 Any text, titles, or captions visible
                    - 🔍 Key visual elements (diagrams, charts, people, objects)
                    - 💡 Educational or informational content
                    - 🎨 Important visual details
                    
                    Provide a concise but comprehensive analysis focusing on educational value.
                    """
                    
                    response = model.generate_content([prompt, image])
                    analysis_results.append({
                        'screenshot': i+1,
                        'path': screenshot_path,
                        'analysis': response.text
                    })
                    
            except Exception as e:
                analysis_results.append({
                    'screenshot': i+1,
                    'path': screenshot_path,
                    'analysis': f"Error analyzing screenshot: {e}"
                })
        
        # Combine all analyses
        combined_analysis = "# 🎥 Visual Content Analysis\n\n"
        for result in analysis_results:
            combined_analysis += f"## Screenshot {result['screenshot']}\n"
            combined_analysis += f"{result['analysis']}\n\n"
        
        return combined_analysis
        
    except Exception as e:
        return f"Error in Gemini vision analysis: {e}"

@tool("Gemini Content Synthesizer")
def synthesize_content_with_gemini(visual_analysis: str, transcript: str = None) -> str:
    """
    Use Gemini to synthesize visual analysis and transcript into beautiful study notes.
    """
    try:
        if not GEMINI_AVAILABLE:
            return "Gemini SDK not available. Please install: pip install google-generativeai"
        
        model = setup_gemini()
        if not model:
            return "Gemini API not configured."
        
        # Create synthesis prompt
        prompt = f"""
        Create comprehensive, beautiful study notes by synthesizing the following content:
        
        VISUAL ANALYSIS:
        {visual_analysis}
        
        TRANSCRIPT (if available):
        {transcript if transcript else "No transcript available"}
        
        Please create a beautiful, well-structured study guide with:
        
        # 📚 Study Guide
        
        ## 🎯 Overview
        [Comprehensive overview of the content]
        
        ## 🔑 Key Concepts
        [Main concepts and ideas, organized with bullet points]
        
        ## 💡 Key Insights
        [Most important takeaways and insights]
        
        ## 📋 Main Topics
        [Detailed breakdown of topics covered]
        
        ## 🎨 Visual Elements
        [Important visual content, diagrams, demonstrations]
        
        ## 📝 Detailed Notes
        [Comprehensive notes organized by themes, not timestamps]
        
        ## 🎓 Learning Objectives
        [What students should learn from this content]
        
        ## 📖 Summary
        [Executive summary for quick review]
        
        ## 🔍 Additional Insights
        [Any additional valuable information]
        
        Use beautiful formatting with:
        - 📋 Clear headings with emojis
        - • Bullet points for organization
        - **Bold text** for emphasis
        - Rich, comprehensive content
        - Focus on educational value
        - No rigid timestamps - focus on content flow
        
        Make this a study guide that would be genuinely useful for learning and review.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error in content synthesis: {e}"

def check_gemini_setup():
    """Check if Gemini is properly configured"""
    if not GEMINI_AVAILABLE:
        return False, "Gemini SDK not installed"
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return False, "GEMINI_API_KEY not found"
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')  # Latest model
        # Test with a simple prompt
        response = model.generate_content("Hello")
        return True, "Gemini configured successfully"
    except Exception as e:
        return False, f"Gemini configuration error: {e}"

if __name__ == "__main__":
    # Test Gemini setup
    success, message = check_gemini_setup()
    print(f"Gemini Setup: {'✅' if success else '❌'} {message}")