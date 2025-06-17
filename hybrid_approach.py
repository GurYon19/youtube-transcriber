#!/usr/bin/env python3
"""
Hybrid approach: 
1. First try to get Hebrew transcripts from YouTube API (fast, no bot detection)
2. For videos without transcripts, create a list for local processing with authentication
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
    """Get Hebrew transcript from YouTube API if available."""
    try:
        video_id = get_video_id_from_url(url)
        if not video_id:
            return None, None, "Could not extract video ID"
        
        print(f"Checking for Hebrew transcript: {video_id}")
        
        # Try Hebrew language codes
        language_preferences = ['he', 'iw']
        
        for lang in language_preferences:
            try:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
                
                if transcript:
                    formatter = TextFormatter()
                    text_transcript = formatter.format_transcript(transcript)
                    video_title = f"video_{video_id}"  # Simple title
                    
                    print(f"✅ Found Hebrew transcript ({lang})")
                    return text_transcript, video_title, None
                    
            except Exception as e:
                continue
        
        return None, None, "No Hebrew transcript available"
        
    except Exception as e:
        return None, None, f"Error: {e}"

def save_transcript_to_file(transcript, video_title):
    """Save transcript to file."""
    if not transcript:
        return None
        
    clean_title = video_title.replace(' ', '_').replace('|', '').replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace('"', '_')
    filename = f"transcript_{clean_title}.txt"
    
    if len(filename) > 200:
        filename = filename[:200] + ".txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)
        
    print(f"📄 Transcript saved: {filename}")
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

def create_remaining_links_file(failed_urls, filename="remaining_links.txt"):
    """Create a file with URLs that need local processing."""
    if not failed_urls:
        print("🎉 All videos had Hebrew transcripts! No local processing needed.")
        return
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Videos that need local audio transcription\n")
        f.write("# These videos don't have Hebrew transcripts available\n")
        f.write("# Process these locally with authentication\n\n")
        for url in failed_urls:
            f.write(f"{url}\n")
    
    print(f"📝 Created {filename} with {len(failed_urls)} videos for local processing")
    return filename

# Main execution
if __name__ == "__main__":
    links_file = "links.txt"
    
    youtube_links = read_links_from_file(links_file)
    
    if not youtube_links:
        print("No links found in links.txt")
        exit()
    
    total_links = len(youtube_links)
    print(f"🚀 Processing {total_links} YouTube links with HYBRID approach:")
    print("📊 Phase 1: Hebrew Transcript API (fast, no login)")
    print("🎵 Phase 2: Local audio processing (for remaining videos)")
    print("-" * 60)
    
    successful_count = 0
    failed_urls = []
    
    # Phase 1: Try transcript API for all videos
    for i, url in enumerate(youtube_links, 1):
        print(f"\n[{i}/{total_links}] Processing: {url}")
        
        # Small delay to be nice to YouTube
        time.sleep(random.uniform(0.5, 1.5))
        
        transcript, video_title, error = get_transcript_from_youtube(url)
        
        if transcript and video_title:
            save_transcript_to_file(transcript, video_title)
            successful_count += 1
        else:
            print(f"❌ No Hebrew transcript: {error}")
            failed_urls.append(url)
    
    # Results summary
    print("\n" + "="*60)
    print("📊 PHASE 1 RESULTS (Transcript API)")
    print("="*60)
    print(f"✅ Hebrew transcripts found: {successful_count}")
    print(f"❌ Need audio processing: {len(failed_urls)}")
    print(f"📈 Success rate: {(successful_count/total_links)*100:.1f}%")
    
    # Phase 2: Create file for local processing
    if failed_urls:
        remaining_file = create_remaining_links_file(failed_urls)
        print("\n" + "="*60)
        print("🎵 PHASE 2: LOCAL AUDIO PROCESSING")
        print("="*60)
        print(f"📁 File created: {remaining_file}")
        print(f"🔢 Videos to process locally: {len(failed_urls)}")
        print("\n🔧 Next steps:")
        print("1. Run local script with authentication")
        print("2. Process remaining videos with Whisper")
        print("3. You can log into YouTube locally for better access")
        print("\n💡 Use: python local_with_auth.py")
    else:
        print("\n🎉 Amazing! All videos had Hebrew transcripts!")
        print("No local processing needed. You're done! 🚀") 