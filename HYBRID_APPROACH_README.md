# 🚀 Hybrid YouTube Transcription Approach

**The BEST solution for getting Hebrew transcripts from YouTube!**

## 🎯 How It Works

This hybrid approach combines two methods for maximum success:

1. **Phase 1**: Extract existing Hebrew transcripts (fast, no authentication needed)
2. **Phase 2**: Download audio and transcribe locally (for videos without transcripts, with authentication)

## 📊 Expected Results

- **Phase 1**: ~60-80% of videos usually have Hebrew transcripts already
- **Phase 2**: Remaining 20-40% processed locally with Whisper
- **Total**: Near 100% success rate!

## 🔧 Setup Instructions

### 1. Install Dependencies (Local)

```bash
pip install -r requirements_local.txt
```

### 2. Prepare Your Links

Make sure your `links.txt` file contains your YouTube URLs:
```
https://www.youtube.com/watch?v=...
https://www.youtube.com/watch?v=...
```

## 🚀 Usage

### Phase 1: Extract Existing Transcripts

```bash
python hybrid_approach.py
```

This will:
- ✅ Extract Hebrew transcripts for videos that have them
- ✅ Create `remaining_links.txt` for videos that need audio processing
- ✅ Show you success statistics

### Phase 2: Local Processing (If Needed)

If some videos don't have transcripts, process them locally:

```bash
python local_with_auth.py
```

## 🔐 Authentication Setup (For Phase 2)

If you get "Sign in to confirm you're not a bot" errors:

### Option 1: Browser Cookies (Easiest)

1. **Edit `local_with_auth.py`**
2. **Uncomment line ~28**:
   ```python
   'cookiesfrombrowser': ('chrome',),  # or 'firefox', 'edge', 'safari'
   ```
3. **Make sure you're logged into YouTube** in that browser
4. **Run the script again**

### Option 2: Cookie File

1. **Export cookies** from your browser to `youtube_cookies.txt`
2. **Edit `local_with_auth.py`**
3. **Uncomment line ~31**:
   ```python
   'cookiefile': 'youtube_cookies.txt',
   ```

## 📁 File Structure

```
├── links.txt                    # Your YouTube URLs
├── hybrid_approach.py           # Phase 1: Extract transcripts
├── local_with_auth.py          # Phase 2: Local processing
├── remaining_links.txt         # Created automatically
├── transcript_*.txt            # Generated transcripts
└── requirements_local.txt      # Dependencies
```

## 🎯 Advantages

### ✅ Phase 1 (Transcript API):
- **Super fast** (seconds per video)
- **No bot detection** issues
- **No authentication** needed
- **High quality** existing transcripts

### ✅ Phase 2 (Local + Auth):
- **You can log in** to YouTube
- **Whisper transcription** for missing content
- **Full control** over the process
- **Works with restricted** videos

## 📊 Example Output

```
🚀 Processing 96 YouTube links with HYBRID approach:
📊 Phase 1: Hebrew Transcript API (fast, no login)
🎵 Phase 2: Local audio processing (for remaining videos)

[1/96] Processing: https://www.youtube.com/watch?v=...
✅ Found Hebrew transcript (he)
📄 Transcript saved: transcript_video_ABC123.txt

[2/96] Processing: https://www.youtube.com/watch?v=...
❌ No Hebrew transcript: No transcript available

============================
📊 PHASE 1 RESULTS
============================
✅ Hebrew transcripts found: 73
❌ Need audio processing: 23
📈 Success rate: 76.0%

📁 File created: remaining_links.txt
🔢 Videos to process locally: 23
💡 Use: python local_with_auth.py
```

## 🔧 Troubleshooting

### "No Hebrew transcript available"
- **Normal!** Not all videos have transcripts
- **Solution**: Phase 2 will handle these

### "Sign in to confirm you're not a bot"
- **Expected** for Phase 2
- **Solution**: Enable authentication (see above)

### "Could not find downloaded file"
- **Check**: File permissions
- **Solution**: Run with administrator rights

### Whisper loading slowly
- **Normal** on first run (downloads model)
- **Subsequent runs** are much faster

## 💡 Pro Tips

1. **Run Phase 1 first** - you might not need Phase 2!
2. **Use Chrome cookies** - usually most reliable
3. **Process in batches** - don't overwhelm your system
4. **Check results** after each phase

## 🎉 Expected Timeline

- **Phase 1**: 5-10 minutes for 96 videos
- **Phase 2**: 2-5 minutes per video (depending on length)
- **Total**: Much faster than pure audio processing!

---

**Happy transcribing! 🎬➡️📝** 