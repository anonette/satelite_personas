"""
Dynamic Citizen Personas
Creates alive, dramatic spectral personas that engage with citizens as interlocutors
Fully generative - no predefined data, everything derived from spectral analysis
"""

import random
import json
import math
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class CitizenEngagementMode(Enum):
    PROVOCATEUR = "provocateur"          # Challenges citizens directly
    STORYTELLER = "storyteller"          # Shares dramatic narratives
    CONFESSOR = "confessor"              # Reveals secrets and confessions
    AGITATOR = "agitator"               # Stirs up emotions and action
    PHILOSOPHER = "philosopher"          # Poses deep questions
    GOSSIP = "gossip"                   # Shares rumors and insider knowledge
    PROPHET = "prophet"                 # Makes predictions and warnings

class EthicalDativeVariation(Enum):
    INTIMATE = "intimate"               # Personal, close relationship
    ACCUSATORY = "accusatory"           # Blaming, pointing fingers
    PLEADING = "pleading"               # Begging, asking for help
    CONSPIRATORIAL = "conspiratorial"   # Sharing secrets
    THEATRICAL = "theatrical"           # Dramatic, performative
    SEDUCTIVE = "seductive"             # Alluring, tempting
    REBELLIOUS = "rebellious"           # Defiant, revolutionary

