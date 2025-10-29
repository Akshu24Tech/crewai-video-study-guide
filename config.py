"""
FAST Configuration for CrewAI Video Study Guide Generator
Optimized for maximum speed while maintaining quality
"""

# ================================
# VIDEO ANALYSIS SETTINGS
# ================================

# YouTube video URL to analyze
VIDEO_URL = 'https://youtu.be/BM6aIZjyF8c' # example

# Output file for the study guide
OUTPUT_FILE = 'my_study_guide.md'

# Speed-optimized features (disable heavy features)
ENABLE_YOUTUBE_SUMMARIZATION = True
ENABLE_WEB_RESEARCH = False  # Disabled for speed
ENABLE_DATA_ANALYSIS = False  # Disabled for speed
ENABLE_VISION_ANALYSIS = False  # Disabled for speed

# ================================
# SCREENSHOT SETTINGS (OPTIMIZED)
# ================================

# Screenshot quality: LOW for speed, MEDIUM for balance
SCREENSHOT_QUALITY = "LOW"

# Fast mode enabled
FAST_MODE = True

# Reduced screenshot limits for speed
MIN_SCREENSHOTS = 3
MAX_SCREENSHOTS = 15  # Reduced from 50

# Force faster settings
FORCE_INTERVAL_SECONDS = 30  # Larger intervals = fewer screenshots
FORCE_MAX_SCREENSHOTS = 10   # Maximum 10 screenshots for speed

# ================================
# PROCESSING OPTIMIZATION
# ================================

# Agent limits (reduced for speed)
MAX_AGENT_ITERATIONS = 2  # Reduced from 3
MAX_EXECUTION_TIME = 180  # Reduced from 600

# Disable memory for speed
USE_AGENT_MEMORY = False

# Disable caching for faster startup
CACHE_RESEARCH_RESULTS = False
CACHE_ANALYSIS_RESULTS = False

# ================================
# CONTENT SETTINGS (STREAMLINED)
# ================================

# Beautiful formatting (keep enabled - minimal performance impact)
BEAUTIFUL_FORMATTING = True
USE_EMOJIS = True
USE_TABLES = False  # Disabled for speed
USE_DIAGRAMS = False  # Disabled for speed

# Streamlined content structure
INCLUDE_EXECUTIVE_SUMMARY = True
INCLUDE_LEARNING_OBJECTIVES = True
INCLUDE_KEY_CONCEPTS = True
INCLUDE_VISUAL_ANALYSIS = False  # Disabled for speed
INCLUDE_SUPPLEMENTARY_RESOURCES = False  # Disabled for speed
INCLUDE_STUDY_STRATEGIES = True
INCLUDE_PRACTICE_QUESTIONS = True
INCLUDE_FURTHER_READING = False  # Disabled for speed

# Essential sections only
SECTIONS = {
    'executive_summary': True,
    'learning_objectives': True,
    'main_content': True,
    'key_concepts': True,
    'visual_elements': False,  # Disabled for speed
    'supplementary_resources': False,  # Disabled for speed
    'study_strategies': True,
    'practice_questions': True,
    'further_reading': False,  # Disabled for speed
    'review_checklist': True
}

# ================================
# SPEED OPTIMIZATIONS
# ================================

# Parallel processing disabled (can cause overhead)
ENABLE_PARALLEL_RESEARCH = False
MAX_CONCURRENT_REQUESTS = 1

# Reduced research depth
MAX_RESEARCH_SOURCES = 3  # Reduced from 10
MAX_YOUTUBE_RELATED = 2   # Reduced from 5
MAX_ARTICLES = 2          # Reduced from 8

# Faster content validation
MIN_CONTENT_LENGTH = 800  # Reduced from 2000
REQUIRE_MULTIPLE_SOURCES = False
VALIDATE_LINKS = False
CHECK_CONTENT_QUALITY = False

# Error handling (faster)
RETRY_FAILED_REQUESTS = False
MAX_RETRIES = 1
FALLBACK_TO_BASIC_MODE = True

# ================================
# OUTPUT SETTINGS (MINIMAL)
# ================================

# Single format only
OUTPUT_FORMATS = ['markdown']

# Simplified markdown styling
MARKDOWN_STYLE = {
    'headers': True,
    'bold_text': True,
    'italic_text': False,  # Disabled for speed
    'code_blocks': False,  # Disabled for speed
    'tables': False,       # Disabled for speed
    'lists': True,
    'links': True,
    'images': False,       # Disabled for speed
    'emojis': True
}

# Simplified content organization
CONTENT_ORGANIZATION = {
    'hierarchical': True,
    'topic_based': True,
    'difficulty_progression': False,  # Disabled for speed
    'visual_separation': True
}

# ================================
# DEBUG SETTINGS (MINIMAL)
# ================================

# Minimal logging for speed
LOG_LEVEL = "WARNING"  # Only warnings and errors
VERBOSE_OUTPUT = False
SAVE_INTERMEDIATE_RESULTS = False

# Performance monitoring (lightweight)
TRACK_PROCESSING_TIME = True
MONITOR_API_USAGE = False
GENERATE_PERFORMANCE_REPORT = False

# Debug options (all disabled for speed)
DEBUG_MODE = False
SAVE_RAW_DATA = False
DETAILED_ERROR_REPORTING = False

# ================================
# SPEED TARGETS
# ================================

# Target processing times
TARGET_TIMES = {
    'short_video': 60,      # Under 1 minute for videos < 10 min
    'medium_video': 180,    # Under 3 minutes for videos < 30 min
    'long_video': 300,      # Under 5 minutes for videos < 2 hours
    'ultra_long_video': 480 # Under 8 minutes for videos > 2 hours
}

# Quality vs Speed balance
SPEED_PRIORITY = "HIGH"  # HIGH, MEDIUM, LOW
QUALITY_THRESHOLD = "GOOD"  # EXCELLENT, GOOD, ACCEPTABLE

print("⚡ FAST configuration loaded successfully!")
print(f"🎯 Target video: {VIDEO_URL}")
print(f"📄 Output file: {OUTPUT_FILE}")
print(f"🚀 Speed priority: {SPEED_PRIORITY}")
print(f"⏱️  Max processing time: {MAX_EXECUTION_TIME}s")
print(f"📊 Max screenshots: {MAX_SCREENSHOTS}")
print(f"🔧 Fast mode: {'ON' if FAST_MODE else 'OFF'}")
