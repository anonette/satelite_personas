"""
Arendtian Philosophical Persona Generator
Enhanced for Civic Ensemble Generation and Political Spectral Dynamics
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
class ArendtianPersona:
    """A civic persona based on Arendtian philosophy"""
    name: str
    dominant_band: str
    persona_type: str
    voice: str
    utterance: str
    arendtian_mode: str
    civic_role: str = "citizen"  # "citizen", "assemblies_member", "witness", "mediator"
    political_stance: str = "engaged"  # "engaged", "withdrawn", "conflicted"
    temporal_presence: str = "stable"  # "stable", "emerging", "fading"

@dataclass
class CivicAssembly:
    """A collection of Arendtian personas forming a civic assembly"""
    location: Dict[str, float]
    date: str
    plurality_leader: ArendtianPersona  # Dominant voice
    dissenting_voice: ArendtianPersona  # Opposition
    mediating_presence: ArendtianPersona  # Bridge-builder
    spectral_witnesses: List[ArendtianPersona]  # Additional voices
    assembly_dynamics: str
    public_tension: str
    citizen_participation: str

class ArendtianPersonaGenerator:
    """Generator for Arendtian civic ensembles and political assemblies"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        # Enhanced spectral archetypes integrated with real image metadata
        self.spectral_archetypes = {
            # NDVI-based vegetation archetypes
            "NDVI": {
                "high": {
                    "archetype": "Verdant Guardian",
                    "personality": "Protective, nurturing, growth-focused",
                    "civic_function": "Green space advocacy and biodiversity protection",
                    "voice_style": "Speaks with organic wisdom and seasonal rhythms",
                    "conflict_triggers": ["deforestation", "concrete expansion", "pollution"],
                    "image_signature": "Dense green canopy, high chlorophyll activity"
                },
                "medium": {
                    "archetype": "Urban Gardener", 
                    "personality": "Pragmatic, adaptive, community-oriented",
                    "civic_function": "Balancing development with green infrastructure",
                    "voice_style": "Practical solutions with environmental awareness",
                    "conflict_triggers": ["over-development", "neglected parks", "air quality"],
                    "image_signature": "Mixed vegetation and urban areas, moderate green"
                },
                "low": {
                    "archetype": "Concrete Realist",
                    "personality": "Direct, efficiency-focused, development-oriented", 
                    "civic_function": "Urban infrastructure and economic development",
                    "voice_style": "Straightforward, results-driven, pragmatic",
                    "conflict_triggers": ["environmental restrictions", "slow permits", "green regulations"],
                    "image_signature": "Minimal vegetation, urban surfaces, built environment"
                }
            },
            
            # Moisture/Water-based archetypes
            "Moisture_Stress": {
                "low": {
                    "archetype": "Hydro Optimist",
                    "personality": "Flowing, adaptive, life-sustaining",
                    "civic_function": "Water resource management and flood resilience", 
                    "voice_style": "Fluid thinking, long-term sustainability focus",
                    "conflict_triggers": ["water waste", "poor drainage", "river pollution"],
                    "image_signature": "Well-watered areas, healthy moisture levels"
                },
                "high": {
                    "archetype": "Drought Warrior",
                    "personality": "Urgent, conservation-minded, crisis-aware",
                    "civic_function": "Water conservation and climate adaptation",
                    "voice_style": "Urgent warnings about resource scarcity",
                    "conflict_triggers": ["water waste", "climate denial", "poor planning"],
                    "image_signature": "Dry areas, stressed vegetation, low moisture"
                }
            },
            
            # Urban Index archetypes
            "Urban_Index": {
                "high": {
                    "archetype": "Metropolitan Maximizer",
                    "personality": "Ambitious, density-focused, efficiency-driven",
                    "civic_function": "Urban planning and infrastructure optimization",
                    "voice_style": "Fast-paced, solution-oriented, growth-minded",
                    "conflict_triggers": ["sprawl", "inefficiency", "under-development"],
                    "image_signature": "Dense urban development, high built-up areas"
                },
                "low": {
                    "archetype": "Natural Preservationist", 
                    "personality": "Conservation-minded, tradition-focused, slow-change",
                    "civic_function": "Heritage preservation and natural area protection",
                    "voice_style": "Thoughtful, historically-aware, cautious",
                    "conflict_triggers": ["rapid development", "heritage destruction", "gentrification"],
                    "image_signature": "Natural areas, low development, preserved landscapes"
                }
            },
            
            # False Color/Visual archetypes based on image analysis
            "False_Color": {
                "vibrant": {
                    "archetype": "Spectral Visionary",
                    "personality": "Creative, pattern-recognizing, future-seeing",
                    "civic_function": "Innovation and creative urban solutions",
                    "voice_style": "Imaginative, sees hidden connections and possibilities",
                    "conflict_triggers": ["boring solutions", "lack of vision", "status quo"],
                    "image_signature": "Rich spectral diversity, complex patterns"
                },
                "muted": {
                    "archetype": "Steady Stabilizer",
                    "personality": "Consistent, reliable, maintenance-focused",
                    "civic_function": "Infrastructure maintenance and steady governance",
                    "voice_style": "Calm, measured, focused on reliability",
                    "conflict_triggers": ["radical changes", "instability", "neglect"],
                    "image_signature": "Uniform spectral response, stable patterns"
                }
            },
            
            # Scene Classification archetypes
            "Scene_Classification": {
                "vegetation": {
                    "archetype": "Ecosystem Advocate",
                    "personality": "Holistic, interconnected-thinking, life-centered",
                    "civic_function": "Ecosystem services and biodiversity protection",
                    "voice_style": "Speaks of connections, cycles, and living systems",
                    "conflict_triggers": ["habitat destruction", "pollution", "fragmentation"],
                    "image_signature": "Classified as vegetation, natural systems"
                },
                "urban": {
                    "archetype": "City Pulse Reader",
                    "personality": "Dynamic, people-focused, activity-oriented", 
                    "civic_function": "Urban vitality and community development",
                    "voice_style": "Energetic, focused on human activity and social life",
                    "conflict_triggers": ["urban decay", "isolation", "poor services"],
                    "image_signature": "Classified as urban, human activity zones"
                },
                "water": {
                    "archetype": "Flow Mediator",
                    "personality": "Connecting, cleansing, boundary-crossing",
                    "civic_function": "Water management and inter-district connections",
                    "voice_style": "Bridges different perspectives, seeks flow and connection",
                    "conflict_triggers": ["barriers", "pollution", "disconnection"],
                    "image_signature": "Classified as water, rivers, lakes"
                }
            }
        }
        
        # Traditional band mapping for fallback compatibility
        self.band_civic_roles = {
            "B1": {"archetype": "Atmospheric Witness", "civic_function": "Air quality monitoring"},
            "B2": {"archetype": "Blue Depth Keeper", "civic_function": "Water clarity assessment"},
            "B3": {"archetype": "Green Life Force", "civic_function": "Vegetation vitality"},
            "B4": {"archetype": "Red Earth Speaker", "civic_function": "Soil and surface analysis"},
            "B5": {"archetype": "Vegetation Edge", "civic_function": "Transition zone monitoring"},
            "B6": {"archetype": "Red Edge Sensor", "civic_function": "Plant stress detection"},
            "B7": {"archetype": "NIR Life Detector", "civic_function": "Biomass assessment"},
            "B8": {"archetype": "NIR Broad Scanner", "civic_function": "Vegetation structure"},
            "B8A": {"archetype": "NIR Narrow Focus", "civic_function": "Detailed vegetation analysis"},
            "B9": {"archetype": "Water Vapor Tracker", "civic_function": "Atmospheric moisture"},
            "B11": {"archetype": "SWIR Heat Reader", "civic_function": "Surface temperature and moisture"},
            "B12": {"archetype": "SWIR Deep Scanner", "civic_function": "Mineral and geological analysis"}
        }
    
    def generate_civic_assembly_from_image_data(self, extracted_data, location: Dict[str, float], 
                                              date: str) -> CivicAssembly:
        """Generate civic assembly using real image metadata and spectral signatures"""
        
        # Use the extracted spectral data to create more realistic personas
        image_types = extracted_data.image_types if hasattr(extracted_data, 'image_types') else []
        derived_indices = extracted_data.derived_indices if hasattr(extracted_data, 'derived_indices') else {}
        visual_analysis = extracted_data.visual_analysis if hasattr(extracted_data, 'visual_analysis') else ""
        semantic_categories = extracted_data.semantic_categories if hasattr(extracted_data, 'semantic_categories') else []
        
        # Generate personas based on actual image signatures
        personas = self._generate_personas_from_image_signatures(
            derived_indices, image_types, visual_analysis, semantic_categories, location, date
        )
        
        # Select assembly roles based on spectral dominance
        plurality_leader = personas[0] if personas else None
        dissenting_voice = personas[1] if len(personas) > 1 else None
        mediating_presence = personas[2] if len(personas) > 2 else None
        spectral_witnesses = personas[3:] if len(personas) > 3 else []
        
        # Analyze dynamics based on real data
        assembly_dynamics = self._analyze_image_based_dynamics(derived_indices, semantic_categories)
        public_tension = self._analyze_spectral_tensions(derived_indices)
        citizen_participation = self._assess_participation_from_diversity(image_types, semantic_categories)
        
        return CivicAssembly(
            location=location,
            date=date,
            plurality_leader=plurality_leader,
            dissenting_voice=dissenting_voice,
            mediating_presence=mediating_presence,
            spectral_witnesses=spectral_witnesses,
            assembly_dynamics=assembly_dynamics,
            public_tension=public_tension,
            citizen_participation=citizen_participation
        )
    
    def _generate_personas_from_image_signatures(self, indices: Dict[str, float], 
                                               image_types: List[str], visual_analysis: str,
                                               semantic_categories: List[str], location: Dict[str, float],
                                               date: str) -> List[ArendtianPersona]:
        """Generate personas based on actual spectral signatures from images"""
        
        personas = []
        
        # NDVI-based persona
        if "NDVI" in indices:
            ndvi_value = indices["NDVI"]
            if ndvi_value > 0.3:
                archetype_info = self.spectral_archetypes["NDVI"]["high"]
            elif ndvi_value > 0.1:
                archetype_info = self.spectral_archetypes["NDVI"]["medium"] 
            else:
                archetype_info = self.spectral_archetypes["NDVI"]["low"]
            
            persona = self._create_image_based_persona(
                "NDVI", ndvi_value, archetype_info, location, date, visual_analysis
            )
            personas.append(persona)
        
        # Moisture stress persona
        if "Moisture_Stress" in indices:
            moisture_value = indices["Moisture_Stress"]
            if moisture_value < 0.3:
                archetype_info = self.spectral_archetypes["Moisture_Stress"]["low"]
            else:
                archetype_info = self.spectral_archetypes["Moisture_Stress"]["high"]
            
            persona = self._create_image_based_persona(
                "Moisture_Stress", moisture_value, archetype_info, location, date, visual_analysis
            )
            personas.append(persona)
        
        # Urban index persona
        if "Urban_Index" in indices:
            urban_value = indices["Urban_Index"]
            if urban_value > 0.6:
                archetype_info = self.spectral_archetypes["Urban_Index"]["high"]
            else:
                archetype_info = self.spectral_archetypes["Urban_Index"]["low"]
            
            persona = self._create_image_based_persona(
                "Urban_Index", urban_value, archetype_info, location, date, visual_analysis
            )
            personas.append(persona)
        
        # Scene classification personas
        for category in semantic_categories:
            if category in ["healthy_vegetation", "moderate_vegetation"]:
                archetype_info = self.spectral_archetypes["Scene_Classification"]["vegetation"]
            elif category in ["urban_development", "infrastructure"]:
                archetype_info = self.spectral_archetypes["Scene_Classification"]["urban"]
            elif category == "water_body":
                archetype_info = self.spectral_archetypes["Scene_Classification"]["water"]
            else:
                continue
            
            persona = self._create_image_based_persona(
                f"Scene_{category}", 1.0, archetype_info, location, date, visual_analysis
            )
            personas.append(persona)
        
        # Visual analysis persona (based on spectral diversity)
        if "False" in " ".join(image_types) or "color" in " ".join(image_types):
            # Determine if spectral response is vibrant or muted
            spectral_diversity = len(indices)
            if spectral_diversity > 3:
                archetype_info = self.spectral_archetypes["False_Color"]["vibrant"]
            else:
                archetype_info = self.spectral_archetypes["False_Color"]["muted"]
            
            persona = self._create_image_based_persona(
                "Spectral_Vision", spectral_diversity / 10.0, archetype_info, location, date, visual_analysis
            )
            personas.append(persona)
        
        return personas[:5]  # Limit to 5 personas
    
    def _create_image_based_persona(self, signature_type: str, intensity: float, 
                                   archetype_info: Dict, location: Dict[str, float],
                                   date: str, visual_analysis: str) -> ArendtianPersona:
        """Create persona based on image signature and archetype"""
        
        # Generate name based on archetype and Prague location
        location_name = location.get("name", "Unknown")
        archetype = archetype_info["archetype"]
        
        # Czech-inspired names based on archetype
        name_mapping = {
            "Verdant Guardian": "Zelený Strážce",
            "Urban Gardener": "Městský Zahradník", 
            "Concrete Realist": "Betonový Realista",
            "Hydro Optimist": "Vodní Optimista",
            "Drought Warrior": "Bojovník Sucha",
            "Metropolitan Maximizer": "Metropolitní Maximalizátor",
            "Natural Preservationist": "Přírodní Ochránce",
            "Spectral Visionary": "Spektrální Vizionář",
            "Steady Stabilizer": "Stabilní Stabilizátor",
            "Ecosystem Advocate": "Ekosystémový Advokát",
            "City Pulse Reader": "Čtečka Pulzu Města",
            "Flow Mediator": "Mediátor Toku"
        }
        
        czech_name = name_mapping.get(archetype, f"Spektrální {archetype}")
        
        # Create voice based on image analysis
        voice_elements = []
        if "vegetation" in visual_analysis.lower():
            voice_elements.append("speaks of green growth and natural cycles")
        if "urban" in visual_analysis.lower():
            voice_elements.append("references city infrastructure and human activity")
        if "water" in visual_analysis.lower():
            voice_elements.append("flows with aquatic wisdom")
        if "stress" in visual_analysis.lower():
            voice_elements.append("warns of environmental pressures")
        
        voice_description = f"{archetype_info['voice_style']}. " + ", ".join(voice_elements) if voice_elements else archetype_info['voice_style']
        
        # Create utterance incorporating actual visual analysis
        analysis_snippet = visual_analysis[:100] + "..." if len(visual_analysis) > 100 else visual_analysis
        utterance = f"From my spectral analysis of {location_name}, I observe: {analysis_snippet}. As the {archetype}, I advocate for {archetype_info['civic_function']}."
        
        # Determine civic role and stance based on archetype
        civic_role = "environmental_advocate" if "Guardian" in archetype or "Advocate" in archetype else "civic_participant"
        political_stance = "actively_engaged" if intensity > 0.6 else "moderately_engaged"
        temporal_presence = "emerging" if "Visionary" in archetype else "stable"
        
        return ArendtianPersona(
            name=czech_name,
            dominant_band=signature_type,
            persona_type=archetype,
            voice=voice_description,
            utterance=utterance,
            arendtian_mode=archetype_info["personality"].split(",")[0].strip(),  # Use personality as mode
            civic_role=civic_role,
            political_stance=political_stance,
            temporal_presence=temporal_presence
        )
    
    def _analyze_image_based_dynamics(self, indices: Dict[str, float], 
                                     semantic_categories: List[str]) -> str:
        """Analyze assembly dynamics based on real image data"""
        
        # Check for environmental vs urban tension
        has_vegetation = any("vegetation" in cat for cat in semantic_categories)
        has_urban = any("urban" in cat for cat in semantic_categories)
        
        ndvi = indices.get("NDVI", 0)
        urban_index = indices.get("Urban_Index", 0)
        
        if has_vegetation and has_urban:
            if ndvi > 0.3 and urban_index > 0.6:
                return "green_urban_balance_tension"
            else:
                return "mixed_development_dialogue"
        elif has_vegetation and ndvi > 0.4:
            return "environmental_protection_focus"
        elif has_urban and urban_index > 0.7:
            return "urban_development_momentum"
        else:
            return "balanced_civic_deliberation"
    
    def _analyze_spectral_tensions(self, indices: Dict[str, float]) -> str:
        """Analyze tensions based on spectral index conflicts"""
        
        ndvi = indices.get("NDVI", 0)
        urban_index = indices.get("Urban_Index", 0)
        moisture_stress = indices.get("Moisture_Stress", 0)
        
        tensions = []
        
        # Green vs Urban tension
        if ndvi > 0.3 and urban_index > 0.6:
            tensions.append("nature_versus_development")
        
        # Water stress tension
        if moisture_stress > 0.6:
            tensions.append("water_scarcity_urgency")
        
        # Development pressure
        if urban_index > 0.8:
            tensions.append("density_versus_livability")
        
        # Environmental degradation
        if ndvi < 0.1 and moisture_stress > 0.5:
            tensions.append("environmental_degradation_crisis")
        
        if tensions:
            return "_and_".join(tensions)
        else:
            return "harmonious_coexistence"
    
    def _assess_participation_from_diversity(self, image_types: List[str], 
                                           semantic_categories: List[str]) -> str:
        """Assess citizen participation based on spectral and semantic diversity"""
        
        # More diverse data suggests more complex civic engagement
        spectral_diversity = len(image_types)
        semantic_diversity = len(semantic_categories)
        
        total_diversity = spectral_diversity + semantic_diversity
        
        if total_diversity > 8:
            return "highly_diverse_engagement"
        elif total_diversity > 5:
            return "moderate_civic_participation"
        elif total_diversity > 3:
            return "focused_community_involvement"
        else:
            return "limited_but_concentrated_participation"
    
    def generate_civic_assembly(self, spectral_data: Dict[str, float], location: Dict[str, float], 
                               date: str, data_source: str = "", data_quality: str = "") -> CivicAssembly:
        """Generate a complete civic assembly with Arendtian dynamics"""
        
        # Analyze spectral politics for assembly composition
        dominant_band, secondary_bands = self._analyze_civic_dominance(spectral_data)
        
        # Generate plurality leader (strongest civic voice)
        plurality_leader = self._generate_civic_member(
            dominant_band, spectral_data[dominant_band], location, date, "plurality_leader"
        )
        
        # Find political opposition
        opposition_band = self._find_political_opposition(dominant_band, spectral_data)
        dissenting_voice = self._generate_civic_member(
            opposition_band, spectral_data[opposition_band], location, date, "dissenting_voice"
        )
        
        # Find mediating presence
        mediating_band = self._find_mediating_voice(dominant_band, opposition_band, spectral_data)
        mediating_presence = self._generate_civic_member(
            mediating_band, spectral_data[mediating_band], location, date, "mediating_presence"
        )
        
        # Generate spectral witnesses (additional voices)
        spectral_witnesses = []
        for band, value in spectral_data.items():
            if value > 0.6 and band not in [dominant_band, opposition_band, mediating_band]:
                witness = self._generate_civic_member(
                    band, value, location, date, "spectral_witness"
                )
                spectral_witnesses.append(witness)
        
        # Analyze assembly dynamics
        assembly_dynamics = self._analyze_assembly_dynamics(spectral_data)
        public_tension = self._analyze_public_tension(plurality_leader, dissenting_voice)
        citizen_participation = self._assess_citizen_participation(spectral_data)
        
        return CivicAssembly(
            location=location,
            date=date,
            plurality_leader=plurality_leader,
            dissenting_voice=dissenting_voice,
            mediating_presence=mediating_presence,
            spectral_witnesses=spectral_witnesses,
            assembly_dynamics=assembly_dynamics,
            public_tension=public_tension,
            citizen_participation=citizen_participation
        )
    
    def _analyze_civic_dominance(self, spectral_data: Dict[str, float]) -> Tuple[str, List[str]]:
        """Analyze spectral data for civic dominance patterns"""
        sorted_bands = sorted(spectral_data.items(), key=lambda x: x[1], reverse=True)
        dominant_band = sorted_bands[0][0]
        secondary_bands = [band for band, value in sorted_bands[1:4]]
        return dominant_band, secondary_bands
    
    def _find_political_opposition(self, dominant_band: str, spectral_data: Dict[str, float]) -> str:
        """Find band representing political opposition"""
        
        # Arendtian oppositions based on philosophical tensions
        civic_oppositions = {
            "B3": "B4",   # Action optimism vs Judging realism
            "B8": "B11",  # Work vitality vs Labor necessity  
            "B9": "B1",   # Willing future vs Thinking anxiety
            "B1": "B3",   # Thinking solitude vs Action collaboration
            "B4": "B9",   # Judging past vs Willing future
            "B11": "B8",  # Labor necessity vs Work creation
        }
        
        preferred_opposition = civic_oppositions.get(dominant_band)
        if preferred_opposition and preferred_opposition in spectral_data:
            return preferred_opposition
        
        # Fall back to different Arendtian mode
        dominant_mode = self.band_civic_roles.get(dominant_band, {}).get("arendtian_mode")
        for band, info in self.band_civic_roles.items():
            if info.get("arendtian_mode") != dominant_mode and band in spectral_data:
                return band
        
        # Ultimate fallback
        return min(spectral_data.items(), key=lambda x: x[1])[0]
    
    def _find_mediating_voice(self, dominant: str, opposition: str, spectral_data: Dict[str, float]) -> str:
        """Find band that can mediate between dominant and opposition"""
        
        # Prefer "Judging" mode for mediation (Arendtian faculty of discernment)
        judging_bands = [band for band, info in self.band_civic_roles.items() 
                        if info.get("arendtian_mode") == "Judging" and band in spectral_data]
        
        if judging_bands:
            return max(judging_bands, key=lambda b: spectral_data[b])
        
        # Fall back to highest remaining band
        remaining = {k: v for k, v in spectral_data.items() if k not in [dominant, opposition]}
        return max(remaining.items(), key=lambda x: x[1])[0]
    
    def _generate_civic_member(self, band: str, intensity: float, location: Dict[str, float], 
                              date: str, assembly_role: str) -> ArendtianPersona:
        """Generate a civic assembly member"""
        
        band_info = self.band_civic_roles.get(band, {
            "archetype": "Unknown Citizen",
            "arendtian_mode": "Undefined",
            "civic_function": "Undefined role",
            "political_role": "Unknown stance",
            "assembly_voice": "Unclear voice",
            "public_stance": "Ambiguous position"
        })
        
        # Generate Czech civic names
        name = self._generate_civic_name(band, intensity, band_info["archetype"], assembly_role)
        
        # Create civic voice based on Arendtian mode and assembly role
        voice = self._create_civic_voice(band, intensity, band_info, assembly_role)
        
        # Generate civic utterance
        utterance = self._create_civic_utterance(band, intensity, band_info, location)
        
        # Determine civic role and political stance
        civic_role = self._determine_civic_role(assembly_role, intensity)
        political_stance = self._determine_political_stance(band_info["arendtian_mode"], intensity)
        
        return ArendtianPersona(
            name=name,
            dominant_band=band,
            persona_type=band_info["archetype"],
            voice=voice,
            utterance=utterance,
            arendtian_mode=band_info["arendtian_mode"],
            civic_role=civic_role,
            political_stance=political_stance,
            temporal_presence=self._determine_temporal_presence(intensity, assembly_role)
        )
    
    def _generate_civic_name(self, band: str, intensity: float, archetype: str, role: str) -> str:
        """Generate Czech-inspired civic names"""
        
        # Czech civic titles and names
        civic_titles = {
            "plurality_leader": ["Starosta", "Radní", "Předseda"],  # Mayor, Councilor, Chairman
            "dissenting_voice": ["Opoziční", "Kritik", "Nesouhlasný"],  # Opposition, Critic, Dissenting
            "mediating_presence": ["Mediátor", "Prostředník", "Rozhodčí"],  # Mediator, Intermediary, Arbiter
            "spectral_witness": ["Svědek", "Pozorovatel", "Občan"]  # Witness, Observer, Citizen
        }
        
        czech_surnames = ["Novák", "Svoboda", "Novotný", "Dvořák", "Černý", "Procházka", "Krejčí", "Horák"]
        
        title = random.choice(civic_titles.get(role, ["Občan"]))
        surname = random.choice(czech_surnames)
        
        # Intensity and band modifiers
        band_modifiers = {
            "B1": "Vzdušný",  # Airy
            "B3": "Zelený",   # Green
            "B4": "Rudý",     # Red
            "B8": "Živý",     # Living
            "B9": "Vodní",    # Watery
            "B11": "Suchý"    # Dry
        }
        
        modifier = band_modifiers.get(band, "Spectral")
        
        return f"{title} {modifier} {surname}"
    
    def _create_civic_voice(self, band: str, intensity: float, band_info: Dict, role: str) -> str:
        """Create civic voice based on Arendtian mode and assembly role"""
        
        mode = band_info["arendtian_mode"]
        
        mode_voice_styles = {
            "Thinking": "contemplative solitude",
            "Action": "collaborative engagement", 
            "Judging": "reflective discernment",
            "Work": "productive creation",
            "Labor": "necessary survival",
            "Willing": "future intention"
        }
        
        role_modifiers = {
            "plurality_leader": "with authority",
            "dissenting_voice": "with resistance", 
            "mediating_presence": "with bridge-building",
            "spectral_witness": "with observation"
        }
        
        voice_style = mode_voice_styles.get(mode, "undefined consciousness")
        role_mod = role_modifiers.get(role, "with presence")
        
        return f"Speaks from {voice_style} {role_mod}, intensity {intensity:.2f}"
    
    def _create_civic_utterance(self, band: str, intensity: float, band_info: Dict, location: Dict[str, float]) -> str:
        """Create civic utterance based on band and location"""
        
        utterances = {
            "B1": f"The air we breathe carries the weight of our collective choices. At coordinates {location['lat']:.3f}, {location['lon']:.3f}, I sense atmospheric responsibility.",
            "B3": f"Together we can cultivate the green spaces that make our city breathe. This place calls for collaborative action.",
            "B4": f"I witness the layers of urban transformation, the pain and persistence embedded in these coordinates.",
            "B8": f"The life force flowing through our infrastructure demands civic attention. I build for the living city.",
            "B9": f"Future weather patterns will test our collective resilience. We must prepare for atmospheric change.",
            "B11": f"The heat burden falls unequally. Those who labor in necessity must be heard in our assembly."
        }
        
        return utterances.get(band, f"I bring the voice of {band} to our civic discourse.")
    
    def _determine_civic_role(self, assembly_role: str, intensity: float) -> str:
        """Determine specific civic role"""
        if assembly_role == "plurality_leader":
            return "assemblies_leader"
        elif assembly_role == "dissenting_voice":
            return "opposition_member" 
        elif assembly_role == "mediating_presence":
            return "mediator"
        else:
            return "citizen_witness"
    
    def _determine_political_stance(self, mode: str, intensity: float) -> str:
        """Determine political stance based on Arendtian mode"""
        if mode in ["Action", "Work"]:
            return "actively_engaged"
        elif mode == "Thinking":
            return "contemplatively_withdrawn"
        elif mode == "Judging":
            return "reflectively_engaged"
        elif mode == "Labor":
            return "necessarily_urgent"
        elif mode == "Willing":
            return "future_oriented"
        else:
            return "undefined_stance"
    
    def _determine_temporal_presence(self, intensity: float, role: str) -> str:
        """Determine temporal presence in assembly"""
        if role == "plurality_leader":
            return "stable"
        elif intensity > 0.7:
            return "emerging"
        elif intensity < 0.3:
            return "fading"
        else:
            return "stable"
    
    def _analyze_assembly_dynamics(self, spectral_data: Dict[str, float]) -> str:
        """Analyze overall assembly dynamics"""
        action_bands = ["B3"]  # Collaborative
        thinking_bands = ["B1", "B2", "B5", "B6", "B8A"]  # Solitary
        work_bands = ["B7", "B8"]  # Productive
        
        action_intensity = sum(spectral_data.get(b, 0) for b in action_bands)
        thinking_intensity = sum(spectral_data.get(b, 0) for b in thinking_bands)
        work_intensity = sum(spectral_data.get(b, 0) for b in work_bands)
        
        if action_intensity > thinking_intensity and action_intensity > work_intensity:
            return "collaborative_momentum"
        elif thinking_intensity > action_intensity:
            return "contemplative_withdrawal"
        elif work_intensity > action_intensity:
            return "productive_focus"
        else:
            return "balanced_deliberation"
    
    def _analyze_public_tension(self, leader: ArendtianPersona, dissenter: ArendtianPersona) -> str:
        """Analyze tension between civic voices"""
        mode_tensions = {
            ("Action", "Thinking"): "public_versus_private",
            ("Work", "Labor"): "creation_versus_necessity",
            ("Judging", "Willing"): "past_versus_future",
            ("Action", "Judging"): "spontaneity_versus_reflection"
        }
        
        key = (leader.arendtian_mode, dissenter.arendtian_mode)
        return mode_tensions.get(key, "civic_disagreement")
    
    def _assess_citizen_participation(self, spectral_data: Dict[str, float]) -> str:
        """Assess level of citizen participation"""
        total_intensity = sum(spectral_data.values())
        high_bands = sum(1 for v in spectral_data.values() if v > 0.6)
        
        if total_intensity > 6.0 and high_bands >= 4:
            return "high_engagement"
        elif total_intensity > 4.0:
            return "moderate_participation"
        else:
            return "limited_turnout"
    
    def assembly_deliberation(self, assembly: CivicAssembly, citizen_inquiry: str, 
                            mediation_style: str = "neutral") -> Dict[str, str]:
        """Generate assembly deliberation with citizen as mediator"""
        
        responses = {}
        
        # Plurality leader opens discourse
        responses["plurality_leader"] = self._civic_response(
            assembly.plurality_leader, citizen_inquiry, "authoritative_opening"
        )
        
        # Dissenting voice provides opposition
        responses["dissenting_voice"] = self._civic_response(
            assembly.dissenting_voice, citizen_inquiry, "loyal_opposition",
            context=responses["plurality_leader"]
        )
        
        # Mediating presence seeks synthesis
        responses["mediating_presence"] = self._civic_response(
            assembly.mediating_presence, citizen_inquiry, "synthetic_mediation",
            context=f"Considering both {assembly.plurality_leader.name} and {assembly.dissenting_voice.name}"
        )
        
        # Spectral witnesses contribute if invited
        if assembly.spectral_witnesses and mediation_style == "inclusive":
            witness_voices = []
            for witness in assembly.spectral_witnesses[:2]:
                voice = self._civic_response(witness, citizen_inquiry, "citizen_testimony")
                witness_voices.append(f"{witness.name}: {voice}")
            responses["citizen_witnesses"] = " | ".join(witness_voices)
        
        return responses
    
    def _civic_response(self, persona: ArendtianPersona, inquiry: str, 
                       response_style: str, context: str = "") -> str:
        """Generate civic response based on Arendtian mode and style"""
        
        if not self.client:
            return self._mock_civic_response(persona, response_style)
        
        style_prompts = {
            "authoritative_opening": f"As {persona.name}, open the civic discourse with authority from your {persona.arendtian_mode} mode.",
            "loyal_opposition": f"As {persona.name}, provide constructive opposition to: {context}",
            "synthetic_mediation": f"As {persona.name}, seek synthesis and common ground in: {context}",
            "citizen_testimony": f"As {persona.name}, offer citizen testimony from your perspective."
        }
        
        prompt = f"""
You are {persona.name}, a civic assembly member speaking from {persona.arendtian_mode} mode.
Your role: {persona.persona_type}
Your political stance: {persona.political_stance}
Your civic function: {self.band_civic_roles.get(persona.dominant_band, {}).get('civic_function', 'Unknown')}

{style_prompts.get(response_style, "Respond as a civic participant.")}

Citizen inquiry: "{inquiry}"

Respond in 2-3 sentences, embodying Arendtian civic discourse.
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": f"You are {persona.name}, speaking in Arendtian civic assembly."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                max_tokens=300
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in civic response: {e}")
            return self._mock_civic_response(persona, response_style)
    
    def _mock_civic_response(self, persona: ArendtianPersona, response_style: str) -> str:
        """Generate mock civic response"""
        style_responses = {
            "authoritative_opening": f"*{persona.name} convenes from {persona.arendtian_mode}* Citizens, we gather to address this civic concern.",
            "loyal_opposition": f"*{persona.name} respectfully dissents* But we must consider the {persona.dominant_band} perspective!",
            "synthetic_mediation": f"*{persona.name} seeks common ground* Perhaps both civic truths can inform our decision.",
            "citizen_testimony": f"*{persona.name} testifies* From the {persona.dominant_band} experience, I witness..."
        }
        return style_responses.get(response_style, f"*{persona.name} participates in civic discourse*")
    
    # Legacy single persona method for backward compatibility  
    def generate_persona(self, spectral_data: Dict[str, float], location: Dict[str, float], 
                        date: str, data_source: str, data_quality: str) -> ArendtianPersona:
        """Generate single persona (legacy method)"""
        assembly = self.generate_civic_assembly(spectral_data, location, date, data_source, data_quality)
        return assembly.plurality_leader
    
    def communicate(self, persona: ArendtianPersona, user_message: str) -> str:
        """Communicate with single persona (legacy method)"""
        return self._civic_response(persona, user_message, "citizen_testimony")
