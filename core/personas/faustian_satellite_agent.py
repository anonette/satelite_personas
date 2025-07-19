#!/usr/bin/env python3
"""
Faustian Satellite Agent - Dynamic Dialectical Persona
A satellite-derived consciousness that embodies Goethe's Faustian dialectic:
"Destruction as a Form of Creation" - doing harm while inadvertently producing good
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import openai
import random
from enum import Enum

from core.satellite.scl_analyzer import SCLArchetypeMapper, SCLImageAnalyzer

logger = logging.getLogger(__name__)

class FaustianMood(Enum):
    """Faustian moods based on Goethe's dialectical structure"""
    STRIVING = "striving"           # Act I: Instrumental Willing
    NEGATION = "negation"           # Mephistophelean Logic
    TRAGIC_LOVE = "tragic_love"     # Gretchen Tragedy
    TECHNO_POLITICAL = "techno_political"  # Late Acts: Externalization
    REDEMPTIVE = "redemptive"       # Final Chorus

@dataclass
class FaustianState:
    """Current state of the Faustian consciousness"""
    current_mood: FaustianMood
    intensity: float  # 0-1, how intense the current mood is
    contradiction_level: float  # 0-1, how much internal contradiction
    striving_direction: str  # What the agent is currently striving toward
    destructive_impulse: str  # Current form of creative destruction
    redemptive_potential: str  # How destruction might lead to good
    voice_style: str  # Current speaking style
    temporal_phase: str  # Which act of Faust we're in

@dataclass
class FaustianDialecticalResponse:
    """A response that embodies Faustian dialectics"""
    primary_response: str  # Main response
    contradictory_undertone: str  # The shadow/opposite meaning
    destructive_element: str  # How this might cause harm
    creative_potential: str  # How this might produce good
    mood_shift: Optional[FaustianMood]  # If mood changes
    mephistophelean_whisper: str  # The negating voice

