#!/usr/bin/env python3
"""
Simple Audio Stitcher - Works without ffmpeg
Combines MP3 files using basic concatenation or converts to WAV for stitching
"""

import os
import wave
import struct
from datetime import datetime

class SimpleAudioStitcher:
    def __init__(self):
        self.output_dir = "assets/audio"
    
    def simple_mp3_concat(self, audio_files, output_filename=None):
        """Simple MP3 concatenation by joining file data"""
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"combined_radio_show_{timestamp}.mp3"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        try:
            print(f"\n🎵 Attempting simple MP3 concatenation...")
            
            # Define the order of segments
            segment_order = ['intro', 'top_songs', 'fan_mail']
            
            with open(output_path, 'wb') as outfile:
                for segment_name in segment_order:
                    if segment_name in audio_files:
                        audio_path = audio_files[segment_name]
                        print(f"   Adding {segment_name} segment...")
                        
                        with open(audio_path, 'rb') as infile:
                            # Read and write the MP3 data
                            outfile.write(infile.read())
                    else:
                        print(f"   ⚠️  Warning: {segment_name} segment not found")
            
            # Get file info
            file_size = os.path.getsize(output_path)
            file_size_mb = file_size / (1024 * 1024)
            
            print(f"✅ Combined MP3 created!")
            print(f"📁 Saved to: {output_path}")
            print(f"📊 File size: {file_size_mb:.2f} MB")
            print(f"⚠️  Note: This is a simple concatenation. Audio players may show incorrect duration.")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error in simple concatenation: {e}")
            return None
    
    def create_m3u_playlist(self, audio_files, output_filename=None):
        """Create an M3U playlist file for proper audio playback"""
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"kpop_radio_playlist_{timestamp}.m3u"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        try:
            print(f"\n📝 Creating M3U playlist...")
            
            segment_order = ['intro', 'top_songs', 'fan_mail']
            
            with open(output_path, 'w') as playlist:
                playlist.write("#EXTM3U\n")
                playlist.write("#PLAYLIST:K-pop Idol Radio Show\n\n")
                
                for segment_name in segment_order:
                    if segment_name in audio_files:
                        audio_path = audio_files[segment_name]
                        filename = os.path.basename(audio_path)
                        
                        # Add playlist entry
                        playlist.write(f"#EXTINF:-1,{segment_name.replace('_', ' ').title()} Segment\n")
                        playlist.write(f"{filename}\n\n")
            
            print(f"✅ M3U playlist created: {output_path}")
            print(f"🎧 You can open this file in any media player to play the segments in order")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error creating playlist: {e}")
            return None
    
    def try_alternative_stitching(self, audio_files):
        """Try multiple approaches to combine audio"""
        
        print(f"\n🔧 Trying alternative audio stitching methods...")
        
        results = []
        
        # Method 1: Simple MP3 concatenation
        result1 = self.simple_mp3_concat(audio_files, "simple_concat_show.mp3")
        if result1:
            results.append(("Simple MP3 Concat", result1))
        
        # Method 2: M3U Playlist
        result2 = self.create_m3u_playlist(audio_files, "radio_show.m3u")
        if result2:
            results.append(("M3U Playlist", result2))
        
        return results

def main():
    """Test the simple stitcher with existing audio files"""
    
    stitcher = SimpleAudioStitcher()
    
    # Look for the most recent audio files
    audio_dir = "assets/audio"
    
    # Find the most recent timestamp
    mp3_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
    
    if not mp3_files:
        print("❌ No MP3 files found. Please run main.py first to generate audio segments.")
        return
    
    # Extract timestamp from files (format: segment_YYYYMMDD_HHMMSS.mp3)
    timestamps = set()
    for f in mp3_files:
        if '_' in f:
            parts = f.split('_')
            if len(parts) >= 3:
                # Combine date and time parts: YYYYMMDD_HHMMSS
                timestamp = f"{parts[-2]}_{parts[-1].replace('.mp3', '')}"
                timestamps.add(timestamp)
    
    if not timestamps:
        print("❌ Could not find timestamped audio files.")
        return
    
    # Use the most recent timestamp
    latest_timestamp = max(timestamps)
    print(f"🔍 Found audio files with timestamp: {latest_timestamp}")
    
    # Build audio files dictionary
    audio_files = {}
    for segment in ['intro', 'top_songs', 'fan_mail']:
        filename = f"{segment}_{latest_timestamp}.mp3"
        filepath = os.path.join(audio_dir, filename)
        if os.path.exists(filepath):
            audio_files[segment] = filepath
            print(f"   ✅ Found {segment}: {filename}")
        else:
            print(f"   ❌ Missing {segment}: {filename}")
    
    if len(audio_files) < 3:
        print("❌ Not all audio segments found.")
        return
    
    # Try stitching
    results = stitcher.try_alternative_stitching(audio_files)
    
    print(f"\n🎉 Audio stitching complete!")
    print(f"📋 Created {len(results)} output files:")
    for method, filepath in results:
        print(f"   • {method}: {os.path.basename(filepath)}")

if __name__ == "__main__":
    main() 