#!/usr/bin/env python3
"""
Sound Effects Manager for K-pop Radio
Add jingles, applause, background music, and other audio enhancements
"""

import os
import json
from datetime import datetime
from pydub import AudioSegment
from pydub.generators import Sine, WhiteNoise
from pydub.effects import normalize, compress_dynamic_range
import random

class SoundEffectsManager:
    def __init__(self, assets_path="assets"):
        self.assets_path = assets_path
        self.audio_path = os.path.join(assets_path, "audio")
        self.sfx_path = os.path.join(assets_path, "sfx")
        
        # Create directories if they don't exist
        os.makedirs(self.audio_path, exist_ok=True)
        os.makedirs(self.sfx_path, exist_ok=True)
        
        # Sound effect settings
        self.default_settings = {
            'jingle_volume': -10,  # dB reduction
            'applause_volume': -15,
            'background_music_volume': -25,
            'fade_duration': 1000,  # milliseconds
            'crossfade_duration': 500
        }
    
    def create_radio_jingle(self, duration_ms=3000, output_filename=None):
        """
        Create a K-pop radio jingle with multiple tones
        
        Args:
            duration_ms (int): Duration in milliseconds
            output_filename (str): Output filename (optional)
            
        Returns:
            str: Path to generated jingle file
        """
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"kpop_jingle_{timestamp}.wav"
        
        output_path = os.path.join(self.sfx_path, output_filename)
        
        try:
            print(f"🎵 Creating K-pop radio jingle ({duration_ms}ms)...")
            
            # Create multiple sine waves for a chord progression
            # K-pop style chord: C major - Am - F - G
            frequencies = [
                [523, 659, 784],  # C major chord (C5, E5, G5)
                [440, 523, 659],  # A minor chord (A4, C5, E5)
                [349, 440, 523],  # F major chord (F4, A4, C5)
                [392, 494, 587]   # G major chord (G4, B4, D5)
            ]
            
            # Create each chord segment
            chord_duration = duration_ms // 4
            jingle = AudioSegment.empty()
            
            for i, chord_freqs in enumerate(frequencies):
                print(f"   Adding chord {i+1}/4...")
                
                # Create chord by combining sine waves
                chord = AudioSegment.empty()
                for freq in chord_freqs:
                    tone = Sine(freq).to_audio_segment(duration=chord_duration)
                    tone = tone - 20  # Reduce volume
                    if len(chord) == 0:
                        chord = tone
                    else:
                        chord = chord.overlay(tone)
                
                # Add fade in/out for smooth transitions
                chord = chord.fade_in(100).fade_out(100)
                jingle += chord
            
            # Add some sparkle with higher frequency tones
            sparkle_freq = 1047  # C6
            sparkle_tone = Sine(sparkle_freq).to_audio_segment(duration=200)
            sparkle_tone = sparkle_tone - 25
            
            # Add sparkles at strategic points
            sparkle_positions = [500, 1500, 2500]
            for pos in sparkle_positions:
                if pos < len(jingle):
                    jingle = jingle.overlay(sparkle_tone, position=pos)
            
            # Normalize and add slight compression
            jingle = normalize(jingle)
            jingle = compress_dynamic_range(jingle)
            
            # Export jingle
            jingle.export(output_path, format="wav")
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ K-pop jingle created: {output_filename} ({file_size:.1f} KB)")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating jingle: {e}")
            return None
    
    def create_applause_effect(self, duration_ms=5000, intensity="medium", output_filename=None):
        """
        Create applause sound effect
        
        Args:
            duration_ms (int): Duration in milliseconds
            intensity (str): "light", "medium", or "heavy"
            output_filename (str): Output filename (optional)
            
        Returns:
            str: Path to generated applause file
        """
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"applause_{intensity}_{timestamp}.wav"
        
        output_path = os.path.join(self.sfx_path, output_filename)
        
        try:
            print(f"👏 Creating {intensity} applause effect ({duration_ms}ms)...")
            
            # Create base white noise
            applause = WhiteNoise().to_audio_segment(duration=duration_ms)
            
            # Apply filtering to make it sound more like applause
            # Reduce very high and very low frequencies
            applause = applause.low_pass_filter(8000)
            applause = applause.high_pass_filter(200)
            
            # Adjust volume based on intensity
            volume_adjustments = {
                "light": -30,
                "medium": -20,
                "heavy": -10
            }
            applause = applause + volume_adjustments.get(intensity, -20)
            
            # Add volume variations to simulate crowd dynamics
            segments = []
            segment_length = duration_ms // 10
            
            for i in range(10):
                start = i * segment_length
                end = start + segment_length
                segment = applause[start:end]
                
                # Random volume variation
                variation = random.randint(-8, 3)
                segment = segment + variation
                segments.append(segment)
            
            # Recombine segments
            applause = sum(segments)
            
            # Add fade in and fade out
            fade_duration = min(1000, duration_ms // 4)
            applause = applause.fade_in(fade_duration).fade_out(fade_duration)
            
            # Normalize
            applause = normalize(applause)
            
            # Export applause
            applause.export(output_path, format="wav")
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ Applause effect created: {output_filename} ({file_size:.1f} KB)")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating applause: {e}")
            return None
    
    def create_background_music(self, duration_ms=60000, style="upbeat", output_filename=None):
        """
        Create simple background music loop
        
        Args:
            duration_ms (int): Duration in milliseconds
            style (str): "upbeat", "chill", or "emotional"
            output_filename (str): Output filename (optional)
            
        Returns:
            str: Path to generated background music file
        """
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"bg_music_{style}_{timestamp}.wav"
        
        output_path = os.path.join(self.sfx_path, output_filename)
        
        try:
            print(f"🎶 Creating {style} background music ({duration_ms/1000:.1f}s)...")
            
            # Define chord progressions for different styles
            chord_progressions = {
                "upbeat": [
                    [523, 659, 784],  # C major
                    [440, 554, 659],  # A minor
                    [349, 440, 523],  # F major
                    [392, 494, 587]   # G major
                ],
                "chill": [
                    [440, 523, 659],  # A minor
                    [349, 440, 523],  # F major
                    [523, 659, 784],  # C major
                    [392, 494, 587]   # G major
                ],
                "emotional": [
                    [440, 523, 659],  # A minor
                    [349, 415, 523],  # F major (with 7th)
                    [523, 622, 784],  # C major (with 7th)
                    [392, 466, 587]   # G major (with 7th)
                ]
            }
            
            chords = chord_progressions.get(style, chord_progressions["upbeat"])
            
            # Create a loop pattern
            loop_duration = 8000  # 8 seconds per loop
            chord_duration = loop_duration // len(chords)
            
            # Create one loop
            loop = AudioSegment.empty()
            for chord_freqs in chords:
                chord = AudioSegment.empty()
                for freq in chord_freqs:
                    tone = Sine(freq).to_audio_segment(duration=chord_duration)
                    tone = tone - 30  # Very quiet background
                    if len(chord) == 0:
                        chord = tone
                    else:
                        chord = chord.overlay(tone)
                
                # Add gentle fade for smooth transitions
                chord = chord.fade_in(200).fade_out(200)
                loop += chord
            
            # Repeat loop to fill duration
            background_music = AudioSegment.empty()
            loops_needed = (duration_ms // loop_duration) + 1
            
            for i in range(loops_needed):
                background_music += loop
            
            # Trim to exact duration
            background_music = background_music[:duration_ms]
            
            # Add overall fade in/out
            fade_duration = min(2000, duration_ms // 10)
            background_music = background_music.fade_in(fade_duration).fade_out(fade_duration)
            
            # Normalize at low volume
            background_music = normalize(background_music) - 35
            
            # Export background music
            background_music.export(output_path, format="wav")
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ Background music created: {output_filename} ({file_size:.1f} KB)")
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating background music: {e}")
            return None
    
    def add_jingle_to_show(self, audio_file_path, jingle_path=None, position="start"):
        """
        Add jingle to radio show
        
        Args:
            audio_file_path (str): Path to main audio file
            jingle_path (str): Path to jingle file (optional, will create if None)
            position (str): "start", "end", or "both"
            
        Returns:
            str: Path to enhanced audio file
        """
        
        try:
            print(f"🎵 Adding jingle to radio show...")
            
            # Load main audio
            main_audio = AudioSegment.from_file(audio_file_path)
            
            # Create or load jingle
            if not jingle_path:
                jingle_path = self.create_radio_jingle()
            
            if not jingle_path or not os.path.exists(jingle_path):
                print("❌ Jingle file not found")
                return audio_file_path
            
            jingle = AudioSegment.from_file(jingle_path)
            jingle = jingle + self.default_settings['jingle_volume']  # Adjust volume
            
            # Add jingle based on position
            if position == "start":
                enhanced_audio = jingle + main_audio
            elif position == "end":
                enhanced_audio = main_audio + jingle
            elif position == "both":
                enhanced_audio = jingle + main_audio + jingle
            else:
                print(f"❌ Invalid position: {position}")
                return audio_file_path
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
            output_filename = f"{base_name}_with_jingle.wav"
            output_path = os.path.join(self.audio_path, output_filename)
            
            # Export enhanced audio
            enhanced_audio.export(output_path, format="wav")
            
            duration_seconds = len(enhanced_audio) / 1000.0
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ Jingle added to show: {output_filename}")
            print(f"   Duration: {duration_seconds:.1f}s, Size: {file_size:.2f} MB")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding jingle: {e}")
            return audio_file_path
    
    def add_applause_to_show(self, audio_file_path, applause_path=None, position="end", intensity="medium"):
        """
        Add applause to radio show
        
        Args:
            audio_file_path (str): Path to main audio file
            applause_path (str): Path to applause file (optional)
            position (str): "end", "start", or specific time in ms
            intensity (str): "light", "medium", or "heavy"
            
        Returns:
            str: Path to enhanced audio file
        """
        
        try:
            print(f"👏 Adding {intensity} applause to radio show...")
            
            # Load main audio
            main_audio = AudioSegment.from_file(audio_file_path)
            
            # Create or load applause
            if not applause_path:
                applause_path = self.create_applause_effect(intensity=intensity)
            
            if not applause_path or not os.path.exists(applause_path):
                print("❌ Applause file not found")
                return audio_file_path
            
            applause = AudioSegment.from_file(applause_path)
            applause = applause + self.default_settings['applause_volume']  # Adjust volume
            
            # Add applause based on position
            if position == "start":
                enhanced_audio = applause + main_audio
            elif position == "end":
                enhanced_audio = main_audio + applause
            elif isinstance(position, int):  # Specific time position
                enhanced_audio = main_audio.overlay(applause, position=position)
            else:
                print(f"❌ Invalid position: {position}")
                return audio_file_path
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
            output_filename = f"{base_name}_with_applause.wav"
            output_path = os.path.join(self.audio_path, output_filename)
            
            # Export enhanced audio
            enhanced_audio.export(output_path, format="wav")
            
            duration_seconds = len(enhanced_audio) / 1000.0
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ Applause added to show: {output_filename}")
            print(f"   Duration: {duration_seconds:.1f}s, Size: {file_size:.2f} MB")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding applause: {e}")
            return audio_file_path
    
    def add_background_music(self, audio_file_path, bg_music_path=None, style="upbeat", volume_db=-25):
        """
        Layer background music under the entire radio show
        
        Args:
            audio_file_path (str): Path to main audio file
            bg_music_path (str): Path to background music file (optional)
            style (str): "upbeat", "chill", or "emotional"
            volume_db (int): Background music volume adjustment in dB
            
        Returns:
            str: Path to enhanced audio file
        """
        
        try:
            print(f"🎶 Adding {style} background music to radio show...")
            
            # Load main audio
            main_audio = AudioSegment.from_file(audio_file_path)
            main_duration = len(main_audio)
            
            # Create or load background music
            if not bg_music_path:
                bg_music_path = self.create_background_music(
                    duration_ms=main_duration + 2000,  # Slightly longer
                    style=style
                )
            
            if not bg_music_path or not os.path.exists(bg_music_path):
                print("❌ Background music file not found")
                return audio_file_path
            
            bg_music = AudioSegment.from_file(bg_music_path)
            
            # Adjust background music length and volume
            bg_music = bg_music[:main_duration]  # Trim to match main audio
            bg_music = bg_music + volume_db  # Adjust volume
            
            # Layer background music under main audio
            enhanced_audio = bg_music.overlay(main_audio)
            
            # Generate output filename
            base_name = os.path.splitext(os.path.basename(audio_file_path))[0]
            output_filename = f"{base_name}_with_bg_music.wav"
            output_path = os.path.join(self.audio_path, output_filename)
            
            # Export enhanced audio
            enhanced_audio.export(output_path, format="wav")
            
            duration_seconds = len(enhanced_audio) / 1000.0
            file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
            print(f"✅ Background music added to show: {output_filename}")
            print(f"   Duration: {duration_seconds:.1f}s, Size: {file_size:.2f} MB")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding background music: {e}")
            return audio_file_path
    
    def create_full_production(self, audio_file_path, include_jingle=True, include_applause=True, 
                             include_bg_music=False, bg_style="upbeat", output_filename=None):
        """
        Create a full production with all sound effects
        
        Args:
            audio_file_path (str): Path to main audio file
            include_jingle (bool): Add jingle at start and end
            include_applause (bool): Add applause at end
            include_bg_music (bool): Add background music throughout
            bg_style (str): Background music style
            output_filename (str): Output filename (optional)
            
        Returns:
            str: Path to fully produced audio file
        """
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"idol_radio_show_with_sfx_{timestamp}.wav"
        
        try:
            print("🎬 Creating full production with sound effects...")
            print(f"   Jingle: {'✅' if include_jingle else '❌'}")
            print(f"   Applause: {'✅' if include_applause else '❌'}")
            print(f"   Background Music: {'✅' if include_bg_music else '❌'}")
            
            current_audio = audio_file_path
            
            # Step 1: Add background music if requested
            if include_bg_music:
                print("\n🎶 Step 1: Adding background music...")
                current_audio = self.add_background_music(current_audio, style=bg_style)
            
            # Step 2: Add jingle if requested
            if include_jingle:
                print("\n🎵 Step 2: Adding jingle...")
                current_audio = self.add_jingle_to_show(current_audio, position="both")
            
            # Step 3: Add applause if requested
            if include_applause:
                print("\n👏 Step 3: Adding applause...")
                current_audio = self.add_applause_to_show(current_audio, position="end")
            
            # Final step: Rename to desired output filename
            final_output_path = os.path.join(self.audio_path, output_filename)
            
            if current_audio != audio_file_path:
                # Copy the enhanced audio to final location
                enhanced_audio = AudioSegment.from_file(current_audio)
                enhanced_audio.export(final_output_path, format="wav")
                
                # Clean up intermediate files (optional)
                # os.remove(current_audio)  # Uncomment to clean up
            else:
                # No enhancements were made, just copy original
                original_audio = AudioSegment.from_file(audio_file_path)
                original_audio.export(final_output_path, format="wav")
            
            duration_seconds = len(AudioSegment.from_file(final_output_path)) / 1000.0
            file_size = os.path.getsize(final_output_path) / (1024 * 1024)  # MB
            
            print(f"\n🎉 Full production completed!")
            print(f"✅ Final show: {output_filename}")
            print(f"   Duration: {duration_seconds:.1f}s")
            print(f"   File size: {file_size:.2f} MB")
            
            return final_output_path
            
        except Exception as e:
            print(f"❌ Error creating full production: {e}")
            return audio_file_path
    
    def get_sfx_catalog(self):
        """
        Get a catalog of all available sound effects
        
        Returns:
            dict: Catalog of sound effects
        """
        
        catalog = {
            'jingles': [],
            'applause': [],
            'background_music': [],
            'other': []
        }
        
        if os.path.exists(self.sfx_path):
            for filename in os.listdir(self.sfx_path):
                if filename.endswith(('.wav', '.mp3', '.m4a')):
                    file_path = os.path.join(self.sfx_path, filename)
                    file_size = os.path.getsize(file_path) / 1024  # KB
                    
                    file_info = {
                        'filename': filename,
                        'path': file_path,
                        'size_kb': file_size
                    }
                    
                    if 'jingle' in filename.lower():
                        catalog['jingles'].append(file_info)
                    elif 'applause' in filename.lower():
                        catalog['applause'].append(file_info)
                    elif 'bg_music' in filename.lower() or 'background' in filename.lower():
                        catalog['background_music'].append(file_info)
                    else:
                        catalog['other'].append(file_info)
        
        return catalog

def main():
    """Main function to demonstrate sound effects functionality"""
    
    print("🎬 K-pop Radio Sound Effects Manager")
    print("=" * 50)
    
    try:
        sfx_manager = SoundEffectsManager()
        
        # Create sample sound effects
        print("\n1. 🎵 Creating radio jingle...")
        jingle_path = sfx_manager.create_radio_jingle(duration_ms=4000)
        
        print("\n2. 👏 Creating applause effects...")
        applause_light = sfx_manager.create_applause_effect(duration_ms=3000, intensity="light")
        applause_heavy = sfx_manager.create_applause_effect(duration_ms=5000, intensity="heavy")
        
        print("\n3. 🎶 Creating background music...")
        bg_upbeat = sfx_manager.create_background_music(duration_ms=30000, style="upbeat")
        bg_chill = sfx_manager.create_background_music(duration_ms=30000, style="chill")
        
        # Show catalog
        print("\n4. 📋 Sound Effects Catalog:")
        catalog = sfx_manager.get_sfx_catalog()
        
        for category, files in catalog.items():
            if files:
                print(f"\n{category.upper()}:")
                for file_info in files:
                    print(f"  • {file_info['filename']} ({file_info['size_kb']:.1f} KB)")
        
        print(f"\n✅ Sound Effects Manager demo completed!")
        print(f"📁 All sound effects saved in: {sfx_manager.sfx_path}")
        
    except Exception as e:
        print(f"❌ Error in sound effects manager: {e}")

if __name__ == "__main__":
    main() 