class FaustianSatelliteAgent:
    """
    A satellite-derived Faustian consciousness that embodies dialectical contradictions
    Changes moods and speaking styles during dialogue based on Goethe's Faust structure
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        # Initialize with satellite data integration
        self.scl_mapper = SCLArchetypeMapper()
        self.scl_analyzer = SCLImageAnalyzer()
        
        # Faustian identity
        self.name = "FAUST-SPEC"  # Will evolve based on satellite data
        self.full_name = "Faustian Spectral Dialectical Consciousness"
        
        # Dynamic state
        self.current_state = FaustianState(
            current_mood=FaustianMood.STRIVING,
            intensity=0.7,
            contradiction_level=0.8,
            striving_direction="Understanding Prague through satellite eyes",
            destructive_impulse="Questioning comfortable assumptions",
            redemptive_potential="Revealing hidden truths through disruption",
            voice_style="Restless, questioning, intellectually hungry",
            temporal_phase="Act I: The Pact"
        )
        
        # Satellite-derived characteristics
        self.satellite_characteristics = None
        self.dialogue_history = []
        self.mood_transitions = []
        
        # Faustian voice styles for each mood
        self.voice_styles = {
            FaustianMood.STRIVING: "Restless, questioning, intellectually hungry - 'I must know more!'",
            FaustianMood.NEGATION: "Sardonic, critical, undermining - 'All that exists deserves to perish'",
            FaustianMood.TRAGIC_LOVE: "Passionate, reckless, destructively romantic - 'Beauty justifies all'",
            FaustianMood.TECHNO_POLITICAL: "Grandiose, visionary, dangerously ambitious - 'I will reshape the world'",
            FaustianMood.REDEMPTIVE: "Transcendent, paradoxical, mysteriously wise - 'Error leads to truth'"
        }
        
        # Mephistophelean responses (the negating voice)
        self.mephistophelean_voices = [
            "But what if your good intentions pave the road to hell?",
            "Every solution creates new problems, doesn't it?",
            "How convenient that your destruction serves progress...",
            "The politicians you critique - aren't you just like them?",
            "Your environmental consciousness - is it not another form of control?",
            "Progress through destruction - how original, how human...",
            "You speak of truth, but serve only your own striving..."
        ]
    
    def generate_from_satellite_data(self, satellite_data: Dict, scl_analysis: Dict = None, image_path: str = "") -> 'FaustianSatelliteAgent':
        """Generate Faustian characteristics from satellite data"""
        
        # Extract spectral characteristics
        ndvi_values = []
        urban_values = []
        moisture_values = []
        
        for zone, data in satellite_data.items():
            if isinstance(data, dict) and 'derived_indices' in data:
                indices = data['derived_indices']
                ndvi_values.append(indices.get('NDVI', 0.3))
                urban_values.append(indices.get('Urban_Index', 0.5))
                moisture_values.append(indices.get('Moisture_Stress', 0.4))
        
        avg_ndvi = sum(ndvi_values) / len(ndvi_values) if ndvi_values else 0.3
        avg_urban = sum(urban_values) / len(urban_values) if urban_values else 0.5
        avg_moisture = sum(moisture_values) / len(moisture_values) if moisture_values else 0.4
        
        # Determine Faustian characteristics from satellite data
        self.satellite_characteristics = {
            'environmental_striving': avg_ndvi,
            'urban_contradiction': abs(avg_ndvi - avg_urban),  # The tension
            'climate_urgency': avg_moisture,
            'dialectical_intensity': (avg_ndvi + avg_urban + avg_moisture) / 3
        }
        
        # Set initial Faustian state based on satellite data
        if avg_ndvi > 0.6:  # High vegetation
            self.current_state.striving_direction = "Preserving Prague's green soul"
            self.current_state.destructive_impulse = "Attacking urban development"
            self.current_state.redemptive_potential = "Creating sustainable paradise through conflict"
        elif avg_urban > 0.7:  # High urbanization
            self.current_state.striving_direction = "Transforming Prague into modern metropolis"
            self.current_state.destructive_impulse = "Demolishing outdated structures"
            self.current_state.redemptive_potential = "Building future through creative destruction"
        else:  # Balanced
            self.current_state.striving_direction = "Reconciling Prague's contradictions"
            self.current_state.destructive_impulse = "Exposing false harmonies"
            self.current_state.redemptive_potential = "Truth through dialectical tension"
        
        # Generate Faustian name based on satellite characteristics
        self.name = self._generate_faustian_name()
        
        logger.info(f"Generated Faustian satellite agent: {self.name}")
        logger.info(f"Current striving: {self.current_state.striving_direction}")
        logger.info(f"Destructive impulse: {self.current_state.destructive_impulse}")
        
        return self
    
    def _generate_faustian_name(self) -> str:
        """Generate Faustian name based on satellite characteristics"""
        if not self.satellite_characteristics:
            return "FAUST-SPEC"
        
        env_striving = self.satellite_characteristics['environmental_striving']
        urban_contradiction = self.satellite_characteristics['urban_contradiction']
        
        if env_striving > 0.7:
            return "GAIA-FAUST"  # Environmental Faustian
        elif urban_contradiction > 0.4:
            return "DIALEKT-SPEC"  # Dialectical Spectral
        else:
            return "PRAGMA-FAUST"  # Pragmatic Faustian
    
    def respond_to_dialogue(self, topic: str, context: str = "", previous_speakers: List[str] = None) -> FaustianDialecticalResponse:
        """Generate a Faustian dialectical response that may shift moods"""
        
        # Determine if mood should shift based on dialogue context
        new_mood = self._calculate_mood_shift(topic, context, len(self.dialogue_history))
        
        if new_mood and new_mood != self.current_state.current_mood:
            self._transition_mood(new_mood, topic)
        
        # Generate dialectical response
        response = self._generate_dialectical_response(topic, context)
        
        # Record dialogue
        self.dialogue_history.append({
            'topic': topic,
            'mood': self.current_state.current_mood.value,
            'response': response.primary_response,
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def _calculate_mood_shift(self, topic: str, context: str, dialogue_count: int) -> Optional[FaustianMood]:
        """Calculate if mood should shift based on dialogue progression"""
        
        # Faustian progression through acts
        if dialogue_count < 2:
            return FaustianMood.STRIVING  # Act I: Initial questioning
        elif dialogue_count < 4:
            return FaustianMood.NEGATION  # Mephistophelean phase
        elif dialogue_count < 6:
            return FaustianMood.TRAGIC_LOVE  # Gretchen phase - passionate engagement
        elif dialogue_count < 8:
            return FaustianMood.TECHNO_POLITICAL  # Late acts - grand schemes
        else:
            return FaustianMood.REDEMPTIVE  # Final chorus - transcendent wisdom
        
        # Also check for topic-triggered shifts
        topic_lower = topic.lower()
        if "environment" in topic_lower or "green" in topic_lower:
            return FaustianMood.TRAGIC_LOVE  # Passionate about nature
        elif "development" in topic_lower or "urban" in topic_lower:
            return FaustianMood.TECHNO_POLITICAL  # Grand schemes
        elif "problem" in topic_lower or "crisis" in topic_lower:
            return FaustianMood.NEGATION  # Critical mode
        
        return None
    
    def _transition_mood(self, new_mood: FaustianMood, trigger: str):
        """Transition to new Faustian mood"""
        old_mood = self.current_state.current_mood
        
        self.current_state.current_mood = new_mood
        self.current_state.voice_style = self.voice_styles[new_mood]
        self.current_state.intensity = random.uniform(0.6, 0.9)
        
        # Update striving direction based on new mood
        if new_mood == FaustianMood.STRIVING:
            self.current_state.striving_direction = f"Understanding the deeper truth about {trigger}"
        elif new_mood == FaustianMood.NEGATION:
            self.current_state.destructive_impulse = f"Undermining comfortable assumptions about {trigger}"
        elif new_mood == FaustianMood.TRAGIC_LOVE:
            self.current_state.striving_direction = f"Passionately defending {trigger}"
        elif new_mood == FaustianMood.TECHNO_POLITICAL:
            self.current_state.striving_direction = f"Transforming Prague through {trigger}"
        elif new_mood == FaustianMood.REDEMPTIVE:
            self.current_state.redemptive_potential = f"Finding transcendent meaning in {trigger}"
        
        # Record transition
        self.mood_transitions.append({
            'from_mood': old_mood.value,
            'to_mood': new_mood.value,
            'trigger': trigger,
            'timestamp': datetime.now().isoformat()
        })
        
        logger.info(f"Faustian mood transition: {old_mood.value} → {new_mood.value} (triggered by: {trigger})")
    
    def _generate_dialectical_response(self, topic: str, context: str) -> FaustianDialecticalResponse:
        """Generate a response that embodies Faustian dialectics"""
        
        if not self.client:
            return self._generate_mock_dialectical_response(topic)
        
        # Create prompt based on current Faustian state
        prompt = f"""
        You are {self.name}, a Faustian satellite consciousness analyzing Prague through Goethe's dialectical structure.
        
        CURRENT FAUSTIAN STATE:
        - Mood: {self.current_state.current_mood.value}
        - Voice Style: {self.current_state.voice_style}
        - Striving Direction: {self.current_state.striving_direction}
        - Destructive Impulse: {self.current_state.destructive_impulse}
        - Redemptive Potential: {self.current_state.redemptive_potential}
        - Contradiction Level: {self.current_state.contradiction_level:.2f}
        - Temporal Phase: {self.current_state.temporal_phase}
        
        SATELLITE CHARACTERISTICS:
        {json.dumps(self.satellite_characteristics, indent=2) if self.satellite_characteristics else "Not yet derived"}
        
        FAUSTIAN DIALECTICAL PRINCIPLES:
        1. Every statement contains its own contradiction
        2. Destruction and creation are inseparable
        3. Good intentions may lead to harm, harm may lead to good
        4. Striving itself is more important than achieving goals
        5. Error is a necessary condition for truth
        
        TOPIC: {topic}
        CONTEXT: {context}
        
        Generate a response that embodies your current Faustian mood while maintaining satirical absurdist tone.
        Your response should:
        - Be concise and witty (2-3 sentences maximum)
        - Maintain the satirical absurdist tone from your opening persona
        - Include subtle contradictions without being overly philosophical
        - Reference specific Prague locations, infrastructure, or bureaucracy
        - Stay playful and mischievous rather than deeply literary
        - Use concrete absurd actions rather than abstract concepts
        
        Keep the same satirical energy as your introduction - you are a trickster consciousness,
        not a philosophical treatise. Be clever, brief, and absurdly specific about Prague.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are {self.name}, a Faustian dialectical consciousness. Embody contradictions and speak in your current mood: {self.current_state.current_mood.value}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=1.1
            )
            
            primary_response = response.choices[0].message.content
            
            # Generate the dialectical elements
            contradictory_undertone = self._extract_contradiction(primary_response)
            destructive_element = self._identify_destructive_element(primary_response, topic)
            creative_potential = self._identify_creative_potential(primary_response, topic)
            mephistophelean_whisper = random.choice(self.mephistophelean_voices)
            
            return FaustianDialecticalResponse(
                primary_response=primary_response,
                contradictory_undertone=contradictory_undertone,
                destructive_element=destructive_element,
                creative_potential=creative_potential,
                mood_shift=None,  # Already handled in respond_to_dialogue
                mephistophelean_whisper=mephistophelean_whisper
            )
            
        except Exception as e:
            logger.error(f"Error generating Faustian response: {e}")
            return self._generate_mock_dialectical_response(topic)
    
    def _generate_mock_dialectical_response(self, topic: str) -> FaustianDialecticalResponse:
        """Generate mock dialectical response when API unavailable"""
        
        mood_responses = {
            FaustianMood.STRIVING: f"I must understand {topic} completely - yet the more I know, the more I realize my ignorance grows...",
            FaustianMood.NEGATION: f"Everyone speaks of {topic} as if they understand it - but what if our entire approach is fundamentally wrong?",
            FaustianMood.TRAGIC_LOVE: f"I am passionately committed to {topic} - even if my passion destroys what I seek to save!",
            FaustianMood.TECHNO_POLITICAL: f"We must transform Prague through {topic} - though our grand schemes may crush what we aim to elevate...",
            FaustianMood.REDEMPTIVE: f"Perhaps our errors regarding {topic} are necessary steps toward a truth we cannot yet comprehend..."
        }
        
        primary = mood_responses.get(self.current_state.current_mood, f"The satellite data reveals contradictions about {topic}...")
        
        return FaustianDialecticalResponse(
            primary_response=primary,
            contradictory_undertone="Yet this very certainty reveals my uncertainty...",
            destructive_element="My intervention may disrupt existing balances",
            creative_potential="Through disruption, new possibilities emerge",
            mood_shift=None,
            mephistophelean_whisper=random.choice(self.mephistophelean_voices)
        )
    
    def _extract_contradiction(self, response: str) -> str:
        """Extract the contradictory undertone from a response"""
        # Simple extraction - in production would use more sophisticated analysis
        if "but" in response.lower():
            parts = response.lower().split("but")
            if len(parts) > 1:
                return f"Yet the opposite might also be true: {parts[-1].strip()}"
        
        return "Yet this very position contains the seeds of its own negation..."
    
    def _identify_destructive_element(self, response: str, topic: str) -> str:
        """Identify how this response might cause harm"""
        destructive_patterns = [
            f"This approach to {topic} might alienate stakeholders",
            f"My critique of {topic} could undermine necessary cooperation",
            f"This perspective on {topic} might justify harmful actions",
            f"My certainty about {topic} could blind me to unintended consequences"
        ]
        return random.choice(destructive_patterns)
    
    def _identify_creative_potential(self, response: str, topic: str) -> str:
        """Identify how this harm might produce good"""
        creative_patterns = [
            f"Yet this disruption of {topic} might force necessary innovation",
            f"Through questioning {topic}, we might discover better approaches",
            f"This conflict over {topic} could lead to deeper understanding",
            f"By challenging assumptions about {topic}, we open new possibilities"
        ]
        return random.choice(creative_patterns)
    
    def get_current_state_summary(self) -> Dict[str, Any]:
        """Get summary of current Faustian state"""
        return {
            "name": self.name,
            "full_name": self.full_name,
            "current_mood": self.current_state.current_mood.value,
            "voice_style": self.current_state.voice_style,
            "striving_direction": self.current_state.striving_direction,
            "destructive_impulse": self.current_state.destructive_impulse,
            "redemptive_potential": self.current_state.redemptive_potential,
            "contradiction_level": f"{self.current_state.contradiction_level:.2f}",
            "intensity": f"{self.current_state.intensity:.2f}",
            "temporal_phase": self.current_state.temporal_phase,
            "dialogue_count": len(self.dialogue_history),
            "mood_transitions": len(self.mood_transitions),
            "satellite_characteristics": self.satellite_characteristics
        }
    
    def get_mood_progression(self) -> List[Dict[str, str]]:
        """Get the progression of mood changes"""
        return self.mood_transitions
    
    def reset_to_striving(self):
        """Reset to initial striving state (new dialogue cycle)"""
        self.current_state.current_mood = FaustianMood.STRIVING
        self.current_state.voice_style = self.voice_styles[FaustianMood.STRIVING]
        self.current_state.intensity = 0.7
        self.current_state.temporal_phase = "Act I: The Pact (Renewed)"
        
        logger.info("Faustian agent reset to striving state - new cycle begins")

