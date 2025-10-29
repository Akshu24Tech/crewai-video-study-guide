"""
Configuration file for the Universal Video Study Guide Generator
Modify the VIDEO_URL to process any YouTube video of any length
"""

# ===== MAIN CONFIGURATION =====
VIDEO_URL = 'https://youtu.be/kNcPTdiDwkI'  # Longer video for HIGH quality testing

# ===== ADVANCED SETTINGS (Optional) =====
# Leave these as None for auto-optimization, or set specific values

FORCE_INTERVAL_SECONDS = None  # None = auto-calculate, or set specific interval (e.g., 60)
FORCE_MAX_SCREENSHOTS = None   # None = auto-calculate, or set specific limit (e.g., 20)
FORCE_MAX_RPM = None          # None = auto-calculate, or set specific rate limit (e.g., 10)

# ===== OUTPUT SETTINGS =====
OUTPUT_FILE = 'final_study_guide.md'
SCREENSHOT_DIR = 'screenshots'

# ===== ENHANCED NOTE-TAKING SETTINGS =====
DETAILED_ANALYSIS = True          # Enable detailed visual analysis
INCLUDE_TRANSCRIPT_QUOTES = True  # Include relevant transcript quotes in notes
EXTRACT_KEY_CONCEPTS = True       # Extract and highlight key concepts
CREATE_SUMMARY_SECTIONS = True    # Create summary sections for longer videos
INCLUDE_TIMESTAMPS = True         # Include precise timestamps in notes

# ===== SPEED OPTIMIZATION SETTINGS =====
ENABLE_PARALLEL_PROCESSING = True # Process multiple screenshots simultaneously
BATCH_SIZE = 5                    # Number of screenshots to process in parallel
FAST_MODE = False                 # Disable for better quality (set True for speed)
REDUCE_API_CALLS = False          # Allow more API calls for better coverage
MAX_CONCURRENT_REQUESTS = 3       # Maximum parallel API requests

# ===== API PROVIDER SETTINGS =====
PRIMARY_LLM_PROVIDER = "gemini"   # Options: "openai", "gemini", "claude", "mixed"
VISION_PROVIDER = "gemini"        # Options: "openai", "gemini" (for vision tasks)
TEXT_PROVIDER = "gemini"          # Options: "openai", "gemini", "claude" (for text tasks)

# ===== SPEED PRESETS =====
SPEED_PRESET = "MAXIMUM_SPEED"     # Gemini for everything, fastest processing

# ===== GEMINI OPTIMIZATION SETTINGS =====
ENABLE_YOUTUBE_SUMMARIZATION = True # Use Gemini's direct YouTube analysis
USE_GEMINI_VISION = True           # Use Gemini for vision analysis (faster)
ENABLE_BEAUTIFUL_OUTPUT = True     # Create beautiful, well-formatted notes

# ===== OUTPUT STYLE SETTINGS =====
OUTPUT_STYLE = "BEAUTIFUL"         # Create beautiful, comprehensive notes
INCLUDE_TIMESTAMPS = False         # Focus on content flow, not rigid timestamps
USE_BULLET_POINTS = True           # Organized bullet point format
CREATE_SECTIONS = True             # Well-structured sections with headings
INCLUDE_KEY_INSIGHTS = True        # Extract key insights and takeaways
GENERATE_SUMMARY = True            # Create executive summary
BEAUTIFUL_FORMATTING = True       # Use emojis, headers, and rich formatting

# ===== SCREENSHOT DENSITY SETTINGS =====
SCREENSHOT_QUALITY = "HIGH"       # Options: "LOW", "MEDIUM", "HIGH", "ULTRA"
ADAPTIVE_DENSITY = True           # Automatically adjust based on video content
MIN_SCREENSHOTS = 10              # Minimum screenshots regardless of video length
MAX_SCREENSHOTS = 50              # Maximum screenshots to prevent overload

# ===== PRESET CONFIGURATIONS =====
"""
SPEED PRESETS:
- SCREENSHOT_QUALITY = "LOW" + FAST_MODE = True
  → Fastest processing, fewer screenshots, good for quick overviews

- SCREENSHOT_QUALITY = "MEDIUM" + FAST_MODE = False  
  → Balanced speed/quality, good for most use cases

- SCREENSHOT_QUALITY = "HIGH" + FAST_MODE = False
  → Best quality notes, more screenshots, slower processing

- SCREENSHOT_QUALITY = "ULTRA" + FAST_MODE = False
  → Maximum detail, most screenshots, slowest but most comprehensive

EXAMPLE USE CASES:

# Quick Overview (Fast):
SCREENSHOT_QUALITY = "LOW"
FAST_MODE = True
# Result: ~8-15 screenshots, 2-3x faster processing

# Educational Content (Balanced):
SCREENSHOT_QUALITY = "HIGH" 
FAST_MODE = False
# Result: ~20-30 screenshots, detailed analysis

# Research/Study (Maximum Detail):
SCREENSHOT_QUALITY = "ULTRA"
FAST_MODE = False  
# Result: ~30-50 screenshots, comprehensive coverage

# Long Videos (Efficient):
SCREENSHOT_QUALITY = "MEDIUM"
FAST_MODE = True
# Result: Optimized for long content, good balance
"""