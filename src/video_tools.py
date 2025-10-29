import os
import cv2
import subprocess
import json
import re
from crewai.tools import tool

SCREENSHOT_DIR = "screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        r'youtube\.com/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def calculate_optimal_interval(duration_minutes):
    """Calculate optimal screenshot interval with intelligent density control"""
    try:
        from config import FAST_MODE, SCREENSHOT_QUALITY, MIN_SCREENSHOTS, MAX_SCREENSHOTS
        
        # Quality-based multipliers
        quality_multipliers = {
            "LOW": 0.5,      # Fewer screenshots, faster processing
            "MEDIUM": 0.75,  # Balanced approach
            "HIGH": 1.0,     # Standard density
            "ULTRA": 1.5     # More screenshots, better coverage
        }
        
        multiplier = quality_multipliers.get(SCREENSHOT_QUALITY, 1.0)
        
        if FAST_MODE:
            # Speed-optimized settings
            base_intervals = {
                2: (20, 8),    # Very short: 20s intervals, ~8 screenshots
                5: (30, 10),   # Short: 30s intervals, ~10 screenshots  
                15: (60, 12),  # Medium: 1min intervals, ~12 screenshots
                30: (120, 12), # Long: 2min intervals, ~12 screenshots
                60: (240, 15), # Very long: 4min intervals, ~15 screenshots
                120: (480, 15),# Extra long: 8min intervals, ~15 screenshots
                300: (900, 20),# Super long: 15min intervals, ~20 screenshots
                float('inf'): (1200, 25) # Ultra long: 20min intervals, ~25 screenshots
            }
        else:
            # Quality-optimized settings
            base_intervals = {
                2: (10, 15),   # Very short: 10s intervals, ~15 screenshots
                5: (20, 20),   # Short: 20s intervals, ~20 screenshots
                15: (45, 25),  # Medium: 45s intervals, ~25 screenshots
                30: (90, 25),  # Long: 1.5min intervals, ~25 screenshots
                60: (180, 30), # Very long: 3min intervals, ~30 screenshots
                120: (300, 30),# Extra long: 5min intervals, ~30 screenshots
                300: (600, 35),# Super long: 10min intervals, ~35 screenshots
                float('inf'): (900, 40) # Ultra long: 15min intervals, ~40 screenshots
            }
        
        # Find appropriate interval based on duration
        for max_duration, (interval, max_shots) in base_intervals.items():
            if duration_minutes <= max_duration:
                # Apply quality multiplier correctly
                # For HIGH quality (1.0), we want smaller intervals and more shots
                if SCREENSHOT_QUALITY == "ULTRA":
                    adjusted_interval = max(5, int(interval * 0.7))  # 30% smaller intervals
                    adjusted_max = min(MAX_SCREENSHOTS, int(max_shots * 1.5))  # 50% more shots
                elif SCREENSHOT_QUALITY == "HIGH":
                    adjusted_interval = max(10, int(interval * 0.8))  # 20% smaller intervals  
                    adjusted_max = min(MAX_SCREENSHOTS, int(max_shots * 1.2))  # 20% more shots
                elif SCREENSHOT_QUALITY == "MEDIUM":
                    adjusted_interval = interval
                    adjusted_max = max_shots
                else:  # LOW
                    adjusted_interval = int(interval * 1.5)  # 50% larger intervals
                    adjusted_max = max(MIN_SCREENSHOTS, int(max_shots * 0.7))  # 30% fewer shots
                
                # Ensure within bounds
                adjusted_max = max(MIN_SCREENSHOTS, min(adjusted_max, MAX_SCREENSHOTS))
                adjusted_interval = max(5, adjusted_interval)
                
                print(f"Quality: {SCREENSHOT_QUALITY}, Duration: {duration_minutes:.1f}min")
                print(f"Base: {interval}s/{max_shots} → Final: {adjusted_interval}s/{adjusted_max}")
                
                return adjusted_interval, adjusted_max
                
    except ImportError:
        pass
    
    # Fallback to original logic
    if duration_minutes <= 2:
        return 15, 20
    elif duration_minutes <= 5:
        return 30, 20
    elif duration_minutes <= 15:
        return 60, 20
    elif duration_minutes <= 30:
        return 120, 20
    elif duration_minutes <= 60:
        return 180, 25
    elif duration_minutes <= 120:
        return 300, 25
    elif duration_minutes <= 300:
        return 600, 30
    else:
        return 900, 35

