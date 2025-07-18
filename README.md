# YouTube Transcription with GitHub Actions

This project automatically transcribes YouTube videos to Hebrew text using OpenAI's Whisper model, running on GitHub Actions.

## Setup

1. **Fork/Clone this repository** to your GitHub account

2. **Add YouTube URLs** to `links.txt` (one URL per line)

3. **Run the workflow**:
   - Go to Actions tab in your GitHub repository
   - Click "YouTube Transcription" workflow
   - Click "Run workflow" button

## How it works

- Downloads audio from YouTube videos using `pytubefix`
- Transcribes audio to Hebrew text using OpenAI Whisper
- Saves transcriptions as text files
- Uploads results as GitHub artifacts
- Optionally commits results back to the repository

## Limitations

⚠️ **Important considerations when running on GitHub Actions:**

- **Time limit**: 6 hours maximum per job
- **Resources**: Limited CPU (2 cores) and RAM (7GB)
- **Storage**: ~14GB available disk space
- **Free tier**: 2000 minutes/month for public repos
- **Model size**: Using 'medium' model for balance of speed/accuracy

## Files

- `a.py` - Main transcription script
- `links.txt` - YouTube URLs to process
- `.github/workflows/transcribe.yml` - GitHub Actions workflow (manual setup)
- `.github/workflows/transcribe-docker.yml` - GitHub Actions workflow (Docker)
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker container definition
- `docker-compose.yml` - Docker Compose configuration
- `.dockerignore` - Files to exclude from Docker build

## Docker Advantages

✅ **No dependency conflicts** - Everything runs in an isolated container  
✅ **Cross-platform** - Works identically on Windows, Mac, Linux  
✅ **Easy setup** - Just install Docker, no Python/ffmpeg setup needed  
✅ **Clean environment** - No leftover files on your system  
✅ **Reproducible** - Same results every time

## Local Usage

### Option 1: Using Docker (Recommended)

**Prerequisites**: Install [Docker](https://www.docker.com/get-started)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t youtube-transcriber .
docker run --rm -v $(pwd):/app/output youtube-transcriber
```

### Option 2: Direct Python Installation

```bash
pip install -r requirements.txt
python a.py
```

### Option 3: Using Docker on Windows

```cmd
# Build the image
docker build -t youtube-transcriber .

# Run on Windows (PowerShell)
docker run --rm -v ${PWD}:/app/output youtube-transcriber

# Run on Windows (Command Prompt)
docker run --rm -v %cd%:/app/output youtube-transcriber
```

## Output

Transcriptions are saved as `transcript_[video_title].txt` files and available as GitHub artifacts for 30 days. 