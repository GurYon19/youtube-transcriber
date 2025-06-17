#!/usr/bin/env python3
"""
Local processing script with authentication support.
This runs on your local computer where you can log into YouTube.
"""

import os
import time
import random
import re
import whisper
import yt_dlp

def download_audio_local_with_auth(url):
    """
    Download audio locally with authentication options.
    This works on your local computer where you can log into YouTube.
    """
    try:
        print(f"🎵 Downloading audio locally: {url}")
        
        # Enhanced yt-dlp configuration for local use with authentication
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192K',
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            
            # LOCAL AUTHENTICATION OPTIONS (uncomment as needed):
            
            # Option 1: Use cookies from your browser (recommended)
            # 'cookiesfrombrowser': ('chrome',),  # or 'firefox', 'edge', 'safari'
            
            # Option 2: Use cookie file (if you export cookies manually)
            # 'cookiefile': 'youtube_cookies.txt',
            
            # Option 3: Enhanced headers for local use
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            },
            
            # Local-friendly settings
            'socket_timeout': 30,
            'retries': 5,
            'fragment_retries': 5,
            'ignoreerrors': False,
            'sleep_interval': 1,
            'max_sleep_interval': 3,
        }
        
        print("🔧 Trying local download with enhanced configuration...")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Get video info and title
                print("📊 Getting video info...")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown Video')
                print(f"📹 Video: {video_title}")
                
                # Download the audio
                print("⬬ Downloading audio...")
                ydl.download([url])
                
                # Find the downloaded file
                import glob
                possible_files = glob.glob(f"{video_title[:50]}*")
                if not possible_files:
                    possible_files = glob.glob("*.mp3") + glob.glob("*.m4a") + glob.glob("*.webm")
                    if possible_files:
                        output_file = max(possible_files, key=os.path.getctime)
                    else:
                        print("❌ Could not find downloaded file")
                        return None, None
                else:
                    output_file = possible_files[0]
                
                print(f"✅ Audio downloaded: {output_file}")
                return output_file, video_title
                
            except yt_dlp.utils.DownloadError as e:
                if "Sign in to confirm" in str(e):
                    print("🔐 Authentication needed! See instructions below.")
                    print("\n" + "="*50)
                    print("🔑 AUTHENTICATION SETUP:")
                    print("="*50)
                    print("1. Open this script (local_with_auth.py)")
                    print("2. Uncomment ONE of these lines around line 28:")
                    print("   # 'cookiesfrombrowser': ('chrome',),")
                    print("   # 'cookiefile': 'youtube_cookies.txt',")
                    print("3. Make sure you're logged into YouTube in your browser")
                    print("4. Run the script again")
                    print("="*50)
                raise e
                
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None, None

def transcribe_with_whisper_local(audio_file):
    """Transcribe audio to Hebrew using Whisper locally."""
    if not audio_file:
        return None
        
    try:
        print("🤖 Loading Whisper model...")
        model = whisper.load_model("medium")  # Good balance for Hebrew
        
        print(f"🗣️  Transcribing: {audio_file}")
        result = model.transcribe(audio_file, language="he")
        
        transcript = result["text"]
        print("✅ Transcription completed!")
        
        return transcript
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return None

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
    """Read links from file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return links
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

def process_video_locally(url, count, total):
    """Process a single video locally with authentication."""
    print(f"\n{'='*60}")
    print(f"🎬 Processing video {count}/{total}")
    print(f"🔗 URL: {url}")
    print('='*60)
    
    try:
        # Step 1: Download audio with auth
        audio_file, video_title = download_audio_local_with_auth(url)
        
        if not audio_file or not video_title:
            return False
        
        # Step 2: Transcribe with Whisper
        transcript = transcribe_with_whisper_local(audio_file)
        
        if not transcript:
            return False
        
        # Step 3: Save transcript
        save_transcript_to_file(transcript, video_title)
        
        # Step 4: Clean up audio file
        try:
            os.remove(audio_file)
            print(f"🗑️  Cleaned up: {audio_file}")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        return False

# Main execution
if __name__ == "__main__":
    input_file = "remaining_links.txt"
    
    # Check if remaining links file exists
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        print("💡 Run the hybrid script first: python hybrid_approach.py")
        exit()
    
    links = read_links_from_file(input_file)
    
    if not links:
        print("No links found to process")
        exit()
    
    total = len(links)
    print(f"🚀 LOCAL PROCESSING WITH AUTHENTICATION")
    print(f"📊 Videos to process: {total}")
    print(f"🤖 Using Whisper for Hebrew transcription")
    print(f"🔐 Authentication: Available for YouTube login")
    
    successful = 0
    failed = 0
    
    for i, url in enumerate(links, 1):
        if process_video_locally(url, i, total):
            successful += 1
        else:
            failed += 1
        
        # Small delay between videos
        if i < total:
            time.sleep(2)
    
    # Final summary
    print("\n" + "="*60)
    print("🏁 LOCAL PROCESSING COMPLETE")
    print("="*60)
    print(f"✅ Successfully processed: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success rate: {(successful/total)*100:.1f}%")
    
    if successful > 0:
        print(f"\n🎉 {successful} new Hebrew transcripts created!")
    
    if failed > 0:
        print(f"\n💡 {failed} videos failed - they might need manual processing") 