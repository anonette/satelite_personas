"""
ElevenLabs Text-to-Speech integration with dynamic funny voice assignment
"""
import os
import requests
import streamlit as st
import base64
import hashlib
from typing import Dict, Optional
import random

class ElevenLabsVoiceManager:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.base_url = "https://api.elevenlabs.io/v1"
        
        # Funny voice IDs from ElevenLabs (these are real voice IDs)
        self.funny_voices = {
            "squeaky_scientist": "pNInz6obpgDQGcFmaJgB",  # Adam - high pitched scientist
            "dramatic_narrator": "21m00Tcm4TlvDq8ikWAM",  # Rachel - dramatic storyteller
            "grumpy_old_man": "AZnzlk1XvdvUeBnXmlld",   # Domi - grumpy character
            "cheerful_activist": "EXAVITQu4vr4xnSDxMaL",  # Bella - upbeat activist
            "mysterious_whisper": "ErXwobaYiN019PkySvjV", # Antoni - mysterious
            "robotic_analyzer": "VR6AewLTigWG4xSOukaG",   # Arnold - robotic
            "bubbly_enthusiast": "oWAxZDx7w5VEj9dCyTzz",  # Grace - bubbly
            "wise_sage": "yoZ06aMxZJJ28mfd3POQ",         # Sam - wise old sage
            "energetic_rebel": "pqHfZKP75CvOlQylNhV4",    # Bill - energetic rebel
            "sarcastic_critic": "g5CIjZEefAph4nQFvHAz"    # Freya - sarcastic
        }
        
        # Voice characteristics for dynamic assignment
        self.voice_traits = {
            "squeaky_scientist": {"pitch": "high", "energy": "analytical", "humor": "nerdy"},
            "dramatic_narrator": {"pitch": "medium", "energy": "theatrical", "humor": "dramatic"},
            "grumpy_old_man": {"pitch": "low", "energy": "grumpy", "humor": "sarcastic"},
            "cheerful_activist": {"pitch": "medium-high", "energy": "upbeat", "humor": "optimistic"},
            "mysterious_whisper": {"pitch": "low", "energy": "mysterious", "humor": "cryptic"},
            "robotic_analyzer": {"pitch": "medium", "energy": "mechanical", "humor": "logical"},
            "bubbly_enthusiast": {"pitch": "high", "energy": "excited", "humor": "giggly"},
            "wise_sage": {"pitch": "low", "energy": "calm", "humor": "philosophical"},
            "energetic_rebel": {"pitch": "medium", "energy": "rebellious", "humor": "edgy"},
            "sarcastic_critic": {"pitch": "medium", "energy": "sarcastic", "humor": "witty"}
        }
    
    def _get_persona_voice_traits(self, persona: Dict) -> Dict[str, str]:
        """Extract voice traits from persona characteristics"""
        band_id = persona.get("band_id", "Unknown")
        character = persona.get("character", "")
        
        # Analyze persona content for voice traits
        traits = {"pitch": "medium", "energy": "medium", "humor": "neutral"}
        
        # Band-specific base traits
        band_traits = {
            "B02": {"pitch": "high", "energy": "analytical", "humor": "nerdy"},      # Blue - atmospheric scientist
            "B03": {"pitch": "medium-high", "energy": "upbeat", "humor": "optimistic"}, # Green - plant lover
            "B04": {"pitch": "medium", "energy": "dramatic", "humor": "theatrical"},  # Red - stress detector
            "B06": {"pitch": "medium", "energy": "calm", "humor": "philosophical"},   # Vegetation - wise
            "B08": {"pitch": "low", "energy": "mysterious", "humor": "cryptic"},      # NIR - invisible spectrum
            "B11": {"pitch": "medium", "energy": "excited", "humor": "giggly"},       # Moisture - bubbly
            "B12": {"pitch": "low", "energy": "grumpy", "humor": "sarcastic"}        # Thermal - hot-tempered
        }
        
        if band_id in band_traits:
            traits.update(band_traits[band_id])
        
        # Modify based on character content
        character_lower = character.lower()
        
        # Energy level adjustments
        if any(word in character_lower for word in ["dramatic", "theatrical", "spectacular"]):
            traits["energy"] = "theatrical"
        elif any(word in character_lower for word in ["rebel", "activist", "fight"]):
            traits["energy"] = "rebellious"
        elif any(word in character_lower for word in ["wise", "sage", "ancient"]):
            traits["energy"] = "calm"
        elif any(word in character_lower for word in ["excited", "enthusiastic", "amazing"]):
            traits["energy"] = "excited"
        
        # Humor style adjustments
        if any(word in character_lower for word in ["sarcastic", "cynical", "critic"]):
            traits["humor"] = "sarcastic"
        elif any(word in character_lower for word in ["mysterious", "cryptic", "shadow"]):
            traits["humor"] = "cryptic"
        elif any(word in character_lower for word in ["cheerful", "optimistic", "bright"]):
            traits["humor"] = "optimistic"
        elif any(word in character_lower for word in ["scientific", "analytical", "data"]):
            traits["humor"] = "nerdy"
        
        return traits
    
    def assign_voice_to_persona(self, persona: Dict) -> str:
        """Dynamically assign a funny voice based on persona characteristics"""
        if not self.api_key:
            return None
        
        # Get persona traits
        persona_traits = self._get_persona_voice_traits(persona)
        
        # Find best matching voice
        best_voice = None
        best_score = 0
        
        for voice_name, voice_traits in self.voice_traits.items():
            score = 0
            
            # Match pitch
            if persona_traits["pitch"] == voice_traits["pitch"]:
                score += 3
            elif abs(self._pitch_to_number(persona_traits["pitch"]) - 
                    self._pitch_to_number(voice_traits["pitch"])) <= 1:
                score += 1
            
            # Match energy
            if persona_traits["energy"] == voice_traits["energy"]:
                score += 3
            
            # Match humor
            if persona_traits["humor"] == voice_traits["humor"]:
                score += 3
            
            if score > best_score:
                best_score = score
                best_voice = voice_name
        
        # Add some randomness for variety
        if best_score < 6:  # If no perfect match, add randomness
            similar_voices = [v for v, traits in self.voice_traits.items() 
                            if any(persona_traits[k] == traits[k] for k in ["energy", "humor"])]
            if similar_voices:
                best_voice = random.choice(similar_voices)
        
        return best_voice or "cheerful_activist"  # Default fallback
    
    def _pitch_to_number(self, pitch: str) -> int:
        """Convert pitch description to number for comparison"""
        pitch_map = {"low": 1, "medium": 2, "medium-high": 3, "high": 4}
        return pitch_map.get(pitch, 2)
    
    def generate_speech(self, text: str, voice_name: str) -> Optional[bytes]:
        """Generate speech audio using ElevenLabs API"""
        if not self.api_key or voice_name not in self.funny_voices:
            return None
        
        voice_id = self.funny_voices[voice_name]
        
        # Clean text for speech
        clean_text = self._clean_text_for_speech(text)
        
        url = f"{self.base_url}/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        # Voice settings for extra funny effect
        voice_settings = self._get_funny_voice_settings(voice_name)
        
        data = {
            "text": clean_text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": voice_settings
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.content
            else:
                st.error(f"ElevenLabs API error: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Speech generation failed: {str(e)}")
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean text for better speech synthesis"""
        import re
        
        # Remove markdown formatting
        text = re.sub(r'\*+([^*]+)\*+', r'\1', text)
        text = re.sub(r'#+\s*', '', text)
        
        # Remove emojis for cleaner speech
        text = re.sub(r'[^\w\s.,!?;:-]', '', text)
        
        # Limit length for API
        if len(text) > 500:
            text = text[:497] + "..."
        
        return text.strip()
    
    def _get_funny_voice_settings(self, voice_name: str) -> Dict:
        """Get voice settings that make voices extra funny"""
        base_settings = {
            "stability": 0.75,
            "similarity_boost": 0.75,
            "style": 0.5,
            "use_speaker_boost": True
        }
        
        # Adjust settings for extra humor
        funny_adjustments = {
            "squeaky_scientist": {"stability": 0.6, "similarity_boost": 0.9, "style": 0.8},
            "dramatic_narrator": {"stability": 0.8, "similarity_boost": 0.7, "style": 0.9},
            "grumpy_old_man": {"stability": 0.9, "similarity_boost": 0.6, "style": 0.7},
            "cheerful_activist": {"stability": 0.5, "similarity_boost": 0.8, "style": 0.8},
            "mysterious_whisper": {"stability": 0.8, "similarity_boost": 0.9, "style": 0.6},
            "robotic_analyzer": {"stability": 0.9, "similarity_boost": 0.5, "style": 0.3},
            "bubbly_enthusiast": {"stability": 0.4, "similarity_boost": 0.9, "style": 0.9},
            "wise_sage": {"stability": 0.9, "similarity_boost": 0.7, "style": 0.4},
            "energetic_rebel": {"stability": 0.6, "similarity_boost": 0.8, "style": 0.8},
            "sarcastic_critic": {"stability": 0.7, "similarity_boost": 0.8, "style": 0.7}
        }
        
        if voice_name in funny_adjustments:
            base_settings.update(funny_adjustments[voice_name])
        
        return base_settings
    
    def get_voice_description(self, voice_name: str) -> str:
        """Get a funny description of the voice"""
        descriptions = {
            "squeaky_scientist": "🤓 High-pitched analytical nerd voice",
            "dramatic_narrator": "🎭 Theatrical storyteller with flair",
            "grumpy_old_man": "😠 Grumpy low-pitched complainer",
            "cheerful_activist": "😊 Upbeat optimistic campaigner",
            "mysterious_whisper": "🕵️ Cryptic low whisper voice",
            "robotic_analyzer": "🤖 Mechanical data processor voice",
            "bubbly_enthusiast": "🫧 Giggly high-energy bubbler",
            "wise_sage": "🧙 Deep philosophical wisdom voice",
            "energetic_rebel": "⚡ Rebellious edgy activist voice",
            "sarcastic_critic": "😏 Witty sarcastic commentator"
        }
        return descriptions.get(voice_name, "🎤 Funny voice")

# Global voice manager instance
voice_manager = ElevenLabsVoiceManager()