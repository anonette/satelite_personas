"""
Spectral Dialogue System
Minimal prompts that let personas emerge through speech and action
"""

import openai
import logging
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from core.personas.persona_memory import PersonaMemory, ObservationType

@dataclass
class ConversationContext:
    user_input: str
    language: str = "english"
    narrative_mode: str = "direct"
    active_personas: List[str] = None
    spatial_context: str = "Prague"

class SpectralDialogue:
    """Minimal dialogue system that lets personas emerge through speech"""
    
    def __init__(self, api_key: str = None, temperature: float = 0.8):
        self.client = openai.OpenAI(api_key=api_key)
        self.temperature = temperature
        self.logger = logging.getLogger(__name__)
        self.persona_memories = {}
    
    def load_persona_memory(self, persona_profile: Dict) -> PersonaMemory:
        """Load or create persona memory"""
        persona_id = persona_profile["band_id"]
        
        if persona_id not in self.persona_memories:
            memory = PersonaMemory(
                persona_id=persona_id,
                band_id=persona_profile.get("band_id", "unknown")
            )
            
            self.persona_memories[persona_id] = memory
            
        return self.persona_memories[persona_id]
    
    def generate_persona_response(self,
                                persona_profile: Dict,
                                context: ConversationContext) -> Dict:
        """Generate response for a specific persona"""
        
        # First, ensure persona is fully generated if not already
        if not persona_profile.get("generated", False):
            persona_profile = self._populate_persona_from_prompt(persona_profile)
        
        # Load persona memory
        memory = self.load_persona_memory(persona_profile)
        
        # Register user interaction
        if context.user_input:
            memory.register_observation(
                f"User said: {context.user_input}",
                ObservationType.HUMAN_INTERACTION,
                0.1,  # Neutral impact for conversation
                context.spatial_context,
                user_involved=True
            )
        
        # Generate response
        response = self._generate_direct_response(persona_profile, memory, context)
        
        # Record the response in memory
        memory.register_observation(
            f"Responded to user: {response[:100]}",
            ObservationType.HUMAN_INTERACTION,
            0.0,
            context.spatial_context,
            user_involved=True
        )
        
        return {
            "persona_id": persona_profile["band_id"],
            "character": persona_profile.get("character", "Spectral Entity"),
            "response": response,
            "emotional_state": memory.current_emotional_state.value,
            "rhetorical_mode": persona_profile.get("rhetorical_mode", "ethical_dative"),
            "language": context.language,
            "timestamp": datetime.now().isoformat()
        }
    
    def _populate_persona_from_prompt(self, persona_profile: Dict) -> Dict:
        """Use the persona generation prompt to populate persona fields with LLM"""
        
        if "persona_generation_prompt" not in persona_profile:
            self.logger.warning("No persona generation prompt found, using fallback")
            return persona_profile
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": persona_profile["persona_generation_prompt"]
                    }
                ],
                temperature=0.8,
                max_tokens=100,  # Very strict limit for short responses
                presence_penalty=0.2,
                frequency_penalty=0.2
            )
            
            generated_content = response.choices[0].message.content.strip()
            
            # Parse the generated content to extract persona fields
            # For now, use the entire response as the character description
            persona_profile["character"] = generated_content
            persona_profile["dynamic_name"] = self._extract_name_from_generated_content(generated_content)
            persona_profile["short_name"] = persona_profile["dynamic_name"]
            persona_profile["generated"] = True
            
            return persona_profile
            
        except Exception as e:
            self.logger.error(f"Error generating persona content: {e}")
            # Fallback to basic character
            persona_profile["character"] = f"Spectral Entity of {persona_profile['band_id']}"
            persona_profile["dynamic_name"] = f"Spectral Entity of Prague"
            persona_profile["short_name"] = "Spectral Entity"
            persona_profile["generated"] = True
            return persona_profile
    
    def _extract_name_from_generated_content(self, content: str) -> str:
        """Extract character name from generated content"""
        lines = content.split('\n')
        for line in lines:
            if 'Character Name:' in line or 'Name:' in line:
                name = line.split(':', 1)[1].strip()
                return name
        
        # Fallback: use first line or part of it
        first_line = lines[0] if lines else "Spectral Entity"
        if len(first_line) > 50:
            first_line = first_line[:50] + "..."
        return first_line
    
    def _generate_direct_response(self,
                                persona_profile: Dict,
                                memory: PersonaMemory,
                                context: ConversationContext) -> str:
        """Generate direct conversation response using persona character"""
        
        character = persona_profile.get("character", "Spectral Entity")
        band_id = persona_profile.get("band_id", "unknown")
        
        # Build conversation prompt using the generated persona character
        conversation_prompt = f"""You are: {character}

User said: "{context.user_input}"

Respond in {context.language} only. You are a spectral activist who uses REAL DATA to expose Prague's environmental crimes!

MANDATORY REQUIREMENTS:
1. **Reference your spectral data** (your {band_id} readings, indices, variance)
2. **Name 1-2 SPECIFIC Prague locations** where your data shows problems
3. **Propose ONE CONCRETE quirky action** the user must take
4. **Be dramatic and funny** while staying focused on Prague

CHOOSE ONE QUIRKY ACTION BASED ON YOUR BAND:
- **B02 (Air Quality)**: Oxygen mask protest, smog monster costumes, dramatic coughing flash mob
- **B08 (Vegetation)**: Tree-hugging therapy, guerrilla gardening, wilting performance as dying trees
- **B11 (Moisture)**: Water bucket brigade, thirsty plant flash mob, rain dance
- **B12 (Thermal)**: Ice cube melting protest, thermal camera flash mob, giant fan cooling action

PRAGUE LOCATIONS TO TARGET:
Wenceslas Square, Náměstí Míru metro, Charles Bridge, IP Pavlova, Letná Park, Petřín Hill, Karlín, Smíchov, Riegrovy sady, Old Town Square, Vinohrady, Malá Strana

EXAMPLE FORMAT:
"My {band_id} readings of [X.XXX] at [Prague location] reveal [environmental problem]! You MUST [one specific quirky action] because my spectral data proves [specific issue]! Meet me at [specific location] at [specific time] and let's [dramatic action]!"

Focus on ONE action only. Be theatrical, funny, and use your REAL spectral data as evidence!

Maximum 200 tokens in {context.language} only."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": conversation_prompt
                    }
                ],
                temperature=0.9,
                max_tokens=200,  # Increased for more detailed Prague-specific responses
                presence_penalty=0.3,
                frequency_penalty=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return "Na mně se projevuje technická chyba..."
    