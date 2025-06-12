import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ScriptGenerator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)
    
    def generate_script_segments(self):
        """Generate three separate K-pop radio show segments"""
        segments = {}
        
        # Segment 1: Greeting and Show Intro
        segments['intro'] = self._generate_intro_segment()
        
        # Segment 2: Top 3 K-pop Songs Today
        segments['top_songs'] = self._generate_top_songs_segment()
        
        # Segment 3: Fan Mail of the Day
        segments['fan_mail'] = self._generate_fan_mail_segment()
        
        return segments
    
    def _generate_intro_segment(self):
        """Generate cheerful greeting and show intro"""
        prompt = """
        You are a cheerful K-pop radio show host. Generate a warm, energetic greeting and show introduction.
        
        Include:
        - Enthusiastic welcome to listeners
        - Introduction of yourself as the host
        - Brief mention of what's coming up on today's show
        
        Keep it upbeat, authentic to K-pop culture, and about 20-25 seconds when read aloud (50-65 words).
        Format as clean script without stage directions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional K-pop radio show script writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating intro segment: {e}")
            return "Hello beautiful listeners! Welcome back to K-pop Vibes Radio! I'm your host Luna, and I'm so excited to be here with you today! We've got an amazing show lined up with the hottest tracks and your lovely messages!"
    
    def _generate_top_songs_segment(self):
        """Generate top 3 K-pop songs segment"""
        prompt = """
        You are a K-pop radio host presenting today's top 3 songs. 
        
        Include:
        - Exciting introduction to the top songs segment
        - 3 realistic K-pop song titles with artist names (make them up but sound authentic)
        - Brief enthusiastic comments about each song
        - Transition to playing the first song
        
        Keep it energetic and about 30-35 seconds when read aloud (75-90 words).
        Format as clean script without stage directions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional K-pop radio show script writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating top songs segment: {e}")
            return "Now it's time for today's hottest tracks! Our top three songs are climbing the charts right now. At number three, we have 'Starlight Dreams' by Luna Eclipse - this track is absolutely magical! Number two goes to 'Electric Heart' by Neon Pulse, and our number one hit today is 'Midnight Dance' by Crystal Wave! Let's start with our chart-topper!"
    
    def _generate_fan_mail_segment(self):
        """Generate fan mail segment"""
        prompt = """
        You are a K-pop radio host reading fan mail. 
        
        Include:
        - Warm introduction to the fan mail segment
        - 1-2 fictional fan messages with names and locations
        - Heartfelt responses to the fans
        - Encouragement for more listeners to send messages
        
        Keep it warm, personal, and about 25-30 seconds when read aloud (65-80 words).
        Format as clean script without stage directions.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional K-pop radio show script writer."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=180,
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating fan mail segment: {e}")
            return "Time for our fan mail of the day! Sarah from Seoul writes: 'Your show brightens my day and helps me discover amazing new music!' Thank you so much, Sarah! And Minho from Busan says: 'Keep spreading the K-pop love!' Your messages mean the world to us! Keep them coming, beautiful listeners!"
    
    def generate_radio_script(self):
        """Generate a single combined radio script (for backward compatibility)"""
        segments = self.generate_script_segments()
        combined_script = f"{segments['intro']}\n\n{segments['top_songs']}\n\n{segments['fan_mail']}"
        return combined_script
    
    def _get_fallback_script(self):
        """Fallback script in case API fails"""
        return """
        Hello beautiful listeners! Welcome back to K-pop Vibes Radio! I'm your host bringing you the hottest tracks today. 
        Our top three songs are: 'Starlight Dreams' by Luna Eclipse, 'Electric Heart' by Neon Pulse, and 'Midnight Dance' by Crystal Wave. 
        Quick fan mail from Sarah in Seoul: 'Your show brightens my day!' Thank you Sarah! 
        Now let's dive into our next amazing track!
        """

if __name__ == "__main__":
    generator = ScriptGenerator()
    
    # Test individual segments
    print("Testing individual segments:")
    print("=" * 60)
    
    segments = generator.generate_script_segments()
    
    for segment_name, script in segments.items():
        print(f"\n{segment_name.upper()} SEGMENT:")
        print("-" * 40)
        print(script)
    
    print("\n" + "=" * 60)
    print("COMBINED SCRIPT:")
    print("-" * 40)
    combined = generator.generate_radio_script()
    print(combined) 