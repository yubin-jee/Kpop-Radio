#!/usr/bin/env python3
"""
Voice Customizer for K-pop Radio
Test different voices and create custom voice mappings
"""

import os
from voice_generator import VoiceGenerator
from korean_script_generator import KoreanScriptGenerator

class VoiceCustomizer:
    def __init__(self):
        self.voice_gen = VoiceGenerator()
        self.script_gen = KoreanScriptGenerator()
        
        # Available voices with descriptions
        self.available_voices = {
            "XB0fDUnXU5powFXDhCwa": {
                "name": "Charlotte",
                "description": "Clear, warm female voice - good for introductions",
                "best_for": "Intro segments, clear pronunciation"
            },
            "EXAVITQu4vr4xnSDxMaL": {
                "name": "Sarah", 
                "description": "Young, energetic female voice - great for upbeat content",
                "best_for": "Top songs, energetic segments"
            },
            "cgSgspJ2msm6clMCkdW9": {
                "name": "Jessica",
                "description": "Personal, heartfelt female voice",
                "best_for": "Fan mail, emotional content"
            },
            "FGY2WhTYpPnrIDTdsKH5": {
                "name": "Laura",
                "description": "Professional female voice",
                "best_for": "News, announcements"
            },
            "Xb7hH8MSUJpSbSDYk0k2": {
                "name": "Alice",
                "description": "Friendly female voice",
                "best_for": "Casual conversation"
            },
            "pFZP5JQG7iQjIQuC4Bku": {
                "name": "Lily",
                "description": "Sweet female voice",
                "best_for": "Gentle segments"
            }
        }
    
    def test_voice_with_korean(self, voice_id, voice_name):
        """Test a specific voice with Korean phrases"""
        
        test_phrases = [
            "Annyeonghaseyo yeoreobun!",
            "Jinjja daebak! This song is amazing!",
            "Saranghae listeners! Gomawo for tuning in!"
        ]
        
        print(f"\n🎤 Testing {voice_name} ({voice_id}) with Korean phrases:")
        print("-" * 50)
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"{i}. Testing: \"{phrase}\"")
            
            # Generate test audio
            test_filename = f"test_{voice_name.lower()}_{i}.mp3"
            audio_path = self.voice_gen.text_to_speech(
                text=phrase,
                output_filename=test_filename,
                voice_id=voice_id
            )
            
            if audio_path:
                print(f"   ✅ Generated: {test_filename}")
            else:
                print(f"   ❌ Failed to generate audio")
        
        return True
    
    def compare_voices_korean(self):
        """Compare multiple voices with the same Korean phrase"""
        
        test_phrase = "Annyeonghaseyo yeoreobun! Welcome to K-pop Vibes Radio! Jinjja excited to be here!"
        
        print(f"\n🎭 Voice Comparison with Korean Content:")
        print("=" * 60)
        print(f"Test phrase: \"{test_phrase}\"")
        print("-" * 60)
        
        # Test top 3 recommended voices
        recommended_voices = [
            "XB0fDUnXU5powFXDhCwa",  # Charlotte
            "EXAVITQu4vr4xnSDxMaL",  # Sarah
            "cgSgspJ2msm6clMCkdW9"   # Jessica
        ]
        
        for voice_id in recommended_voices:
            voice_info = self.available_voices.get(voice_id, {})
            voice_name = voice_info.get("name", "Unknown")
            
            print(f"\n🎤 {voice_name}:")
            print(f"   Description: {voice_info.get('description', 'N/A')}")
            
            # Generate comparison audio
            comparison_filename = f"comparison_{voice_name.lower()}.mp3"
            audio_path = self.voice_gen.text_to_speech(
                text=test_phrase,
                output_filename=comparison_filename,
                voice_id=voice_id
            )
            
            if audio_path:
                file_size = os.path.getsize(audio_path) / 1024  # KB
                print(f"   ✅ Generated: {comparison_filename} ({file_size:.1f} KB)")
            else:
                print(f"   ❌ Failed to generate audio")
    
    def create_custom_voice_mapping(self):
        """Interactive voice mapping creator"""
        
        print(f"\n🎛️  Custom Voice Mapping Creator")
        print("=" * 50)
        
        segments = ['intro', 'top_songs', 'fan_mail']
        custom_mapping = {}
        
        print("Available voices:")
        for voice_id, info in self.available_voices.items():
            print(f"  {info['name']}: {voice_id}")
            print(f"    - {info['description']}")
            print(f"    - Best for: {info['best_for']}")
            print()
        
        # For demo purposes, create a few preset mappings
        presets = {
            "korean_optimized": {
                'intro': "XB0fDUnXU5powFXDhCwa",      # Charlotte - clear
                'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Sarah - energetic
                'fan_mail': "cgSgspJ2msm6clMCkdW9"     # Jessica - heartfelt
            },
            "variety_pack": {
                'intro': "FGY2WhTYpPnrIDTdsKH5",      # Laura - professional
                'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Sarah - energetic
                'fan_mail': "pFZP5JQG7iQjIQuC4Bku"     # Lily - sweet
            },
            "single_voice": {
                'intro': "XB0fDUnXU5powFXDhCwa",      # Charlotte for all
                'top_songs': "XB0fDUnXU5powFXDhCwa",   
                'fan_mail': "XB0fDUnXU5powFXDhCwa"     
            }
        }
        
        print("🎯 Available Presets:")
        for preset_name, mapping in presets.items():
            print(f"\n{preset_name.upper()}:")
            for segment, voice_id in mapping.items():
                voice_name = self.available_voices.get(voice_id, {}).get("name", "Unknown")
                print(f"  • {segment}: {voice_name}")
        
        return presets
    
    def generate_voice_samples(self):
        """Generate sample audio for each available voice"""
        
        sample_text = "Hello! I'm excited to be your K-pop radio host today! Annyeonghaseyo!"
        
        print(f"\n🎵 Generating Voice Samples")
        print("=" * 40)
        print(f"Sample text: \"{sample_text}\"")
        print("-" * 40)
        
        for voice_id, info in self.available_voices.items():
            voice_name = info["name"]
            print(f"\n🎤 Generating sample for {voice_name}...")
            
            sample_filename = f"sample_{voice_name.lower()}.mp3"
            audio_path = self.voice_gen.text_to_speech(
                text=sample_text,
                output_filename=sample_filename,
                voice_id=voice_id
            )
            
            if audio_path:
                file_size = os.path.getsize(audio_path) / 1024  # KB
                print(f"   ✅ Generated: {sample_filename} ({file_size:.1f} KB)")
                print(f"   Description: {info['description']}")
            else:
                print(f"   ❌ Failed to generate sample")

def main():
    """Main function to run voice customization tools"""
    
    print("🎛️  K-pop Radio Voice Customizer")
    print("=" * 50)
    
    try:
        customizer = VoiceCustomizer()
        
        # Show available options
        print("\n🎯 Available Actions:")
        print("1. Compare voices with Korean content")
        print("2. Generate voice samples")
        print("3. Show custom voice mapping presets")
        print("4. Test specific voice with Korean phrases")
        
        # For demo, run comparison
        customizer.compare_voices_korean()
        
        # Show presets
        presets = customizer.create_custom_voice_mapping()
        
        print(f"\n💡 To use a custom voice mapping:")
        print("   1. Copy the voice IDs from the presets above")
        print("   2. Modify the voice_mapping in korean_main.py")
        print("   3. Or create your own mapping using the voice IDs")
        
        print(f"\n🎧 All sample files are saved in assets/audio/")
        
    except Exception as e:
        print(f"❌ Error in voice customizer: {e}")

if __name__ == "__main__":
    main() 