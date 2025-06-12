#!/usr/bin/env python3
"""
Korean-American K-pop Idol Radio Show Generator

This script generates a complete K-pop radio show with:
1. Korean-English mixed scripts for authentic feel
2. Multiple voices optimized for Korean pronunciation
3. Professional audio stitching

Usage: python korean_main.py
"""

import os
import sys
from datetime import datetime
from korean_script_generator import KoreanScriptGenerator
from voice_generator import VoiceGenerator
from simple_stitcher import SimpleAudioStitcher
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
    """Main function to run the Korean-American K-pop radio show generator"""
    
    print("🇰🇷🇺🇸 Korean-American K-pop Idol Radio Show Generator 🇰🇷🇺🇸")
    print("=" * 70)
    
    # Check API keys
    if not check_api_keys():
        sys.exit(1)
    
    try:
        # Step 1: Generate Korean-English mixed script segments
        print("\n📝 Generating Korean-English mixed radio script segments...")
        script_gen = KoreanScriptGenerator()
        segments = script_gen.generate_korean_mixed_segments()
        
        if not segments:
            print("❌ Failed to generate script segments")
            sys.exit(1)
        
        print("✅ Korean-mixed script segments generated successfully!")
        
        # Display generated segments
        for segment_name, script in segments.items():
            print(f"\n" + "─" * 60)
            print(f"🇰🇷 {segment_name.upper()} SEGMENT (Korean-English Mixed):")
            print("─" * 60)
            print(script)
        
        # Step 2: Generate audio for each segment with Korean-optimized voices
        print("\n🎤 Converting segments to audio with Korean-optimized voices...")
        voice_gen = VoiceGenerator()
        
        # Use Korean-optimized voice mapping
        korean_voice_mapping = script_gen.get_korean_voice_mapping()
        
        print(f"\n🎭 Voice Assignment:")
        voice_names = {
            "XB0fDUnXU5powFXDhCwa": "Charlotte",
            "EXAVITQu4vr4xnSDxMaL": "Sarah", 
            "cgSgspJ2msm6clMCkdW9": "Jessica"
        }
        
        for segment, voice_id in korean_voice_mapping.items():
            voice_name = voice_names.get(voice_id, "Unknown")
            print(f"   • {segment}: {voice_name} (optimized for Korean pronunciation)")
        
        audio_files = voice_gen.generate_segment_audio(segments, korean_voice_mapping)
        
        if not audio_files:
            print("❌ Failed to generate audio segments")
            sys.exit(1)
        
        print("✅ All Korean-mixed audio segments generated successfully!")
        
        # Step 3: Stitch segments together using simple stitcher
        print("\n🎵 Combining segments into final Korean-American radio show...")
        
        stitcher = SimpleAudioStitcher()
        results = stitcher.try_alternative_stitching(audio_files)
        
        if not results:
            print("❌ Failed to stitch audio segments")
            sys.exit(1)
        
        print("\n🎉 Korean-American K-pop idol radio show generated successfully!")
        
        # Display summary
        print("\n" + "=" * 70)
        print("📋 KOREAN-AMERICAN RADIO SHOW GENERATION SUMMARY:")
        print("=" * 70)
        print(f"🇰🇷 Generated {len(segments)} Korean-English mixed script segments")
        print(f"🎤 Created {len(audio_files)} audio files with Korean-optimized voices")
        print(f"🎵 Combined into {len(results)} output formats")
        
        # Show individual files
        print(f"\n📁 Individual segment files:")
        for segment_name, file_path in audio_files.items():
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            voice_name = voice_names.get(korean_voice_mapping[segment_name], "Unknown")
            print(f"   • {segment_name}: {os.path.basename(file_path)} ({file_size:.2f} MB) - {voice_name}")
        
        print(f"\n🎧 Final combined files:")
        for method, filepath in results:
            print(f"   • {method}: {os.path.basename(filepath)}")
        
        # Korean phrases used
        print(f"\n🇰🇷 Korean phrases included:")
        korean_phrases = [
            "Annyeonghaseyo (Hello)",
            "Yeoreobun (Everyone)", 
            "Jinjja (Really)",
            "Daebak (Awesome)",
            "Saranghae (I love you)",
            "Gomawo (Thank you)",
            "Jjang (The best)",
            "Chingu (Friend)"
        ]
        
        for phrase in korean_phrases:
            print(f"   • {phrase}")
        
        print(f"\n✨ Your authentic Korean-American K-pop radio show is ready!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Generation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 