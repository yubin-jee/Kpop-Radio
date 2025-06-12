# 🎵 K-pop Idol Radio Show Generator

A Python project that generates complete K-pop radio shows with multiple segments, different voices, and professional audio stitching using OpenAI GPT for script generation and ElevenLabs for text-to-speech conversion.

## Features

- 🎤 **Multiple Segments**: Generates 3 distinct radio segments (intro, top songs, fan mail)
- 🎭 **Multiple Voices**: Uses different ElevenLabs voices for each segment
- 🎵 **Professional Content**: Authentic K-pop radio content with realistic songs and fan interactions
- 🔊 **High-Quality Audio**: Converts scripts to broadcast-quality audio using ElevenLabs TTS
- 🎬 **Audio Stitching**: Combines segments into a complete radio show (with fallback playlist)
- 📁 **Smart File Management**: Automatically saves all files with timestamps
- ⚡ **Easy-to-use Interface**: Beautiful console interface with progress indicators

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API keys:**
   - Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Get your ElevenLabs API key from [ElevenLabs Settings](https://elevenlabs.io/app/settings/api-keys)
   
3. **Create a `.env` file in the project root:**
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ELEVEN_API_KEY=your_elevenlabs_api_key_here
   ```

## Usage

Run the main script to generate a complete K-pop radio show segment:

```bash
python main.py
```

The script will:
1. Generate 3 separate radio segments using GPT (intro, top songs, fan mail)
2. Convert each segment to audio using different ElevenLabs voices
3. Combine all segments into a complete radio show
4. Save individual segments and final show to `assets/audio/`

## Project Structure

```
kpop-idol-radio/
├── main.py                 # Main orchestration script
├── script_generator.py     # GPT script generation (3 segments)
├── voice_generator.py      # ElevenLabs TTS with multiple voices
├── audio_stitcher.py       # Audio combining and processing
├── requirements.txt        # Python dependencies
├── .env                   # API keys (create this file)
├── assets/
│   └── audio/             # Generated audio files and final show
└── README.md              # This file
```

## Individual Components

### Script Generator
```bash
python script_generator.py
```
Generates and displays all 3 K-pop radio segments individually.

### Voice Generator
```bash
python voice_generator.py
```
Tests the text-to-speech functionality with different voices.

### Audio Stitcher
```bash
python audio_stitcher.py
```
Tests the audio combining functionality.

## Customization

- **Voice Mapping**: Modify the `voice_mapping` in `main.py` to assign different voices to segments
- **Segment Content**: Edit prompts in `script_generator.py` to change the style of each segment
- **Audio Settings**: Adjust voice settings in `voice_generator.py` for different audio characteristics
- **Segment Order**: Change the `segment_order` in `audio_stitcher.py` to reorder segments
- **Silence Duration**: Modify `silence_duration` in `audio_stitcher.py` for different pacing

## Requirements

- Python 3.7+
- OpenAI API key with GPT-4 access
- ElevenLabs API key
- Internet connection for API calls

## Output

Generated files are saved in `assets/audio/` with timestamps:

### Individual Segments:
- `intro_YYYYMMDD_HHMMSS.mp3` - Warm welcome and show introduction
- `top_songs_YYYYMMDD_HHMMSS.mp3` - Top 3 K-pop songs segment  
- `fan_mail_YYYYMMDD_HHMMSS.mp3` - Fan mail reading segment

### Final Show:
- `idol_radio_show.wav` - Combined complete radio show (or playlist file if stitching fails)
- Quality: High-quality audio suitable for broadcasting
- Duration: Typically 60-90 seconds total

## Troubleshooting

### Audio Stitching Issues
If audio stitching fails (missing ffmpeg), the system will:
1. Create individual MP3 files for each segment
2. Generate a playlist file showing the correct playback order
3. You can manually play the files in sequence or install ffmpeg for automatic stitching

### Installing ffmpeg (Optional)
For automatic audio stitching:
```bash
# macOS with Homebrew
brew install ffmpeg

# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

Enjoy creating your professional K-pop radio shows! 🎉 