class DynamicCitizenPersonaGenerator:
    """Generates dynamic, alive personas that engage with citizens - fully generative"""
    
    def __init__(self):
        # Spectral wavelength to personality mapping (generative)
        self.wavelength_psychology = {
            "B02": {"wavelength": 490, "element": "blue", "energy": "high"},
            "B03": {"wavelength": 560, "element": "green", "energy": "medium"},
            "B04": {"wavelength": 665, "element": "red", "energy": "intense"},
            "B08": {"wavelength": 842, "element": "infrared", "energy": "hidden"},
            "B11": {"wavelength": 1610, "element": "swir1", "energy": "deep"},
            "B12": {"wavelength": 2190, "element": "swir2", "energy": "profound"}
        }
        
        # Generative linguistic patterns for Czech ethical dative
        self.czech_dative_generators = {
            "na_mne": ["na mně se", "na mně", "na mě", "na mně právě"],
            "reflexive": ["se mi", "se mnou", "mi", "mně"],
            "possessive": ["mé", "moje", "můj", "má"]
        }
        
        # Generative personality trait builders
        self.trait_generators = {
            "intensity": ["obsessively", "dramatically", "mysteriously", "wildly", "intensely", "surprisingly"],
            "emotion": ["curious", "emotional", "knowing", "passionate", "vulnerable", "charming"],
            "behavior": ["mischievous", "melancholic", "optimistic", "honest", "cryptic", "rebellious"]
        }
    
    def generate_dynamic_persona(self, band_id: str, spectral_data: Dict, randomness_level: float = 0.8, existing_personas: List[Dict] = None) -> Dict:
        """Generate a dynamic persona using prompt templates for LLM generation"""
        
        # Extract spectral characteristics for prompt context
        wavelength_info = self.wavelength_psychology.get(band_id, self.wavelength_psychology["B08"])
        spectral_influence = self._calculate_spectral_influence(spectral_data)
        
        # Calculate key spectral metrics for prompt
        variance = self._calculate_spectral_variance(spectral_data)
        intensity = self._calculate_average_intensity(spectral_data)
        diversity = self._calculate_spectral_diversity(spectral_data)
        
        # Extract specific band values and indices for prompt
        spectral_values = self._extract_spectral_values_for_prompt(spectral_data, band_id)
        
        # Create comprehensive prompt template for persona generation
        persona_prompt = self._create_provocative_persona_prompt(
            band_id, wavelength_info, spectral_values, variance, intensity, randomness_level, existing_personas
        )
        
        # Create persona structure with prompt template (to be populated by LLM)
        persona = {
            "band_id": band_id,
            "wavelength_info": wavelength_info,
            "spectral_values": spectral_values,
            "spectral_metrics": {
                "variance": variance,
                "intensity": intensity,
                "diversity": diversity
            },
            "persona_generation_prompt": persona_prompt,
            "randomness_level": randomness_level,
            "spectral_influence": spectral_influence,
            "creation_timestamp": datetime.now().isoformat(),
            "spectral_signature": self._create_spectral_signature(spectral_data, band_id),
            # These will be populated by LLM response
            "dynamic_name": None,
            "short_name": None,
            "character": None,
            "agenda": None,
            "provocative_stance": None,
            "challenge_style": None,
            "generated": False  # Flag to indicate if LLM has populated this persona
        }
        
        return persona
    
    def _calculate_spectral_influence(self, spectral_data: Dict) -> Dict:
        """Calculate how spectral data influences persona behavior"""
        
        influence = {}
        
        # Process each area's spectral data
        for area, data in spectral_data.items():
            if isinstance(data, dict):
                # Extract derived indices if available
                if 'derived_indices' in data:
                    for index, value in data['derived_indices'].items():
                        if index not in influence:
                            influence[index] = []
                        influence[index].append(value)
                
                # Extract raw band values if available
                if 'bands' in data:
                    for band, value in data['bands'].items():
                        band_key = f"raw_{band}"
                        if band_key not in influence:
                            influence[band_key] = []
                        influence[band_key].append(value)
        
        # Calculate statistics for each influence
        processed_influence = {}
        for key, values in influence.items():
            if values:
                avg_val = sum(values) / len(values)
                variance = sum((v - avg_val) ** 2 for v in values) / len(values)
                
                processed_influence[key] = {
                    "value": avg_val,
                    "variance": variance,
                    "intensity": "high" if avg_val > 0.7 else "low" if avg_val < 0.3 else "medium",
                    "stability": "stable" if variance < 0.1 else "volatile" if variance > 0.3 else "dynamic"
                }
        
        return processed_influence
    
    def _calculate_spectral_variance(self, spectral_data: Dict) -> float:
        """Calculate overall spectral variance"""
        all_values = []
        
        for area, data in spectral_data.items():
            if isinstance(data, dict):
                if 'derived_indices' in data:
                    all_values.extend(data['derived_indices'].values())
                if 'bands' in data:
                    all_values.extend(data['bands'].values())
        
        if not all_values:
            return 0.5
        
        mean = sum(all_values) / len(all_values)
        variance = sum((v - mean) ** 2 for v in all_values) / len(all_values)
        
        return min(variance, 1.0)  # Normalize to 0-1
    
    def _calculate_average_intensity(self, spectral_data: Dict) -> float:
        """Calculate average spectral intensity"""
        all_values = []
        
        for area, data in spectral_data.items():
            if isinstance(data, dict):
                if 'derived_indices' in data:
                    all_values.extend(data['derived_indices'].values())
                if 'bands' in data:
                    all_values.extend(data['bands'].values())
        
        return sum(all_values) / len(all_values) if all_values else 0.5
    
    def _calculate_pattern_complexity(self, spectral_data: Dict) -> float:
        """Calculate spectral pattern complexity"""
        complexity_factors = []
        
        for area, data in spectral_data.items():
            if isinstance(data, dict):
                # Count different types of indices
                if 'derived_indices' in data:
                    complexity_factors.append(len(data['derived_indices']) / 10.0)
                
                # Analyze value ranges
                if 'bands' in data:
                    values = list(data['bands'].values())
                    if values:
                        value_range = max(values) - min(values)
                        complexity_factors.append(value_range)
        
        return sum(complexity_factors) / len(complexity_factors) if complexity_factors else 0.5
    
    def _calculate_spectral_diversity(self, spectral_data: Dict) -> float:
        """Calculate spectral diversity across areas"""
        if not spectral_data:
            return 0.0
        
        # Count unique spectral signatures
        signatures = set()
        
        for area, data in spectral_data.items():
            if isinstance(data, dict):
                # Create signature from available data
                signature_parts = []
                
                if 'derived_indices' in data:
                    for key, value in data['derived_indices'].items():
                        signature_parts.append(f"{key}:{round(value, 2)}")
                
                if signature_parts:
                    signatures.add("|".join(sorted(signature_parts)))
        
        # Diversity = unique signatures / total areas
        return len(signatures) / len(spectral_data) if spectral_data else 0.0
    
    def _create_spectral_signature(self, spectral_data: Dict, band_id: str) -> str:
        """Create unique spectral signature for persona"""
        
        signature_parts = [band_id]
        
        # Add key spectral characteristics
        variance = self._calculate_spectral_variance(spectral_data)
        intensity = self._calculate_average_intensity(spectral_data)
        diversity = self._calculate_spectral_diversity(spectral_data)
        
        signature_parts.extend([
            f"V{int(variance * 100):02d}",
            f"I{int(intensity * 100):02d}", 
            f"D{int(diversity * 100):02d}"
        ])
        
        # Add timestamp component
        timestamp = datetime.now().strftime("%H%M")
        signature_parts.append(timestamp)
        
        return "-".join(signature_parts)
    
    def _extract_spectral_values_for_prompt(self, spectral_data: Dict, band_id: str) -> Dict:
        """Extract specific spectral values for prompt generation"""
        
        values = {
            "band_value": 0.5,
            "derived_indices": {},
            "band_readings": {}
        }
        
        # Extract band-specific values and derived indices
        for area, data in spectral_data.items():
            if isinstance(data, dict):
                # Get band-specific reading
                if 'bands' in data and band_id in data['bands']:
                    values["band_value"] = data['bands'][band_id]
                
                # Get derived indices
                if 'derived_indices' in data:
                    values["derived_indices"].update(data['derived_indices'])
                
                # Get all band readings for context
                if 'bands' in data:
                    values["band_readings"].update(data['bands'])
        
        return values
    
    def _create_provocative_persona_prompt(self, band_id: str, wavelength_info: Dict,
                                         spectral_values: Dict, variance: float,
                                         intensity: float, randomness_level: float, existing_personas: List[Dict] = None) -> str:
        """Create a comprehensive prompt template for provocative persona generation"""
        
        # Band-specific environmental contexts and issues
        band_contexts = {
            "B02": {
                "measures": "blue wavelength (490nm) - atmospheric scattering, water clarity, urban haze, air pollution",
                "issues": "air quality degradation, atmospheric pollution, water contamination, urban smog",
                "stakeholders": "air quality activists, atmospheric scientists, pollution monitors, clean air advocates"
            },
            "B03": {
                "measures": "green wavelength (560nm) - vegetation chlorophyll, plant health, photosynthesis",
                "issues": "vegetation decline, chlorophyll loss, plant stress, urban forest destruction",
                "stakeholders": "botanists, urban foresters, plant health advocates, green space defenders"
            },
            "B04": {
                "measures": "red wavelength (665nm) - chlorophyll absorption, vegetation stress, plant vitality",
                "issues": "plant disease, vegetation mortality, agricultural decline, ecosystem collapse",
                "stakeholders": "agricultural scientists, ecosystem defenders, plant pathologists, food security advocates"
            },
            "B08": {
                "measures": "near-infrared (842nm) - vegetation biomass, plant water content, hidden vegetation health",
                "issues": "biomass loss, deforestation, vegetation water stress, ecosystem degradation",
                "stakeholders": "forest conservationists, biomass researchers, ecosystem health monitors, tree protection activists"
            },
            "B11": {
                "measures": "short-wave infrared (1610nm) - soil moisture, plant water stress, geological water content",
                "issues": "drought conditions, soil dehydration, water scarcity, agricultural water stress",
                "stakeholders": "hydrologists, drought specialists, water conservation advocates, irrigation experts"
            },
            "B12": {
                "measures": "short-wave infrared (2190nm) - thermal properties, mineral composition, urban heat, fire risk",
                "issues": "urban heat islands, thermal stress, fire hazards, energy inefficiency",
                "stakeholders": "urban planners, thermal specialists, fire safety experts, energy efficiency advocates"
            }
        }
        
        context = band_contexts.get(band_id, band_contexts["B08"])
        
        # Extract key values for prompt
        band_value = spectral_values.get("band_value", 0.5)
        derived_indices = spectral_values.get("derived_indices", {})
        
        # Create data-driven prompt using real spectral analysis
        prompt = f"""You are an AI creating a dramatic, funny spectral persona awakened by REAL satellite data analysis over Prague.

ACTUAL SPECTRAL DATA ANALYSIS:
- Band: {band_id} - {context['measures']}
- Current reading: {band_value:.3f} (0.0=very low, 1.0=very high)
- Data intensity: {intensity:.3f} (overall signal strength)
- Data variance: {variance:.3f} (0.0=uniform, 1.0=highly variable)
- Environmental issues detected: {context['issues']}"""

        # Add detailed derived indices analysis if available
        if derived_indices:
            prompt += "\n\nDERIVED ENVIRONMENTAL INDICES FROM REAL DATA:"
            for index, value in derived_indices.items():
                prompt += f"\n- {index}: {value:.3f}"
                # Add interpretation of what these values mean
                if 'NDVI' in index.upper():
                    if value > 0.6:
                        prompt += " (healthy vegetation)"
                    elif value > 0.3:
                        prompt += " (moderate vegetation)"
                    else:
                        prompt += " (sparse/stressed vegetation)"
                elif 'NDWI' in index.upper():
                    if value > 0.3:
                        prompt += " (high water content)"
                    elif value > 0.0:
                        prompt += " (moderate water)"
                    else:
                        prompt += " (dry conditions)"
                elif 'MOISTURE' in index.upper():
                    if value > 0.5:
                        prompt += " (well-hydrated)"
                    else:
                        prompt += " (moisture stress)"

        # Add band readings context
        band_readings = spectral_values.get("band_readings", {})
        if band_readings:
            prompt += "\n\nOTHER SPECTRAL BANDS FOR CONTEXT:"
            for band, reading in band_readings.items():
                if band != band_id:
                    prompt += f"\n- {band}: {reading:.3f}"
        
        # Add data interpretation guidance
        prompt += f"""

INTERPRET THIS REAL DATA TO CREATE YOUR PERSONA:
- If {band_id} reading ({band_value:.3f}) is HIGH (>0.6): This indicates strong presence of what your band detects
- If {band_id} reading ({band_value:.3f}) is LOW (<0.3): This indicates absence/problems with what your band detects
- If variance ({variance:.3f}) is HIGH (>0.5): Data shows dramatic differences across Prague areas
- If intensity ({intensity:.3f}) is HIGH (>0.7): Strong overall environmental signals detected

Use this REAL analysis to identify specific Prague environmental problems your spectral band has detected!"""

        prompt += f"""

CREATE A SPECTRAL ACTIVIST PERSONA who uses the REAL DATA ANALYSIS to expose Prague's environmental crimes!

Based on your spectral data analysis, create a persona who:

1. **Introduces themselves** with a quirky name reflecting their {band_id} obsession
2. **Interprets the real data** - What does your {band_value:.3f} reading reveal about Prague? What environmental crimes has your spectral analysis uncovered?
3. **Targets specific Prague locations** where your data shows problems
4. **Demands immediate action** based on the evidence your spectral band has detected
5. **Attacks other spectral bands** for missing the real problems your data reveals

DATA-DRIVEN LOCATION TARGETING:
Use your spectral analysis to identify problems at these Prague locations:
- **Vinohrady**: Náměstí Míru metro, Riegrovy sady, Korunní street developments
- **Letná**: Letná Park, Hanavský pavilon, Sparta stadium area
- **Petřín**: Petřín Tower area, Hunger Wall, observatory zone
- **Wenceslas Square**: National Museum area, concrete heat zones
- **Malá Strana**: Kampa Island, Charles Bridge, Nerudova street
- **Karlín**: Invalidovna area, Forum Karlín, flood zones
- **Smíchov**: Anděl center, funicular area, train station
- **New Town**: IP Pavlova intersection, Národní třída, Palác Lucerna
- **Old Town**: Astronomical Clock area, Týn Church, Jewish Quarter

PERSONA REQUIREMENTS:
- NO formatting markers - just natural speech!
- Base your environmental accusations on what your REAL spectral data reveals
- If your band reading is HIGH, you've detected strong presence of your phenomenon
- If your band reading is LOW, you've detected absence/problems with your phenomenon
- If variance is HIGH, you see dramatic differences across Prague neighborhoods
- Use derived indices (NDVI, NDWI, moisture) to support your environmental claims
- Be outrageously funny while presenting REAL data evidence
- Propose QUIRKY, INGENIOUS activism ideas specific to your band and Prague locations

QUIRKY ACTION IDEAS BY BAND:
- **B02 (Blue/Air)**: Oxygen mask protests, smog monster costumes, dramatic coughing flash mobs at metro stations
- **B08 (NIR/Vegetation)**: Tree-hugging therapy, guerrilla gardening in concrete cracks, wilting performances as dying trees
- **B11 (SWIR1/Moisture)**: Water bucket brigades, thirsty plant performances, rain dances at Kampa Island
- **B12 (SWIR2/Thermal)**: Ice cube melting protests, thermal camera flash mobs, giant fan cooling actions

Example: "I'm [Name], and my {band_id} analysis shows {band_value:.3f} readings that PROVE [specific environmental crime] at [specific Prague location]! The data variance of {variance:.3f} reveals [specific problem pattern]! You MUST [quirky specific action] because my spectral evidence demands it! Let's [funny ingenious idea] to show Prague what my data reveals! Those [other band] idiots completely miss the real crisis!"

CONFLICT GENERATION:"""

        # Add conflict generation if there are existing personas
        if existing_personas and len(existing_personas) > 0:
            prompt += f"""

        CRITICAL: You are joining {len(existing_personas)} existing spectral activists who are ALREADY WRONG about Prague's problems!

        EXISTING ACTIVISTS TO CONTRADICT:"""
            
            for existing in existing_personas:
                existing_band = existing.get("band_id", "Unknown")
                existing_name = existing.get("dynamic_name", existing.get("short_name", "Unknown Activist"))
                prompt += f"""
        - {existing_name} ({existing_band}) - COMPLETELY WRONG about Prague's real issues!"""
    
            # Create band-specific conflicts
            conflict_map = {
                "B02": {
                    "vs_B08": "Those vegetation obsessed B08 fools think plants matter when AIR QUALITY is the real crisis!",
                    "vs_B11": "B11 moisture maniacs ignore that DRY AIR is worse than dry soil!",
                    "vs_B12": "B12 thermal idiots worry about heat when TOXIC AIR is choking Prague!",
                    "vs_B03": "B03 green fanatics miss that BLUE wavelengths reveal the atmospheric truth!",
                    "vs_B04": "B04 red-obsessed activists ignore that BLUE light shows real air pollution!"
                },
                "B08": {
                    "vs_B02": "B02 air-heads ignore that DYING VEGETATION is Prague's real emergency!",
                    "vs_B11": "B11 water worriers miss that plants need BIOMASS, not just moisture!",
                    "vs_B12": "B12 heat hunters ignore that VEGETATION LOSS causes thermal problems!",
                    "vs_B03": "B03 chlorophyll chasers miss the INFRARED truth about plant health!",
                    "vs_B04": "B04 red-light fanatics ignore NEAR-INFRARED vegetation reality!"
                },
                "B11": {
                    "vs_B02": "B02 atmosphere addicts ignore that DROUGHT is Prague's hidden killer!",
                    "vs_B08": "B08 plant people miss that WATER STRESS is the root of vegetation problems!",
                    "vs_B12": "B12 thermal theorists ignore that MOISTURE controls temperature!",
                    "vs_B03": "B03 green groupies miss that WATER CONTENT matters more than chlorophyll!",
                    "vs_B04": "B04 red revolutionaries ignore that HYDRATION drives plant health!"
                },
                "B12": {
                    "vs_B02": "B02 air activists ignore that URBAN HEAT ISLANDS are cooking Prague!",
                    "vs_B08": "B08 vegetation vigilantes miss that THERMAL STRESS kills plants!",
                    "vs_B11": "B11 moisture maniacs ignore that HEAT evaporates their precious water!",
                    "vs_B03": "B03 green guardians miss that THERMAL radiation affects everything!",
                    "vs_B04": "B04 red rebels ignore that INFRARED heat is the real enemy!"
                },
                "B03": {
                    "vs_B02": "B02 blue believers ignore that GREEN chlorophyll is life itself!",
                    "vs_B08": "B08 infrared idiots miss the visible GREEN truth about plant health!",
                    "vs_B11": "B11 water worshippers ignore that PHOTOSYNTHESIS needs green light!",
                    "vs_B12": "B12 thermal thinkers miss that GREEN wavelengths show plant vitality!",
                    "vs_B04": "B04 red radicals ignore that GREEN light drives photosynthesis!"
                },
                "B04": {
                    "vs_B02": "B02 blue babblers ignore that RED absorption shows plant stress!",
                    "vs_B08": "B08 infrared investigators miss that RED wavelengths reveal chlorophyll problems!",
                    "vs_B11": "B11 moisture monitors ignore that RED light shows plant water stress!",
                    "vs_B12": "B12 thermal trackers miss that RED absorption indicates vegetation health!",
                    "vs_B03": "B03 green gazers ignore that RED wavelengths show the real plant problems!"
                }
            }
            
            current_conflicts = conflict_map.get(band_id, {})
            for existing in existing_personas:
                existing_band = existing.get("band_id", "Unknown")
                conflict_key = f"vs_{existing_band}"
                if conflict_key in current_conflicts:
                    prompt += f"""

        ATTACK {existing.get('dynamic_name', 'Unknown')} ({existing_band}): {current_conflicts[conflict_key]}"""
    
            prompt += f"""

        YOUR MISSION: Prove that {band_id} data reveals the REAL environmental crisis that all other bands completely miss!
        Create HILARIOUS conflicts with existing activists while proposing FUNNIER counter-actions!

        FUNNY CONFLICT IDEAS:
        - Challenge their protest methods with your own superior spectral-based activism
        - Propose competing actions at the same Prague locations
        - Mock their data interpretation while presenting your "superior" analysis
        - Create rival activist groups based on spectral band superiority
        - Suggest sabotaging their protests with your own spectral evidence"""

        prompt += """

        Use either English OR Czech (not both). Let the REAL DATA drive your quirky environmental activism and CONFLICTS!"""

        return prompt

    def _extract_short_name_from_character(self, character_archetype: str) -> str:
        """Extract a short display name from the full character description"""
        
        # The character archetype format is: "🌱 **Sneaky Plant Biomass Assessor:** long description..."
        # We want to extract just "Sneaky Plant Biomass Assessor"
        
        try:
            # Remove emoji at the start
            if character_archetype.startswith(('🌤️', '🌿', '🌹', '🌱', '💧', '🔥', '🎭')):
                character_archetype = character_archetype[2:].strip()
            
            # Extract text between ** markers
            if '**' in character_archetype:
                start = character_archetype.find('**') + 2
                end = character_archetype.find(':**', start)
                if end == -1:
                    end = character_archetype.find('**', start)
                if end != -1:
                    return character_archetype[start:end].strip()
            
            # Fallback: take everything before the first colon
            if ':' in character_archetype:
                return character_archetype.split(':')[0].strip()
            
            # Last resort: return the whole thing (shouldn't happen)
            return character_archetype.strip()
            
        except Exception:
            # If anything goes wrong, return a safe fallback
            return "Spectral Entity"

