#!/usr/bin/env python3
"""
Enhanced K-pop Idol Radio Show Generator

Advanced features:
- Custom voice management with ElevenLabs API fluency
- Language selection (English/Korean/Mixed) with --lang flag
- Sound effects integration (jingles, applause, background music)
- Configuration-driven voice assignments per segment
- Full production pipeline with idol_radio_show_with_sfx.wav output

Usage: 
    python main.py                    # Default configuration
    python main.py --lang korean      # Korean-focused content
    python main.py --lang english     # English-only content
    python main.py --lang mixed       # Korean-English mixed (default)
    python main.py --preset korean_focus    # Apply Korean preset
    python main.py --no-sfx           # Disable sound effects
"""

import os
import sys
import argparse
from datetime import datetime
from dotenv import load_dotenv

# Import our enhanced modules
from config import config, apply_preset
from custom_voice import CustomVoiceManager
from sound_effects import SoundEffectsManager
from korean_script_generator import KoreanScriptGenerator
from script_generator import ScriptGenerator
from voice_generator import VoiceGenerator
from simple_stitcher import SimpleAudioStitcher

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description='Enhanced K-pop Idol Radio Show Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                           # Default mixed language with SFX
  python main.py --lang korean             # Korean-focused content
  python main.py --lang english            # English-only content
  python main.py --preset korean_focus     # Apply Korean preset
  python main.py --no-sfx                  # No sound effects
  python main.py --voice-dj YOUR_VOICE_ID  # Use custom voice for DJ
        """
    )
    
    parser.add_argument(
        '--lang', '--language',
        choices=['english', 'korean', 'mixed'],
        default=config.language_settings['default_language'],
        help='Language for content generation (default: %(default)s)'
    )
    
    parser.add_argument(
        '--preset',
        choices=['korean_focus', 'english_focus', 'full_production', 'minimal_production'],
        help='Apply a configuration preset'
    )
    
    parser.add_argument(
        '--no-sfx', '--no-sound-effects',
        action='store_true',
        help='Disable sound effects (jingles, applause, background music)'
    )
    
    parser.add_argument(
        '--voice-dj',
        help='Custom voice ID for DJ/host segments'
    )
    
    parser.add_argument(
        '--voice-fan',
        help='Custom voice ID for fan mail segments'
    )
    
    parser.add_argument(
        '--voice-guest',
        help='Custom voice ID for guest/energetic segments'
    )
    
    parser.add_argument(
        '--list-voices',
        action='store_true',
        help='List all available voices and exit'
    )
    
    parser.add_argument(
        '--output',
        default=config.output_settings['final_filename'],
        help='Output filename (default: %(default)s)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    return parser.parse_args()

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

def setup_configuration(args):
    """Setup configuration based on command line arguments"""
    
    # Apply preset if specified
    if args.preset:
        apply_preset(args.preset)
    
    # Set language
    if args.lang:
        config.set_language(args.lang)
    
    # Update voice assignments if specified
    if args.voice_dj:
        config.update_voice_mapping('dj', args.voice_dj)
    if args.voice_fan:
        config.update_voice_mapping('fan', args.voice_fan)
    if args.voice_guest:
        config.update_voice_mapping('guest', args.voice_guest)
    
    # Handle sound effects
    if args.no_sfx:
        config.enable_sound_effects(jingle=False, applause=False, background_music=False)
    
    # Update output filename
    if args.output != config.output_settings['final_filename']:
        config.output_settings['final_filename'] = args.output
    
    # Ensure directories exist
    config.ensure_directories()

def generate_script_content(language):
    """Generate script content based on language setting"""
    
    print(f"📝 Generating {language} script content...")
    
    if language == 'korean' or language == 'mixed':
        # Use Korean-mixed script generator
        script_gen = KoreanScriptGenerator()
        segments = script_gen.generate_korean_mixed_segments()
        
        if language == 'korean':
            print("🇰🇷 Using Korean-focused script generator")
        else:
            print("🇰🇷🇺🇸 Using Korean-English mixed script generator")
            
    else:  # English
        # Use English-only script generator
        script_gen = ScriptGenerator()
        segments = script_gen.generate_script_segments()
        print("🇺🇸 Using English-only script generator")
    
    return segments

def generate_audio_with_custom_voices(segments, verbose=False):
    """Generate audio using custom voice management"""
    
    print("🎤 Generating audio with custom voice assignments...")
    
    # Initialize voice generator and custom voice manager
    voice_gen = VoiceGenerator()
    custom_voice_manager = CustomVoiceManager()
    
    # Create voice mapping from configuration
    voice_mapping = {}
    for segment_name in segments.keys():
        voice_id = config.get_voice_for_segment(segment_name)
        voice_mapping[segment_name] = voice_id
        
        if verbose:
            # Get voice details
            voice_details = custom_voice_manager.get_voice_details(voice_id)
            voice_name = voice_details['name'] if voice_details else 'Unknown'
            print(f"   {segment_name}: {voice_name} ({voice_id})")
    
    # Generate audio for each segment
    audio_files = voice_gen.generate_segment_audio(segments, voice_mapping)
    
    if not audio_files:
        print("❌ Failed to generate audio segments")
        return None
    
    print("✅ All audio segments generated successfully!")
    return audio_files

def apply_sound_effects(audio_files, verbose=False):
    """Apply sound effects to create full production"""
    
    if not config.sound_effects['enabled']:
        print("🔇 Sound effects disabled, skipping...")
        return None
    
    print("🎬 Applying sound effects for full production...")
    
    # First, stitch segments together
    stitcher = SimpleAudioStitcher()
    base_show_path = stitcher.try_alternative_stitching(audio_files)
    
    if not base_show_path:
        print("❌ Failed to stitch audio segments")
        return None
    
    # Use the simple concatenated version for sound effects
    if isinstance(base_show_path, list):
        # Get the simple concat version
        for method, filepath in base_show_path:
            if 'concat' in method.lower():
                base_show_path = filepath
                break
        else:
            base_show_path = base_show_path[0][1]  # Use first available
    
    # Initialize sound effects manager
    sfx_manager = SoundEffectsManager()
    
    # Apply full production with sound effects
    final_audio_path = sfx_manager.create_full_production(
        audio_file_path=base_show_path,
        include_jingle=config.sound_effects['include_jingle'],
        include_applause=config.sound_effects['include_applause'],
        include_bg_music=config.sound_effects['include_background_music'],
        bg_style=config.sound_effects['background_music_style'],
        output_filename=config.get_final_output_filename()
    )
    
    return final_audio_path

def list_available_voices():
    """List all available voices and exit"""
    
    print("🎤 Listing all available ElevenLabs voices...")
    print("=" * 60)
    
    try:
        custom_voice_manager = CustomVoiceManager()
        voice_data = custom_voice_manager.list_all_voices()
        
        if not voice_data:
            print("❌ No voices found")
            return
        
        organized = voice_data.get('organized', {})
        details = voice_data.get('details', {})
        
        # Show organized voices
        for category, voices in organized.items():
            if voices:
                print(f"\n{category.upper()} VOICES ({len(voices)}):")
                print("-" * 40)
                for voice in voices:
                    print(f"🎤 {voice['name']}")
                    print(f"   ID: {voice['voice_id']}")
                    if voice['description']:
                        print(f"   Description: {voice['description'][:80]}...")
                    print()
        
        # Show K-pop recommendations
        print("\n🌟 RECOMMENDED FOR K-POP RADIO:")
        print("-" * 40)
        recommendations = custom_voice_manager.get_recommended_voices_for_kpop()
        
        for role, config_info in recommendations.items():
            print(f"\n{role.upper().replace('_', ' ')}:")
            primary = config_info['primary']
            print(f"  Primary: {primary['name']} ({primary['voice_id']}) {'✅' if primary['available'] else '❌'}")
            alternative = config_info['alternative']
            print(f"  Alternative: {alternative['name']} ({alternative['voice_id']}) {'✅' if alternative['available'] else '❌'}")
            print(f"  Use for: {config_info['description']}")
        
        print(f"\n📊 Total voices available: {voice_data['total_count']}")
        
    except Exception as e:
        print(f"❌ Error listing voices: {e}")

def main():
    """Main function to run the enhanced K-pop radio show generator"""
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Handle voice listing
    if args.list_voices:
        list_available_voices()
        return
    
    print("🎵 Enhanced K-pop Idol Radio Show Generator 🎵")
    print("=" * 60)
    
    # Check API keys
    if not check_api_keys():
        sys.exit(1)
    
    # Setup configuration
    setup_configuration(args)
    
    # Print current configuration
    if args.verbose:
        config.print_current_config()
    
    try:
        # Step 1: Generate script content based on language setting
        print(f"\n📝 Step 1: Generating script content...")
        segments = generate_script_content(config.language_settings['default_language'])
        
        if not segments:
            print("❌ Failed to generate script segments")
            sys.exit(1)
        
        print("✅ Script segments generated successfully!")
        
        # Display generated segments
        for segment_name, script in segments.items():
            print(f"\n" + "─" * 60)
            print(f"📻 {segment_name.upper()} SEGMENT:")
            print("─" * 60)
            print(script)
        
        # Step 2: Generate audio with custom voice assignments
        print(f"\n🎤 Step 2: Converting to audio with custom voices...")
        audio_files = generate_audio_with_custom_voices(segments, verbose=args.verbose)
        
        if not audio_files:
            print("❌ Failed to generate audio segments")
            sys.exit(1)
        
        # Step 3: Apply sound effects and create final production
        print(f"\n🎬 Step 3: Creating final production...")
        
        if config.sound_effects['enabled'] and not args.no_sfx:
            final_audio_path = apply_sound_effects(audio_files, verbose=args.verbose)
        else:
            # Just stitch segments without sound effects
            print("🔇 Creating show without sound effects...")
            stitcher = SimpleAudioStitcher()
            results = stitcher.try_alternative_stitching(audio_files)
            
            if results and isinstance(results, list):
                # Copy the simple concat version to final filename
                import shutil
                from pydub import AudioSegment
                
                for method, filepath in results:
                    if 'concat' in method.lower():
                        final_filename = config.get_final_output_filename()
                        final_path = config.get_output_path(final_filename)
                        
                        # Convert to WAV format
                        audio = AudioSegment.from_file(filepath)
                        audio.export(final_path, format="wav")
                        final_audio_path = final_path
                        break
                else:
                    final_audio_path = results[0][1]
            else:
                final_audio_path = results
        
        if not final_audio_path:
            print("❌ Failed to create final production")
            sys.exit(1)
        
        # Step 4: Display results
        print("\n🎉 K-pop idol radio show generated successfully!")
        
        # Show final results
        print("\n" + "=" * 60)
        print("📋 GENERATION SUMMARY:")
        print("=" * 60)
        
        print(f"🌐 Language: {config.language_settings['default_language']}")
        print(f"🎤 Generated {len(segments)} segments with custom voices")
        print(f"🎬 Sound effects: {'✅' if config.sound_effects['enabled'] and not args.no_sfx else '❌'}")
        
        # Show individual segment files
        print(f"\n📁 Individual segment files:")
        for segment_name, file_path in audio_files.items():
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                voice_id = config.get_voice_for_segment(segment_name)
                print(f"   • {segment_name}: {os.path.basename(file_path)} ({file_size:.2f} MB) - Voice: {voice_id}")
        
        # Show final output
        if os.path.exists(final_audio_path):
            file_size = os.path.getsize(final_audio_path) / (1024 * 1024)  # MB
            from pydub import AudioSegment
            audio = AudioSegment.from_file(final_audio_path)
            duration_seconds = len(audio) / 1000.0
            
            print(f"\n🎧 Final radio show:")
            print(f"   📁 File: {os.path.basename(final_audio_path)}")
            print(f"   ⏱️  Duration: {duration_seconds:.1f} seconds")
            print(f"   📊 Size: {file_size:.2f} MB")
            print(f"   📍 Location: {final_audio_path}")
        
        # Show voice assignments used
        print(f"\n🎤 Voice assignments used:")
        custom_voice_manager = CustomVoiceManager()
        for segment_name in segments.keys():
            voice_id = config.get_voice_for_segment(segment_name)
            voice_details = custom_voice_manager.get_voice_details(voice_id)
            voice_name = voice_details['name'] if voice_details else 'Unknown'
            print(f"   • {segment_name}: {voice_name} ({voice_id})")
        
        print(f"\n✨ Your enhanced K-pop radio show is ready!")
        print(f"🎵 Play: {final_audio_path}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Generation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 