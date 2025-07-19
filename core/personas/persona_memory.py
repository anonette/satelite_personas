"""
Persona Memory System - Logophoric Integrity
Maintains memory and perspective consistency for spectral band personas
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum
import json
import logging

class ObservationType(Enum):
    ENVIRONMENTAL_CHANGE = "environmental_change"
    HUMAN_INTERACTION = "human_interaction"
    INTER_PERSONA_DIALOGUE = "inter_persona_dialogue"
    SPATIAL_EVENT = "spatial_event"
    TEMPORAL_SHIFT = "temporal_shift"

class EmotionalState(Enum):
    CALM = "calm"
    CONCERNED = "concerned"
    DISTRESSED = "distressed"
    ANGRY = "angry"
    MELANCHOLIC = "melancholic"
    CURIOUS = "curious"
    PROTECTIVE = "protective"

@dataclass
class Observation:
    """Single observation/memory entry for a persona"""
    timestamp: datetime
    observation_type: ObservationType
    content: str
    ethical_impact: float  # -1.0 to 1.0, negative = harmful, positive = beneficial
    spatial_context: Optional[Dict[str, float]] = None  # lat, lon, area
    related_personas: List[str] = field(default_factory=list)
    user_involved: bool = False
    emotional_response: EmotionalState = EmotionalState.CALM
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "observation_type": self.observation_type.value,
            "content": self.content,
            "ethical_impact": self.ethical_impact,
            "spatial_context": self.spatial_context,
            "related_personas": self.related_personas,
            "user_involved": self.user_involved,
            "emotional_response": self.emotional_response.value
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Observation':
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            observation_type=ObservationType(data["observation_type"]),
            content=data["content"],
            ethical_impact=data["ethical_impact"],
            spatial_context=data.get("spatial_context"),
            related_personas=data.get("related_personas", []),
            user_involved=data.get("user_involved", False),
            emotional_response=EmotionalState(data.get("emotional_response", "calm"))
        )

class PersonaMemory:
    """Memory system maintaining logophoric integrity for spectral personas"""
    
    def __init__(self, persona_id: str, band_id: str, max_memories: int = 100):
        self.persona_id = persona_id
        self.band_id = band_id
        self.max_memories = max_memories
        
        # Core memory components
        self.observations: List[Observation] = []
        self.current_emotional_state = EmotionalState.CALM
        self.ethical_positioning_history: List[Dict] = []
        self.relationship_map: Dict[str, float] = {}  # persona_id -> relationship strength
        
        # Temporal awareness
        self.first_observation: Optional[datetime] = None
        self.last_interaction: Optional[datetime] = None
        
        # Spatial awareness
        self.primary_location: Optional[Dict[str, float]] = None
        self.observed_areas: List[Dict] = []
        
        # Personality evolution
        self.personality_traits: Dict[str, float] = {
            "sensitivity": 0.5,      # How strongly affected by changes
            "memory_retention": 0.7,  # How well memories are preserved
            "social_engagement": 0.5, # Willingness to interact
            "ethical_intensity": 0.5  # Strength of ethical positioning
        }
        
        self.logger = logging.getLogger(f"{__name__}.{persona_id}")
    
    def register_observation(self, 
                           content: str,
                           observation_type: ObservationType,
                           ethical_impact: float,
                           spatial_context: Optional[Dict] = None,
                           related_personas: List[str] = None,
                           user_involved: bool = False) -> Observation:
        """Register a new observation/memory"""
        
        # Determine emotional response based on ethical impact and personality
        emotional_response = self._calculate_emotional_response(ethical_impact)
        
        observation = Observation(
            timestamp=datetime.now(),
            observation_type=observation_type,
            content=content,
            ethical_impact=ethical_impact,
            spatial_context=spatial_context,
            related_personas=related_personas or [],
            user_involved=user_involved,
            emotional_response=emotional_response
        )
        
        self.observations.append(observation)
        
        # Update temporal tracking
        if self.first_observation is None:
            self.first_observation = observation.timestamp
        self.last_interaction = observation.timestamp
        
        # Update spatial awareness
        if spatial_context:
            self._update_spatial_awareness(spatial_context)
        
        # Update relationships
        if related_personas:
            self._update_relationships(related_personas, ethical_impact)
        
        # Update emotional state
        self._update_emotional_state(observation)
        
        # Maintain memory limits
        self._maintain_memory_limits()
        
        self.logger.info(f"Registered observation: {content[:50]}...")
        return observation
    
    def _calculate_emotional_response(self, ethical_impact: float) -> EmotionalState:
        """Calculate emotional response based on impact and personality"""
        sensitivity = self.personality_traits["sensitivity"]
        adjusted_impact = ethical_impact * sensitivity
        
        if adjusted_impact < -0.7:
            return EmotionalState.DISTRESSED
        elif adjusted_impact < -0.3:
            return EmotionalState.CONCERNED
        elif adjusted_impact < -0.1:
            return EmotionalState.MELANCHOLIC
        elif adjusted_impact > 0.5:
            return EmotionalState.PROTECTIVE
        elif adjusted_impact > 0.2:
            return EmotionalState.CURIOUS
        else:
            return EmotionalState.CALM
    
    def _update_spatial_awareness(self, spatial_context: Dict):
        """Update understanding of spatial environment"""
        if self.primary_location is None:
            self.primary_location = spatial_context.copy()
        
        # Add to observed areas if significantly different
        is_new_area = True
        for area in self.observed_areas:
            if (abs(area.get("lat", 0) - spatial_context.get("lat", 0)) < 0.001 and
                abs(area.get("lon", 0) - spatial_context.get("lon", 0)) < 0.001):
                is_new_area = False
                break
        
        if is_new_area:
            self.observed_areas.append({
                **spatial_context,
                "first_observed": datetime.now().isoformat(),
                "observation_count": 1
            })
        else:
            # Update observation count for existing area
            for area in self.observed_areas:
                if (abs(area.get("lat", 0) - spatial_context.get("lat", 0)) < 0.001 and
                    abs(area.get("lon", 0) - spatial_context.get("lon", 0)) < 0.001):
                    area["observation_count"] = area.get("observation_count", 0) + 1
                    break
    
    def _update_relationships(self, related_personas: List[str], ethical_impact: float):
        """Update relationship strengths with other personas"""
        for persona_id in related_personas:
            current_strength = self.relationship_map.get(persona_id, 0.0)
            
            # Positive impacts strengthen relationships, negative ones weaken them
            impact_factor = ethical_impact * 0.1  # Scale down the impact
            new_strength = max(-1.0, min(1.0, current_strength + impact_factor))
            
            self.relationship_map[persona_id] = new_strength
    
    def _update_emotional_state(self, observation: Observation):
        """Update current emotional state based on recent observations"""
        # Weight recent observations more heavily
        recent_observations = self.get_recent_observations(hours=1)
        
        if not recent_observations:
            return
        
        # Calculate weighted average of recent emotional impacts
        total_weight = 0
        weighted_impact = 0
        
        for obs in recent_observations:
            # More recent observations have higher weight
            age_hours = (datetime.now() - obs.timestamp).total_seconds() / 3600
            weight = max(0.1, 1.0 - age_hours)  # Linear decay over 1 hour
            
            weighted_impact += obs.ethical_impact * weight
            total_weight += weight
        
        if total_weight > 0:
            avg_impact = weighted_impact / total_weight
            self.current_emotional_state = self._calculate_emotional_response(avg_impact)
    
    def _maintain_memory_limits(self):
        """Maintain memory within limits, preserving important memories"""
        if len(self.observations) <= self.max_memories:
            return
        
        # Sort by importance (combination of ethical impact and recency)
        def memory_importance(obs: Observation) -> float:
            age_days = (datetime.now() - obs.timestamp).days
            recency_factor = max(0.1, 1.0 - age_days / 30)  # Decay over 30 days
            impact_factor = abs(obs.ethical_impact)
            user_factor = 1.5 if obs.user_involved else 1.0
            
            return impact_factor * recency_factor * user_factor
        
        # Keep the most important memories
        self.observations.sort(key=memory_importance, reverse=True)
        self.observations = self.observations[:self.max_memories]
        
        # Re-sort by timestamp for chronological access
        self.observations.sort(key=lambda x: x.timestamp)
    
    def get_recent_observations(self, hours: int = 24) -> List[Observation]:
        """Get observations from the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [obs for obs in self.observations if obs.timestamp >= cutoff_time]
    
    def get_observations_by_type(self, observation_type: ObservationType) -> List[Observation]:
        """Get all observations of a specific type"""
        return [obs for obs in self.observations if obs.observation_type == observation_type]
    
    def get_observations_involving_user(self) -> List[Observation]:
        """Get all observations involving user interaction"""
        return [obs for obs in self.observations if obs.user_involved]
    
    def get_relationship_strength(self, persona_id: str) -> float:
        """Get relationship strength with another persona (-1.0 to 1.0)"""
        return self.relationship_map.get(persona_id, 0.0)
    
    def get_memory_summary(self) -> Dict:
        """Get summary of memory state for context generation"""
        recent_obs = self.get_recent_observations(hours=6)
        user_interactions = self.get_observations_involving_user()
        
        return {
            "total_observations": len(self.observations),
            "recent_observations": len(recent_obs),
            "user_interactions": len(user_interactions),
            "current_emotional_state": self.current_emotional_state.value,
            "primary_location": self.primary_location,
            "observed_areas_count": len(self.observed_areas),
            "active_relationships": len([r for r in self.relationship_map.values() if abs(r) > 0.1]),
            "personality_traits": self.personality_traits.copy(),
            "time_since_first_observation": (
                (datetime.now() - self.first_observation).total_seconds() / 3600
                if self.first_observation else 0
            ),
            "time_since_last_interaction": (
                (datetime.now() - self.last_interaction).total_seconds() / 3600
                if self.last_interaction else 0
            )
        }
    
    def generate_context_for_response(self, current_topic: str = "") -> str:
        """Generate contextual information for response generation"""
        summary = self.get_memory_summary()
        recent_obs = self.get_recent_observations(hours=2)
        
        context_parts = []
        
        # Current state
        context_parts.append(f"Current emotional state: {summary['current_emotional_state']}")
        
        # Recent experiences
        if recent_obs:
            recent_impacts = [obs.ethical_impact for obs in recent_obs]
            avg_impact = sum(recent_impacts) / len(recent_impacts)
            context_parts.append(f"Recent experiences (avg impact: {avg_impact:.2f})")
            
            # Most significant recent observation
            most_significant = max(recent_obs, key=lambda x: abs(x.ethical_impact))
            context_parts.append(f"Most significant recent: {most_significant.content[:100]}")
        
        # Spatial awareness
        if summary["primary_location"]:
            loc = summary["primary_location"]
            context_parts.append(f"Primary location: {loc.get('lat', 0):.3f}, {loc.get('lon', 0):.3f}")
        
        # Relationships
        strong_relationships = {k: v for k, v in self.relationship_map.items() if abs(v) > 0.3}
        if strong_relationships:
            context_parts.append(f"Strong relationships: {strong_relationships}")
        
        # Memory depth
        if summary["total_observations"] > 10:
            context_parts.append(f"Memory depth: {summary['total_observations']} observations over {summary['time_since_first_observation']:.1f} hours")
        
        return " | ".join(context_parts)
    
    def save_to_file(self, filepath: str):
        """Save memory state to JSON file"""
        data = {
            "persona_id": self.persona_id,
            "band_id": self.band_id,
            "current_emotional_state": self.current_emotional_state.value,
            "personality_traits": self.personality_traits,
            "primary_location": self.primary_location,
            "observed_areas": self.observed_areas,
            "relationship_map": self.relationship_map,
            "observations": [obs.to_dict() for obs in self.observations],
            "first_observation": self.first_observation.isoformat() if self.first_observation else None,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved memory to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving memory: {e}")
    
    def load_from_file(self, filepath: str):
        """Load memory state from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.persona_id = data["persona_id"]
            self.band_id = data["band_id"]
            self.current_emotional_state = EmotionalState(data["current_emotional_state"])
            self.personality_traits = data["personality_traits"]
            self.primary_location = data.get("primary_location")
            self.observed_areas = data.get("observed_areas", [])
            self.relationship_map = data.get("relationship_map", {})
            
            # Load observations
            self.observations = [
                Observation.from_dict(obs_data) 
                for obs_data in data.get("observations", [])
            ]
            
            # Load timestamps
            if data.get("first_observation"):
                self.first_observation = datetime.fromisoformat(data["first_observation"])
            if data.get("last_interaction"):
                self.last_interaction = datetime.fromisoformat(data["last_interaction"])
            
            self.logger.info(f"Loaded memory from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Error loading memory: {e}")

if __name__ == "__main__":
    # Test the memory system
    memory = PersonaMemory("B08_chlorophyll_guardian", "B08")
    
    # Register some test observations
    memory.register_observation(
        "Vegetation health declining in observed area",
        ObservationType.ENVIRONMENTAL_CHANGE,
        -0.6,
        {"lat": 50.075, "lon": 14.437},
        ["B11_moisture_detective"],
        user_involved=False
    )
    
    memory.register_observation(
        "User asked about chlorophyll levels",
        ObservationType.HUMAN_INTERACTION,
        0.2,
        user_involved=True
    )
    
    memory.register_observation(
        "Moisture levels dropping rapidly",
        ObservationType.INTER_PERSONA_DIALOGUE,
        -0.8,
        related_personas=["B11_moisture_detective"]
    )
    
    # Test memory functions
    print("=== Memory Summary ===")
    summary = memory.get_memory_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")
    
    print("\n=== Context for Response ===")
    context = memory.generate_context_for_response("vegetation health")
    print(context)
    
    print("\n=== Recent Observations ===")
    recent = memory.get_recent_observations(hours=1)
    for obs in recent:
        print(f"{obs.timestamp}: {obs.content} (impact: {obs.ethical_impact})")
    
    # Test save/load
    memory.save_to_file("test_memory.json")
    
    new_memory = PersonaMemory("test", "test")
    new_memory.load_from_file("test_memory.json")
    print(f"\nLoaded memory has {len(new_memory.observations)} observations")