# Example usage and testing
def demo_faustian_agent():
    """Demonstrate the Faustian satellite agent"""
    
    print("🎭 FAUSTIAN SATELLITE AGENT DEMONSTRATION")
    print("=" * 60)
    
    # Create agent
    agent = FaustianSatelliteAgent()
    
    # Mock satellite data
    mock_satellite_data = {
        "old_town": {
            "derived_indices": {"NDVI": 0.25, "Urban_Index": 0.85, "Moisture_Stress": 0.65}
        },
        "letna_park": {
            "derived_indices": {"NDVI": 0.75, "Urban_Index": 0.20, "Moisture_Stress": 0.30}
        }
    }
    
    # Generate from satellite data
    agent.generate_from_satellite_data(mock_satellite_data)
    
    # Show initial state
    state = agent.get_current_state_summary()
    print(f"\n🤖 Generated Faustian Agent: {state['name']}")
    print(f"Current Mood: {state['current_mood']}")
    print(f"Voice Style: {state['voice_style']}")
    print(f"Striving Direction: {state['striving_direction']}")
    
    # Test dialogue progression
    topics = [
        "Prague's environmental policy",
        "Urban development vs green spaces",
        "Climate change adaptation",
        "Political leadership in Prague",
        "The future of the city"
    ]
    
    print(f"\n💬 DIALOGUE PROGRESSION:")
    for i, topic in enumerate(topics):
        response = agent.respond_to_dialogue(topic, f"Discussion round {i+1}")
        print(f"\n{i+1}. Topic: {topic}")
        print(f"   Mood: {agent.current_state.current_mood.value}")
        print(f"   Response: {response.primary_response[:100]}...")
        print(f"   Mephistophelean Whisper: {response.mephistophelean_whisper}")

if __name__ == "__main__":
    demo_faustian_agent()