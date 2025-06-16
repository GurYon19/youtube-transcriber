import os
import time
import random
import re
import whisper
from pytubefix import YouTube

def download_audio_from_youtube(url):
    """
    Downloads the audio track from a YouTube video and saves it as a file.
    Includes bot detection workarounds.
    """
    
    try:
        print(f"Downloading audio from link: {url}")
        
        # Add random delay to avoid bot detection
        delay = random.uniform(1, 3)
        print(f"Waiting {delay:.1f} seconds to avoid bot detection...")
        time.sleep(delay)
        
        # Try multiple approaches to avoid bot detection
        approaches = [
            # Approach 1: Use po_token and WEB client
            lambda: YouTube(url, use_po_token=True, client='WEB'),
            # Approach 2: Use WEB client only
            lambda: YouTube(url, client='WEB'),
            # Approach 3: Use ANDROID client
            lambda: YouTube(url, client='ANDROID'),
            # Approach 4: Default approach
            lambda: YouTube(url)
        ]
        
        yt = None
        last_error = None
        
        for i, approach in enumerate(approaches, 1):
            try:
                print(f"Trying approach {i}/{len(approaches)}...")
                yt = approach()
                print(f"✅ Approach {i} successful!")
                break
            except Exception as e:
                last_error = e
                print(f"❌ Approach {i} failed: {e}")
                if i < len(approaches):
                    time.sleep(random.uniform(0.5, 1.5))
                continue
        
        if not yt:
            print(f"All approaches failed. Last error: {last_error}")
            return None
        
        # Select the best quality audio stream
        audio_stream = yt.streams.get_audio_only()
        
        if not audio_stream:
            print("No audio stream available for this video")
            return None
        
        # Download the file (name will be automatically determined by video title)
        output_file = audio_stream.download()
        print(f"Audio saved to file: {output_file}")
        
        return output_file
        
    except Exception as e:
        print(f"Error occurred while downloading video: {e}")
        return None

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
    Safely gets the video title with bot detection workarounds.
    """
    
    try:
        # Add small delay
        time.sleep(random.uniform(0.5, 1.0))
        
        # Try multiple approaches to get title
        approaches = [
            lambda: YouTube(url, use_po_token=True, client='WEB'),
            lambda: YouTube(url, client='WEB'),
            lambda: YouTube(url, client='ANDROID'),
            lambda: YouTube(url)
        ]
        
        for i, approach in enumerate(approaches, 1):
            try:
                yt = approach()
                title = yt.title
                print(f"Video title: {title}")
                return title
            except Exception as e:
                print(f"Failed to get title with approach {i}: {e}")
                if i < len(approaches):
                    time.sleep(random.uniform(0.3, 0.8))
                continue
        
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
        # Step 1: Download audio
        audio_file = download_audio_from_youtube(url)
        
        if audio_file:
            # Step 2: Transcribe audio
            transcript = transcribe_audio_with_whisper(audio_file)
            
            # Step 3: Get video title safely
            video_title = get_safe_video_title(url)
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

