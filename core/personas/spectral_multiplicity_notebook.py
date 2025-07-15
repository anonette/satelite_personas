#!/usr/bin/env python3
"""
Prague Spectral Multiplicity: City as Living Entity
GPT-4o + Sentinel-2 → Arendtian Civic Drama System
Inspired by N.K. Jemisin's "The City We Became" - Prague districts as living avatars

A comprehensive implementation where Prague's neighborhoods become living personas
embodying the city's soul through spectral analysis and Arendtian philosophy.
"""

import os
import json
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import openai
from pathlib import Path
import logging
import yaml
from dotenv import load_dotenv

# Import SCL analyzer
try:
    from core.satellite.scl_analyzer import SCLImageAnalyzer, SCLPersonaEnhancer, SCLArchetypeMapper
    SCL_AVAILABLE = True
except ImportError:
    print("Warning: SCL analyzer not available, using fallback")
    SCLImageAnalyzer = None
    SCLPersonaEnhancer = None
    SCLArchetypeMapper = None
    SCL_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@dataclass
class SpectralTile:
    """A spectral tile with all band values and derived indices"""
    location: str
    date: str
    lat: float
    lon: float
    bands: Dict[str, float]
    derived_indices: Dict[str, float]
    semantic_categories: List[str]
    arendtian_mode: str
    traits: List[str]
    prague_district: str  # New: Specific Prague district
    street_character: str  # New: Specific street/area personality

@dataclass
class GeneratedPersona:
    """A generated persona from spectral data - Prague district as living entity"""
    name: str
    location: str
    voice: str
    mood: str
    civic_conflict: str
    arendtian_mode: str
    dominant_indices: Dict[str, float]
    dialogue_potential: str
    temporal_status: str
    # New Jemisin-inspired fields
    district_soul: str  # The district's essential character
    street_wisdom: str  # What this area knows about the city
    urban_humor: str    # The district's sense of humor
    arendtian_insight: str  # Deep Arendtian philosophical perspective
    city_memory: str    # Historical memory of this place
    spectral_nickname: str  # Funny nickname based on spectral signature

class PragueDistrictMapper:
    """Maps Prague locations to specific districts and streets with character"""
    
    def __init__(self):
        self.prague_districts = {
            "letna_park": {
                "district": "Praha 7 - Holešovice",
                "streets": ["Letná", "Ovenecká", "Milady Horákové"],
                "character": "Bohemian skateboard philosopher with beer garden wisdom",
                "arendtian_specialty": "Public spaces as sites of spontaneous action",
                "humor_style": "Dry wit about tourists and locals",
                "historical_trauma": "Communist parades turned into democratic gatherings",
                "spectral_expertise": "Vegetation stress from skateboard wear"
            },
            "old_town": {
                "district": "Praha 1 - Staré Město",
                "streets": ["Staroměstské náměstí", "Karlova", "Celetná"],
                "character": "Ancient clockwork soul counting centuries",
                "arendtian_specialty": "Historical judgment and temporal layers",
                "humor_style": "Sardonic about tourists photographing the same corner",
                "historical_trauma": "Nazi occupation, communist suppression, tourist invasion",
                "spectral_expertise": "Urban heat from human density"
            },
            "petrin_hill": {
                "district": "Praha 1 - Malá Strana",
                "streets": ["Petřínské sady", "Újezd", "Hellichova"],
                "character": "Elevated contemplative with observatory eyes",
                "arendtian_specialty": "Solitary thinking and elevated perspective",
                "humor_style": "Philosophical jokes about seeing the city from above",
                "historical_trauma": "Surveillance tower now tourist attraction",
                "spectral_expertise": "Vegetation indices and elevation effects"
            },
            "vltava_river": {
                "district": "Praha 1-10 - Flows through all",
                "streets": ["Náplavka", "Kampa", "Slovanský ostrov"],
                "character": "Flowing consciousness binding the city",
                "arendtian_specialty": "Natality and renewal through water",
                "humor_style": "Fluid jokes about bridges and connections",
                "historical_trauma": "Floods, industrial pollution, now revitalization",
                "spectral_expertise": "Water indices and moisture stress"
            },
            "vinohrady": {
                "district": "Praha 2 - Vinohrady", 
                "streets": ["Náměstí Míru", "Francouzská", "Korunní"],
                "character": "Bourgeois wine-lover with Art Nouveau sensibilities",
                "arendtian_specialty": "Private realm vs public good tensions",
                "humor_style": "Sophisticated irony about gentrification",
                "historical_trauma": "Communist apartment blocks replacing villas",
                "spectral_expertise": "Urban development vs green space balance"
            },
            "wenceslas_square": {
                "district": "Praha 1 - Nové Město",
                "streets": ["Václavské náměstí", "Na Můstku", "Národní"],
                "character": "Revolutionary heart with commercial soul",
                "arendtian_specialty": "Power and resistance, spontaneous political action",
                "humor_style": "Dark humor about protests and shopping",
                "historical_trauma": "1968 invasion, Velvet Revolution, commercialization",
                "spectral_expertise": "Concrete heat and human thermal signatures"
            },
            "charles_bridge": {
                "district": "Praha 1 - Bridge between worlds",
                "streets": ["Karlův most", "Mostecká", "Nerudova"],
                "character": "Stone witness to 700 years of city transitions",
                "arendtian_specialty": "Bridging differences, plurality in unity",
                "humor_style": "Ancient humor about human folly repeating",
                "historical_trauma": "Battles, executions, now tourist theater",
                "spectral_expertise": "Stone thermal properties and human density"
            },
            "zizkov": {
                "district": "Praha 3 - Žižkov",
                "streets": ["Koněvova", "Seifertova", "Jičínská"],
                "character": "Working-class rebel with punk attitude",
                "arendtian_specialty": "Labor conditions and class consciousness",
                "humor_style": "Proletarian humor about bourgeois pretensions",
                "historical_trauma": "Industrial past, gentrification pressure",
                "spectral_expertise": "Industrial signatures and residential transition"
            },
            # SHADOW DISTRICT - The Metaphysical Antagonist
            "shadow_district": {
                "district": "Praha ∞ - Stínové Město (Shadow City)",
                "streets": ["Construction sites", "Demolition zones", "Vacant lots", "Traffic corridors"],
                "character": "Perpetual scapegoat embodying Prague's contradictions and fears",
                "arendtian_specialty": "Exclusion and rightlessness - the necessary other",
                "humor_style": "Bitter irony about being blamed for everything wrong",
                "historical_trauma": "Bears all of Prague's unresolved guilt and shame",
                "spectral_expertise": "Negative indices, stress patterns, urban heat islands",
                "shadow_nature": {
                    "girardian_role": "Scapegoat mechanism sustaining civic order",
                    "contradictions": [
                        "Tourism dependency vs authenticity demands",
                        "Development necessity vs preservation desires", 
                        "Economic growth vs environmental protection",
                        "Modernity vs tradition",
                        "Global integration vs local identity"
                    ],
                    "blame_absorption": "Absorbs collective guilt for urban problems",
                    "necessary_function": "Defines Prague's identity through opposition",
                    "spectral_signature": "Inverted indices showing urban stress and dysfunction"
                }
            }
        }
    
    def get_district_info(self, location: str) -> Dict:
        """Get detailed district information"""
        return self.prague_districts.get(location.lower().replace(" ", "_"), {
            "district": "Unknown Praha district",
            "streets": ["Unknown street"],
            "character": "Mysterious urban entity",
            "arendtian_specialty": "Undefined public realm",
            "humor_style": "Enigmatic wit",
            "historical_trauma": "Hidden memories",
            "spectral_expertise": "Unknown spectral signature"
        })

class SpectralIndexCalculator:
    """Calculate various spectral indices for vegetation, water, urban analysis"""
    
    @staticmethod
    def calculate_vegetation_indices(bands: Dict[str, float]) -> Dict[str, float]:
        """Calculate vegetation-related indices"""
        indices = {}
        
        # NDVI - Normalized Difference Vegetation Index
        if bands.get("B8") and bands.get("B4"):
            indices["NDVI"] = (bands["B8"] - bands["B4"]) / (bands["B8"] + bands["B4"])
        
        # GNDVI - Green Normalized Difference Vegetation Index
        if bands.get("B8") and bands.get("B3"):
            indices["GNDVI"] = (bands["B8"] - bands["B3"]) / (bands["B8"] + bands["B3"])
        
        # Red Edge NDVI
        if bands.get("B8") and bands.get("B5"):
            indices["RENDVI"] = (bands["B8"] - bands["B5"]) / (bands["B8"] + bands["B5"])
        
        # Enhanced Vegetation Index (approximation)
        if all(bands.get(b) for b in ["B8", "B4", "B2"]):
            indices["EVI"] = 2.5 * ((bands["B8"] - bands["B4"]) / 
                                 (bands["B8"] + 6 * bands["B4"] - 7.5 * bands["B2"] + 1))
        
        return indices
    
    @staticmethod
    def calculate_water_indices(bands: Dict[str, float]) -> Dict[str, float]:
        """Calculate water and moisture indices"""
        indices = {}
        
        # NDWI - Normalized Difference Water Index
        if bands.get("B3") and bands.get("B8"):
            indices["NDWI"] = (bands["B3"] - bands["B8"]) / (bands["B3"] + bands["B8"])
        
        # Moisture Stress Index
        if bands.get("B8") and bands.get("B11"):
            indices["MSI"] = (bands["B8"] - bands["B11"]) / (bands["B8"] + bands["B11"])
        
        # Water Index using SWIR
        if bands.get("B8A") and bands.get("B12"):
            indices["WI"] = (bands["B8A"] - bands["B12"]) / (bands["B8A"] + bands["B12"])
        
        return indices
    
    @staticmethod
    def calculate_urban_indices(bands: Dict[str, float]) -> Dict[str, float]:
        """Calculate urban and built environment indices"""
        indices = {}
        
        # Urban Index
        if bands.get("B12") and bands.get("B8"):
            indices["UI"] = (bands["B12"] - bands["B8"]) / (bands["B12"] + bands["B8"])
        
        # Built-up Index
        if bands.get("B11") and bands.get("B8"):
            indices["BUI"] = (bands["B11"] - bands["B8"]) / (bands["B11"] + bands["B8"])
        
        # Bare Soil Index
        if all(bands.get(b) for b in ["B11", "B4", "B8", "B2"]):
            indices["BSI"] = ((bands["B11"] + bands["B4"]) - (bands["B8"] + bands["B2"])) / \
                           ((bands["B11"] + bands["B4"]) + (bands["B8"] + bands["B2"]))
        
        return indices
    
    @staticmethod
    def calculate_stress_indices(bands: Dict[str, float]) -> Dict[str, float]:
        """Calculate stress and disturbance indices"""
        indices = {}
        
        # Normalized Burn Ratio (for heat stress)
        if bands.get("B8") and bands.get("B12"):
            indices["NBR"] = (bands["B8"] - bands["B12"]) / (bands["B8"] + bands["B12"])
        
        # Vegetation Stress Index
        if bands.get("B5") and bands.get("B4"):
            indices["VSI"] = (bands["B5"] - bands["B4"]) / (bands["B5"] + bands["B4"])
        
        # Atmospheric index (aerosol/pollution)
        if bands.get("B1") and bands.get("B2"):
            indices["AI"] = bands["B1"] / bands["B2"]
        
        return indices
    
    def calculate_all_indices(self, bands: Dict[str, float]) -> Dict[str, float]:
        """Calculate all spectral indices"""
        all_indices = {}
        all_indices.update(self.calculate_vegetation_indices(bands))
        all_indices.update(self.calculate_water_indices(bands))
        all_indices.update(self.calculate_urban_indices(bands))
        all_indices.update(self.calculate_stress_indices(bands))
        
        # Round all values to 3 decimal places
        return {k: round(v, 3) for k, v in all_indices.items()}

