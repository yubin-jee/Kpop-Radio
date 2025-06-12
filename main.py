#!/usr/bin/env python3
"""
K-pop Idol Radio Show Generator

This script generates a K-pop radio show segment by:
1. Creating a script using OpenAI GPT-4
2. Converting the script to audio using ElevenLabs TTS
3. Saving the audio file to assets/audio/

Usage: python main.py
"""

import os
import sys
from datetime import datetime
from script_generator import ScriptGenerator
from voice_generator import VoiceGenerator
from dotenv import load_dotenv

def check_api_keys():
    """Check if required API keys are set"""
    load_dotenv()
    
    openai_key = os.getenv('OPENAI_API_KEY')
    eleven_key = os.getenv('ELEVEN_API_KEY')
    
    missing_keys = []
    if not openai_key or openai_key == 'your_openai_api_key_here':
        missing_keys.append('OPENAI_API_KEY')
    if not eleven_key or eleven_key == 'your_elevenlabs_api_key_here':
        missing_keys.append('ELEVEN_API_KEY')
    
    if missing_keys:
        print("❌ Missing API keys in .env file:")
        for key in missing_keys:
            print(f"   - {key}")
        print("\nPlease add your API keys to the .env file and try again.")
        return False
    
    print("✅ API keys found!")
    return True

def main():
    """Main function to run the K-pop radio show generator"""
    
    print("🎵 K-pop Idol Radio Show Generator 🎵")
    print("=" * 50)
    
    # Check API keys
    if not check_api_keys():
        sys.exit(1)
    
    try:
        # Step 1: Generate script segments
        print("\n📝 Generating radio script segments...")
        script_gen = ScriptGenerator()
        segments = script_gen.generate_script_segments()
        
        if not segments:
            print("❌ Failed to generate script segments")
            sys.exit(1)
        
        print("✅ Script segments generated successfully!")
        
        # Display generated segments
        for segment_name, script in segments.items():
            print(f"\n" + "─" * 50)
            print(f"{segment_name.upper()} SEGMENT:")
            print("─" * 50)
            print(script)
        
        # Step 2: Generate audio for each segment with different voices
        print("\n🎤 Converting segments to audio with different voices...")
        voice_gen = VoiceGenerator()
        
        # Define voice mapping for different segments
        voice_mapping = {
            'intro': "21m00Tcm4TlvDq8ikWAM",      # Rachel - warm, welcoming
            'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Bella - energetic  
            'fan_mail': "21m00Tcm4TlvDq8ikWAM"     # Rachel - warm, personal
        }
        
        audio_files = voice_gen.generate_segment_audio(segments, voice_mapping)
        
        if not audio_files:
            print("❌ Failed to generate audio segments")
            sys.exit(1)
        
        print("✅ All audio segments generated successfully!")
        
        # Step 3: Stitch segments together
        print("\n🎵 Combining segments into final radio show...")
        from audio_stitcher import AudioStitcher
        
        stitcher = AudioStitcher()
        final_audio_path = stitcher.stitch_segments(audio_files, "idol_radio_show.wav")
        
        if not final_audio_path:
            print("❌ Failed to stitch audio segments")
            sys.exit(1)
        
        print("\n🎉 K-pop idol radio show generated successfully!")
        print(f"🎧 Final show saved to: {final_audio_path}")
        
        # Display summary
        print("\n" + "=" * 60)
        print("📋 GENERATION SUMMARY:")
        print("=" * 60)
        print(f"📝 Generated {len(segments)} script segments")
        print(f"🎤 Created {len(audio_files)} audio files with different voices")
        print(f"🎵 Combined into final radio show: {os.path.basename(final_audio_path)}")
        
        # Show individual files
        print(f"\n📁 Individual segment files:")
        for segment_name, file_path in audio_files.items():
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            print(f"   • {segment_name}: {os.path.basename(file_path)} ({file_size:.2f} MB)")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Generation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 