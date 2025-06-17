#!/usr/bin/env python3
"""
Alternative approach: Use YouTube's existing transcripts instead of downloading audio.
Many videos already have auto-generated Hebrew transcripts.
"""

import os
import time
import random
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def get_video_id_from_url(url):
    """Extract video ID from YouTube URL."""
    video_id_match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})(?:\S+)?', url)
    if video_id_match:
        return video_id_match.group(1)
    return None

def get_transcript_from_youtube(url):
    """
    Get transcript directly from YouTube (if available).
    Much faster and no bot detection issues.
    """
    try:
        video_id = get_video_id_from_url(url)
        if not video_id:
            print(f"Could not extract video ID from: {url}")
            return None, None
        
        print(f"Getting transcript for video ID: {video_id}")
        
        # Only get Hebrew transcripts
        language_preferences = ['he', 'iw']  # 'he' = Hebrew, 'iw' = Hebrew (alternative code)
        
        for lang in language_preferences:
            try:
                print(f"Trying Hebrew language code: {lang}")
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                
                if transcript:
                    # Format the transcript
                    formatter = TextFormatter()
                    text_transcript = formatter.format_transcript(transcript)
                    
                    # Get video title from transcript metadata or use video ID
                    try:
                        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
                        video_title = f"video_{video_id}"  # Fallback
                        # Try to get a better title if possible
                    except:
                        video_title = f"video_{video_id}"
                    
                    print(f"✅ Successfully got Hebrew transcript with language code: {lang}")
                    return text_transcript, video_title
                    
            except Exception as e:
                print(f"❌ Hebrew language code {lang} failed: {e}")
                continue
        
        print("❌ No Hebrew transcript available for this video")
        return None, None
        
    except Exception as e:
        print(f"Error getting transcript: {e}")
        return None, None

def save_transcript_to_file(transcript, video_title):
    """Save transcript to file."""
    if not transcript:
        return None
        
    # Create a clean filename
    clean_title = video_title.replace(' ', '_').replace('|', '').replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace('"', '_')
    filename = f"transcript_{clean_title}.txt"
    
    # Ensure the filename is not too long
    if len(filename) > 200:
        filename = filename[:200] + ".txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)
        
    print(f"Transcript saved to: {filename}")
    return filename

def read_links_from_file(file_path):
    """Read YouTube links from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return links
    except Exception as e:
        print(f"Error reading links file: {e}")
        return []

def process_youtube_link_transcript(url, processed_count, total_count):
    """Process a single YouTube link using transcript API."""
    print(f"\n--- Processing video {processed_count}/{total_count} (Hebrew Transcript API) ---")
    print(f"URL: {url}")
    
    # Add small delay to avoid rate limiting
    delay = random.uniform(1, 3)
    print(f"Waiting {delay:.1f} seconds...")
    time.sleep(delay)
    
    try:
        transcript, video_title = get_transcript_from_youtube(url)
        
        if transcript and video_title:
            save_transcript_to_file(transcript, video_title)
            return True
        else:
            print("No Hebrew transcript available, skipping this video.")
            return False
            
    except Exception as e:
        print(f"Error processing video {url}: {e}")
        return False

# Main execution
if __name__ == "__main__":
    links_file = "links.txt"
    
    youtube_links = read_links_from_file(links_file)
    
    if not youtube_links:
        print("No links found in links.txt")
        exit()
    
    total_links = len(youtube_links)
    print(f"Found {total_links} YouTube links to process using Hebrew Transcript API.")
    print("This method is much faster and avoids bot detection!")
    print("📝 Only Hebrew transcripts will be extracted!")
    
    successful_count = 0
    failed_count = 0
    
    for i, url in enumerate(youtube_links, 1):
        success = process_youtube_link_transcript(url, i, total_links)
        
        if success:
            successful_count += 1
        else:
            failed_count += 1
    
    # Final summary
    print("\n--- Processing Complete ---")
    print(f"Total videos processed: {total_links}")
    print(f"Successful Hebrew transcripts: {successful_count}")
    print(f"Failed/No Hebrew transcript: {failed_count}")
    print(f"Success rate: {(successful_count/total_links)*100:.1f}%") 