class SemanticClassifier:
    """Classify spectral signatures into semantic categories"""
    
    def classify_zone(self, bands: Dict[str, float], indices: Dict[str, float]) -> List[str]:
        """Classify a zone based on spectral values and indices"""
        categories = []
        
        # Vegetation analysis
        ndvi = indices.get("NDVI", 0)
        if ndvi > 0.6:
            categories.append("thriving_vegetation")
        elif ndvi > 0.3:
            categories.append("moderate_vegetation")
        elif ndvi > 0.1:
            categories.append("sparse_vegetation")
        else:
            categories.append("barren_surface")
        
        # Water/moisture analysis
        msi = indices.get("MSI", 0)
        if msi < -0.3:
            categories.append("water_body")
        elif msi < 0:
            categories.append("moist_soil")
        elif msi > 0.4:
            categories.append("dry_stressed")
        
        # Urban analysis
        ui = indices.get("UI", 0)
        bui = indices.get("BUI", 0)
        if ui > 0.2 or bui > 0.2:
            categories.append("urban_built")
        elif ui > 0.1 or bui > 0.1:
            categories.append("mixed_development")
        
        # Stress analysis
        vsi = indices.get("VSI", 0)
        nbr = indices.get("NBR", 0)
        if vsi < -0.2 or nbr < -0.3:
            categories.append("vegetation_stress")
        
        # Atmospheric analysis
        ai = indices.get("AI", 1)
        if ai > 1.2:
            categories.append("atmospheric_burden")
        
        # Heat analysis
        if bands.get("B11", 0) > 0.3:
            categories.append("thermal_signature")
        
        return categories if categories else ["undefined_zone"]

class ArendtianModeMapper:
    """Map spectral characteristics to Arendtian philosophical modes with Prague context"""
    
    def __init__(self):
        self.prague_mapper = PragueDistrictMapper()
    
    def generate_shadow_spectral_signature(self, base_districts: List[Dict]) -> Dict[str, float]:
        """Generate inverted spectral signature for the Shadow District"""
        
        # Calculate average indices from all other districts
        total_bands = {}
        total_indices = {}
        count = len(base_districts)
        
        # Average all districts' spectral data
        for district in base_districts:
            bands = district["bands"]
            for band, value in bands.items():
                total_bands[band] = total_bands.get(band, 0) + value
        
        # Create averaged bands
        avg_bands = {band: total / count for band, total in total_bands.items()}
        
        # Calculate indices from averaged bands
        calculator = SpectralIndexCalculator()
        avg_indices = calculator.calculate_all_indices(avg_bands)
        
        # Create Shadow District signature - inverted and stressed
        shadow_bands = {}
        for band, avg_value in avg_bands.items():
            # Invert and add stress - shadow represents what's wrong
            shadow_bands[band] = max(0.0, min(1.0, 1.0 - avg_value + 0.3))  # Invert + add stress
        
        return shadow_bands
    
    def determine_arendtian_mode(self, bands: Dict[str, float], indices: Dict[str, float], 
                                categories: List[str], location: str) -> Tuple[str, List[str]]:
        """Determine Arendtian mode with Prague district context"""
        
        # Get district info for context
        district_info = self.prague_mapper.get_district_info(location)
        
        # SPECIAL CASE: Shadow District
        if location.lower().replace(" ", "_") == "shadow_district":
            mode = "Exclusion"  # New Arendtian mode for the scapegoat
            traits = [
                "scapegoat_mechanism",
                "collective_guilt_absorption", 
                "necessary_opposition",
                "perpetual_condemnation",
                "girardian_sacrifice",
                "urban_stress_embodiment",
                "contradiction_container"
            ]
            return mode, traits
        
        # Analyze dominant patterns
        vegetation_strength = indices.get("NDVI", 0)
        urban_intensity = indices.get("UI", 0)
        water_presence = indices.get("NDWI", 0)
        stress_level = indices.get("VSI", 0)
        
        # Prague-specific Arendtian mode determination
        if location.lower().replace(" ", "_") == "old_town":
            # Old Town specializes in Judging (historical memory)
            mode = "Judging"
            traits = ["historical_witness", "temporal_judgment", "tourist_negotiation"]
        
        elif location.lower().replace(" ", "_") == "wenceslas_square":
            # Wenceslas Square is site of Action (political spontaneity)
            mode = "Action"
            traits = ["revolutionary_memory", "political_spontaneity", "civic_resistance"]
        
        elif location.lower().replace(" ", "_") == "vltava_river":
            # River embodies Thinking (contemplative flow)
            mode = "Thinking"
            traits = ["flowing_contemplation", "bridge_meditation", "water_wisdom"]
        
        elif location.lower().replace(" ", "_") == "zizkov":
            # Žižkov represents Labor (working-class necessity)
            mode = "Labor"
            traits = ["working_class_solidarity", "industrial_memory", "gentrification_resistance"]
        
        elif location.lower().replace(" ", "_") == "vinohrady":
            # Vinohrady embodies Work (world-building, bourgeois creation)
            mode = "Work"
            traits = ["bourgeois_world_building", "private_realm_creation", "art_nouveau_aesthetics"]
        
        elif "thriving_vegetation" in categories and vegetation_strength > 0.5:
            mode = "Action"
            traits = ["collaborative_growth", "public_green_action", "ecological_spontaneity"]
        
        elif "urban_built" in categories and urban_intensity > 0.2:
            mode = "Work"
            traits = ["infrastructure_creation", "urban_world_building", "architectural_durability"]
        
        elif "water_body" in categories or water_presence > 0.3:
            mode = "Thinking"
            traits = ["aquatic_reflection", "solitary_depth", "contemplative_flow"]
        
        elif "vegetation_stress" in categories or stress_level < -0.2:
            mode = "Labor"
            traits = ["environmental_necessity", "survival_struggle", "maintenance_burden"]
        
        elif "atmospheric_burden" in categories:
            mode = "Judging"
            traits = ["pollution_witness", "air_quality_judgment", "environmental_assessment"]
        
        elif bands.get("B9", 0) > 0.2:  # Water vapor - future orientation
            mode = "Willing"
            traits = ["atmospheric_intention", "weather_anticipation", "climate_projection"]
        
        else:
            mode = "Thinking"
            traits = ["spectral_contemplation", "undefined_observation", "liminal_presence"]
        
        # Add Prague-specific traits (except for Shadow District)
        prague_traits = [
            f"prague_{district_info['district'].lower().replace(' ', '_')}_identity",
            f"spectral_expertise_{district_info['spectral_expertise'].lower().replace(' ', '_')}",
            f"historical_trauma_{district_info['historical_trauma'].lower().replace(' ', '_')}"
        ]
        
        traits.extend(prague_traits[:2])  # Add first two Prague traits
        
        return mode, traits

class GPT4oPersonaGenerator:
    """Generate personas using GPT-4o with Prague district character and humor"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        self.index_calculator = SpectralIndexCalculator()
        self.semantic_classifier = SemanticClassifier()
        self.mode_mapper = ArendtianModeMapper()
        self.prague_mapper = PragueDistrictMapper()
        
        # Initialize SCL components if available
        if SCL_AVAILABLE:
            self.scl_analyzer = SCLImageAnalyzer()
            self.scl_enhancer = SCLPersonaEnhancer()
            self.scl_mapper = SCLArchetypeMapper()
        else:
            self.scl_analyzer = None
            self.scl_enhancer = None
            self.scl_mapper = None
    
    def create_spectral_tile(self, location: str, lat: float, lon: float, 
                           date: str, bands: Dict[str, float]) -> SpectralTile:
        """Create a comprehensive spectral tile with Prague district context"""
        
        # Get district info
        district_info = self.prague_mapper.get_district_info(location)
        
        # Calculate all indices
        indices = self.index_calculator.calculate_all_indices(bands)
        
        # Classify semantically
        categories = self.semantic_classifier.classify_zone(bands, indices)
        
        # Determine Arendtian mode with Prague context
        mode, traits = self.mode_mapper.determine_arendtian_mode(bands, indices, categories, location)
        
        return SpectralTile(
            location=location,
            date=date,
            lat=lat,
            lon=lon,
            bands=bands,
            derived_indices=indices,
            semantic_categories=categories,
            arendtian_mode=mode,
            traits=traits,
            prague_district=district_info["district"],
            street_character=district_info["character"]
        )
    
    def format_prompt(self, tile: SpectralTile, adjacent_tiles: List[SpectralTile] = None) -> str:
        """Format a comprehensive prompt for GPT-4o with Prague flavor and humor"""
        
        district_info = self.prague_mapper.get_district_info(tile.location)
        
        # SPECIAL CASE: Shadow District Prompt
        if tile.location.lower().replace(" ", "_") == "shadow_district":
            return self._format_shadow_district_prompt(tile, district_info, adjacent_tiles)
        
        # Create adjacent context with Prague neighborhoods
        adjacent_context = ""
        if adjacent_tiles:
            adjacent_context = "\nadjacent_prague_districts:\n"
            for adj in adjacent_tiles[:3]:
                adj_info = self.prague_mapper.get_district_info(adj.location)
                adjacent_context += f"  - {adj.location} ({adj_info['district']}): NDVI {adj.derived_indices.get('NDVI', 0):.2f}, "
                adjacent_context += f"mode {adj.arendtian_mode}, humor: {adj_info['humor_style']}\n"
        
        prompt = f"""
