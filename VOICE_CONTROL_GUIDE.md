# 🇰🇷🇺🇸 Voice Control & Korean-English Mixed Content Guide

## Overview
Your K-pop radio generator now supports **full voice control** and **authentic Korean-English mixed scripts** for a truly Korean-American radio experience!

## 🎤 Available Voices

### Current Voice Options
| Voice Name | Voice ID | Best For | Description |
|------------|----------|----------|-------------|
| **Charlotte** | `XB0fDUnXU5powFXDhCwa` | Intro segments | Clear, warm female voice - excellent for Korean pronunciation |
| **Sarah** | `EXAVITQu4vr4xnSDxMaL` | Top songs | Young, energetic female voice - perfect for upbeat content |
| **Jessica** | `cgSgspJ2msm6clMCkdW9` | Fan mail | Personal, heartfelt female voice - great for emotional content |
| **Laura** | `FGY2WhTYpPnrIDTdsKH5` | News/announcements | Professional female voice |
| **Alice** | `Xb7hH8MSUJpSbSDYk0k2` | Casual conversation | Friendly female voice |
| **Lily** | `pFZP5JQG7iQjIQuC4Bku` | Gentle segments | Sweet female voice |

## 🇰🇷 Korean-English Mixed Content

### Korean Phrases Included
- **Annyeonghaseyo** (안녕하세요) - Hello
- **Yeoreobun** (여러분) - Everyone
- **Jinjja** (진짜) - Really
- **Daebak** (대박) - Awesome/Amazing
- **Saranghae** (사랑해) - I love you
- **Gomawo** (고마워) - Thank you (casual)
- **Gamsahamnida** (감사합니다) - Thank you (formal)
- **Jjang** (짱) - The best
- **Chingu** (친구) - Friend
- **Neo-mu joha** (너무 좋아) - So good
- **Choegoui** (최고의) - The best
- **Jeongmal** (정말) - Really

### Sample Korean-Mixed Scripts

**Intro Segment:**
> "Annyeonghaseyo, yeoreobun! Hello beautiful listeners! I'm your host Minji, and welcome to K-pop Vibes Radio! Jinjja excited to be here with you today! We've got some daebak music and your lovely messages coming up!"

**Top Songs Segment:**
> "Jigeum! Now it's time for today's choegoui hits! Wah, these songs are jinjja daebak! At number three, we have 'Neon Dreams' by STELLAR - omo, this track is neo-mu joha!"

**Fan Mail Segment:**
> "Fan mail time! Soo-jin from LA writes: 'Saranghae your show!' Jeongmal gomawo, Soo-jin! Your messages make my heart so full. Keep sending them, yeoreobun!"

## 🎛️ Voice Control Options

### Method 1: Use Korean-Optimized Main Script
```bash
python korean_main.py
```
This uses the pre-configured Korean-optimized voice mapping:
- **Intro**: Charlotte (clear pronunciation)
- **Top Songs**: Sarah (energetic)
- **Fan Mail**: Jessica (heartfelt)

### Method 2: Test Different Voices
```bash
python voice_customizer.py
```
This generates comparison samples so you can hear how different voices handle Korean pronunciation.

### Method 3: Custom Voice Mapping

#### Available Presets:

**Korean Optimized** (Recommended):
```python
{
    'intro': "XB0fDUnXU5powFXDhCwa",      # Charlotte
    'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Sarah
    'fan_mail': "cgSgspJ2msm6clMCkdW9"     # Jessica
}
```

**Variety Pack**:
```python
{
    'intro': "FGY2WhTYpPnrIDTdsKH5",      # Laura
    'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Sarah
    'fan_mail': "pFZP5JQG7iQjIQuC4Bku"     # Lily
}
```

**Single Voice** (Consistent host):
```python
{
    'intro': "XB0fDUnXU5powFXDhCwa",      # Charlotte for all
    'top_songs': "XB0fDUnXU5powFXDhCwa",   
    'fan_mail': "XB0fDUnXU5powFXDhCwa"     
}
```

## 🔧 How to Customize Voices

### Option 1: Modify the Korean Script Generator
Edit `korean_script_generator.py` and change the `get_korean_voice_mapping()` method:

```python
def get_korean_voice_mapping(self):
    return {
        'intro': "YOUR_PREFERRED_VOICE_ID",
        'top_songs': "YOUR_PREFERRED_VOICE_ID", 
        'fan_mail': "YOUR_PREFERRED_VOICE_ID"
    }
```

### Option 2: Create Your Own Main Script
Copy `korean_main.py` and modify the voice mapping section:

```python
# Use your custom voice mapping
custom_voice_mapping = {
    'intro': "XB0fDUnXU5powFXDhCwa",      # Charlotte
    'top_songs': "cgSgspJ2msm6clMCkdW9",   # Jessica  
    'fan_mail': "pFZP5JQG7iQjIQuC4Bku"     # Lily
}

audio_files = voice_gen.generate_segment_audio(segments, custom_voice_mapping)
```

## 🎧 Generated Audio Files

When you run the generator, you'll get:

### Individual Segments:
- `intro_[timestamp].mp3` - Korean-English greeting
- `top_songs_[timestamp].mp3` - Top 3 songs with Korean expressions
- `fan_mail_[timestamp].mp3` - Fan mail with Korean endearments

### Combined Show:
- `simple_concat_show.mp3` - Complete radio show
- `radio_show.m3u` - Playlist file for professional playback

### Voice Comparison Files:
- `comparison_charlotte.mp3` - Charlotte voice sample
- `comparison_sarah.mp3` - Sarah voice sample  
- `comparison_jessica.mp3` - Jessica voice sample

## 🌟 Best Practices for Korean-American Radio

1. **Voice Selection**: Charlotte has the clearest pronunciation for Korean words
2. **Energy Matching**: Use Sarah for upbeat segments, Jessica for emotional content
3. **Consistency**: Consider using the same voice for the entire show for brand consistency
4. **Korean Pronunciation**: The romanized Korean is optimized for English TTS engines
5. **Cultural Authenticity**: Scripts naturally mix languages like real Korean-American hosts

## 🚀 Quick Start Commands

```bash
# Generate Korean-American radio show with optimized voices
python korean_main.py

# Test different voices with Korean content
python voice_customizer.py

# Generate regular English-only show (original)
python main.py
```

## 📁 File Structure
```
kpop-idol-radio/
├── korean_main.py              # Korean-mixed main generator
├── korean_script_generator.py  # Korean-English script generator
├── voice_customizer.py         # Voice testing and customization
├── voice_generator.py          # TTS engine
├── simple_stitcher.py         # Audio combining
└── assets/audio/              # All generated audio files
```

Your K-pop radio generator now creates authentic Korean-American content with full voice control! 🎉 