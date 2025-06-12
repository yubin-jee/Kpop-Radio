import os
from datetime import datetime

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("Warning: pydub not available. Audio stitching will be limited.")

class AudioStitcher:
    def __init__(self):
        self.silence_duration = 1000  # 1 second of silence between segments
    
    def stitch_segments(self, audio_files, output_filename=None, add_silence=True):
        """Combine multiple audio files into a single file"""
        
        if not PYDUB_AVAILABLE:
            return self._simple_concatenate(audio_files, output_filename)
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"idol_radio_show_{timestamp}.wav"
        
        output_path = os.path.join("assets", "audio", output_filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            print(f"\n🎵 Stitching audio segments together...")
            
            # Create silence segment if needed
            silence = AudioSegment.silent(duration=self.silence_duration) if add_silence else None
            
            # Load and combine audio segments
            combined_audio = AudioSegment.empty()
            
            # Define the order of segments
            segment_order = ['intro', 'top_songs', 'fan_mail']
            
            for i, segment_name in enumerate(segment_order):
                if segment_name in audio_files:
                    audio_path = audio_files[segment_name]
                    print(f"   Adding {segment_name} segment...")
                    
                    try:
                        # Load the audio file - try different methods
                        if audio_path.endswith('.mp3'):
                            # For MP3, try without ffmpeg first
                            with open(audio_path, 'rb') as f:
                                segment_audio = AudioSegment.from_file(f, format="mp3")
                        elif audio_path.endswith('.wav'):
                            segment_audio = AudioSegment.from_wav(audio_path)
                        else:
                            # Try to detect format automatically
                            segment_audio = AudioSegment.from_file(audio_path)
                        
                        # Add the segment to combined audio
                        combined_audio += segment_audio
                        
                        # Add silence between segments (except after the last one)
                        if add_silence and i < len(segment_order) - 1 and silence:
                            combined_audio += silence
                            
                    except Exception as segment_error:
                        print(f"   ⚠️  Error loading {segment_name}: {segment_error}")
                        print(f"   Trying alternative method...")
                        # Fallback: just note the file exists for manual combination
                        continue
                else:
                    print(f"   ⚠️  Warning: {segment_name} segment not found, skipping...")
            
            if len(combined_audio) == 0:
                print("❌ No audio segments could be combined!")
                return self._simple_concatenate(audio_files, output_filename)
            
            # Export the combined audio
            combined_audio.export(output_path, format="wav")
            
            # Get file info
            duration_seconds = len(combined_audio) / 1000.0
            file_size = os.path.getsize(output_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"✅ Combined audio saved successfully!")
            print(f"📁 Saved to: {output_path}")
            print(f"⏱️  Duration: {duration_seconds:.1f} seconds")
            print(f"📊 File size: {file_size_mb:.2f} MB")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error stitching audio: {e}")
            print("🔄 Falling back to simple file listing...")
            return self._simple_concatenate(audio_files, output_filename)
    
    def _simple_concatenate(self, audio_files, output_filename=None):
        """Simple fallback when pydub/ffmpeg is not available"""
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"idol_radio_show_{timestamp}.txt"
        
        output_path = os.path.join("assets", "audio", output_filename)
        
        try:
            print(f"\n📝 Creating playlist file (audio stitching not available)...")
            
            # Create a playlist file with the segments in order
            segment_order = ['intro', 'top_songs', 'fan_mail']
            
            with open(output_path, 'w') as f:
                f.write("K-pop Idol Radio Show Playlist\n")
                f.write("=" * 40 + "\n\n")
                f.write("Play these files in order:\n\n")
                
                for i, segment_name in enumerate(segment_order):
                    if segment_name in audio_files:
                        audio_path = audio_files[segment_name]
                        f.write(f"{i+1}. {segment_name.upper()}: {os.path.basename(audio_path)}\n")
                        f.write(f"   Full path: {audio_path}\n\n")
            
            print(f"✅ Playlist created: {output_path}")
            print(f"📝 Individual audio files are ready to play in sequence")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating playlist: {e}")
            return None
    
    def add_intro_music(self, main_audio_path, intro_music_path, output_filename=None):
        """Add intro music to the beginning of the radio show"""
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"idol_radio_show_with_music_{timestamp}.wav"
        
        output_path = os.path.join("assets", "audio", output_filename)
        
        try:
            print(f"\n🎶 Adding intro music...")
            
            # Load the main audio and intro music
            main_audio = AudioSegment.from_file(main_audio_path)
            intro_music = AudioSegment.from_file(intro_music_path)
            
            # Fade in/out for smooth transitions
            intro_music = intro_music.fade_in(500).fade_out(1000)  # 0.5s fade in, 1s fade out
            
            # Combine intro music with main audio
            combined = intro_music + main_audio
            
            # Export the result
            combined.export(output_path, format="wav")
            
            print(f"✅ Audio with intro music saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error adding intro music: {e}")
            return None
    
    def adjust_volume(self, audio_path, volume_change_db, output_filename=None):
        """Adjust the volume of an audio file"""
        
        if not output_filename:
            base_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_filename = f"{base_name}_adjusted.wav"
        
        output_path = os.path.join("assets", "audio", output_filename)
        
        try:
            audio = AudioSegment.from_file(audio_path)
            adjusted_audio = audio + volume_change_db  # Increase/decrease volume
            adjusted_audio.export(output_path, format="wav")
            
            print(f"✅ Volume adjusted audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Error adjusting volume: {e}")
            return None

if __name__ == "__main__":
    # Test the audio stitcher
    stitcher = AudioStitcher()
    
    # Example usage (would need actual audio files)
    print("Audio Stitcher initialized successfully!")
    print("Use this class to combine multiple audio segments into a single radio show.") 