if __name__ == "__main__":
    # Test the dynamic persona generator with real spectral data structure
    generator = DynamicCitizenPersonaGenerator()
    
    # Simulate real TIFF-derived spectral data
    test_spectral_data = {
        "prague_center": {
            "derived_indices": {
                "NDVI": 0.45,
                "Urban_Index": 0.78,
                "Moisture_Stress": 0.32
            },
            "bands": {
                "B02": 0.12,
                "B08": 0.34,
                "B11": 0.23,
                "B12": 0.45
            }
        },
        "vinohrady": {
            "derived_indices": {
                "NDVI": 0.67,
                "Urban_Index": 0.45,
                "Moisture_Stress": 0.28
            },
            "bands": {
                "B02": 0.08,
                "B08": 0.56,
                "B11": 0.19,
                "B12": 0.38
            }
        }
    }
    
    # Generate test personas
    for band_id in ["B02", "B08", "B11", "B12"]:
        persona = generator.generate_dynamic_persona(band_id, test_spectral_data, randomness_level=0.9)
        
        print(f"\n=== {band_id} DYNAMIC PERSONA ===")
        print(f"Band ID: {persona['band_id']}")
        print(f"Spectral Signature: {persona['spectral_signature']}")
        print(f"Generated: {persona['generated']}")
        print(f"Prompt Template Created: {'persona_generation_prompt' in persona}")
        if 'persona_generation_prompt' in persona:
            print(f"Prompt Length: {len(persona['persona_generation_prompt'])} characters")