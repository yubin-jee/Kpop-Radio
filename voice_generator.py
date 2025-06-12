import os
from elevenlabs import ElevenLabs, VoiceSettings, save
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

class VoiceGenerator:
    def __init__(self):
        self.api_key = os.getenv('ELEVEN_API_KEY')
        if not self.api_key:
            raise ValueError("ELEVEN_API_KEY not found in environment variables")
        
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=self.api_key)
        
        # Using a popular female voice ID (Rachel) - you can change this
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel voice
        
    def text_to_speech(self, text, output_filename=None, voice_id=None):
        """Convert text to speech using ElevenLabs API"""
        
        # Use provided voice_id or default
        selected_voice_id = voice_id if voice_id else self.voice_id
        
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"kpop_radio_{timestamp}.mp3"
        
        output_path = os.path.join("assets", "audio", output_filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        try:
            print(f"Generating audio with voice {selected_voice_id}...")
            
            # Configure voice settings
            voice_settings = VoiceSettings(
                stability=0.5,
                similarity_boost=0.8,
                style=0.2,
                use_speaker_boost=True
            )
            
            # Generate audio using the ElevenLabs client
            audio = self.client.text_to_speech.convert(
                voice_id=selected_voice_id,
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings=voice_settings
            )
            
            # Save the audio file
            save(audio, output_path)
            print(f"Audio saved successfully to: {output_path}")
            return output_path
                
        except Exception as e:
            print(f"Error generating audio: {e}")
            return None
    
    def generate_segment_audio(self, segments, voice_mapping=None):
        """Generate audio for multiple segments with different voices"""
        
        # Default voice mapping if none provided
        if voice_mapping is None:
            voice_mapping = {
                'intro': "21m00Tcm4TlvDq8ikWAM",      # Rachel (warm, welcoming)
                'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Bella (energetic)
                'fan_mail': "21m00Tcm4TlvDq8ikWAM"     # Rachel (warm, personal)
            }
        
        audio_files = {}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for segment_name, script in segments.items():
            voice_id = voice_mapping.get(segment_name, self.voice_id)
            filename = f"{segment_name}_{timestamp}.mp3"
            
            print(f"\n🎤 Generating {segment_name} segment...")
            audio_path = self.text_to_speech(
                text=script,
                output_filename=filename,
                voice_id=voice_id
            )
            
            if audio_path:
                audio_files[segment_name] = audio_path
            else:
                print(f"❌ Failed to generate audio for {segment_name} segment")
                return None
        
        return audio_files
    
    def get_available_voices(self):
        """Get list of available voices from ElevenLabs"""
        try:
            voice_list = self.client.voices.get_all()
            return voice_list
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []

if __name__ == "__main__":
    try:
        generator = VoiceGenerator()
        
        # Test with sample text
        sample_text = "Hello! This is a test of the K-pop radio voice generator!"
        audio_path = generator.text_to_speech(sample_text, "test_audio.mp3")
        
        if audio_path:
            print(f"Test audio generated: {audio_path}")
        else:
            print("Failed to generate test audio")
    except Exception as e:
        print(f"Error initializing voice generator: {e}")
        print("Make sure your ELEVEN_API_KEY is set in the .env file") 