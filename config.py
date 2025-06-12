#!/usr/bin/env python3
"""
Configuration Settings for K-pop Idol Radio Show Generator
Centralized configuration for voices, paths, languages, and sound effects
"""

import os
from datetime import datetime

class RadioConfig:
    """Configuration class for K-pop radio show generator"""
    
    def __init__(self):
        # ===== VOICE CONFIGURATION =====
        # Default voice IDs for different roles
        self.voice_roles = {
            'dj': 'XB0fDUnXU5powFXDhCwa',        # Charlotte - Main DJ/Host (clear, warm)
            'fan': 'cgSgspJ2msm6clMCkdW9',       # Jessica - Fan mail reader (personal, heartfelt)
            'guest': 'EXAVITQu4vr4xnSDxMaL',    # Sarah - Guest/energetic segments (young, energetic)
            'announcer': 'FGY2WhTYpPnrIDTdsKH5'  # Laura - Professional announcements
        }
        
        # Voice mapping for specific segments
        self.segment_voices = {
            'intro': self.voice_roles['dj'],
            'top_songs': self.voice_roles['guest'],
            'fan_mail': self.voice_roles['fan'],
            'outro': self.voice_roles['dj'],
            'news': self.voice_roles['announcer']
        }
        
        # Voice settings for ElevenLabs
        self.voice_settings = {
            'stability': 0.5,
            'similarity_boost': 0.8,
            'style': 0.2,
            'use_speaker_boost': True
        }
        
        # ===== LANGUAGE CONFIGURATION =====
        self.language_settings = {
            'default_language': 'english',  # 'english', 'korean', or 'mixed'
            'korean_romanization': True,    # Use romanized Korean for TTS
            'include_korean_phrases': True, # Include Korean expressions in English content
            'korean_phrase_frequency': 'medium'  # 'low', 'medium', 'high'
        }
        
        # Korean phrases by frequency level
        self.korean_phrases = {
            'low': [
                'annyeonghaseyo',  # hello
                'gomawo',          # thank you
                'saranghae'        # I love you
            ],
            'medium': [
                'annyeonghaseyo', 'gomawo', 'saranghae',
                'jinjja', 'daebak', 'yeoreobun', 'jjang'
            ],
            'high': [
                'annyeonghaseyo', 'gomawo', 'saranghae', 'jinjja', 'daebak', 
                'yeoreobun', 'jjang', 'neo-mu joha', 'choegoui', 'jeongmal',
                'gamsahamnida', 'chingu', 'omo', 'wah'
            ]
        }
        
        # ===== PATH CONFIGURATION =====
        self.paths = {
            'assets_root': 'assets',
            'audio_output': 'assets/audio',
            'sound_effects': 'assets/sfx',
            'voice_catalog': 'assets/audio',
            'temp_files': 'assets/temp'
        }
        
        # ===== SOUND EFFECTS CONFIGURATION =====
        self.sound_effects = {
            'enabled': True,
            'include_jingle': True,
            'include_applause': True,
            'include_background_music': False,  # Set to True to enable background music
            'jingle_position': 'both',          # 'start', 'end', 'both'
            'applause_position': 'end',         # 'start', 'end'
            'applause_intensity': 'medium',     # 'light', 'medium', 'heavy'
            'background_music_style': 'upbeat', # 'upbeat', 'chill', 'emotional'
            'volume_settings': {
                'jingle_volume': -10,           # dB reduction
                'applause_volume': -15,         # dB reduction
                'background_music_volume': -25  # dB reduction
            }
        }
        
        # ===== AUDIO CONFIGURATION =====
        self.audio_settings = {
            'output_format': 'wav',             # 'wav', 'mp3'
            'sample_rate': 44100,               # Hz
            'bit_depth': 16,                    # bits
            'channels': 1,                      # mono
            'normalize_audio': True,
            'add_silence_between_segments': True,
            'silence_duration': 500             # milliseconds
        }
        
        # ===== CONTENT CONFIGURATION =====
        self.content_settings = {
            'show_duration_target': 90,         # seconds (target duration)
            'segment_count': 3,                 # number of segments
            'include_timestamps': True,
            'include_show_id': True,
            'show_name': 'K-pop Vibes Radio',
            'host_name': 'Minji',
            'station_id': 'KPOP-FM'
        }
        
        # ===== OUTPUT CONFIGURATION =====
        self.output_settings = {
            'final_filename': 'idol_radio_show_with_sfx.wav',
            'include_timestamp_in_filename': True,
            'save_individual_segments': True,
            'save_intermediate_files': False,   # Keep temp files for debugging
            'create_playlist_file': True,
            'generate_metadata': True
        }
        
        # ===== API CONFIGURATION =====
        self.api_settings = {
            'openai_model': 'gpt-3.5-turbo',
            'elevenlabs_model': 'eleven_monolingual_v1',
            'max_retries': 3,
            'timeout_seconds': 30,
            'cache_voice_list': True,
            'cache_duration_minutes': 5
        }
    
    def get_voice_for_segment(self, segment_name):
        """Get the configured voice ID for a specific segment"""
        return self.segment_voices.get(segment_name, self.voice_roles['dj'])
    
    def get_voice_for_role(self, role):
        """Get the configured voice ID for a specific role"""
        return self.voice_roles.get(role, self.voice_roles['dj'])
    
    def get_korean_phrases_for_level(self, level=None):
        """Get Korean phrases for the configured or specified level"""
        if level is None:
            level = self.language_settings['korean_phrase_frequency']
        return self.korean_phrases.get(level, self.korean_phrases['medium'])
    
    def get_output_path(self, filename=None, path_type='audio_output'):
        """Get full output path for a file"""
        base_path = self.paths.get(path_type, self.paths['audio_output'])
        
        if filename is None:
            return base_path
        
        # Add timestamp if configured
        if self.output_settings['include_timestamp_in_filename'] and not filename.startswith('temp_'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
        
        return os.path.join(base_path, filename)
    
    def ensure_directories(self):
        """Create all configured directories if they don't exist"""
        for path_name, path_value in self.paths.items():
            os.makedirs(path_value, exist_ok=True)
            print(f"📁 Ensured directory: {path_value}")
    
    def update_voice_mapping(self, segment_or_role, voice_id):
        """Update voice mapping for a segment or role"""
        if segment_or_role in self.segment_voices:
            self.segment_voices[segment_or_role] = voice_id
            print(f"🎤 Updated {segment_or_role} segment voice to: {voice_id}")
        elif segment_or_role in self.voice_roles:
            self.voice_roles[segment_or_role] = voice_id
            print(f"🎤 Updated {segment_or_role} role voice to: {voice_id}")
        else:
            print(f"❌ Unknown segment or role: {segment_or_role}")
    
    def set_language(self, language):
        """Set the primary language for content generation"""
        valid_languages = ['english', 'korean', 'mixed']
        if language.lower() in valid_languages:
            self.language_settings['default_language'] = language.lower()
            print(f"🌐 Language set to: {language}")
        else:
            print(f"❌ Invalid language. Choose from: {valid_languages}")
    
    def enable_sound_effects(self, jingle=True, applause=True, background_music=False):
        """Enable or disable sound effects"""
        self.sound_effects['include_jingle'] = jingle
        self.sound_effects['include_applause'] = applause
        self.sound_effects['include_background_music'] = background_music
        
        print(f"🎬 Sound effects updated:")
        print(f"   Jingle: {'✅' if jingle else '❌'}")
        print(f"   Applause: {'✅' if applause else '❌'}")
        print(f"   Background Music: {'✅' if background_music else '❌'}")
    
    def get_final_output_filename(self):
        """Get the final output filename with timestamp if configured"""
        filename = self.output_settings['final_filename']
        
        if self.output_settings['include_timestamp_in_filename']:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{timestamp}{ext}"
        
        return filename
    
    def print_current_config(self):
        """Print current configuration summary"""
        print("⚙️  Current Configuration Summary:")
        print("=" * 50)
        
        print(f"\n🎤 VOICES:")
        print(f"   DJ/Host: {self.voice_roles['dj']}")
        print(f"   Fan Mail: {self.voice_roles['fan']}")
        print(f"   Guest/Energetic: {self.voice_roles['guest']}")
        print(f"   Announcer: {self.voice_roles['announcer']}")
        
        print(f"\n🌐 LANGUAGE:")
        print(f"   Primary: {self.language_settings['default_language']}")
        print(f"   Korean phrases: {'✅' if self.language_settings['include_korean_phrases'] else '❌'}")
        print(f"   Korean frequency: {self.language_settings['korean_phrase_frequency']}")
        
        print(f"\n🎬 SOUND EFFECTS:")
        print(f"   Enabled: {'✅' if self.sound_effects['enabled'] else '❌'}")
        print(f"   Jingle: {'✅' if self.sound_effects['include_jingle'] else '❌'}")
        print(f"   Applause: {'✅' if self.sound_effects['include_applause'] else '❌'}")
        print(f"   Background Music: {'✅' if self.sound_effects['include_background_music'] else '❌'}")
        
        print(f"\n📁 OUTPUT:")
        print(f"   Format: {self.audio_settings['output_format']}")
        print(f"   Final file: {self.get_final_output_filename()}")
        print(f"   Save segments: {'✅' if self.output_settings['save_individual_segments'] else '❌'}")

# Create a global config instance
config = RadioConfig()

# Preset configurations for easy switching
PRESETS = {
    'korean_focus': {
        'language': 'mixed',
        'korean_phrases': True,
        'korean_frequency': 'high',
        'voices': {
            'dj': 'XB0fDUnXU5powFXDhCwa',      # Charlotte - best for Korean
            'fan': 'cgSgspJ2msm6clMCkdW9',     # Jessica
            'guest': 'EXAVITQu4vr4xnSDxMaL'   # Sarah
        }
    },
    'english_focus': {
        'language': 'english',
        'korean_phrases': False,
        'korean_frequency': 'low',
        'voices': {
            'dj': 'FGY2WhTYpPnrIDTdsKH5',      # Laura - professional
            'fan': 'cgSgspJ2msm6clMCkdW9',     # Jessica
            'guest': 'EXAVITQu4vr4xnSDxMaL'   # Sarah
        }
    },
    'full_production': {
        'sound_effects': {
            'jingle': True,
            'applause': True,
            'background_music': True
        }
    },
    'minimal_production': {
        'sound_effects': {
            'jingle': False,
            'applause': False,
            'background_music': False
        }
    }
}

def apply_preset(preset_name):
    """Apply a preset configuration"""
    if preset_name not in PRESETS:
        print(f"❌ Unknown preset: {preset_name}")
        print(f"Available presets: {list(PRESETS.keys())}")
        return False
    
    preset = PRESETS[preset_name]
    print(f"🎯 Applying preset: {preset_name}")
    
    # Apply language settings
    if 'language' in preset:
        config.set_language(preset['language'])
    
    if 'korean_phrases' in preset:
        config.language_settings['include_korean_phrases'] = preset['korean_phrases']
    
    if 'korean_frequency' in preset:
        config.language_settings['korean_phrase_frequency'] = preset['korean_frequency']
    
    # Apply voice settings
    if 'voices' in preset:
        for role, voice_id in preset['voices'].items():
            config.update_voice_mapping(role, voice_id)
    
    # Apply sound effects settings
    if 'sound_effects' in preset:
        sfx = preset['sound_effects']
        config.enable_sound_effects(
            jingle=sfx.get('jingle', config.sound_effects['include_jingle']),
            applause=sfx.get('applause', config.sound_effects['include_applause']),
            background_music=sfx.get('background_music', config.sound_effects['include_background_music'])
        )
    
    print(f"✅ Preset '{preset_name}' applied successfully!")
    return True

if __name__ == "__main__":
    print("⚙️  K-pop Radio Configuration")
    print("=" * 40)
    
    # Ensure directories exist
    config.ensure_directories()
    
    # Print current configuration
    config.print_current_config()
    
    print(f"\n🎯 Available presets: {list(PRESETS.keys())}")
    print(f"\nTo apply a preset: apply_preset('preset_name')")
    print(f"To customize: modify config.voice_roles, config.language_settings, etc.") 