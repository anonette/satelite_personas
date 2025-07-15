"""
Classic Mystical Persona Generator
Enhanced for Spectral Urban Multiplicity - micro-agents and ensemble generation
"""

import json
import random
from typing import Dict, List, Optional, Tuple
import openai
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ClassicPersona:
    """A classic mystical persona from spectral data"""
    name: str
    dominant_band: str
    counter_band: str
    voice_sample: str
    temperament: str
    memory: str
    warning: str
    agent_type: str = "macro"  # "macro" or "micro"
    intensity: float = 1.0  # Spectral intensity 0-1
    temporal_role: str = "stable"  # "stable", "emerging", "fading"

@dataclass
class SpectralEnsemble:
    """A collection of micro-agents from spectral flux"""
    location: Dict[str, float]
    date: str
    dominant_agent: ClassicPersona
    conflicting_agent: ClassicPersona
    supporting_agent: ClassicPersona
    micro_agents: List[ClassicPersona]
    ensemble_mood: str
    political_tension: str

class ClassicPersonaGenerator:
    """Generator for classic mystical personas and spectral ensembles"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        # Enhanced band roles for micro-agent generation
        self.band_agent_roles = {
            "B1": {
                "role": "Smog Spirit",
                "temperament": "paranoid, breathless",
                "political_role": "sky warning",
                "micro_type": "atmospheric alarm",
                "voice_style": "gasping urgency"
            },
            "B2": {
                "role": "Azure Contemplator", 
                "temperament": "melancholic blue, deep contemplation",
                "political_role": "water memory keeper",
                "micro_type": "aquatic consciousness",
                "voice_style": "flowing meditation"
            },
            "B3": {
                "role": "Beautifier",
                "temperament": "shallow optimism, surface actor",
                "political_role": "green marketing",
                "micro_type": "surface enthusiast",
                "voice_style": "glimmering promises"
            },
            "B4": {
                "role": "Chronicler of Stress",
                "temperament": "bleeding realist, raw truth-teller",
                "political_role": "infrastructure witness",
                "micro_type": "pain documentarian",
                "voice_style": "stark testimony"
            },
            "B5": {
                "role": "Plant Whisperer",
                "temperament": "subtle, anxious, transitional",
                "political_role": "vegetation advocate",
                "micro_type": "edge sensor",
                "voice_style": "rustling concern"
            },
            "B6": {
                "role": "Boundary Walker",
                "temperament": "edge-walker, boundary consciousness",
                "political_role": "threshold guardian",
                "micro_type": "liminal navigator",
                "voice_style": "spectral boundary"
            },
            "B7": {
                "role": "Sensor Ghost",
                "temperament": "liminal whispers, threshold guardian",
                "political_role": "transition monitor",
                "micro_type": "spectral detective",
                "voice_style": "haunting observation"
            },
            "B8": {
                "role": "Vitalist",
                "temperament": "proud, reflecting, prideful civic agent",
                "political_role": "life force advocate",
                "micro_type": "infrared champion",
                "voice_style": "confident proclamation"
            },
            "B8A": {
                "role": "Refined Perceiver",
                "temperament": "refined perception, subtle observations",
                "political_role": "nuance detector",
                "micro_type": "subtle analyst",
                "voice_style": "whispered precision"
            },
            "B9": {
                "role": "Cloud-Lover",
                "temperament": "absent, poetic, atmospheric mystic",
                "political_role": "rain memory",
                "micro_type": "vapor dreamer",
                "voice_style": "ethereal longing"
            },
            "B11": {
                "role": "Heat-Witness",
                "temperament": "dry, hoarse, prophetic",
                "political_role": "infrastructural trauma",
                "micro_type": "drought herald",
                "voice_style": "parched warning"
            },
            "B12": {
                "role": "The Irreversible One",
                "temperament": "silent, wounded, ancient heat",
                "political_role": "geological memory",
                "micro_type": "burn scar keeper",
                "voice_style": "deep time silence"
            }
        }
        
        self.prague_districts = {
            "Praha 1": "Medieval core, touristic heart",
            "Praha 2": "New Town, commercial district", 
            "Praha 3": "Vinohrady, bourgeois quarter",
            "Praha 4": "Nusle, mixed residential",
            "Praha 5": "Smíchov, industrial heritage",
            "Praha 6": "Dejvice, diplomatic quarter",
            "Praha 7": "Holešovice, cultural revival",
            "Praha 8": "Karlín, flood-prone rebirth",
            "Praha 9": "Vysočany, industrial periphery",
            "Praha 10": "Vršovice, working-class heritage"
        }
    
    def generate_spectral_ensemble(self, spectral_data: Dict[str, float], location: Dict[str, float], 
                                 date: str, data_source: str, data_quality: str) -> SpectralEnsemble:
        """Generate a complete spectral ensemble with micro-agents"""
        
        # Analyze spectral flux for ensemble dynamics
        dominant_band, secondary_bands = self._analyze_spectral_flux(spectral_data)
        
        # Generate core triad
        dominant_agent = self._generate_micro_agent(
            dominant_band, spectral_data[dominant_band], location, date, "dominant"
        )
        
        # Find conflicting band (opposite energy)
        conflicting_band = self._find_conflicting_band(dominant_band, spectral_data)
        conflicting_agent = self._generate_micro_agent(
            conflicting_band, spectral_data[conflicting_band], location, date, "conflicting"
        )
        
        # Find supporting band (harmonious energy)
        supporting_band = self._find_supporting_band(dominant_band, spectral_data)
        supporting_agent = self._generate_micro_agent(
            supporting_band, spectral_data[supporting_band], location, date, "supporting"
        )
        
        # Generate additional micro-agents for high-intensity bands
        micro_agents = []
        for band, value in spectral_data.items():
            if value > 0.7 and band not in [dominant_band, conflicting_band, supporting_band]:
                micro_agent = self._generate_micro_agent(
                    band, value, location, date, "temporal"
                )
                micro_agents.append(micro_agent)
        
        # Determine ensemble dynamics
        ensemble_mood = self._calculate_ensemble_mood(spectral_data)
        political_tension = self._analyze_political_tension(dominant_agent, conflicting_agent)
        
        return SpectralEnsemble(
            location=location,
            date=date,
            dominant_agent=dominant_agent,
            conflicting_agent=conflicting_agent,
            supporting_agent=supporting_agent,
            micro_agents=micro_agents,
            ensemble_mood=ensemble_mood,
            political_tension=political_tension
        )
    
    def _analyze_spectral_flux(self, spectral_data: Dict[str, float]) -> Tuple[str, List[str]]:
        """Analyze spectral data to find dominant and secondary bands"""
        sorted_bands = sorted(spectral_data.items(), key=lambda x: x[1], reverse=True)
        dominant_band = sorted_bands[0][0]
        secondary_bands = [band for band, value in sorted_bands[1:4]]
        return dominant_band, secondary_bands
    
    def _find_conflicting_band(self, dominant_band: str, spectral_data: Dict[str, float]) -> str:
        """Find band that creates dramatic tension with dominant"""
        conflicts = {
            "B1": "B8",   # Atmospheric anxiety vs life force
            "B3": "B4",   # Surface optimism vs bleeding reality
            "B8": "B11",  # Vegetation pride vs drought
            "B9": "B12",  # Water vapor vs ancient heat
            "B11": "B3",  # Dryness vs green hope
            "B4": "B9",   # Harsh reality vs poetic absence
        }
        
        preferred_conflict = conflicts.get(dominant_band)
        if preferred_conflict and preferred_conflict in spectral_data:
            return preferred_conflict
        
        # Fall back to lowest value band for contrast
        return min(spectral_data.items(), key=lambda x: x[1])[0]
    
    def _find_supporting_band(self, dominant_band: str, spectral_data: Dict[str, float]) -> str:
        """Find band that harmonizes with dominant"""
        harmonies = {
            "B8": "B5",   # NIR + Red edge harmony
            "B3": "B2",   # Green + Blue natural harmony
            "B11": "B12", # SWIR harmony
            "B4": "B5",   # Red + Red edge stress harmony
        }
        
        preferred_harmony = harmonies.get(dominant_band)
        if preferred_harmony and preferred_harmony in spectral_data:
            return preferred_harmony
        
        # Fall back to highest remaining value
        remaining_bands = {k: v for k, v in spectral_data.items() if k != dominant_band}
        return max(remaining_bands.items(), key=lambda x: x[1])[0]
    
    def _generate_micro_agent(self, band: str, intensity: float, location: Dict[str, float], 
                             date: str, role_type: str) -> ClassicPersona:
        """Generate a micro-agent for specific spectral band"""
        
        band_info = self.band_agent_roles.get(band, {
            "role": "Unknown Entity",
            "temperament": "mysterious",
            "political_role": "undefined",
            "micro_type": "spectral anomaly",
            "voice_style": "enigmatic"
        })
        
        # Generate Czech-inspired names based on band and intensity
        name = self._generate_czech_micro_name(band, intensity, band_info["role"])
        
        # Create voice sample based on band characteristics and intensity
        voice_sample = self._create_micro_voice(band, intensity, band_info, location)
        
        # Determine temporal role based on intensity
        temporal_role = self._determine_temporal_role(intensity, role_type)
        
        return ClassicPersona(
            name=name,
            dominant_band=band,
            counter_band="",  # Micro-agents are pure expressions
            voice_sample=voice_sample,
            temperament=f"{band_info['temperament']} (intensity: {intensity:.2f})",
            memory=self._generate_micro_memory(band, location),
            warning=self._generate_micro_warning(band, intensity),
            agent_type="micro",
            intensity=intensity,
            temporal_role=temporal_role
        )
    
    def _generate_czech_micro_name(self, band: str, intensity: float, role: str) -> str:
        """Generate Czech-inspired names for micro-agents"""
        
        czech_prefixes = {
            "B1": ["Kouř", "Mlha", "Dech"],  # Smoke, Fog, Breath
            "B2": ["Modrý", "Vodník", "Nebe"],  # Blue, Water sprite, Sky
            "B3": ["Zelený", "Tráva", "List"],  # Green, Grass, Leaf
            "B4": ["Červený", "Krev", "Bolest"],  # Red, Blood, Pain
            "B5": ["Hranice", "Přechod", "Most"],  # Border, Transition, Bridge
            "B8": ["Život", "Síla", "Růst"],  # Life, Force, Growth
            "B9": ["Pára", "Oblak", "Déšť"],  # Steam, Cloud, Rain
            "B11": ["Sušení", "Teplo", "Žízeň"],  # Drying, Heat, Thirst
            "B12": ["Popel", "Žár", "Věčnost"]  # Ash, Heat, Eternity
        }
        
        czech_suffixes = ["ová", "ík", "ka", "ek", "ář", "ice"]
        
        prefixes = czech_prefixes.get(band, ["Spectral"])
        prefix = random.choice(prefixes)
        suffix = random.choice(czech_suffixes)
        
        # Intensity modifiers
        if intensity > 0.8:
            intensity_mod = "Veliký"  # Great
        elif intensity > 0.6:
            intensity_mod = "Silný"   # Strong  
        elif intensity > 0.4:
            intensity_mod = "Jemný"   # Gentle
        else:
            intensity_mod = "Tichý"   # Quiet
        
        return f"{intensity_mod} {prefix}{suffix}"
    
    def _create_micro_voice(self, band: str, intensity: float, band_info: Dict, location: Dict[str, float]) -> str:
        """Create voice sample for micro-agent"""
        
        voice_templates = {
            "B1": "The air tastes of {intensity_desc}. I whisper warnings through the haze.",
            "B3": "I shimmer on surfaces, promising {intensity_desc} renewal. Do you see my gleam?",
            "B4": "I bleed {intensity_desc} truth from these stones. The city's pain speaks through me.",
            "B8": "My infrared eyes see {intensity_desc} life force. I am the hidden vitality.",
            "B9": "I drift as {intensity_desc} vapor, remembering when clouds brought mercy.",
            "B11": "I am {intensity_desc} dryness, the thirst that buildings feel."
        }
        
        intensity_descriptions = {
            0.8: "overwhelming", 0.6: "persistent", 0.4: "subtle", 0.2: "fading"
        }
        
        # Find closest intensity description
        intensity_desc = "mysterious"
        for threshold, desc in intensity_descriptions.items():
            if intensity >= threshold:
                intensity_desc = desc
                break
        
        template = voice_templates.get(band, "I am the {intensity_desc} voice of {band}.")
        return template.format(intensity_desc=intensity_desc, band=band)
    
    def _determine_temporal_role(self, intensity: float, role_type: str) -> str:
        """Determine if agent is stable, emerging, or fading"""
        if role_type == "temporal":
            return "emerging" if intensity > 0.7 else "fading"
        elif role_type == "dominant":
            return "stable"
        else:
            return "responding"
    
    def _generate_micro_memory(self, band: str, location: Dict[str, float]) -> str:
        """Generate memory for micro-agent"""
        memories = {
            "B1": "I remember cleaner air, before the particles gathered.",
            "B3": "There was a time when green here meant more than decoration.",
            "B4": "I have watched this place stress and bleed through decades.",
            "B8": "I recall when life force flowed stronger through this soil.",
            "B9": "Rain once came regularly. I miss its conversations.",
            "B11": "The heat grows. I feel the city's thirst increasing."
        }
        return memories.get(band, "I carry spectral memories of this place.")
    
    def _generate_micro_warning(self, band: str, intensity: float) -> str:
        """Generate warning for micro-agent"""
        if intensity > 0.8:
            urgency = "urgent"
        elif intensity > 0.6:
            urgency = "growing"
        else:
            urgency = "subtle"
        
        warnings = {
            "B1": f"The atmospheric burden becomes {urgency}.",
            "B3": f"Surface beauty masks {urgency} reality.",
            "B4": f"The bleeding grows {urgency}.",
            "B8": f"Life force faces {urgency} pressure.",
            "B9": f"Water absence becomes {urgency}.",
            "B11": f"The drying trend is {urgency}."
        }
        return warnings.get(band, f"Spectral changes are {urgency}.")
    
    def _calculate_ensemble_mood(self, spectral_data: Dict[str, float]) -> str:
        """Calculate overall mood of the spectral ensemble"""
        avg_intensity = sum(spectral_data.values()) / len(spectral_data)
        max_intensity = max(spectral_data.values())
        variance = sum((v - avg_intensity) ** 2 for v in spectral_data.values()) / len(spectral_data)
        
        if max_intensity > 0.8 and variance > 0.1:
            return "turbulent_awakening"
        elif avg_intensity > 0.6:
            return "heightened_awareness"
        elif variance > 0.15:
            return "conflicted_tension"
        else:
            return "harmonious_murmur"
    
    def _analyze_political_tension(self, dominant: ClassicPersona, conflicting: ClassicPersona) -> str:
        """Analyze political tension between agents"""
        tensions = {
            ("B8", "B11"): "life_versus_drought",
            ("B3", "B4"): "optimism_versus_realism", 
            ("B1", "B9"): "pollution_versus_purity",
            ("B8", "B1"): "vitality_versus_contamination"
        }
        
        key = (dominant.dominant_band, conflicting.dominant_band)
        return tensions.get(key, "spectral_disagreement")
    
    def ensemble_dialogue(self, ensemble: SpectralEnsemble, user_message: str, 
                         mediator_approach: str = "neutral") -> Dict[str, str]:
        """Generate ensemble dialogue with user as mediator"""
        
        responses = {}
        
        # Dominant agent speaks first
        responses["dominant"] = self._agent_response(
            ensemble.dominant_agent, user_message, "assertive"
        )
        
        # Conflicting agent responds with tension
        responses["conflicting"] = self._agent_response(
            ensemble.conflicting_agent, user_message, "contrarian", 
            context=responses["dominant"]
        )
        
        # Supporting agent tries to bridge
        responses["supporting"] = self._agent_response(
            ensemble.supporting_agent, user_message, "harmonizing",
            context=f"Hearing both {ensemble.dominant_agent.name} and {ensemble.conflicting_agent.name}"
        )
        
        # Micro-agents whisper if conditions are right
        if ensemble.micro_agents and mediator_approach == "open":
            micro_voices = []
            for agent in ensemble.micro_agents[:2]:  # Limit to avoid chaos
                voice = self._agent_response(agent, user_message, "whispered")
                micro_voices.append(f"{agent.name}: {voice}")
            responses["micro_chorus"] = " | ".join(micro_voices)
        
        return responses
    
    def _agent_response(self, agent: ClassicPersona, user_message: str, 
                       response_style: str, context: str = "") -> str:
        """Generate agent response based on style and context"""
        
        if not self.client:
            return self._mock_agent_response(agent, response_style)
        
        style_prompts = {
            "assertive": f"Respond confidently as {agent.name}, asserting your {agent.dominant_band} perspective.",
            "contrarian": f"As {agent.name}, disagree with or complicate the previous statement: {context}",
            "harmonizing": f"As {agent.name}, try to find common ground or deeper truth: {context}",
            "whispered": f"As {agent.name}, offer a brief, haunting observation."
        }
        
        prompt = f"""
