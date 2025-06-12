#!/usr/bin/env python3
"""
Custom Voice Manager for ElevenLabs API
Advanced voice management and custom voice integration
"""

import os
import json
from datetime import datetime
from elevenlabs import ElevenLabs, VoiceSettings, Voice
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class CustomVoiceManager:
    def __init__(self):
        self.api_key = os.getenv('ELEVEN_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVEN_API_KEY not found in environment variables")
        
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=self.api_key)
        
        # Cache for voices to avoid repeated API calls
        self._voice_cache = None
        self._cache_timestamp = None
        
    def list_all_voices(self, include_cloned=True, refresh_cache=False):
        """
        List all available voices from your ElevenLabs account
        
        Args:
            include_cloned (bool): Include your custom cloned voices
            refresh_cache (bool): Force refresh the voice cache
            
        Returns:
            dict: Organized voice data with categories
        """
        
        # Check cache (refresh every 5 minutes)
        current_time = datetime.now()
        if (not refresh_cache and self._voice_cache and self._cache_timestamp and 
            (current_time - self._cache_timestamp).seconds < 300):
            print("📋 Using cached voice data...")
            return self._voice_cache
        
        try:
            print("🔍 Fetching all voices from your ElevenLabs account...")
            
            # Get all voices
            voices_response = self.client.voices.get_all()
            
            if not voices_response or not hasattr(voices_response, 'voices'):
                print("❌ No voices found or API error")
                return {}
            
            # Organize voices by category
            organized_voices = {
                'premade': [],
                'cloned': [],
                'professional': [],
                'generated': []
            }
            
            voice_details = {}
            
            for voice in voices_response.voices:
                voice_info = {
                    'voice_id': voice.voice_id,
                    'name': voice.name,
                    'category': getattr(voice, 'category', 'unknown'),
                    'description': getattr(voice, 'description', ''),
                    'preview_url': getattr(voice, 'preview_url', ''),
                    'available_for_tiers': getattr(voice, 'available_for_tiers', []),
                    'settings': getattr(voice, 'settings', None),
                    'sharing': getattr(voice, 'sharing', None),
                    'high_quality_base_model_ids': getattr(voice, 'high_quality_base_model_ids', []),
                    'safety_control': getattr(voice, 'safety_control', None),
                    'voice_verification': getattr(voice, 'voice_verification', None),
                    'owner_id': getattr(voice, 'owner_id', None),
                    'permission_on_resource': getattr(voice, 'permission_on_resource', None)
                }
                
                # Categorize voice
                category = voice_info['category'].lower()
                if category in organized_voices:
                    organized_voices[category].append(voice_info)
                else:
                    organized_voices['generated'].append(voice_info)
                
                voice_details[voice.voice_id] = voice_info
            
            # Cache the results
            self._voice_cache = {
                'organized': organized_voices,
                'details': voice_details,
                'total_count': len(voice_details),
                'last_updated': current_time.isoformat()
            }
            self._cache_timestamp = current_time
            
            # Display summary
            print(f"✅ Found {len(voice_details)} total voices:")
            for category, voices in organized_voices.items():
                if voices:
                    print(f"   • {category.title()}: {len(voices)} voices")
            
            return self._voice_cache
            
        except Exception as e:
            print(f"❌ Error fetching voices: {e}")
            return {}
    
    def get_voice_details(self, voice_id):
        """
        Get detailed information about a specific voice
        
        Args:
            voice_id (str): The voice ID to get details for
            
        Returns:
            dict: Detailed voice information
        """
        
        try:
            print(f"🔍 Getting details for voice: {voice_id}")
            
            voice = self.client.voices.get(voice_id)
            
            if not voice:
                print(f"❌ Voice {voice_id} not found")
                return None
            
            voice_details = {
                'voice_id': voice.voice_id,
                'name': voice.name,
                'category': getattr(voice, 'category', 'unknown'),
                'description': getattr(voice, 'description', ''),
                'preview_url': getattr(voice, 'preview_url', ''),
                'available_for_tiers': getattr(voice, 'available_for_tiers', []),
                'settings': getattr(voice, 'settings', None),
                'sharing': getattr(voice, 'sharing', None),
                'high_quality_base_model_ids': getattr(voice, 'high_quality_base_model_ids', []),
                'safety_control': getattr(voice, 'safety_control', None),
                'voice_verification': getattr(voice, 'voice_verification', None),
                'owner_id': getattr(voice, 'owner_id', None),
                'permission_on_resource': getattr(voice, 'permission_on_resource', None)
            }
            
            print(f"✅ Voice details retrieved for: {voice.name}")
            return voice_details
            
        except Exception as e:
            print(f"❌ Error getting voice details: {e}")
            return None
    
    def use_custom_voice(self, voice_id, text, output_filename=None, voice_settings=None):
        """
        Generate audio using a custom voice ID (including cloned voices)
        
        Args:
            voice_id (str): Custom voice ID from your dashboard
            text (str): Text to convert to speech
            output_filename (str): Output filename (optional)
            voice_settings (dict): Custom voice settings (optional)
            
        Returns:
            str: Path to generated audio file
        """
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"custom_voice_{timestamp}.mp3"
        
        output_path = os.path.join("assets", "audio", output_filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            print(f"🎤 Generating audio with custom voice: {voice_id}")
            
            # Get voice details first to validate
            voice_details = self.get_voice_details(voice_id)
            if not voice_details:
                print(f"❌ Invalid voice ID: {voice_id}")
                return None
            
            print(f"   Using voice: {voice_details['name']} ({voice_details['category']})")
            
            # Configure voice settings
            if voice_settings:
                settings = VoiceSettings(**voice_settings)
            else:
                settings = VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.8,
                    style=0.2,
                    use_speaker_boost=True
                )
            
            # Generate audio
            audio = self.client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings=settings
            )
            
            # Save audio
            with open(output_path, 'wb') as f:
                for chunk in audio:
                    f.write(chunk)
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ Custom voice audio generated: {output_filename} ({file_size:.1f} KB)")
            return output_path
            
        except Exception as e:
            print(f"❌ Error generating audio with custom voice: {e}")
            return None
    
    def test_voice_quality(self, voice_id, test_phrases=None):
        """
        Test a voice with multiple phrases to evaluate quality
        
        Args:
            voice_id (str): Voice ID to test
            test_phrases (list): Custom test phrases (optional)
            
        Returns:
            list: Paths to generated test audio files
        """
        
        if not test_phrases:
            test_phrases = [
                "Hello! Welcome to our K-pop radio show!",
                "Annyeonghaseyo yeoreobun! This is your host speaking.",
                "Today we have some amazing songs from BTS, BLACKPINK, and NewJeans!",
                "Thank you for listening, and we'll see you next time!"
            ]
        
        print(f"🧪 Testing voice quality for: {voice_id}")
        
        voice_details = self.get_voice_details(voice_id)
        if voice_details:
            print(f"   Voice: {voice_details['name']} ({voice_details['category']})")
        
        test_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"   Testing phrase {i}/{len(test_phrases)}: \"{phrase[:50]}...\"")
            
            test_filename = f"voice_test_{voice_id}_{i}_{timestamp}.mp3"
            audio_path = self.use_custom_voice(
                voice_id=voice_id,
                text=phrase,
                output_filename=test_filename
            )
            
            if audio_path:
                test_files.append(audio_path)
        
        print(f"✅ Voice quality test completed: {len(test_files)} test files generated")
        return test_files
    
    def compare_voices(self, voice_ids, test_text=None):
        """
        Compare multiple voices with the same text
        
        Args:
            voice_ids (list): List of voice IDs to compare
            test_text (str): Text to use for comparison
            
        Returns:
            dict: Comparison results with file paths
        """
        
        if not test_text:
            test_text = "Annyeonghaseyo! Welcome to K-pop Vibes Radio! Today we have some jinjja daebak music for you!"
        
        print(f"🎭 Comparing {len(voice_ids)} voices...")
        print(f"Test text: \"{test_text}\"")
        print("-" * 60)
        
        comparison_results = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for voice_id in voice_ids:
            voice_details = self.get_voice_details(voice_id)
            voice_name = voice_details['name'] if voice_details else 'Unknown'
            
            print(f"\n🎤 Testing: {voice_name} ({voice_id})")
            
            comparison_filename = f"comparison_{voice_name.lower().replace(' ', '_')}_{timestamp}.mp3"
            audio_path = self.use_custom_voice(
                voice_id=voice_id,
                text=test_text,
                output_filename=comparison_filename
            )
            
            if audio_path:
                file_size = os.path.getsize(audio_path) / 1024  # KB
                comparison_results[voice_id] = {
                    'name': voice_name,
                    'file_path': audio_path,
                    'file_size_kb': file_size,
                    'details': voice_details
                }
                print(f"   ✅ Generated: {comparison_filename} ({file_size:.1f} KB)")
            else:
                comparison_results[voice_id] = {
                    'name': voice_name,
                    'file_path': None,
                    'error': 'Failed to generate audio'
                }
                print(f"   ❌ Failed to generate audio")
        
        print(f"\n✅ Voice comparison completed: {len([r for r in comparison_results.values() if r.get('file_path')])} successful")
        return comparison_results
    
    def save_voice_catalog(self, filename=None):
        """
        Save a complete catalog of all available voices to JSON
        
        Args:
            filename (str): Output filename (optional)
            
        Returns:
            str: Path to saved catalog file
        """
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voice_catalog_{timestamp}.json"
        
        output_path = os.path.join("assets", "audio", filename)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            print("📋 Creating voice catalog...")
            
            voice_data = self.list_all_voices(refresh_cache=True)
            
            if not voice_data:
                print("❌ No voice data to save")
                return None
            
            # Save to JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(voice_data, f, indent=2, ensure_ascii=False)
            
            file_size = os.path.getsize(output_path) / 1024  # KB
            print(f"✅ Voice catalog saved: {filename} ({file_size:.1f} KB)")
            print(f"   Total voices: {voice_data['total_count']}")
            
            return output_path
            
        except Exception as e:
            print(f"❌ Error saving voice catalog: {e}")
            return None
    
    def get_recommended_voices_for_kpop(self):
        """
        Get recommended voices specifically for K-pop radio content
        
        Returns:
            dict: Recommended voice mappings for different roles
        """
        
        print("🌟 Getting K-pop radio voice recommendations...")
        
        # Get all voices
        voice_data = self.list_all_voices()
        if not voice_data:
            return {}
        
        all_voices = voice_data.get('details', {})
        
        # Recommended voices for K-pop radio (based on testing)
        recommendations = {
            'dj_host': {
                'primary': 'XB0fDUnXU5powFXDhCwa',  # Charlotte - clear, warm
                'alternative': 'EXAVITQu4vr4xnSDxMaL',  # Sarah - energetic
                'description': 'Main DJ/Host voice - clear pronunciation for Korean words'
            },
            'energetic_segments': {
                'primary': 'EXAVITQu4vr4xnSDxMaL',  # Sarah - young, energetic
                'alternative': 'cgSgspJ2msm6clMCkdW9',  # Jessica - personal
                'description': 'For top songs, exciting announcements'
            },
            'emotional_segments': {
                'primary': 'cgSgspJ2msm6clMCkdW9',  # Jessica - heartfelt
                'alternative': 'pFZP5JQG7iQjIQuC4Bku',  # Lily - sweet
                'description': 'For fan mail, emotional content'
            },
            'professional_segments': {
                'primary': 'FGY2WhTYpPnrIDTdsKH5',  # Laura - professional
                'alternative': 'XB0fDUnXU5powFXDhCwa',  # Charlotte - clear
                'description': 'For news, announcements, formal content'
            }
        }
        
        # Validate recommendations against available voices
        validated_recommendations = {}
        for role, config in recommendations.items():
            primary_voice = all_voices.get(config['primary'])
            alternative_voice = all_voices.get(config['alternative'])
            
            if primary_voice or alternative_voice:
                validated_recommendations[role] = {
                    'primary': {
                        'voice_id': config['primary'],
                        'name': primary_voice['name'] if primary_voice else 'Not Available',
                        'available': primary_voice is not None
                    },
                    'alternative': {
                        'voice_id': config['alternative'],
                        'name': alternative_voice['name'] if alternative_voice else 'Not Available',
                        'available': alternative_voice is not None
                    },
                    'description': config['description']
                }
        
        print(f"✅ Found {len(validated_recommendations)} recommended voice categories")
        return validated_recommendations

