"""
Configuration for CrewAI Video Study Guide Generator
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration settings"""
    
    # Video Analysis Settings
    VIDEO_URL = os.getenv('VIDEO_URL', 'https://youtu.be/kNcPTdiDwkI')
    OUTPUT_FILE = os.getenv('OUTPUT_FILE', 'my_study_guide.md')
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Processing Settings
    SCREENSHOT_QUALITY = "HIGH"
    FAST_MODE = True
    MIN_SCREENSHOTS = 3
    MAX_SCREENSHOTS = 15
    FORCE_INTERVAL_SECONDS = 30
    FORCE_MAX_SCREENSHOTS = 10
    
    # Agent Settings
    MAX_AGENT_ITERATIONS = 2
    MAX_EXECUTION_TIME = 180
    USE_AGENT_MEMORY = False
    
    # Output Settings
    BEAUTIFUL_FORMATTING = True
    USE_EMOJIS = True