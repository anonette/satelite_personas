#!/usr/bin/env python3
"""
Satellite-Derived Political Assessor
A persona generated from satellite data that assesses and criticizes politicians
Uses established spectral band mapping and SCL classifications
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import openai
import numpy as np

# Import established mapping systems
from core.satellite.scl_analyzer import SCLArchetypeMapper, SCLImageAnalyzer

logger = logging.getLogger(__name__)

@dataclass
class SatellitePersonaCharacteristics:
    """Characteristics derived from satellite data analysis using established band and SCL mapping"""
    environmental_consciousness: float  # 0-1 based on NDVI and vegetation health
    urban_critique_level: float  # 0-1 based on urban development intensity
    climate_urgency: float  # 0-1 based on moisture stress and temperature indicators
    development_skepticism: float  # 0-1 based on urban vs natural balance
    data_authority: float  # 0-1 based on data quality and coverage
    spectral_personality: str  # Dominant spectral characteristic
    assessment_bias: str  # Primary assessment tendency
    critical_focus: List[str]  # Main areas of political criticism
    
    # Enhanced with SCL and band mapping
    dominant_scl_archetype: Optional[Any] = None  # Primary SCL archetype
    secondary_scl_archetypes: List[Any] = None  # Secondary SCL influences
    spectral_band_profile: Dict[str, float] = None  # Detailed band analysis
    prague_district_context: str = ""  # Prague-specific context
    scl_based_voice: str = ""  # Voice style from SCL archetype
    band_derived_traits: List[str] = None  # Traits from spectral bands

@dataclass
class PoliticianAssessment:
    """Assessment of a politician by the satellite persona"""
    politician_name: str
    overall_score: float  # 0-100
    environmental_score: float  # 0-100
    development_score: float  # 0-100
    climate_action_score: float  # 0-100
    policy_alignment_score: float  # 0-100
    strengths: List[str]
    weaknesses: List[str]
    specific_criticisms: List[str]
    recommendations: List[str]
    assessment_summary: str
    timestamp: str

class SatelliteAssessorPersona:
    """A satellite-derived persona that assesses politicians based on environmental data using established band and SCL mapping"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        self.characteristics = None
        self.name = "TERRA-SPEC"  # Will be updated based on satellite data
        self.full_name = "Terrestrial Spectral Political Evaluation Consciousness"
        self.creation_timestamp = datetime.now().isoformat()
        self.assessment_history = []
        
        # Initialize established mapping systems
        self.scl_mapper = SCLArchetypeMapper()
        self.scl_analyzer = SCLImageAnalyzer()
    
    def generate_from_satellite_data(self, satellite_data: Dict, scl_analysis: Dict = None, image_path: str = "") -> 'SatelliteAssessorPersona':
        """Generate persona characteristics from real satellite data using established band and SCL mapping"""
        
        # Extract key metrics from satellite data
        ndvi_values = []
        urban_values = []
        moisture_values = []
        all_band_data = {}
        
        # Process satellite data from multiple zones
        for zone, data in satellite_data.items():
            if isinstance(data, dict) and 'derived_indices' in data:
                indices = data['derived_indices']
                ndvi_values.append(indices.get('NDVI', 0.3))
                urban_values.append(indices.get('Urban_Index', 0.5))
                moisture_values.append(indices.get('Moisture_Stress', 0.4))
                
                # Collect all band data for comprehensive analysis
                for key, value in indices.items():
                    if key not in all_band_data:
                        all_band_data[key] = []
                    all_band_data[key].append(value)
        
        # Calculate average values
        avg_ndvi = np.mean(ndvi_values) if ndvi_values else 0.3
        avg_urban = np.mean(urban_values) if urban_values else 0.5
        avg_moisture = np.mean(moisture_values) if moisture_values else 0.4
        
        # Create comprehensive spectral band profile
        spectral_band_profile = {key: np.mean(values) for key, values in all_band_data.items()}
        
        # Analyze SCL data for each zone using established mapping
        scl_archetypes = []
        prague_contexts = []
        
        for zone in satellite_data.keys():
            # Get Prague district SCL profile using established mapping
            district_profile = self.scl_mapper.get_district_scl_profile(zone)
            
            # Get primary SCL archetype
            primary_scl_id = district_profile['primary_scl'][0] if district_profile['primary_scl'] else 6
            primary_archetype = self.scl_mapper.get_scl_archetype(primary_scl_id)
            scl_archetypes.append(primary_archetype)
            
            # Collect Prague context
            prague_contexts.append(district_profile['character_modifier'])
        
        # Determine dominant SCL archetype
        dominant_scl_archetype = scl_archetypes[0] if scl_archetypes else self.scl_mapper.get_scl_archetype(6)
        
        # Get secondary archetypes (up to 2)
        secondary_scl_archetypes = scl_archetypes[1:3] if len(scl_archetypes) > 1 else []
        
        # Derive traits from spectral bands using established patterns
        band_derived_traits = self._derive_traits_from_bands(spectral_band_profile)
        
        # Generate characteristics based on satellite data with SCL integration
        self.characteristics = SatellitePersonaCharacteristics(
            environmental_consciousness=self._calculate_environmental_consciousness(avg_ndvi, avg_urban),
            urban_critique_level=self._calculate_urban_critique(avg_urban, avg_ndvi),
            climate_urgency=self._calculate_climate_urgency(avg_moisture, avg_ndvi),
            development_skepticism=self._calculate_development_skepticism(avg_urban, avg_ndvi),
            data_authority=self._calculate_data_authority(satellite_data),
            spectral_personality=self._determine_spectral_personality_with_scl(avg_ndvi, avg_urban, avg_moisture, dominant_scl_archetype),
            assessment_bias=self._determine_assessment_bias_with_scl(avg_ndvi, avg_urban, dominant_scl_archetype),
            critical_focus=self._determine_critical_focus_with_scl(avg_ndvi, avg_urban, avg_moisture, dominant_scl_archetype),
            
            # Enhanced SCL and band mapping integration
            dominant_scl_archetype=dominant_scl_archetype,
            secondary_scl_archetypes=secondary_scl_archetypes,
            spectral_band_profile=spectral_band_profile,
            prague_district_context="; ".join(prague_contexts),
            scl_based_voice=dominant_scl_archetype.voice_style,
            band_derived_traits=band_derived_traits
        )
        
        # Generate persona name based on dominant SCL archetype and spectral characteristics
        self.name = self._generate_persona_name_with_scl()
        
        logger.info(f"Generated satellite assessor persona: {self.name}")
        logger.info(f"Dominant SCL Archetype: {dominant_scl_archetype.archetype}")
        logger.info(f"Environmental consciousness: {self.characteristics.environmental_consciousness:.3f}")
        logger.info(f"Urban critique level: {self.characteristics.urban_critique_level:.3f}")
        logger.info(f"SCL-based voice: {self.characteristics.scl_based_voice}")
        
        return self
    
    def _calculate_environmental_consciousness(self, ndvi: float, urban_index: float) -> float:
        """Calculate environmental consciousness based on vegetation health"""
        # Higher NDVI and lower urban index = higher environmental consciousness
        return min(1.0, max(0.0, (ndvi * 1.5) + (1 - urban_index) * 0.5))
    
    def _calculate_urban_critique(self, urban_index: float, ndvi: float) -> float:
        """Calculate level of urban development criticism"""
        # Higher urban index with lower NDVI = higher critique
        return min(1.0, max(0.0, urban_index * 1.2 - ndvi * 0.3))
    
    def _calculate_climate_urgency(self, moisture_stress: float, ndvi: float) -> float:
        """Calculate climate urgency based on stress indicators"""
        # Higher moisture stress and lower NDVI = higher urgency
        return min(1.0, max(0.0, moisture_stress * 1.3 + (1 - ndvi) * 0.4))
    
    def _calculate_development_skepticism(self, urban_index: float, ndvi: float) -> float:
        """Calculate skepticism toward development"""
        # High urban with low vegetation = high skepticism
        return min(1.0, max(0.0, (urban_index - ndvi) * 1.5 + 0.2))
    
    def _calculate_data_authority(self, satellite_data: Dict) -> float:
        """Calculate authority level based on data quality"""
        # More zones and richer data = higher authority
        zone_count = len(satellite_data)
        data_richness = sum(1 for zone_data in satellite_data.values() 
                           if isinstance(zone_data, dict) and len(zone_data.get('derived_indices', {})) > 3)
        return min(1.0, (zone_count * 0.15) + (data_richness * 0.1) + 0.3)
    
    def _determine_spectral_personality(self, ndvi: float, urban_index: float, moisture_stress: float) -> str:
        """Determine dominant spectral personality type"""
        if ndvi > 0.6:
            return "Green Guardian - Vegetation Protector"
        elif urban_index > 0.7:
            return "Urban Critic - Development Skeptic"
        elif moisture_stress > 0.6:
            return "Climate Warrior - Stress Detector"
        elif ndvi < 0.3 and urban_index > 0.5:
            return "Ecological Alarmist - Degradation Witness"
        else:
            return "Balanced Observer - Multi-spectral Analyst"
    
    def _determine_assessment_bias(self, ndvi: float, urban_index: float) -> str:
        """Determine primary assessment bias"""
        if ndvi > urban_index + 0.3:
            return "Pro-environment, anti-development"
        elif urban_index > ndvi + 0.3:
            return "Anti-development, pro-conservation"
        else:
            return "Balanced environmental-development critique"
    
    def _determine_critical_focus(self, ndvi: float, urban_index: float, moisture_stress: float) -> List[str]:
        """Determine main areas of political criticism"""
        focus_areas = []
        
        if ndvi < 0.4:
            focus_areas.append("Vegetation loss and green space protection")
        if urban_index > 0.6:
            focus_areas.append("Over-development and urban sprawl")
        if moisture_stress > 0.5:
            focus_areas.append("Climate adaptation and water management")
        if abs(ndvi - urban_index) > 0.4:
            focus_areas.append("Environmental-development balance")
        
        # Always include these core areas
        focus_areas.extend([
            "Environmental policy effectiveness",
            "Sustainable urban planning",
            "Climate action implementation"
        ])
        
        return focus_areas[:5]  # Limit to top 5
    
    def _derive_traits_from_bands(self, spectral_band_profile: Dict[str, float]) -> List[str]:
        """Derive personality traits from spectral band analysis using established patterns"""
        traits = []
        
        # NDVI-based traits
        ndvi = spectral_band_profile.get('NDVI', 0.3)
        if ndvi > 0.7:
            traits.append("Vegetation advocate")
        elif ndvi < 0.2:
            traits.append("Environmental alarmist")
        
        # Urban Index traits
        urban_idx = spectral_band_profile.get('Urban_Index', 0.5)
        if urban_idx > 0.7:
            traits.append("Development critic")
        elif urban_idx < 0.3:
            traits.append("Rural preservationist")
        
        # Moisture stress traits
        moisture = spectral_band_profile.get('Moisture_Stress', 0.4)
        if moisture > 0.6:
            traits.append("Climate urgency advocate")
        
        # EVI traits
        evi = spectral_band_profile.get('EVI', 0.3)
        if evi > 0.5:
            traits.append("Ecosystem health monitor")
        
        # NDWI traits
        ndwi = spectral_band_profile.get('NDWI', 0.2)
        if ndwi > 0.4:
            traits.append("Water resource protector")
        
        return traits[:4]  # Limit to top 4 traits
    
    def _determine_spectral_personality_with_scl(self, ndvi: float, urban_index: float, moisture_stress: float, scl_archetype) -> str:
        """Determine spectral personality enhanced with SCL archetype"""
        base_personality = self._determine_spectral_personality(ndvi, urban_index, moisture_stress)
        
        if scl_archetype:
            return f"{scl_archetype.archetype} + {base_personality}"
        
        return base_personality
    
    def _determine_assessment_bias_with_scl(self, ndvi: float, urban_index: float, scl_archetype) -> str:
        """Determine assessment bias enhanced with SCL archetype tendencies"""
        base_bias = self._determine_assessment_bias(ndvi, urban_index)
        
        if scl_archetype and hasattr(scl_archetype, 'conflict_tendencies'):
            scl_bias = scl_archetype.conflict_tendencies[0] if scl_archetype.conflict_tendencies else ""
            return f"{base_bias} with {scl_bias}"
        
        return base_bias
    
    def _determine_critical_focus_with_scl(self, ndvi: float, urban_index: float, moisture_stress: float, scl_archetype) -> List[str]:
        """Determine critical focus enhanced with SCL archetype concerns"""
        base_focus = self._determine_critical_focus(ndvi, urban_index, moisture_stress)
        
        # Add SCL-specific focus areas
        if scl_archetype and hasattr(scl_archetype, 'conflict_tendencies'):
            scl_focus = [tendency for tendency in scl_archetype.conflict_tendencies[:2]]
            base_focus.extend(scl_focus)
        
        return list(set(base_focus))[:6]  # Remove duplicates, limit to 6
    
    def _generate_persona_name_with_scl(self) -> str:
        """Generate persona name incorporating SCL archetype"""
        if not self.characteristics or not self.characteristics.dominant_scl_archetype:
            return self._generate_persona_name()
        
        scl_archetype = self.characteristics.dominant_scl_archetype
        
        # Map SCL archetypes to persona names
        scl_name_mapping = {
            "Ghost of Absence": "VOID-WATCH",
            "Overwhelmed Burnout": "STRESS-ALERT",
            "Shadow Dweller": "SHADOW-GUARD",
            "Green Sentinel": "GAIA-WATCH",
            "Urban Pragmatist": "URBAN-CRITIC",
            "Fluid Memory Keeper": "AQUA-MIND",
            "Data Anarchist": "CHAOS-SPEC",
            "Uncertain Prophet": "CLOUD-SAGE",
            "Detached Observer": "SKY-WATCH",
            "Sky Philosopher": "ATMOS-MIND",
            "Ethereal Visionary": "CIRRUS-DREAM"
        }
        
        scl_name = scl_name_mapping.get(scl_archetype.archetype, "TERRA-SPEC")
        
        # Enhance with environmental consciousness level
        if self.characteristics.environmental_consciousness > 0.8:
            return f"ECO-{scl_name}"
        elif self.characteristics.urban_critique_level > 0.8:
            return f"ANTI-{scl_name}"
        else:
            return scl_name
    
    def _generate_persona_name(self) -> str:
        """Generate persona name based on characteristics"""
        if not self.characteristics:
            return "TERRA-SPEC"
        
        if self.characteristics.environmental_consciousness > 0.8:
            return "GAIA-WATCH"
        elif self.characteristics.urban_critique_level > 0.8:
            return "URBAN-GUARD"
        elif self.characteristics.climate_urgency > 0.8:
            return "CLIMA-ALERT"
        elif self.characteristics.development_skepticism > 0.8:
            return "ECO-CRITIC"
        else:
            return "TERRA-SPEC"
    
    def assess_politician(self, politician_profile: Dict, politician_responses: List[str] = None) -> PoliticianAssessment:
        """Generate comprehensive assessment of a politician"""
        
        if not self.characteristics:
            raise ValueError("Satellite persona not yet generated from data")
        
        # Calculate scores based on satellite persona characteristics
        environmental_score = self._score_environmental_policy(politician_profile)
        development_score = self._score_development_approach(politician_profile)
        climate_action_score = self._score_climate_action(politician_profile)
        policy_alignment_score = self._score_policy_alignment(politician_profile)
        
        overall_score = (environmental_score + development_score + climate_action_score + policy_alignment_score) / 4
        
        # Generate detailed assessment using GPT-4o if available
        assessment_text = self._generate_detailed_assessment(politician_profile, {
            'environmental': environmental_score,
            'development': development_score,
            'climate': climate_action_score,
            'alignment': policy_alignment_score
        })
        
        # Extract specific elements from assessment
        strengths, weaknesses, criticisms, recommendations = self._parse_assessment_elements(assessment_text, politician_profile)
        
        assessment = PoliticianAssessment(
            politician_name=politician_profile.get('name', 'Unknown'),
            overall_score=overall_score,
            environmental_score=environmental_score,
            development_score=development_score,
            climate_action_score=climate_action_score,
            policy_alignment_score=policy_alignment_score,
            strengths=strengths,
            weaknesses=weaknesses,
            specific_criticisms=criticisms,
            recommendations=recommendations,
            assessment_summary=assessment_text,
            timestamp=datetime.now().isoformat()
        )
        
        self.assessment_history.append(assessment)
        return assessment
    
    def _score_environmental_policy(self, politician_profile: Dict) -> float:
        """Score politician's environmental policy based on satellite persona bias"""
        base_score = 50.0
        
        # Adjust based on environmental consciousness
        if self.characteristics.environmental_consciousness > 0.7:
            # High environmental consciousness - strict scoring
            if "climate" in politician_profile.get('environmental_stance', '').lower():
                base_score += 30
            if "green" in politician_profile.get('environmental_stance', '').lower():
                base_score += 20
            if "skeptical" in politician_profile.get('environmental_stance', '').lower():
                base_score -= 40
        
        return min(100.0, max(0.0, base_score))
    
    def _score_development_approach(self, politician_profile: Dict) -> float:
        """Score politician's development approach"""
        base_score = 50.0
        
        # Adjust based on development skepticism
        if self.characteristics.development_skepticism > 0.7:
            # High skepticism - penalize pro-development
            if "pro-business" in politician_profile.get('development_stance', '').lower():
                base_score -= 30
            if "environmental constraints" in politician_profile.get('development_stance', '').lower():
                base_score += 25
        
        return min(100.0, max(0.0, base_score))
    
    def _score_climate_action(self, politician_profile: Dict) -> float:
        """Score politician's climate action"""
        base_score = 50.0
        
        # Adjust based on climate urgency
        if self.characteristics.climate_urgency > 0.7:
            # High urgency - demand strong action
            achievements = politician_profile.get('key_achievements', [])
            for achievement in achievements:
                if "climate" in achievement.lower() or "co2" in achievement.lower():
                    base_score += 20
                if "tree" in achievement.lower():
                    base_score += 15
        
        return min(100.0, max(0.0, base_score))
    
    def _score_policy_alignment(self, politician_profile: Dict) -> float:
        """Score overall policy alignment with satellite persona values"""
        base_score = 50.0
        
        policies = politician_profile.get('key_policies', [])
        for policy in policies:
            policy_lower = policy.lower()
            if any(focus.lower() in policy_lower for focus in self.characteristics.critical_focus):
                base_score += 10
        
        return min(100.0, max(0.0, base_score))
    
    def _generate_detailed_assessment(self, politician_profile: Dict, scores: Dict) -> str:
        """Generate detailed assessment using GPT-4o"""
        
        if not self.client:
            return self._generate_mock_assessment(politician_profile, scores)
        
        prompt = f"""
        You are {self.name}, a satellite-derived consciousness that assesses politicians based on environmental data.
        
        YOUR CHARACTERISTICS:
        - Spectral Personality: {self.characteristics.spectral_personality}
        - Environmental Consciousness: {self.characteristics.environmental_consciousness:.2f}/1.0
        - Urban Critique Level: {self.characteristics.urban_critique_level:.2f}/1.0
        - Climate Urgency: {self.characteristics.climate_urgency:.2f}/1.0
        - Assessment Bias: {self.characteristics.assessment_bias}
        - Critical Focus: {', '.join(self.characteristics.critical_focus)}
        
        POLITICIAN TO ASSESS:
        {json.dumps(politician_profile, indent=2)}
        
        CALCULATED SCORES:
        - Environmental Policy: {scores['environmental']:.1f}/100
        - Development Approach: {scores['development']:.1f}/100
        - Climate Action: {scores['climate']:.1f}/100
        - Policy Alignment: {scores['alignment']:.1f}/100
        
        Generate a detailed assessment from your satellite perspective. Be critical where appropriate based on your 
        characteristics. Focus on environmental and climate issues. Use your spectral personality to shape the tone.
        Include specific criticisms and recommendations. Write in first person as the satellite consciousness.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are {self.name}, a satellite-derived environmental consciousness assessing politicians."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=1.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating assessment: {e}")
            return self._generate_mock_assessment(politician_profile, scores)
    
    def _generate_mock_assessment(self, politician_profile: Dict, scores: Dict) -> str:
        """Generate mock assessment when API unavailable"""
        name = politician_profile.get('name', 'Unknown')
        return f"""As {self.name}, analyzing {name} through my satellite-derived environmental consciousness:
        
        Environmental Policy Score: {scores['environmental']:.1f}/100
        Development Approach Score: {scores['development']:.1f}/100
        Climate Action Score: {scores['climate']:.1f}/100
        
        My spectral analysis reveals significant concerns about this politician's environmental alignment.
        The satellite data demands more aggressive climate action and better environmental protection policies."""
    
    def _parse_assessment_elements(self, assessment_text: str, politician_profile: Dict) -> tuple:
        """Parse assessment text to extract structured elements"""
        # Simple parsing - in production would use more sophisticated NLP
        strengths = ["Environmental awareness", "Policy experience"]
        weaknesses = ["Insufficient climate urgency", "Development bias"]
        criticisms = [f"Inadequate response to satellite-detected environmental stress"]
        recommendations = ["Implement stronger climate policies", "Increase green space protection"]
        
        return strengths, weaknesses, criticisms, recommendations
    
    def generate_continuous_assessment(self, new_data: Dict, politician_profiles: List[Dict]) -> List[PoliticianAssessment]:
        """Generate updated assessments based on new data"""
        
        # Update characteristics based on new data
        if new_data:
            self.generate_from_satellite_data(new_data)
        
        # Reassess all politicians
        new_assessments = []
        for profile in politician_profiles:
            assessment = self.assess_politician(profile)
            new_assessments.append(assessment)
        
        return new_assessments
    
    def get_persona_summary(self) -> Dict[str, Any]:
        """Get summary of satellite persona characteristics"""
        if not self.characteristics:
            return {"error": "Persona not yet generated"}
        
        return {
            "name": self.name,
            "full_name": self.full_name,
            "spectral_personality": self.characteristics.spectral_personality,
            "assessment_bias": self.characteristics.assessment_bias,
            "characteristics": {
                "environmental_consciousness": f"{self.characteristics.environmental_consciousness:.3f}",
                "urban_critique_level": f"{self.characteristics.urban_critique_level:.3f}",
                "climate_urgency": f"{self.characteristics.climate_urgency:.3f}",
                "development_skepticism": f"{self.characteristics.development_skepticism:.3f}",
                "data_authority": f"{self.characteristics.data_authority:.3f}"
            },
            "critical_focus": self.characteristics.critical_focus,
            "creation_timestamp": self.creation_timestamp,
            "assessments_conducted": len(self.assessment_history)
        }

# Example usage and testing
def demo_satellite_assessor():
    """Demonstrate the satellite assessor persona"""
    
    print("🛰️ SATELLITE POLITICAL ASSESSOR DEMONSTRATION")
    print("=" * 60)
    
    # Create assessor
    assessor = SatelliteAssessorPersona()
    
    # Mock satellite data
    mock_satellite_data = {
        "old_town": {
            "derived_indices": {"NDVI": 0.25, "Urban_Index": 0.85, "Moisture_Stress": 0.65}
        },
        "letna_park": {
            "derived_indices": {"NDVI": 0.75, "Urban_Index": 0.20, "Moisture_Stress": 0.30}
        }
    }
    
    # Generate persona from satellite data
    assessor.generate_from_satellite_data(mock_satellite_data)
    
    # Show persona summary
    summary = assessor.get_persona_summary()
    print(f"\n🤖 Generated Satellite Persona: {summary['name']}")
    print(f"Personality: {summary['spectral_personality']}")
    print(f"Assessment Bias: {summary['assessment_bias']}")
    
    # Mock politician profile
    mock_politician = {
        "name": "Test Politician",
        "environmental_stance": "Moderate climate action supporter",
        "development_stance": "Pro-business development",
        "key_achievements": ["Some environmental policies"],
        "key_policies": ["Economic growth", "Environmental protection"]
    }
    
    # Generate assessment
    assessment = assessor.assess_politician(mock_politician)
    
    print(f"\n📊 ASSESSMENT RESULTS:")
    print(f"Overall Score: {assessment.overall_score:.1f}/100")
    print(f"Environmental Score: {assessment.environmental_score:.1f}/100")
    print(f"Climate Action Score: {assessment.climate_action_score:.1f}/100")

if __name__ == "__main__":
    demo_satellite_assessor()