import os
import time
import random
import re
import whisper
import yt_dlp
import json

def download_audio_from_youtube(url):
    """
    Downloads the audio track from a YouTube video using yt-dlp.
    More robust against bot detection.
    Returns (audio_file_path, video_title) tuple.
    """
    
    try:
        print(f"Downloading audio from link: {url}")
        
        # Add random delay to avoid bot detection
        delay = random.uniform(2, 5)
        print(f"Waiting {delay:.1f} seconds to avoid bot detection...")
        time.sleep(delay)
        
        # Configure yt-dlp options for audio download
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(title)s.%(ext)s',
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192K',
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            # Bot detection avoidance
            'extractor_args': {
                'youtube': {
                    'skip': ['hls', 'dash'],
                    'player_client': ['android']
                }
            },
            # Add user agent to look more like a real browser
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                # Extract info first to get the title
                print("Getting video info...")
                info = ydl.extract_info(url, download=False)
                video_title = info.get('title', 'Unknown Video')
                print(f"Video title: {video_title}")
                
                # Download the audio
                print("Downloading audio...")
                ydl.download([url])
                
                # Find the downloaded file (yt-dlp may change the filename)
                import glob
                possible_files = glob.glob(f"{video_title[:50]}*")  # First 50 chars to avoid long filenames
                if not possible_files:
                    # Try broader search
                    possible_files = glob.glob("*.mp3") + glob.glob("*.m4a") + glob.glob("*.webm")
                    if possible_files:
                        # Get the most recently created file
                        output_file = max(possible_files, key=os.path.getctime)
                    else:
                        print("Could not find downloaded audio file")
                        return None, None
                else:
                    output_file = possible_files[0]
                
                print(f"Audio saved to file: {output_file}")
                return output_file, video_title
                
            except yt_dlp.utils.DownloadError as e:
                print(f"yt-dlp download error: {e}")
                return None, None
                
    except Exception as e:
        print(f"Error occurred while downloading video: {e}")
        return None, None

def transcribe_audio_with_whisper(audio_file_path):
    """
    Transcribes the audio file to Hebrew using the Whisper model.
    """
    if not audio_file_path:
        return None
        
    try:
        print("Loading transcription model... (this may take time on first run)")
        # Using 'medium' model for good balance between speed and accuracy for Hebrew
        # Consider using 'small' for faster processing on GitHub Actions
        model = whisper.load_model("medium") 
        
        print(f"Starting transcription of file: {audio_file_path}")
        # Transcribe the file specifying Hebrew language
        result = model.transcribe(audio_file_path, language="he")
        
        transcript_text = result["text"]
        print("Transcription completed successfully.")
        
        return transcript_text
    except Exception as e:
        print(f"Error occurred during transcription process: {e}")
        return None

def save_transcript_to_file(transcript, video_title):
    """
    Saves the transcript to a text file.
    """
    if not transcript:
        return
        
    # Create a clean filename
    clean_title = video_title.replace(' ', '_').replace('|', '').replace('/', '_').replace('\\', '_').replace(':', '_').replace('?', '_').replace('*', '_').replace('<', '_').replace('>', '_').replace('"', '_')
    filename = f"transcript_{clean_title}.txt"
    
    # Ensure the filename is not too long
    if len(filename) > 200:
        filename = filename[:200] + ".txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(transcript)
        
    print(f"Full transcript saved to file: {filename}")
    return filename

def get_safe_video_title(url):
    """
    Safely gets the video title using yt-dlp.
    """
    
    try:
        print("Getting video title...")
        
        # Configure yt-dlp for info extraction only
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_client': ['android']
                }
            }
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Unknown Video')
                print(f"Video title: {title}")
                return title
            except Exception as e:
                print(f"Failed to get title with yt-dlp: {e}")
                
        # Fallback: extract video ID from URL as title
        video_id_match = re.search(r'(?:v=|/)([a-zA-Z0-9_-]{11})(?:\S+)?', url)
        if video_id_match:
            video_id = video_id_match.group(1)
            print(f"Using video ID as title: {video_id}")
            return f"video_{video_id}"
        else:
            print("Could not extract video ID, using generic title")
            return f"video_{int(time.time())}"
            
    except Exception as e:
        print(f"Error getting video title: {e}")
        return f"video_{int(time.time())}"

def read_links_from_file(file_path):
    """
    Reads all YouTube links from a text file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
        return links
    except Exception as e:
        print(f"Error reading links file: {e}")
        return []

def process_youtube_link(url, processed_count, total_count):
    """
    Processes a single YouTube link: downloads audio, transcribes, and saves.
    """
    print(f"\n--- Processing video {processed_count}/{total_count} ---")
    print(f"URL: {url}")
    
    try:
        # Step 1: Download audio and get title
        audio_file, video_title = download_audio_from_youtube(url)
        
        if audio_file and video_title:
            # Step 2: Transcribe audio
            transcript = transcribe_audio_with_whisper(audio_file)
            
            # Step 3: Save transcript
            save_transcript_to_file(transcript, video_title)
            
            # Clean up temporary audio file
            os.remove(audio_file)
            print(f"Temporary audio file '{audio_file}' deleted.")
            
            return True
        else:
            print("Failed to download audio, skipping this video.")
            return False
            
    except Exception as e:
        print(f"Error processing video {url}: {e}")
        return False

# --- Main program section ---
if __name__ == "__main__":
    links_file = "links.txt"
    
    # Read all links from the file
    youtube_links = read_links_from_file(links_file)
    
    if not youtube_links:
        print("No links found in links.txt or file doesn't exist.")
        exit()
    
    total_links = len(youtube_links)
    print(f"Found {total_links} YouTube links to process.")
    
    # Process each link
    successful_count = 0
    failed_count = 0
    
    for i, url in enumerate(youtube_links, 1):
        success = process_youtube_link(url, i, total_links)
        
        if success:
            successful_count += 1
        else:
            failed_count += 1
    
    # Final summary
    print("\n--- Processing Complete ---")
    print(f"Total videos processed: {total_links}")
    print(f"Successful transcriptions: {successful_count}")
    print(f"Failed transcriptions: {failed_count}")