def main():
    """Main function to demonstrate custom voice functionality"""
    
    print("🎤 ElevenLabs Custom Voice Manager")
    print("=" * 50)
    
    try:
        voice_manager = CustomVoiceManager()
        
        # List all available voices
        print("\n1. 📋 Listing all available voices...")
        voice_data = voice_manager.list_all_voices()
        
        if voice_data:
            organized = voice_data.get('organized', {})
            for category, voices in organized.items():
                if voices:
                    print(f"\n{category.upper()} VOICES ({len(voices)}):")
                    for voice in voices[:3]:  # Show first 3 of each category
                        print(f"  • {voice['name']} ({voice['voice_id']})")
                        if voice['description']:
                            print(f"    {voice['description'][:80]}...")
                    if len(voices) > 3:
                        print(f"    ... and {len(voices) - 3} more")
        
        # Get K-pop recommendations
        print("\n2. 🌟 K-pop Radio Voice Recommendations...")
        recommendations = voice_manager.get_recommended_voices_for_kpop()
        
        for role, config in recommendations.items():
            print(f"\n{role.upper().replace('_', ' ')}:")
            print(f"  Primary: {config['primary']['name']} ({'✅' if config['primary']['available'] else '❌'})")
            print(f"  Alternative: {config['alternative']['name']} ({'✅' if config['alternative']['available'] else '❌'})")
            print(f"  Use for: {config['description']}")
        
        # Save voice catalog
        print("\n3. 💾 Saving voice catalog...")
        catalog_path = voice_manager.save_voice_catalog()
        
        print(f"\n✅ Custom Voice Manager demo completed!")
        print(f"📁 Voice catalog saved to: {catalog_path}")
        
    except Exception as e:
        print(f"❌ Error in custom voice manager: {e}")

if __name__ == "__main__":
    main() 