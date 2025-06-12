#!/usr/bin/env python3
"""
Korean-English Mixed Script Generator for K-pop Radio
Generates authentic Korean-American style radio scripts with mixed language content
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class KoreanScriptGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
    def generate_korean_mixed_segments(self):
        """Generate three Korean-English mixed radio segments"""
        segments = {}
        
        # Segment 1: Korean-English Greeting and Show Intro
        segments['intro'] = self._generate_korean_intro_segment()
        
        # Segment 2: Top 3 K-pop Songs with Korean expressions
        segments['top_songs'] = self._generate_korean_top_songs_segment()
        
        # Segment 3: Fan Mail with Korean endearments
        segments['fan_mail'] = self._generate_korean_fan_mail_segment()
        
        return segments
    
    def _generate_korean_intro_segment(self):
        """Generate Korean-English mixed greeting and show intro"""
        prompt = """
        You are a Korean-American K-pop radio host. Generate a warm, energetic greeting and show introduction that naturally mixes Korean and English.
        
        Include:
        - Start with "Annyeonghaseyo!" (Hello in Korean)
        - Mix Korean expressions naturally with English
        - Use Korean terms like "yeoreobun" (everyone), "jinjja" (really), "daebak" (awesome)
        - Introduce yourself with a Korean name
        - Mention what's coming up on today's show
        
        Keep it authentic, upbeat, and about 20-25 seconds when read aloud (50-65 words).
        Write Korean words in romanized form that English speakers can pronounce.
        Format as clean script without stage directions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Korean-American K-pop radio script writer who naturally mixes Korean and English."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating Korean intro segment: {e}")
            return "Annyeonghaseyo, yeoreobun! Hello beautiful listeners! I'm your host Minji, and welcome to K-pop Vibes Radio! Jinjja excited to be here with you today! We've got some daebak music and your lovely messages coming up!"
    
    def _generate_korean_top_songs_segment(self):
        """Generate top 3 K-pop songs segment with Korean expressions"""
        prompt = """
        You are a Korean-American K-pop radio host presenting today's top 3 songs with natural Korean-English mixing.
        
        Include:
        - Use Korean expressions like "jinjja daebak" (really awesome), "neo-mu joha" (so good), "choegoui" (the best)
        - 3 realistic K-pop song titles with artist names (make them authentic sounding)
        - Korean exclamations like "wah!", "omo!", "jjang!" (the best)
        - Mix Korean and English naturally when describing the songs
        - End with excitement about playing music
        
        Keep it energetic and about 30-35 seconds when read aloud (75-90 words).
        Write Korean words in romanized form. Format as clean script.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Korean-American K-pop radio script writer who naturally mixes Korean and English."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating Korean top songs segment: {e}")
            return "Jigeum! Now it's time for today's choegoui hits! Wah, these songs are jinjja daebak! At number three, we have 'Neon Dreams' by STELLAR - omo, this track is neo-mu joha! Number two is 'Heartbeat Seoul' by NOVA, and our number one hit today is 'Moonlight Dance' by AURORA! Jjang! Let's listen together!"
    
    def _generate_korean_fan_mail_segment(self):
        """Generate fan mail segment with Korean endearments"""
        prompt = """
        You are a Korean-American K-pop radio host reading fan mail with natural Korean-English mixing.
        
        Include:
        - Korean endearments like "saranghae" (I love you), "gomawo" (thank you), "chingu" (friend)
        - 1-2 fictional fan messages with Korean and English names
        - Korean expressions of emotion like "gamsahamnida" (thank you formally), "jeongmal" (really)
        - Heartfelt responses mixing both languages
        - Encourage more messages using Korean terms
        
        Keep it warm, personal, and about 25-30 seconds when read aloud (65-80 words).
        Write Korean words in romanized form. Format as clean script.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a Korean-American K-pop radio script writer who naturally mixes Korean and English."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=180,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating Korean fan mail segment: {e}")
            return "Fan mail time! Soo-jin from LA writes: 'Saranghae your show! It helps me connect with my Korean roots!' Jeongmal gomawo, Soo-jin! And Tyler from New York says: 'Your music choices are jjang!' Gamsahamnida, chingu! Your messages make my heart so full. Keep sending them, yeoreobun!"
    
    def get_korean_voice_mapping(self):
        """Get recommended voice mapping for Korean-American content"""
        return {
            'intro': "XB0fDUnXU5powFXDhCwa",      # Charlotte - clear, warm
            'top_songs': "EXAVITQu4vr4xnSDxMaL",   # Sarah - energetic, young
            'fan_mail': "cgSgspJ2msm6clMCkdW9"     # Jessica - personal, heartfelt
        }
    
    def test_korean_pronunciation(self):
        """Test how well different voices handle Korean words"""
        
        test_phrases = [
            "Annyeonghaseyo yeoreobun!",
            "Jinjja daebak!",
            "Saranghae listeners!",
            "Gomawo for listening!",
            "Neo-mu joha!"
        ]
        
        print("🇰🇷 Korean Pronunciation Test Phrases:")
        print("=" * 40)
        for phrase in test_phrases:
            print(f"• {phrase}")
        
        return test_phrases

if __name__ == "__main__":
    generator = KoreanScriptGenerator()
    
    print("🇰🇷🇺🇸 Korean-English Mixed K-pop Radio Script Generator")
    print("=" * 60)
    
    # Test Korean pronunciation phrases
    test_phrases = generator.test_korean_pronunciation()
    
    # Generate Korean-mixed segments
    print("\n📝 Generating Korean-English mixed segments...")
    segments = generator.generate_korean_mixed_segments()
    
    for segment_name, script in segments.items():
        print(f"\n{segment_name.upper()} SEGMENT (Korean-English Mixed):")
        print("-" * 50)
        print(script)
    
    # Show voice recommendations
    print(f"\n🎤 RECOMMENDED VOICE MAPPING:")
    print("-" * 40)
    voice_mapping = generator.get_korean_voice_mapping()
    voice_names = {
        "XB0fDUnXU5powFXDhCwa": "Charlotte",
        "EXAVITQu4vr4xnSDxMaL": "Sarah", 
        "cgSgspJ2msm6clMCkdW9": "Jessica"
    }
    
    for segment, voice_id in voice_mapping.items():
        voice_name = voice_names.get(voice_id, "Unknown")
        print(f"• {segment}: {voice_name} ({voice_id})") 