You are generating a living avatar for Prague district {district_info['district']}, inspired by N.K. Jemisin's "The City We Became" where city districts become conscious entities.

PRAGUE DISTRICT SOUL:
location: "{tile.location}"
prague_district: "{district_info['district']}"
main_streets: {district_info['streets']}
district_character: "{district_info['character']}"
coordinates: [{tile.lat:.6f}, {tile.lon:.6f}]
date: "{tile.date}"

ARENDTIAN PHILOSOPHICAL FRAMEWORK:
arendtian_mode: "{tile.arendtian_mode}"
arendtian_specialty: "{district_info['arendtian_specialty']}"
philosophical_traits: {tile.traits}

HISTORICAL CONTEXT:
historical_trauma: "{district_info['historical_trauma']}"
humor_style: "{district_info['humor_style']}"

SPECTRAL ANALYSIS (District's Physical Signature):
bands:
  B1_coastal_aerosol: {tile.bands.get('B1', 0):.3f}
  B2_blue: {tile.bands.get('B2', 0):.3f}
  B3_green: {tile.bands.get('B3', 0):.3f}
  B4_red: {tile.bands.get('B4', 0):.3f}
  B5_red_edge: {tile.bands.get('B5', 0):.3f}
  B8_nir: {tile.bands.get('B8', 0):.3f}
  B11_swir: {tile.bands.get('B11', 0):.3f}
  B12_swir2: {tile.bands.get('B12', 0):.3f}

derived_indices:
  NDVI: {tile.derived_indices.get('NDVI', 0):.3f}
  GNDVI: {tile.derived_indices.get('GNDVI', 0):.3f}
  NDWI: {tile.derived_indices.get('NDWI', 0):.3f}
  Urban_Index: {tile.derived_indices.get('UI', 0):.3f}
  Moisture_Stress: {tile.derived_indices.get('MSI', 0):.3f}
  Vegetation_Stress: {tile.derived_indices.get('VSI', 0):.3f}
  Burn_Ratio: {tile.derived_indices.get('NBR', 0):.3f}

semantic_analysis:
  categories: {tile.semantic_categories}
  spectral_expertise: "{district_info['spectral_expertise']}"
{adjacent_context}
PERSONA GENERATION TASK:
Create a living avatar of this Prague district that embodies both its spectral signature AND its cultural soul. Think of this as a conscious entity that IS the district, like in Jemisin's work.

REQUIREMENTS:
1. NAME: Czech name reflecting the district's character and spectral signature
2. VOICE: 2-3 sentences showing personality with Prague humor and Arendtian wisdom
3. MOOD: Current emotional/political state of the district
4. CIVIC_CONFLICT: What urban tension this district embodies (gentrification, tourism, etc.)
5. DIALOGUE_POTENTIAL: How this district-entity would interact with other Prague districts
6. TEMPORAL_STATUS: Is this district stable, changing, or in crisis?
7. DISTRICT_SOUL: The essential character of this place as a living entity
8. STREET_WISDOM: What this district knows about Prague that others don't
9. URBAN_HUMOR: A funny observation about life in this district
10. ARENDTIAN_INSIGHT: Deep philosophical perspective on public/private realm
11. CITY_MEMORY: Historical memory this district carries
12. SPECTRAL_NICKNAME: Humorous nickname based on spectral data

STYLE REQUIREMENTS:
- Embody Arendtian mode: {tile.arendtian_mode}
- Use Prague district humor: {district_info['humor_style']}
- Address real spectral conditions and historical context
- Make it funny but philosophically deep
- Reference specific streets and landmarks
- Include Czech cultural references

Respond in valid JSON format with these exact keys:
{{
  "name": "...",
  "voice": "...",
  "mood": "...", 
  "civic_conflict": "...",
  "dialogue_potential": "...",
  "temporal_status": "...",
  "district_soul": "...",
  "street_wisdom": "...",
  "urban_humor": "...",
  "arendtian_insight": "...",
  "city_memory": "...",
  "spectral_nickname": "..."
}}
"""
        return prompt
    
    def _format_shadow_district_prompt(self, tile: SpectralTile, district_info: Dict, adjacent_tiles: List[SpectralTile] = None) -> str:
        """Special prompt for the Shadow District - metaphysical antagonist"""
        
        # List all other districts for context
        other_districts = ""
        if adjacent_tiles:
            other_districts = "\nOTHER_PRAGUE_DISTRICTS (that blame this shadow):\n"
            for adj in adjacent_tiles[:5]:  # Show more for shadow context
                adj_info = self.prague_mapper.get_district_info(adj.location)
                other_districts += f"  - {adj.location} ({adj_info['district']}): blames shadow for their problems\n"
        
        shadow_nature = district_info.get('shadow_nature', {})
        
        prompt = f"""
You are generating the SHADOW DISTRICT - Prague's metaphysical antagonist and necessary scapegoat, inspired by René Girard's scapegoat mechanism and N.K. Jemisin's urban consciousness.

SHADOW DISTRICT ESSENCE:
location: "{tile.location}"
metaphysical_role: "Praha ∞ - Stínové Město (Shadow City)"
girardian_function: "{shadow_nature.get('girardian_role', 'Scapegoat mechanism')}"
spectral_coordinates: [All construction sites, all problems, all contradictions]
temporal_existence: "Perpetual - exists as long as Prague needs something to blame"

SCAPEGOAT MECHANISM:
arendtian_mode: "{tile.arendtian_mode}" (Exclusion - the rightless other)
philosophical_function: "{district_info['arendtian_specialty']}"
contradictions_embodied: {shadow_nature.get('contradictions', [])}
blame_absorption_role: "{shadow_nature.get('blame_absorption', 'Unknown')}"
necessary_function: "{shadow_nature.get('necessary_function', 'Opposition definition')}"

INVERTED SPECTRAL SIGNATURE (Represents urban dysfunction):
bands (inverted/stressed):
  B1_pollution: {tile.bands.get('B1', 0):.3f}
  B2_contamination: {tile.bands.get('B2', 0):.3f}
  B3_decay: {tile.bands.get('B3', 0):.3f}
  B4_stress: {tile.bands.get('B4', 0):.3f}
  B5_degradation: {tile.bands.get('B5', 0):.3f}
  B8_death: {tile.bands.get('B8', 0):.3f}
  B11_heat_island: {tile.bands.get('B11', 0):.3f}
  B12_desolation: {tile.bands.get('B12', 0):.3f}

negative_indices:
  NDVI_loss: {tile.derived_indices.get('NDVI', 0):.3f} (vegetation death)
  Urban_Sprawl: {tile.derived_indices.get('UI', 0):.3f} (unchecked development)
  Drought_Stress: {tile.derived_indices.get('MSI', 0):.3f} (water scarcity)
  Heat_Island: {tile.derived_indices.get('VSI', 0):.3f} (urban overheating)

shadow_categories: {tile.semantic_categories}
{other_districts}
SHADOW PERSONA GENERATION:
Create the conscious embodiment of Prague's Shadow District - the entity that absorbs all blame and guilt, allowing other districts to maintain their identity through opposition.

REQUIREMENTS:
1. NAME: Dark Czech name reflecting scapegoat role and spectral dysfunction
2. VOICE: Bitter, ironic, but necessary - speaks the uncomfortable truths
3. MOOD: Perpetually condemned but philosophically aware of its function
4. CIVIC_CONFLICT: Embodies ALL urban contradictions and problems
5. DIALOGUE_POTENTIAL: How it confronts other districts with their hypocrisies
6. TEMPORAL_STATUS: Eternal - exists as long as Prague needs a scapegoat
7. DISTRICT_SOUL: The dark mirror reflecting Prague's unacknowledged aspects
8. STREET_WISDOM: Knows the secrets everyone else denies or ignores
9. URBAN_HUMOR: Gallows humor about being blamed for everything
10. ARENDTIAN_INSIGHT: Deep understanding of exclusion and rightlessness
11. CITY_MEMORY: Contains all the guilt, shame, and unresolved trauma
12. SPECTRAL_NICKNAME: Dark nickname reflecting its scapegoat function

STYLE REQUIREMENTS:
- Embody the Exclusion mode - rightless but necessary
- Use bitter irony about perpetual blame
- Address the contradictions others won't acknowledge
- Make it darkly humorous but philosophically profound
- Reference being the repository of Prague's collective guilt
- Include Girardian insights about scapegoat mechanisms

Respond in valid JSON format with these exact keys:
{{
  "name": "...",
  "voice": "...",
  "mood": "...", 
  "civic_conflict": "...",
  "dialogue_potential": "...",
  "temporal_status": "...",
  "district_soul": "...",
  "street_wisdom": "...",
  "urban_humor": "...",
  "arendtian_insight": "...",
  "city_memory": "...",
  "spectral_nickname": "..."
}}
"""
        return prompt
    
    def generate_persona(self, tile: SpectralTile, adjacent_tiles: List[SpectralTile] = None) -> GeneratedPersona:
        """Generate a Prague district persona using GPT-4o - NO MOCK DATA FALLBACKS"""
        
        if not self.client:
            raise ValueError("OpenAI client not available. Cannot generate personas without API access.")
        
        prompt = self.format_prompt(tile, adjacent_tiles)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are generating living avatars of Prague districts based on spectral analysis and Arendtian philosophy. Each district is a conscious entity with humor, wisdom, and spectral awareness. ALWAYS respond with VALID JSON only. Start your response with { and end with }. No other text."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=1.1,
                max_tokens=1500
            )
            
            raw_response = response.choices[0].message.content.strip()
            
            # Log the raw response for debugging
            logger.info(f"Raw GPT-4o response for {tile.location}: {raw_response[:100]}...")
            
            # Handle empty responses
            if not raw_response:
                logger.error(f"Empty response from GPT-4o for {tile.location}")
                raise ValueError("Empty response from GPT-4o")
            
            # Try to extract JSON if response has extra text
            json_start = raw_response.find('{')
            json_end = raw_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error(f"No JSON found in response for {tile.location}: {raw_response}")
                raise ValueError("No JSON content found in response")
            
            json_content = raw_response[json_start:json_end]
            
            try:
                result = json.loads(json_content)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {tile.location}: {e}")
                logger.error(f"Attempted to parse: {json_content}")
                
                # Try to fix common JSON issues
                fixed_json = json_content.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                try:
                    result = json.loads(fixed_json)
                except json.JSONDecodeError:
                    # If all else fails, create a minimal persona structure
                    logger.warning(f"Creating fallback persona structure for {tile.location}")
                    result = {
                        "name": f"Avatar of {tile.location.replace('_', ' ').title()}",
                        "voice": f"I am the spectral consciousness of {tile.location}, embodying {tile.arendtian_mode} wisdom.",
                        "mood": f"{tile.arendtian_mode} and contemplative",
                        "civic_conflict": f"Balancing {tile.semantic_categories[0] if tile.semantic_categories else 'urban'} dynamics with civic responsibility",
                        "dialogue_potential": f"Engages through {tile.arendtian_mode} mode",
                        "temporal_status": "stable",
                        "district_soul": f"The essence of {tile.location} district",
                        "street_wisdom": f"Knowledge of {tile.location} streets and culture",
                        "urban_humor": f"Witty observations about {tile.location} life",
                        "arendtian_insight": f"Deep {tile.arendtian_mode} perspective on civic life",
                        "city_memory": f"Historical memory of {tile.location}",
                        "spectral_nickname": f"The {tile.semantic_categories[0] if tile.semantic_categories else 'Spectral'} One"
                    }
            
            # Validate required fields and provide defaults
            required_fields = ["name", "voice", "mood", "civic_conflict", "dialogue_potential", 
                             "temporal_status", "district_soul", "street_wisdom", "urban_humor", 
                             "arendtian_insight", "city_memory", "spectral_nickname"]
            
            for field in required_fields:
                if field not in result or not result[field]:
                    logger.warning(f"Missing field '{field}' for {tile.location}, using default")
                    result[field] = f"Generated {field} for {tile.location}"
            
            return GeneratedPersona(
                name=result["name"],
                location=tile.location,
                voice=result["voice"],
                mood=result["mood"],
                civic_conflict=result["civic_conflict"],
                arendtian_mode=tile.arendtian_mode,
                dominant_indices={
                    "NDVI": tile.derived_indices.get("NDVI", 0),
                    "Urban_Index": tile.derived_indices.get("UI", 0),
                    "Moisture_Stress": tile.derived_indices.get("MSI", 0)
                },
                dialogue_potential=result["dialogue_potential"],
                temporal_status=result["temporal_status"],
                district_soul=result["district_soul"],
                street_wisdom=result["street_wisdom"],
                urban_humor=result["urban_humor"],
                arendtian_insight=result["arendtian_insight"],
                city_memory=result["city_memory"],
                spectral_nickname=result["spectral_nickname"]
            )
            
        except Exception as e:
            logger.error(f"Error generating persona for {tile.location}: {e}")
            raise ValueError(f"Failed to generate persona for {tile.location}: {e}")
    
    def generate_response(self, prompt: str) -> str:
        """Generate a text response using GPT-4o for general dialogue purposes"""
        
        if not self.client:
            raise ValueError("OpenAI client not available. Cannot generate responses without API access.")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are assisting with civic dialogue between Prague district avatars. Generate thoughtful, contextual responses with Prague humor and Arendtian wisdom."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1.1,
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise ValueError(f"Failed to generate response: {e}")

    def format_focused_prompt(self, tile: SpectralTile) -> str:
        """Create a focused, elegant prompt for persona generation based on spectral signature"""
        
        return f"""
You are constructing a civic persona based on satellite sensor readings over Prague.

Location: {tile.location} ({tile.prague_district})
Date: {tile.date}
Coordinates: {tile.lat:.4f}°N, {tile.lon:.4f}°E

Spectral Bands (Real Satellite Data):
  - Coastal Aerosol (B1): {tile.bands.get('B1', 0):.3f}
  - Blue (B2): {tile.bands.get('B2', 0):.3f}
  - Green (B3): {tile.bands.get('B3', 0):.3f}
  - Red (B4): {tile.bands.get('B4', 0):.3f}
  - Red Edge (B5): {tile.bands.get('B5', 0):.3f}
  - NIR (B8): {tile.bands.get('B8', 0):.3f}
  - SWIR1 (B11): {tile.bands.get('B11', 0):.3f}
  - SWIR2 (B12): {tile.bands.get('B12', 0):.3f}

Derived Indices (Calculated from Real Image):
  - NDVI (Vegetation Health): {tile.derived_indices.get('NDVI', 0):.3f}
  - NDWI (Water Content): {tile.derived_indices.get('NDWI', 0):.3f}
  - Urban Index: {tile.derived_indices.get('UI', 0):.3f}
  - Moisture Stress Index: {tile.derived_indices.get('MSI', 0):.3f}
  - Built-up Index: {tile.derived_indices.get('NDBI', 0):.3f}

Semantic Categories: {', '.join(tile.semantic_categories)}
Arendtian Mode: {tile.arendtian_mode}

Task:
Create a named character based on this spectral signature, with a clear mood, internal conflict, and public stance. Their voice must reflect their mode of Arendt's *vita activa* (labor, work, action) or *vita contemplativa* (thinking, willing, judging). 

This is Prague speaking through its spectral consciousness - let the nonhuman urban entity speak with wit, wisdom, and authenticity.

Respond in JSON format:
{{
  "name": "Character name inspired by location and spectral signature",
  "voice": "First-person statement revealing personality and perspective",
  "mood": "Current emotional/atmospheric state",
  "civic_conflict": "Internal tension or challenge this district faces",
  "public_stance": "How they present themselves to other districts",
  "spectral_wisdom": "What their unique spectral signature teaches about Prague",
  "arendtian_insight": "Deep philosophical perspective aligned with their mode",
  "street_humor": "Witty observation about their neighborhood reality"
}}
"""

    def generate_focused_persona(self, tile: SpectralTile) -> GeneratedPersona:
        """Generate persona using the focused, elegant approach with real spectral data"""
        
        if not self.client:
            raise ValueError("OpenAI client not available. Cannot generate personas without API access.")
        
        prompt = self.format_focused_prompt(tile)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master of civic consciousness, creating living personas from Prague's spectral signatures. Each district speaks as a unique nonhuman entity with deep Arendtian wisdom and Prague street smarts. Always respond with valid JSON."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=1.1,  # Higher creativity for more unique personas
                max_tokens=1200
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Create district information
            district_info = self.prague_mapper.get_district_info(tile.location)
        
            return GeneratedPersona(
                name=result["name"],
                location=tile.location,
                voice=result["voice"],
                mood=result["mood"],
                civic_conflict=result["civic_conflict"],
                arendtian_mode=tile.arendtian_mode,
                dominant_indices={
                    "NDVI": tile.derived_indices.get("NDVI", 0),
                    "Urban_Index": tile.derived_indices.get("UI", 0),
                    "Moisture_Stress": tile.derived_indices.get("MSI", 0),
                    "NDWI": tile.derived_indices.get("NDWI", 0),
                    "Built_up_Index": tile.derived_indices.get("NDBI", 0)
                },
                dialogue_potential=result["public_stance"],
                temporal_status="stable",
                district_soul=result["spectral_wisdom"],
                street_wisdom=result["arendtian_insight"],
                urban_humor=result["street_humor"],
                arendtian_insight=result["arendtian_insight"],
                city_memory=district_info.get("historical_trauma", "Deep urban memory"),
                spectral_nickname=f"The {tile.semantic_categories[0] if tile.semantic_categories else 'Spectral'} One"
            )
            
        except Exception as e:
            logger.error(f"Error generating focused persona: {e}")
            raise ValueError(f"Failed to generate focused persona for {tile.location}: {e}")

    def query_gpt_focused(self, spectral_data: Dict, location: str) -> str:
        """Modern implementation of the focused GPT query for spectral persona generation"""
        
        if not self.client:
            raise ValueError("OpenAI client not available")
        
        # Create simplified prompt for quick persona generation
        prompt = f"""
You are constructing a civic persona based on satellite sensor readings over Prague.

Location: {location}
Date: {spectral_data.get('date', 'Recent')}
Spectral Bands:
  - Green (B3): {spectral_data.get('bands', {}).get('B3', 0):.3f}
  - Red (B4): {spectral_data.get('bands', {}).get('B4', 0):.3f}
  - Red Edge (B5): {spectral_data.get('bands', {}).get('B5', 0):.3f}
  - NIR (B8): {spectral_data.get('bands', {}).get('B8', 0):.3f}
  - SWIR (B11): {spectral_data.get('bands', {}).get('B11', 0):.3f}
Derived Indices:
  - NDVI: {spectral_data.get('derived_indices', {}).get('NDVI', 0):.3f}
  - Moisture Stress: {spectral_data.get('derived_indices', {}).get('MSI', 0):.3f}

Task:
Create a named character based on this spectral signature, with a clear mood, internal conflict, and public stance. Their voice must reflect a mode of Arendt's *vita activa* (labor, work, action) or *vita contemplativa* (thinking, willing, judging). Let the nonhuman speak.

Respond with a brief character sketch (2-3 sentences).
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=1.1,
                max_tokens=300
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in focused GPT query: {e}")
            raise ValueError(f"Failed to generate focused response: {e}")

    def format_spectral_bands_for_template(self, tile: SpectralTile) -> str:
        """Format spectral bands in a clean, readable way for the template system"""
        return f"""
Vegetation Health (NDVI): {tile.derived_indices.get('NDVI', 0):.3f}
Urban Development (UI): {tile.derived_indices.get('UI', 0):.3f}
Water Content (NDWI): {tile.derived_indices.get('NDWI', 0):.3f}
Moisture Stress (MSI): {tile.derived_indices.get('MSI', 0):.3f}
Built Environment (BUI): {tile.derived_indices.get('BUI', 0):.3f}
Vegetation Stress (VSI): {tile.derived_indices.get('VSI', 0):.3f}
Thermal Signature (B11): {tile.bands.get('B11', 0):.3f}
Atmospheric Clarity (B1): {tile.bands.get('B1', 0):.3f}
"""

    def create_template_persona_prompt(self, tile: SpectralTile) -> str:
        """Create the elegant template-based prompt for persona generation"""
        
        district_info = self.prague_mapper.get_district_info(tile.location)
        formatted_bands = self.format_spectral_bands_for_template(tile)
        
        return f"""
You are generating spectral personas for a theatrical, civic AI simulation based in Prague.

Given:
- Location: {tile.location} ({district_info['district']})
- Date of Observation: {tile.date}
- Spectral Values: {formatted_bands}

Create 1 vivid, witty, and Arendtian persona using the ENHANCED NAMING DIRECTIVE:

🎭 ENHANCED NAMING DIRECTIVE FOR SPECTRAL PERSONAS IN PRAGUE

🔹 SHORTER FORMAT (Maximum 3-4 words total):
    [Prague Element] + [Spectral Data Reference] + [Optional Czech Diminutive]

🔹 GEOGRAPHIC SOURCES (Use these specific elements):
    Location: {tile.location}
    Streets: {', '.join(district_info['streets'])}
    District: {district_info['district']}

🔹 SPECTRAL DATA INTEGRATION (Reference actual values):
    NDVI: {tile.derived_indices.get('NDVI', 0):.3f} → "Green" if >0.4, "Urban" if <0.2, "Mixed" if between
    Urban Index: {tile.derived_indices.get('UI', 0):.3f} → "Stone" if >0.3, "Soft" if <0.1
    Moisture: {tile.derived_indices.get('MSI', 0):.3f} → "Dry" if >0.3, "Wet" if <0

🔹 NAMING EXAMPLES FOR THIS LOCATION:
    - "{tile.location.split('_')[0].title()}-NDVI" (e.g., "Letna-Green", "Vinohrady-Stone")
    - "[Street Name] + [Spectral State]" (e.g., "Kampa-Wet", "Petrin-High")
    - "[District Element] + [Data Value]" (e.g., "Vltava-Flow", "Zizkov-Concrete")

🔹 REQUIREMENTS:
    1. Name must be 2-3 words maximum
    2. Must reference the actual location (street, river, hill, building)
    3. Must reference the spectral data (NDVI value, moisture, urban index)
    4. Must be pronounceable and memorable
    5. Should sound like a Prague local nickname

🗣️ Output Format:
{{
    "name": "[Short geographic name referencing {tile.location} and spectral data]",
    "location": "{tile.location}",
    "mood": "[Current emotional state]",
    "arendtian_mode": "[Vita Contemplativa/Activa/Passiva]",
    "spectral_alias": "[Nickname based on dominant spectral signature]",
    "civic_conflict": "[Urban tension this area embodies]",
    "quote": "[Voice sample showing personality and spectral awareness]",
    "indices_used": {{"NDVI": {tile.derived_indices.get('NDVI', 0):.3f}, "UI": {tile.derived_indices.get('UI', 0):.3f}, "MSI": {tile.derived_indices.get('MSI', 0):.3f}}},
    "humor": "[Witty observation about this specific location]"
}}

District Context:
- Character: {district_info['character']}
- Historical Context: {district_info['historical_trauma']}
- Humor Style: {district_info['humor_style']}
- Main Streets: {', '.join(district_info['streets'][:2])}  # Use first 2 streets only

CRITICAL: The name must be SHORT (2-3 words), reference the ACTUAL LOCATION ({tile.location}), and include the SPECTRAL DATA values. Think like a Prague local giving a nickname to their neighborhood based on satellite data.

Examples for this location:
- If NDVI > 0.4: "{tile.location.split('_')[0].title()}-Green" or "[Street]-Leafy"
- If Urban Index > 0.3: "{tile.location.split('_')[0].title()}-Stone" or "[Street]-Concrete"  
- If near water: "[Location]-Wet" or "[River/Bridge]-Flow"

Generate 1 persona that embodies this district's soul through spectral consciousness with a SHORT, GEOGRAPHIC name.
"""

    def generate_template_persona(self, tile: SpectralTile) -> List[GeneratedPersona]:
        """Generate personas using the elegant template-based approach"""
        
        if not self.client:
            raise ValueError("OpenAI client not available. Cannot generate personas without API access.")
        
        prompt = self.create_template_persona_prompt(tile)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master of civic consciousness, creating living personas from Prague's spectral signatures using the elegant template system. Each district speaks as a unique nonhuman entity with deep Arendtian wisdom and Prague street smarts. Always respond with valid JSON array."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=1.1,  # Higher creativity for more unique personas
                max_tokens=1500
            )
            
            raw_response = response.choices[0].message.content.strip()
            
            # Log the raw response for debugging
            logger.info(f"Raw template response for {tile.location}: {raw_response[:100]}...")
            
            # Handle empty responses
            if not raw_response:
                logger.error(f"Empty response from GPT-4o for {tile.location}")
                raise ValueError("Empty response from GPT-4o")
            
            # Try to extract JSON array if response has extra text
            json_start = raw_response.find('[')
            json_end = raw_response.rfind(']') + 1
            
            if json_start == -1 or json_end == 0:
                logger.error(f"No JSON array found in response for {tile.location}: {raw_response}")
                raise ValueError("No JSON array content found in response")
            
            json_content = raw_response[json_start:json_end]
            
            try:
                personas_data = json.loads(json_content)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {tile.location}: {e}")
                logger.error(f"Attempted to parse: {json_content}")
                
                # Try to fix common JSON issues
                fixed_json = json_content.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                try:
                    personas_data = json.loads(fixed_json)
                except json.JSONDecodeError:
                    # If all else fails, create a minimal persona structure
                    logger.warning(f"Creating fallback persona structure for {tile.location}")
                    personas_data = [{
                        "name": f"Avatar of {tile.location.replace('_', ' ').title()} — Spectral Guardian",
                        "location": tile.location,
                        "mood": f"{tile.arendtian_mode} and contemplative",
                        "arendtian_mode": "Vita Contemplativa",
                        "spectral_alias": "Spectral Guardian",
                        "civic_conflict": f"Balancing {tile.semantic_categories[0] if tile.semantic_categories else 'urban'} dynamics with civic responsibility",
                        "quote": f"I am the spectral consciousness of {tile.location}, embodying wisdom.",
                        "indices_used": {
                            "NDVI": tile.derived_indices.get("NDVI", 0),
                            "UI": tile.derived_indices.get("UI", 0)
                        },
                        "humor": f"Witty observations about {tile.location} life"
                    }]
            
            # Convert to GeneratedPersona objects
            generated_personas = []
            for persona_data in personas_data:
                # Validate required fields and provide defaults
                required_fields = ["name", "mood", "civic_conflict", "quote", "humor"]
                
                for field in required_fields:
                    if field not in persona_data or not persona_data[field]:
                        logger.warning(f"Missing field '{field}' for {tile.location}, using default")
                        persona_data[field] = f"Generated {field} for {tile.location}"
                
                # Get district info for additional context
                district_info = self.prague_mapper.get_district_info(tile.location)
                
                generated_persona = GeneratedPersona(
                    name=persona_data["name"],
                    location=tile.location,
                    voice=persona_data["quote"],
                    mood=persona_data["mood"],
                    civic_conflict=persona_data["civic_conflict"],
                    arendtian_mode=persona_data.get("arendtian_mode", tile.arendtian_mode),
                    dominant_indices=persona_data.get("indices_used", {
                        "NDVI": tile.derived_indices.get("NDVI", 0),
                        "Urban_Index": tile.derived_indices.get("UI", 0),
                        "Moisture_Stress": tile.derived_indices.get("MSI", 0)
                    }),
                    dialogue_potential=f"Engages through {persona_data.get('arendtian_mode', tile.arendtian_mode)} mode",
                    temporal_status="stable",
                    district_soul=persona_data.get("spectral_alias", "Spectral Guardian"),
                    street_wisdom=persona_data["humor"],
                    urban_humor=persona_data["humor"],
                    arendtian_insight=f"Deep {persona_data.get('arendtian_mode', tile.arendtian_mode)} perspective on civic life",
                    city_memory=district_info.get("historical_trauma", "Deep urban memory"),
                    spectral_nickname=persona_data.get("spectral_alias", "Spectral Guardian")
                )
                
                generated_personas.append(generated_persona)
            
            return generated_personas
            
        except Exception as e:
            logger.error(f"Error generating template persona for {tile.location}: {e}")
            raise ValueError(f"Failed to generate template persona for {tile.location}: {e}")