You are {agent.name}, a spectral micro-agent emerging from band {agent.dominant_band}.
Your role: {self.band_agent_roles.get(agent.dominant_band, {}).get('role', 'Unknown')}
Your temperament: {agent.temperament}
Your intensity: {agent.intensity:.2f}

{style_prompts.get(response_style, "Respond as yourself.")}

Human message: "{user_message}"

Respond in 1-2 sentences, staying true to your spectral nature.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are {agent.name}, a spectral micro-agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                max_tokens=200
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in agent response: {e}")
            return self._mock_agent_response(agent, response_style)
    
    def _mock_agent_response(self, agent: ClassicPersona, response_style: str) -> str:
        """Generate mock response for agent"""
        style_responses = {
            "assertive": f"*{agent.name} pulses with {agent.dominant_band} energy* I speak for the {agent.intensity:.1f} intensity here.",
            "contrarian": f"*{agent.name} disagrees* But the {agent.dominant_band} tells a different story!",
            "harmonizing": f"*{agent.name} seeks balance* Perhaps both {agent.dominant_band} truths can coexist.",
            "whispered": f"*{agent.name} whispers* The {agent.dominant_band} remembers..."
        }
        return style_responses.get(response_style, f"*{agent.name} emanates {agent.dominant_band} consciousness*")
    
    # Legacy single persona method for backward compatibility
    def generate_persona(self, spectral_data: Dict[str, float], location: Dict[str, float], 
                        date: str, data_source: str, data_quality: str) -> ClassicPersona:
        """Generate single persona (legacy method)"""
        ensemble = self.generate_spectral_ensemble(spectral_data, location, date, data_source, data_quality)
        return ensemble.dominant_agent
    
    def communicate(self, persona: ClassicPersona, user_message: str) -> str:
        """Communicate with single persona (legacy method)"""
        return self._agent_response(persona, user_message, "assertive") 