@tool("Video Screenshot and Transcript Extractor")
def extract_video_data(youtube_url: str, interval_seconds: int = None) -> str:
    """
    Downloads a YouTube video, automatically calculates optimal screenshot intervals based on duration,
    and retrieves the full video transcript. Works with any video length from 30 seconds to 10+ hours.
    Returns a string summary of the extracted data paths.
    """
    try:
        video_path = os.path.join(os.getcwd(), "temp_video.mp4")
        
        # Use yt-dlp to download video (more reliable than pytube)
        print(f"Downloading video from: {youtube_url}")
        cmd = [
            'yt-dlp', 
            '-f', 'best[ext=mp4]/best',
            '-o', video_path,
            '--no-playlist',
            youtube_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Failed to download video: {result.stderr}"
        
        print("Download complete.")
        
        # Screenshots
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return f"Error: Could not open video at {video_path}"

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_seconds = total_frames / fps
        duration_minutes = duration_seconds / 60
        
        # Auto-calculate optimal interval if not provided
        if interval_seconds is None:
            interval_seconds, max_screenshots = calculate_optimal_interval(duration_minutes)
        else:
            # Use provided interval but still calculate max screenshots
            _, max_screenshots = calculate_optimal_interval(duration_minutes)
        
        # Check for forced settings from config
        try:
            from config import FORCE_INTERVAL_SECONDS, FORCE_MAX_SCREENSHOTS
            if FORCE_INTERVAL_SECONDS is not None:
                interval_seconds = FORCE_INTERVAL_SECONDS
                print(f"Using forced interval: {interval_seconds}s")
            if FORCE_MAX_SCREENSHOTS is not None:
                max_screenshots = FORCE_MAX_SCREENSHOTS
                print(f"Using forced max screenshots: {max_screenshots}")
        except ImportError:
            pass
        
        print(f"Video info: {duration_minutes:.1f} minutes ({duration_seconds:.0f}s), {fps:.1f} fps")
        print(f"Using {interval_seconds}s intervals, max {max_screenshots} screenshots")
        
        frame_interval = int(fps * interval_seconds) # Calculate frames to skip
        frame_count = 0
        screenshot_details = []

        while frame_count * frame_interval < total_frames and len(screenshot_details) < max_screenshots:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count * frame_interval)
            
            ret, frame = cap.read()
            if not ret:
                break
                
            time_in_seconds = (frame_count * frame_interval) / fps
            minutes = int(time_in_seconds // 60)
            seconds = int(time_in_seconds % 60)
            time_str = f"{minutes:02d}_{seconds:02d}"

            screenshot_name = f"ss_{time_str}.jpg"
            screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
            cv2.imwrite(screenshot_path, frame)

            screenshot_details.append(f"File: {screenshot_path}, Time: {time_str}")
            print(f"Screenshot {len(screenshot_details)}: {time_str} ({time_in_seconds/60:.1f} min)")
            frame_count += 1

        cap.release()
        print(f"Extracted {len(screenshot_details)} screenshots from {duration_seconds/60:.1f} minute video")
        os.remove(video_path)

        # Get transcript with timestamps
        try:
            from youtube_transcript_api import YouTubeTranscriptApi
            video_id = extract_video_id(youtube_url)
            
            if video_id:
                # Try to get transcript in different languages
                try:
                    transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
                except:
                    try:
                        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en-US'])
                    except:
                        try:
                            # Try to get any available transcript
                            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
                        except:
                            # If all else fails, skip transcript
                            raise Exception("No transcript available")
                
                # Save full transcript with timestamps
                transcript_path = os.path.join(os.getcwd(), "transcript.txt")
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write("=== FULL TRANSCRIPT WITH TIMESTAMPS ===\n\n")
                    for item in transcript_list:
                        start_time = item['start']
                        duration = item['duration']
                        text = item['text']
                        minutes = int(start_time // 60)
                        seconds = int(start_time % 60)
                        f.write(f"[{minutes:02d}:{seconds:02d}] {text}\n")
                    
                    f.write("\n\n=== PLAIN TEXT TRANSCRIPT ===\n\n")
                    f.write(" ".join([item['text'] for item in transcript_list]))
                
                # Also save a structured transcript for easier processing
                structured_transcript_path = os.path.join(os.getcwd(), "transcript_structured.json")
                with open(structured_transcript_path, "w", encoding="utf-8") as f:
                    json.dump(transcript_list, f, indent=2)
                
                screenshot_details.append(f"Transcript available at: {transcript_path}")
                screenshot_details.append(f"Structured transcript at: {structured_transcript_path}")
            else:
                screenshot_details.append("Warning: Could not extract video ID for transcript")

        except Exception as e:
            screenshot_details.append(f"Warning: Could not get transcript: {e}")


        if not screenshot_details:
             return "No screenshots or data were extracted from the video."

        return "\n".join(screenshot_details)

    except Exception as e:
        return f"An error occurred during video processing: {e}"          