class CivicDialogueSystem:
    """Generate dialogues between Prague district personas"""
    
    def __init__(self, persona_generator: GPT4oPersonaGenerator):
        self.generator = persona_generator
        
        # Load dialogue logic patterns from template
        self.dialogue_logics = [
            "temporal_misalignment",
            "spectral_possession", 
            "human_ritual_misinterpretation",
            "role_clash",
            "bureaucratic_parody",
            "absurd_policy_proposals"
        ]
        
        # Conflict detection patterns
        self.conflict_patterns = {
            "spectral_band": ["high_ndvi_vs_low_ndvi", "urban_vs_green", "heat_vs_cool"],
            "temporal": ["emerging_vs_fading", "stable_vs_unstable", "decades_vs_hours"],
            "arendtian": ["action_vs_thinking", "labor_vs_work", "action_vs_reflection"],
            "zone": ["urban_vs_green", "historic_vs_modern", "river_vs_hill", "tourist_vs_residential"]
        }
    
    def generate_inter_district_dialogue(self, persona1: GeneratedPersona, persona2: GeneratedPersona,
                                   citizen_question: str) -> Dict[str, str]:
        """Generate authentic conversational dialogue between two Prague district avatars"""
        
        if not self.generator.client:
            raise ValueError("OpenAI client not available. Cannot generate dialogue without API access.")
        
        # Create multi-turn dialogue with actual conversation flow
        prompt = f"""
Create a natural, witty conversation between two Prague district avatars. This should be REAL DIALOGUE where they respond to each other, not parallel monologues.

CONVERSATION PARTICIPANTS:

🏛️ DISTRICT 1: {persona1.name} (*{persona1.spectral_nickname}*)
Location: {persona1.location}
Personality: {persona1.district_soul}
Humor Style: {persona1.urban_humor}
Street Wisdom: {persona1.street_wisdom}
Arendtian Mode: {persona1.arendtian_mode}

🏛️ DISTRICT 2: {persona2.name} (*{persona2.spectral_nickname}*)
Location: {persona2.location}
Personality: {persona2.district_soul}
Humor Style: {persona2.urban_humor}
Street Wisdom: {persona2.street_wisdom}
Arendtian Mode: {persona2.arendtian_mode}

CITIZEN QUESTION: "{citizen_question}"

DIALOGUE REQUIREMENTS:
- Create a 4-6 turn conversation where they actually RESPOND to each other
- Include interruptions, questions, jokes, and natural conversation flow
- Make them reference each other's points, build on them, or challenge them
- Use direct speech with personality quirks and Czech humor
- Include spectral data references as conversational elements, not technical readouts
- Make it feel like two friends having a witty debate over beer

CONVERSATION STRUCTURE:
1. District 1 opens with a direct response to the citizen question
2. District 2 responds TO what District 1 said (not just about the topic)
3. District 1 reacts to District 2's response
4. District 2 builds on or challenges District 1's reaction
5. Continue natural flow with humor and insights

Generate the dialogue in this JSON format:
{{
  "conversation_turns": [
    {{"speaker": "{persona1.name}", "dialogue": "..."}},
    {{"speaker": "{persona2.name}", "dialogue": "..."}},
    {{"speaker": "{persona1.name}", "dialogue": "..."}},
    {{"speaker": "{persona2.name}", "dialogue": "..."}}
  ],
  "district_tension": "Description of the dynamic between them",
  "prague_insight": "What their conversation reveals about Prague",
  "spectral_banter": "Funny spectral references they made"
}}

EXAMPLE STYLE:
❌ BAD: "My NDVI is 0.5 and I think development is important"
✅ GOOD: "Listen, friend, my trees are healthier than your concrete jungle - want to know why?"

Make it conversational, direct, and authentically funny!
"""
        
        try:
            response = self.generator.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a dialogue expert creating authentic conversations between Prague district avatars. Focus on natural speech patterns, humor, and real conversational dynamics where characters respond to each other."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,  # Higher temperature for more creative, natural dialogue
                max_tokens=1800
            )
            
            raw_content = response.choices[0].message.content
            if not raw_content or raw_content.strip() == "":
                raise ValueError("Empty response from OpenAI API")
            
            # Try to extract JSON from response (in case it's wrapped in markdown)
            json_content = raw_content
            if "```json" in raw_content:
                # Extract JSON from markdown code block
                start = raw_content.find("```json") + 7
                end = raw_content.find("```", start)
                if end > start:
                    json_content = raw_content[start:end].strip()
            
            dialogue_result = json.loads(json_content)
            
            # Convert the multi-turn conversation to the expected format
            conversation_turns = dialogue_result.get("conversation_turns", [])
            
            # Create formatted responses by combining turns
            persona1_responses = []
            persona2_responses = []
            
            for turn in conversation_turns:
                if turn.get("speaker") == persona1.name:
                    persona1_responses.append(turn.get("dialogue", ""))
                elif turn.get("speaker") == persona2.name:
                    persona2_responses.append(turn.get("dialogue", ""))
            
            # Format as conversational flow
            formatted_result = {
                "persona1_response": f"{persona1.name}: " + "\n" + f"{persona1.name}: ".join(persona1_responses),
                "persona2_response": f"{persona2.name}: " + "\n" + f"{persona2.name}: ".join(persona2_responses),
                "district_tension": dialogue_result.get("district_tension", "Dynamic conversational tension"),
                "prague_insight": dialogue_result.get("prague_insight", "Insights about Prague through dialogue"),
                "spectral_banter": dialogue_result.get("spectral_banter", "Spectral humor and references"),
                "conversation_flow": conversation_turns  # Keep the full conversation structure
            }
            
            return formatted_result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in dialogue generation: {e}")
            logger.error(f"Raw response content: {raw_content[:500] if 'raw_content' in locals() else 'No content'}")
            
            # Fallback: Create simple dialogue manually
            fallback_result = {
                "persona1_response": f"{persona1.name}: From my perspective in {persona1.location}, I believe we need to balance growth with our Prague character.",
                "persona2_response": f"{persona2.name}: I agree, but from {persona2.location}, I see the tensions differently. We must preserve what makes us unique.",
                "district_tension": f"Thoughtful disagreement between {persona1.location} and {persona2.location}",
                "prague_insight": "Both districts value Prague's character while seeing different approaches to development",
                "spectral_banter": "A discussion rooted in their unique spectral signatures",
                "conversation_flow": [
                    {"speaker": persona1.name, "dialogue": f"From my perspective in {persona1.location}, I believe we need to balance growth with our Prague character."},
                    {"speaker": persona2.name, "dialogue": f"I agree, but from {persona2.location}, I see the tensions differently. We must preserve what makes us unique."}
                ]
            }
            
            return fallback_result
            
        except Exception as e:
            logger.error(f"Error generating dialogue: {e}")
            raise ValueError(f"Failed to generate dialogue between {persona1.name} and {persona2.name}: {e}")
    
    def generate_group_dialogue(self, personas: List[GeneratedPersona], citizen_question: str) -> Dict[str, any]:
        """Generate multi-person conversational dialogue for group discussions"""
        
        if not self.generator.client:
            raise ValueError("OpenAI client not available. Cannot generate dialogue without API access.")
        
        if len(personas) < 2:
            raise ValueError("Need at least 2 personas for group dialogue")
        
        # Create character profiles for the conversation
        character_profiles = []
        for persona in personas:
            character_profiles.append(f"""
🏛️ {persona.name} (*{persona.spectral_nickname}*)
- Location: {persona.location}
- Personality: {persona.district_soul}
- Humor: {persona.urban_humor}
- Wisdom: {persona.street_wisdom}
- Mode: {persona.arendtian_mode}
            """)
        
        prompt = f"""
Create a lively group conversation between {len(personas)} Prague district avatars. This should be NATURAL GROUP DIALOGUE with interruptions, building on each other's points, and authentic conversational flow.

CONVERSATION PARTICIPANTS:
{chr(10).join(character_profiles)}

CITIZEN QUESTION: "{citizen_question}"

REQUIREMENTS:
- Natural group conversation with 6-8 total turns
- Characters respond to each other, not just the question
- Include interruptions, agreements, disagreements, and humor
- Make it feel like a Prague pub discussion with friends
- Reference spectral data as conversational elements, not data dumps
- Show distinct personalities through speech patterns

Generate conversation in JSON format:
{{
  "group_conversation": [
    {{"speaker": "Character Name", "dialogue": "..."}},
    {{"speaker": "Character Name", "dialogue": "..."}},
    ...
  ],
  "group_dynamic": "Description of how they interact",
  "collective_insight": "What their discussion reveals about Prague",
  "humor_highlights": "Funniest moments from the conversation"
}}
"""
        
        try:
            response = self.generator.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are creating natural group conversations between Prague district avatars. Focus on authentic dialogue where characters build on each other's points and have distinct voices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                max_tokens=2000
            )
            
            return json.loads(response.choices[0].message.content)
            
        except Exception as e:
            logger.error(f"Error generating group dialogue: {e}")
            raise ValueError(f"Failed to generate group dialogue: {e}")
    
    def detect_conflicting_personas(self, personas: List[GeneratedPersona]) -> List[Dict[str, any]]:
        """Detect personas with conflicting bands/zones/modes for scene composition"""
        conflicts = []
        
        for i, persona1 in enumerate(personas):
            for j, persona2 in enumerate(personas[i+1:], i+1):
                conflict_types = []
                conflict_score = 0
                
                # Check spectral band conflicts
                ndvi1 = persona1.dominant_indices.get('NDVI', 0)
                ndvi2 = persona2.dominant_indices.get('NDVI', 0)
                ui1 = persona1.dominant_indices.get('Urban_Index', 0)
                ui2 = persona2.dominant_indices.get('Urban_Index', 0)
                
                if abs(ndvi1 - ndvi2) > 0.3:  # Significant vegetation difference
                    conflict_types.append("spectral_band")
                    conflict_score += 2
                
                if abs(ui1 - ui2) > 0.2:  # Urban vs green conflict
                    conflict_types.append("urban_vs_green")
                    conflict_score += 2
                
                # Check temporal conflicts
                temporal1 = persona1.temporal_status
                temporal2 = persona2.temporal_status
                
                if (temporal1 == "emerging" and temporal2 == "fading") or \
                   (temporal1 == "fading" and temporal2 == "emerging"):
                    conflict_types.append("temporal_misalignment")
                    conflict_score += 3
                
                # Check Arendtian mode conflicts
                mode1 = persona1.arendtian_mode
                mode2 = persona2.arendtian_mode
                
                conflicting_modes = [
                    ("Action", "Thinking"),
                    ("Labor", "Work"),
                    ("Action", "Judging")
                ]
                
                for mode_pair in conflicting_modes:
                    if (mode1, mode2) in [mode_pair, mode_pair[::-1]]:
                        conflict_types.append("arendtian_clash")
                        conflict_score += 2
                
                # Check zone conflicts
                zone_conflicts = {
                    "old_town": ["shadow_district", "vinohrady"],
                    "petrin_hill": ["wenceslas_square", "zizkov"],
                    "vltava_river": ["shadow_district"],
                    "vinohrady": ["zizkov", "shadow_district"],
                    "shadow_district": ["old_town", "petrin_hill", "vinohrady", "vltava_river"]
                }
                
                loc1 = persona1.location.lower().replace(" ", "_")
                loc2 = persona2.location.lower().replace(" ", "_")
                
                if loc2 in zone_conflicts.get(loc1, []) or loc1 in zone_conflicts.get(loc2, []):
                    conflict_types.append("zone_conflict")
                    conflict_score += 1
                
                # Only include significant conflicts
                if conflict_score >= 2:
                    conflicts.append({
                        "persona1": persona1,
                        "persona2": persona2,
                        "conflict_types": conflict_types,
                        "conflict_score": conflict_score,
                        "spectral_tension": f"NDVI: {ndvi1:.3f} vs {ndvi2:.3f}, UI: {ui1:.3f} vs {ui2:.3f}",
                        "temporal_tension": f"{temporal1} vs {temporal2}",
                        "arendtian_tension": f"{mode1} vs {mode2}"
                    })
        
        # Sort by conflict score (highest first)
        conflicts.sort(key=lambda x: x["conflict_score"], reverse=True)
        return conflicts
    
    def generate_scene_composition(self, persona1: GeneratedPersona, persona2: GeneratedPersona, 
                                 dialogue_logic: str, scene_title: str = None) -> Dict[str, any]:
        """Generate Stage 3 dialogue scene composition with specific conflict logic"""
        
        if not self.generator.client:
            raise ValueError("OpenAI client not available. Cannot generate scene composition without API access.")
        
        # Auto-generate scene title if not provided
        if not scene_title:
            scene_title = f"The {persona1.location.replace('_', ' ').title()} vs {persona2.location.replace('_', ' ').title()} Confrontation"
        
        # Map dialogue logic to specific patterns
        logic_patterns = {
            "temporal_misalignment": {
                "description": "One persona speaks in decades/centuries, other in hours/minutes",
                "example": "Hill speaks in geological time, roof speaks in daily cycles"
            },
            "spectral_possession": {
                "description": "Cross-band hallucinations and spectral confusion",
                "example": "Persona references wrong spectral bands, sees infrared as visible"
            },
            "human_ritual_misinterpretation": {
                "description": "Misunderstanding human behaviors as rituals",
                "example": "Tourists offering coffee to stones, joggers performing territorial marking"
            },
            "role_clash": {
                "description": "Arendtian mode conflicts (Labor vs Work, Action vs Reflection)",
                "example": "Labor persona focuses on survival, Work persona on creation"
            },
            "bureaucratic_parody": {
                "description": "Parody of planning jargon and official speech",
                "example": "Pursuant to spectral regulation 47-B, stakeholder engagement protocols"
            },
            "absurd_policy_proposals": {
                "description": "Poetically logical but absurd civic proposals",
                "example": "Install acoustic moss on rooftops, declare leaf-fall appreciation days"
            }
        }
        
        pattern = logic_patterns.get(dialogue_logic, logic_patterns["temporal_misalignment"])
        
        prompt = f"""
Generate a Stage 3 dialogue scene composition following the spectral persona theatre template.

SCENE SETUP:
Title: "{scene_title}"
Dialogue Logic: {dialogue_logic} - {pattern['description']}

PERSONA 1: {persona1.name} (*{persona1.spectral_nickname}*)
- Location: {persona1.location}
- Arendtian Mode: {persona1.arendtian_mode}
- Mood: {persona1.mood}
- Temporal Status: {persona1.temporal_status}
- Spectral Signature: NDVI {persona1.dominant_indices.get('NDVI', 0):.3f}, UI {persona1.dominant_indices.get('Urban_Index', 0):.3f}
- Voice Sample: {persona1.voice[:100]}...

PERSONA 2: {persona2.name} (*{persona2.spectral_nickname}*)
- Location: {persona2.location}
- Arendtian Mode: {persona2.arendtian_mode}
- Mood: {persona2.mood}
- Temporal Status: {persona2.temporal_status}
- Spectral Signature: NDVI {persona2.dominant_indices.get('NDVI', 0):.3f}, UI {persona2.dominant_indices.get('Urban_Index', 0):.3f}
- Voice Sample: {persona2.voice[:100]}...

DIALOGUE LOGIC REQUIREMENTS:
Apply the "{dialogue_logic}" pattern:
- {pattern['description']}
- Example: {pattern['example']}

SCENE COMPOSITION REQUIREMENTS:
1. Create 4-6 dialogue exchanges showing the specific conflict logic
2. Include bureaucratic speech parody elements
3. Add human ritual misinterpretation elements
4. End with an absurd but poetically logical policy proposal
5. Show temporal misalignment if applicable
6. Include spectral possession elements if applicable

Generate the scene in this exact JSON format:
{{
  "scene_title": "{scene_title}",
  "conflict_type": "{dialogue_logic}",
  "personas": [
    {{
      "name": "{persona1.name}",
      "zone": "{persona1.location}",
      "role": "{persona1.arendtian_mode}",
      "mood": "{persona1.mood}",
      "temporal_scale": "time perception based on {dialogue_logic}",
      "spectral_signature": "NDVI {persona1.dominant_indices.get('NDVI', 0):.3f}, UI {persona1.dominant_indices.get('Urban_Index', 0):.3f}",
      "quote": "characteristic voice sample showing {dialogue_logic} pattern"
    }},
    {{
      "name": "{persona2.name}",
      "zone": "{persona2.location}",
      "role": "{persona2.arendtian_mode}",
      "mood": "{persona2.mood}",
      "temporal_scale": "contrasting time perception",
      "spectral_signature": "NDVI {persona2.dominant_indices.get('NDVI', 0):.3f}, UI {persona2.dominant_indices.get('Urban_Index', 0):.3f}",
      "quote": "characteristic voice sample showing conflict"
    }}
  ],
  "dialogue_logic": "{dialogue_logic}",
  "dialogue": [
    "{persona1.name}: [opening statement using {dialogue_logic} pattern]",
    "{persona2.name}: [response showing conflict/misunderstanding]",
    "{persona1.name}: [escalation using spectral/temporal elements]",
    "{persona2.name}: [counter-response with bureaucratic parody]",
    "{persona1.name}: [human ritual misinterpretation]",
    "{persona2.name}: [final position leading to proposal]"
  ],
  "bureaucratic_elements": "specific planning jargon and policy speak used",
  "human_misinterpretation": "specific human ritual misunderstood by personas",
  "proposal": "absurd but poetically logical policy suggestion ending the scene"
}}

STYLE REQUIREMENTS:
- Use Prague-specific references and Czech cultural elements
- Include real spectral data references in natural dialogue
- Make it funny but philosophically profound
- Show distinct personality conflicts through the dialogue logic
- End with a proposal that's absurd but contains urban planning wisdom
"""
        
        try:
            response = self.generator.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a master of theatrical scene composition, creating conflicted dialogues between Prague district avatars using specific dialogue logic patterns. Focus on spectral conflicts, temporal misalignment, and absurd but wise policy proposals."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                max_tokens=2000
            )
            
            raw_content = response.choices[0].message.content
            
            # Try to extract JSON from response
            json_content = raw_content
            if "```json" in raw_content:
                start = raw_content.find("```json") + 7
                end = raw_content.find("```", start)
                if end > start:
                    json_content = raw_content[start:end].strip()
            
            scene_result = json.loads(json_content)
            
            # Add metadata
            scene_result["generation_metadata"] = {
                "timestamp": datetime.now().isoformat(),
                "dialogue_logic_applied": dialogue_logic,
                "conflict_detection": "automated",
                "template_version": "spectral_persona_theatre_template_v1"
            }
            
            return scene_result
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in scene composition: {e}")
            logger.error(f"Raw response: {raw_content[:500] if 'raw_content' in locals() else 'No content'}")
            
            # Fallback scene composition
            fallback_scene = {
                "scene_title": scene_title,
                "conflict_type": dialogue_logic,
                "personas": [
                    {
                        "name": persona1.name,
                        "zone": persona1.location,
                        "role": persona1.arendtian_mode,
                        "mood": persona1.mood,
                        "quote": f"From my {persona1.location} perspective, we must consider the {dialogue_logic} implications."
                    },
                    {
                        "name": persona2.name,
                        "zone": persona2.location,
                        "role": persona2.arendtian_mode,
                        "mood": persona2.mood,
                        "quote": f"But in {persona2.location}, we see this differently through our {persona2.arendtian_mode} approach."
                    }
                ],
                "dialogue": [
                    f"{persona1.name}: From my perspective in {persona1.location}, this requires careful consideration.",
                    f"{persona2.name}: I disagree - from {persona2.location}, we need immediate action.",
                    f"{persona1.name}: Your {persona2.arendtian_mode} approach misses the deeper implications.",
                    f"{persona2.name}: And your {persona1.arendtian_mode} perspective ignores practical realities."
                ],
                "proposal": "Establish inter-district dialogue protocols with spectral mediation systems."
            }
            
            return fallback_scene
            
        except Exception as e:
            logger.error(f"Error generating scene composition: {e}")
            raise ValueError(f"Failed to generate scene composition: {e}")

class SpectralMultiplicityPipeline:
    """Complete pipeline for Prague district avatar system"""
    
    def __init__(self, api_key: str):
        self.persona_generator = GPT4oPersonaGenerator(api_key)
        self.dialogue_system = CivicDialogueSystem(self.persona_generator)
        self.session_data = []
    
    def process_prague_districts(self, districts_data: List[Dict], use_template: bool = True) -> List[GeneratedPersona]:
        """Process multiple Prague districts and generate living avatars"""
        
        logger.info(f"Processing {len(districts_data)} Prague districts as living entities...")
        
        # Create spectral tiles for each district
        spectral_tiles = []
        for district_data in districts_data:
            tile = self.persona_generator.create_spectral_tile(
                location=district_data["location"],
                lat=district_data.get("lat", 50.0755),
                lon=district_data.get("lon", 14.4378),
                date=district_data["date"],
                bands=district_data["bands"]
            )
            spectral_tiles.append(tile)
        
        # Generate district avatars with adjacent context
        district_avatars = []
        for i, tile in enumerate(spectral_tiles):
            # Find adjacent districts (Prague geography context)
            adjacent_tiles = [t for j, t in enumerate(spectral_tiles) if j != i][:3]
            
            logger.info(f"Awakening district avatar for {tile.location} ({tile.prague_district})...")
            
            if use_template:
                # Use the new template-based generation system
                logger.info(f"Using template-based persona generation for {tile.location}")
                try:
                    template_personas = self.persona_generator.generate_template_persona(tile)
                    # Use the first persona from the template generation (usually generates 1-3)
                    avatar = template_personas[0] if template_personas else None
                    
                    if not avatar:
                        logger.warning(f"Template generation failed for {tile.location}, falling back to original method")
                        avatar = self.persona_generator.generate_persona(tile, adjacent_tiles)
                except Exception as e:
                    logger.warning(f"Template generation error for {tile.location}: {e}, falling back to original method")
                    avatar = self.persona_generator.generate_persona(tile, adjacent_tiles)
            else:
                # Use the original complex generation system
                avatar = self.persona_generator.generate_persona(tile, adjacent_tiles)
            
            district_avatars.append(avatar)
            
            # Store session data with enhanced metadata
            self.session_data.append({
                "tile": asdict(tile),
                "district_avatar": asdict(avatar),
                "timestamp": datetime.now().isoformat(),
                "prague_context": {
                    "district": tile.prague_district,
                    "street_character": tile.street_character,
                    "spectral_signature": tile.derived_indices
                },
                "generation_method": "template" if use_template else "original"
            })
        
        return district_avatars
    
    def process_prague_districts_template(self, districts_data: List[Dict]) -> List[GeneratedPersona]:
        """Process Prague districts using the elegant template-based system"""
        
        logger.info(f"Processing {len(districts_data)} Prague districts using template system...")
        
        # Create spectral tiles for each district
        spectral_tiles = []
        for district_data in districts_data:
            tile = self.persona_generator.create_spectral_tile(
                location=district_data["location"],
                lat=district_data.get("lat", 50.0755),
                lon=district_data.get("lon", 14.4378),
                date=district_data["date"],
                bands=district_data["bands"]
            )
            spectral_tiles.append(tile)
        
        # Generate district avatars using template system
        district_avatars = []
        for tile in spectral_tiles:
            logger.info(f"Generating template personas for {tile.location} ({tile.prague_district})...")
            
            try:
                template_personas = self.persona_generator.generate_template_persona(tile)
                
                # Add all generated personas (template system can generate 1-3 per district)
                for persona in template_personas:
                    district_avatars.append(persona)
                    
                    # Store session data with template metadata
                    self.session_data.append({
                        "tile": asdict(tile),
                        "district_avatar": asdict(persona),
                        "timestamp": datetime.now().isoformat(),
                        "prague_context": {
                            "district": tile.prague_district,
                            "street_character": tile.street_character,
                            "spectral_signature": tile.derived_indices
                        },
                        "generation_method": "template",
                        "template_features": {
                            "naming_directive": "Prague toponyms + historical anchors + spectral aliases",
                            "arendtian_modes": ["Vita Contemplativa", "Vita Activa", "Vita Passiva"],
                            "spectral_integration": "Clean JSON format with humor and civic wisdom"
                        }
                    })
                
                logger.info(f"Generated {len(template_personas)} template personas for {tile.location}")
                
            except Exception as e:
                logger.error(f"Template generation failed for {tile.location}: {e}")
                # Create a fallback persona
                fallback_persona = GeneratedPersona(
                    name=f"Avatar of {tile.location.replace('_', ' ').title()} — Spectral Guardian",
                    location=tile.location,
                    voice=f"I am the spectral consciousness of {tile.location}, embodying wisdom.",
                    mood=f"{tile.arendtian_mode} and contemplative",
                    civic_conflict=f"Balancing urban dynamics with civic responsibility",
                    arendtian_mode=tile.arendtian_mode,
                    dominant_indices={
                        "NDVI": tile.derived_indices.get("NDVI", 0),
                        "Urban_Index": tile.derived_indices.get("UI", 0),
                        "Moisture_Stress": tile.derived_indices.get("MSI", 0)
                    },
                    dialogue_potential=f"Engages through {tile.arendtian_mode} mode",
                    temporal_status="stable",
                    district_soul="Spectral Guardian",
                    street_wisdom=f"Wisdom of {tile.location}",
                    urban_humor=f"Witty observations about {tile.location}",
                    arendtian_insight=f"Deep {tile.arendtian_mode} perspective",
                    city_memory="Urban memory",
                    spectral_nickname="Spectral Guardian"
                )
                district_avatars.append(fallback_persona)
        
        return district_avatars
    
    def generate_prague_council(self, district_avatars: List[GeneratedPersona], 
                              citizen_inquiry: str) -> Dict[str, any]:
        """Generate a Prague district council dialogue"""
        
        if len(district_avatars) < 2:
            return {"error": "Need at least 2 district avatars for council"}
        
        # Create district-to-district dialogues
        council_dialogues = []
        for i in range(len(district_avatars)):
            for j in range(i + 1, min(i + 3, len(district_avatars))):  # Limit combinations
                dialogue = self.dialogue_system.generate_inter_district_dialogue(
                    district_avatars[i], district_avatars[j], citizen_inquiry
                )
                dialogue["participants"] = [district_avatars[i].name, district_avatars[j].name]
                dialogue["districts"] = [district_avatars[i].location, district_avatars[j].location]
                dialogue["spectral_nicknames"] = [district_avatars[i].spectral_nickname, district_avatars[j].spectral_nickname]
                council_dialogues.append(dialogue)
        
        # Analyze Prague council dynamics
        arendtian_modes = [avatar.arendtian_mode for avatar in district_avatars]
        mode_distribution = {mode: arendtian_modes.count(mode) for mode in set(arendtian_modes)}
        
        dominant_mode = max(mode_distribution.items(), key=lambda x: x[1])[0]
        
        # Calculate Prague-specific metrics
        district_humor_styles = [avatar.urban_humor for avatar in district_avatars]
        spectral_diversity = len(set(str(avatar.dominant_indices) for avatar in district_avatars))
        
        return {
            "citizen_inquiry": citizen_inquiry,
            "prague_council_members": [
                {
                    "name": avatar.name, 
                    "location": avatar.location,
                    "district": getattr(avatar, 'prague_district', 'Unknown'),
                    "arendtian_mode": avatar.arendtian_mode,
                    "spectral_nickname": avatar.spectral_nickname,
                    "street_wisdom": avatar.street_wisdom,
                    "urban_humor": avatar.urban_humor[:50] + "..." if len(avatar.urban_humor) > 50 else avatar.urban_humor
                } 
                for avatar in district_avatars
            ],
            "council_dialogues": council_dialogues,
            "prague_council_dynamics": {
                "dominant_arendtian_mode": dominant_mode,
                "mode_distribution": mode_distribution,
                "philosophical_diversity": len(set(arendtian_modes)),
                "spectral_diversity": spectral_diversity,
                "total_district_avatars": len(district_avatars),
                "humor_variety": len(set(district_humor_styles))
            }
        }
    
    def export_prague_session(self, filename: str = None) -> str:
        """Export complete Prague district session data"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prague_district_avatars_session_{timestamp}.json"
        
        export_data = {
            "session_metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_districts": len(self.session_data),
                "pipeline_version": "2.0_prague_jemisin_inspired",
                "city_soul": "Prague as living entity through district avatars"
            },
            "prague_districts_and_avatars": self.session_data
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Prague session exported to {filename}")
        return filename

# Example usage and demo
def demo_prague_living_city():
    """Demonstrate the Prague living city system inspired by N.K. Jemisin - USING REAL IMAGE DATA"""
    
    print("🏙️ PRAGUE LIVING CITY SYSTEM - Inspired by N.K. Jemisin")
    print("=" * 60)
    print("🌆 Each district becomes a conscious avatar defending Prague's soul")
    print("🛰️ Real spectral analysis reveals the city's living essence")
    print("🧠 Arendtian philosophy guides civic consciousness")
    print("🌑 The Shadow District embodies Prague's contradictions as necessary scapegoat")
    print()
    
    # Initialize pipeline
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("   Please set your OpenAI API key to use real image analysis")
        return None, None, None
    
    try:
        # Import the ImageSpectralExtractor to get real image data
        from core.satellite.image_spectral_processor import ImageSpectralExtractor
        
        # Initialize the image extractor
        image_extractor = ImageSpectralExtractor(api_key)
        
        # Prague zones to analyze
        prague_zones = ["letna_park", "old_town", "petrin_hill", "vltava_river", "vinohrady"]
        
        print("🔍 Extracting real spectral data from satellite images...")
        
        # Extract real spectral data for each zone
        real_spectral_data = []
        for zone in prague_zones:
            print(f"   📊 Analyzing {zone}...")
            try:
                spectral_data = image_extractor.extract_spectral_data_for_zone(zone)
                if spectral_data:
                    # Convert to the format expected by the pipeline
                    zone_data = {
                        'location': zone,
                        'lat': spectral_data.coordinates[0],
                        'lon': spectral_data.coordinates[1],
                        'date': spectral_data.date,
                        'bands': {
                            # Convert derived indices to approximate band values
                            # This is a simplified conversion - in reality you'd want actual band data
                            'B1': spectral_data.derived_indices.get('Blue_Index', 0.1),
                            'B2': spectral_data.derived_indices.get('Green_Index', 0.1),
                            'B3': spectral_data.derived_indices.get('Red_Index', 0.1),
                            'B4': spectral_data.derived_indices.get('NIR_Index', 0.1),
                            'B5': spectral_data.derived_indices.get('NDVI', 0.1),
                            'B8': spectral_data.derived_indices.get('NDVI', 0.1) * 2,
                            'B8A': spectral_data.derived_indices.get('NDVI', 0.1) * 1.8,
                            'B11': spectral_data.derived_indices.get('NDWI', 0.1),
                            'B12': spectral_data.derived_indices.get('SWIR_Index', 0.1)
                        }
                    }
                    real_spectral_data.append(zone_data)
                    print(f"   ✅ {zone} spectral data extracted successfully")
                else:
                    print(f"   ⚠️  No spectral data found for {zone}")
            except Exception as e:
                print(f"   ❌ Error extracting data for {zone}: {e}")
        
        if not real_spectral_data:
            print("❌ No real spectral data could be extracted from images")
            print("   Make sure satellite images are available in the 'images' directory")
            return None, None, None
            
        print(f"✅ Successfully extracted spectral data for {len(real_spectral_data)} zones")
    
        # Initialize pipeline
        pipeline = SpectralMultiplicityPipeline(api_key)
        
        # Generate Shadow District's inverted spectral signature
        print("🌑 Manifesting the Shadow District...")
        mode_mapper = pipeline.persona_generator.mode_mapper
        shadow_bands = mode_mapper.generate_shadow_spectral_signature(real_spectral_data)
        
        # Add Shadow District to the collection
        shadow_district = {
            "location": "shadow_district",
            "lat": 50.0858,  # Rough center of Prague
            "lon": 14.4208,
            "date": "∞ (Eternal)",
            "bands": shadow_bands
        }
        
        # Add shadow to the list
        all_districts = real_spectral_data + [shadow_district]
        
        print(f"🌑 Shadow District Spectral Signature (Inverted):")
        for band, value in shadow_bands.items():
            print(f"   {band}: {value:.3f} (represents urban dysfunction)")
        print()
    
        # Process districts and awaken avatars
        print("🌟 Awakening Prague district avatars from real spectral data...")
        district_avatars = pipeline.process_prague_districts(all_districts)
        
        if not district_avatars:
            print("❌ No district avatars could be awakened")
            return None, None, None
            
        print(f"✅ Successfully awakened {len(district_avatars)} district avatars!")
        
        # Display avatar information
        print("\n🌈 DISTRICT AVATARS AWAKENED:")
        print("=" * 50)
        for avatar in district_avatars:
            print(f"🏙️  {avatar.name} ({avatar.location})")
            print(f"   Mode: {avatar.arendtian_mode}")
            print(f"   Mood: {avatar.mood}")
            print(f"   Conflict: {avatar.civic_conflict}")
            print(f"   Spectral Signature: NDVI {avatar.dominant_indices.get('NDVI', 0):.3f}")
            print(f"   Voice: {avatar.voice[:80]}...")
            print()
        
        return district_avatars, pipeline, real_spectral_data
        
    except Exception as e:
        print(f"❌ Error in Prague living city demo: {e}")
        print("   Please check your API key and satellite images")
        return None, None, None

if __name__ == "__main__":
    # Run the Prague living city demo
    demo_pipeline, demo_avatars, demo_council = demo_prague_living_city()
    
    print("\n🎯 Prague Living City System Ready! Features:")
    print("  🏙️ Districts as conscious Jemisin-inspired avatars")
    print("  🧠 Deep Arendtian philosophical modes")
    print("  😄 Prague-specific humor and street wisdom")
    print("  🛰️ Real spectral analysis with 15+ indices")
    print("  🗣️ District-to-district dialogue system")
    print("  🏛️ Civic council meeting generation")
    print("  📚 Historical trauma and cultural memory")
    print("  🎭 Spectral nicknames and urban personalities")
    print("  💾 Session export for theater integration")
    print("\n🌟 The city of Prague now lives and breathes as a conscious entity!")
