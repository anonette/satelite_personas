#!/usr/bin/env python3
"""
Integrated Image Personas System
Combines real Sentinel-2 image analysis with GPT-4o vision for generating Arendtian civic personas
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import openai
from dotenv import load_dotenv
import logging

# Import our modules
from core.satellite.image_spectral_processor import ImageSpectralExtractor, ExtractedSpectralData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@dataclass
class ImageBasedPersona:
    """A persona generated from actual satellite imagery"""
    name: str
    location: str
    coordinates: tuple
    date: str
    image_types_used: List[str]
    spectral_signature: Dict[str, float]
    visual_characteristics: str
    voice: str
    civic_conflict: str
    arendtian_mode: str
    environmental_concerns: List[str]
    dialogue_potential: str
    image_analysis: str

class ImagePersonaGenerator:
    """Generate personas from actual satellite images using GPT-4o vision"""
    
    def __init__(self, api_key: str, images_directory: str = "images"):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        self.image_extractor = ImageSpectralExtractor(api_key, images_directory)
        
        # Check if vision analysis is working
        self.vision_available = self.image_extractor.vision_analyzer.vision_available if self.image_extractor.vision_analyzer.client else False
        
        # Arendtian mode mapping for image-based analysis
        self.arendtian_modes = {
            "healthy_vegetation": "Action",
            "urban_development": "Work", 
            "water_body": "Thinking",
            "environmental_stress": "Labor",
            "infrastructure": "Work",
            "mixed_urban": "Judging"
        }
    
    def determine_arendtian_mode(self, spectral_data: ExtractedSpectralData) -> str:
        """Determine Arendtian mode from image analysis with location-specific preferences"""
        
        # Check dominant characteristics from semantic categories first
        for category in spectral_data.semantic_categories:
            if category in self.arendtian_modes:
                return self.arendtian_modes[category]
        
        # Enhanced location-specific mode preferences based on Prague's character
        location_key = spectral_data.location_name.lower().replace(" ", "_")
        location_mode_preferences = {
            "letna_park": {
                "primary": "Action",      # Skateboarding, gathering, protests
                "secondary": "Thinking",  # Beer garden contemplation
                "conditions": {"high_vegetation": "Action", "urban_pressure": "Labor"}
            },
            "old_town": {
                "primary": "Judging",     # Historical reflection, evaluation
                "secondary": "Thinking",  # Contemplative historical space
                "conditions": {"tourist_pressure": "Labor", "preservation": "Judging"}
            },
            "petrin_hill": {
                "primary": "Thinking",    # Observatory, elevated perspective
                "secondary": "Action",    # Rose gardens, nature preservation
                "conditions": {"high_elevation": "Thinking", "stressed_vegetation": "Labor"}
            },
            "vltava_river": {
                "primary": "Thinking",    # Flowing contemplation, reflection
                "secondary": "Labor",     # Flood management, water quality
                "conditions": {"water_stress": "Labor", "flow_disruption": "Action"}
            },
            "vinohrady": {
                "primary": "Work",        # Residential development, wine heritage
                "secondary": "Action",    # Community building, café culture
                "conditions": {"gentrification": "Labor", "community_building": "Action"}
            }
        }
        
        # Get location preferences
        location_prefs = location_mode_preferences.get(location_key, {
            "primary": "Judging", 
            "secondary": "Thinking",
            "conditions": {}
        })
        
        # Analyze spectral characteristics for contextual mode determination
        indices = spectral_data.derived_indices
        ndvi = indices.get("NDVI", 0)
        urban_index = indices.get("Urban_Index", 0)
        moisture_stress = indices.get("Moisture_Stress", 0)
        
        # Determine based on environmental stress and context
        analysis_text = spectral_data.visual_analysis.lower()
        
        # High stress conditions trigger Labor mode
        if (moisture_stress > 0.7 or 
            "stress" in analysis_text or 
            "degradation" in analysis_text or 
            "damage" in analysis_text):
            return "Labor"
        
        # High vegetation with signs of community activity suggests Action
        elif (ndvi > 0.4 and 
              any(word in analysis_text for word in ["thriving", "healthy", "dense", "vibrant"])):
            return "Action"
        
        # Water or contemplative features suggest Thinking
        elif ("water" in analysis_text or 
              "calm" in analysis_text or 
              "reflection" in analysis_text or
              location_key in ["petrin_hill", "vltava_river"]):
            return "Thinking"
        
        # High urban development but balanced suggests Work
        elif (urban_index > 0.6 and ndvi > 0.2):
            return "Work"
        
        # Historical or evaluative context suggests Judging
        elif (location_key == "old_town" or 
              "heritage" in analysis_text or
              "historic" in analysis_text):
            return "Judging"
        
        # Use location-specific primary preference
        primary_mode = location_prefs["primary"]
        
        # Add some variation by occasionally using secondary mode
        import random
        if random.random() < 0.3:  # 30% chance to use secondary mode
            return location_prefs["secondary"]
        
        return primary_mode
    
    def generate_persona_from_images(self, spectral_data: ExtractedSpectralData) -> ImageBasedPersona:
        """Generate persona from processed satellite imagery"""
        
        if not self.client:
            raise RuntimeError("OpenAI API client not available. Cannot generate persona without API access.")
        
        arendtian_mode = self.determine_arendtian_mode(spectral_data)
        
        # Create comprehensive prompt combining image analysis with persona generation
        if self.vision_available:
            # Full prompt with vision analysis
            prompt = f"""
You are generating a dramatic civic persona for Prague based on ACTUAL Sentinel-2 satellite imagery analysis.

REAL SATELLITE DATA ANALYSIS:
Location: {spectral_data.location_name}
Coordinates: {spectral_data.coordinates}
Date: {spectral_data.date}
Available Image Types: {', '.join(spectral_data.image_types)}

SPECTRAL INDICES FROM IMAGES:
{json.dumps(spectral_data.derived_indices, indent=2)}

PIXEL STATISTICS FROM IMAGES:
{json.dumps(spectral_data.pixel_statistics, indent=2)}

GPT-4o VISION ANALYSIS OF IMAGES:
{spectral_data.visual_analysis}

SEMANTIC CLASSIFICATION:
Categories: {spectral_data.semantic_categories}

ARENDTIAN FRAMEWORK:
Assigned Mode: {arendtian_mode}

PERSONA GENERATION REQUIREMENTS:
Create a PROVOCATIVE and IMAGINATIVE Czech civic persona that embodies the spectral signature of {spectral_data.location_name}. 

NAME CREATIVITY RULES:
- Reference the SPECIFIC Prague location ({spectral_data.location_name})
- Use historical, architectural, or cultural elements of that area
- Be imaginative and provocative, not generic
- Examples of creative approaches:
  * For Letná Park: "Letná Rebel", "Skate Park Prophet", "Beer Garden Oracle"
  * For Old Town: "Astronomical Clock Keeper", "Cobblestone Chronicler", "Gothic Awakener"
  * For Petřín Hill: "Observatory Sage", "Tower Guardian", "Rose Garden Mystic"
  * For Vltava River: "Current Reader", "Bridge Whisperer", "Flood Memory Keeper"
  * For Vinohrady: "Vineyard Ghost", "Art Nouveau Dreamer", "Café Revolutionary"

The persona should:
1. Reflect ACTUAL satellite observations from the data
2. Address real environmental conditions visible in the imagery
3. Speak from the {arendtian_mode} mode with conviction
4. Have a provocative perspective on Prague's civic challenges
5. Reference specific spectral data in their voice

IMPORTANT: Respond ONLY with valid JSON. Create a UNIQUE, LOCATION-SPECIFIC name.

{{
  "name": "Creative name reflecting {spectral_data.location_name} characteristics and satellite data",
  "voice": "Provocative 2-3 sentences about Prague's conditions based on spectral analysis",
  "civic_conflict": "Sharp, specific environmental/urban tension this area represents",
  "environmental_concerns": ["specific satellite-observed issue 1", "specific satellite-observed issue 2"],
  "dialogue_potential": "How they'd provocatively engage with other Prague zones"
}}
"""
        else:
            # Simplified prompt using only statistical data
            prompt = f"""
You are generating a provocative civic persona for Prague based on ACTUAL Sentinel-2 satellite imagery statistical analysis.

REAL SATELLITE DATA ANALYSIS:
Location: {spectral_data.location_name}
Coordinates: {spectral_data.coordinates}
Date: {spectral_data.date}
Available Image Types: {', '.join(spectral_data.image_types)}

SPECTRAL INDICES FROM IMAGES:
{json.dumps(spectral_data.derived_indices, indent=2)}

PIXEL STATISTICS FROM IMAGES:
{json.dumps(spectral_data.pixel_statistics, indent=2)}

STATISTICAL ANALYSIS:
{spectral_data.visual_analysis}

SEMANTIC CLASSIFICATION:
Categories: {spectral_data.semantic_categories}

ARENDTIAN FRAMEWORK:
Assigned Mode: {arendtian_mode}

Create a PROVOCATIVE Czech civic persona for {spectral_data.location_name}. 

NAME MUST BE:
- Specific to {spectral_data.location_name}
- Imaginative and provocative
- Reference local landmarks, history, or character
- NOT generic like "Zelený" or "Václav"

Use the actual statistical measurements to create a sharp, memorable persona.

IMPORTANT: Respond ONLY with valid JSON.

{{
  "name": "Imaginative name specific to {spectral_data.location_name}",
  "voice": "Provocative perspective on Prague based on spectral data",
  "civic_conflict": "Sharp tension based on the spectral analysis",
  "environmental_concerns": ["issue 1 from data", "issue 2 from data"],
  "dialogue_potential": "How they'd challenge other zones"
}}
"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a satellite image analysis expert who generates civic personas based on real spectral data from Prague. You MUST respond with valid JSON only, no other text."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=1.1,
                max_tokens=800,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # Check if content is None or empty
            if not content or content.strip() == "":
                raise ValueError("OpenAI API returned empty response")
            
            # Log the raw response for debugging
            logger.info(f"OpenAI response received: {len(content)} characters")
            logger.debug(f"Raw OpenAI response: {content}")
            
            # Parse the JSON response
            result = json.loads(content)
            
            # Validate required fields
            required_fields = ["name", "voice", "civic_conflict", "environmental_concerns", "dialogue_potential"]
            missing_fields = [field for field in required_fields if field not in result]
            
            if missing_fields:
                raise ValueError(f"Missing required fields in API response: {missing_fields}")
            
            # Extract visual characteristics from the analysis
            visual_chars = self._extract_visual_characteristics(spectral_data)
            
            logger.info(f"Successfully generated persona: {result['name']} for {spectral_data.location_name}")
            
            return ImageBasedPersona(
                name=result["name"],
                location=spectral_data.location_name,
                coordinates=spectral_data.coordinates,
                date=spectral_data.date,
                image_types_used=spectral_data.image_types,
                spectral_signature=spectral_data.derived_indices,
                visual_characteristics=visual_chars,
                voice=result["voice"],
                civic_conflict=result["civic_conflict"],
                arendtian_mode=arendtian_mode,
                environmental_concerns=result["environmental_concerns"] if isinstance(result["environmental_concerns"], list) else [str(result["environmental_concerns"])],
                dialogue_potential=result["dialogue_potential"],
                image_analysis=spectral_data.visual_analysis[:500] + "..." if len(spectral_data.visual_analysis) > 500 else spectral_data.visual_analysis
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            logger.error(f"Failed to parse content: {content}")
            raise RuntimeError(f"OpenAI API returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Error generating image-based persona: {e}")
            raise RuntimeError(f"Failed to generate persona from satellite data: {e}")
    
    def _extract_visual_characteristics(self, spectral_data: ExtractedSpectralData) -> str:
        """Extract key visual characteristics from analysis"""
        analysis = spectral_data.visual_analysis.lower()
        
        characteristics = []
        
        # Base characteristics on actual spectral indices
        ndvi = spectral_data.derived_indices.get("NDVI", 0)
        urban_index = spectral_data.derived_indices.get("Urban_Index", 0)
        
        if ndvi > 0.3:
            characteristics.append("active vegetation")
        elif ndvi > 0.1:
            characteristics.append("sparse vegetation")
        else:
            characteristics.append("minimal vegetation")
        
        if urban_index > 0.6:
            characteristics.append("dense urban development")
        elif urban_index > 0.3:
            characteristics.append("moderate urban development")
        else:
            characteristics.append("low urban density")
        
        # Add analysis-based characteristics
        if "water" in analysis:
            characteristics.append("water presence")
        
        if "stress" in analysis or "dry" in analysis:
            characteristics.append("environmental stress indicators")
        
        return ", ".join(characteristics) if characteristics else "mixed spectral signature"

class ImageCivicAssembly:
    """Generate civic assemblies from multiple image-based personas"""
    
    def __init__(self, persona_generator: ImagePersonaGenerator):
        self.generator = persona_generator
    
    def convene_assembly_from_images(self, zone_names: List[str], 
                                   citizen_question: str) -> Dict[str, any]:
        """Create civic assembly from multiple satellite image zones - limited to 5 personas maximum"""
        
        # Limit to maximum 5 personas
        max_personas = 5
        limited_zones = zone_names[:max_personas]
        
        logger.info(f"Processing satellite images for zones: {', '.join(limited_zones)} (limit: {max_personas})")
        
        # Generate personas for each zone
        personas = []
        failed_zones = []
        
        for zone in limited_zones:
            # Stop if we've reached the limit
            if len(personas) >= max_personas:
                logger.info(f"Reached maximum of {max_personas} personas. Stopping generation.")
                break
                
            try:
                spectral_data = self.generator.image_extractor.extract_spectral_data_for_zone(zone)
                
                if spectral_data:
                    persona = self.generator.generate_persona_from_images(spectral_data)
                    personas.append(persona)
                    logger.info(f"Successfully generated persona: {persona.name} for {zone}")
                else:
                    failed_zones.append(zone)
                    logger.warning(f"No spectral data available for {zone}")
                    
            except Exception as e:
                failed_zones.append(zone)
                logger.error(f"Failed to generate persona for {zone}: {e}")
                continue
        
        if not personas:
            raise RuntimeError(f"Failed to generate any personas from {len(limited_zones)} zones")
        
        logger.info(f"Generated {len(personas)} personas from satellite analysis (limit: {max_personas})")
        
        # Generate dialogues between personas
        dialogues = self._generate_satellite_based_dialogues(personas, citizen_question)
        
        # Summarize environmental conditions
        environmental_summary = self._summarize_environmental_conditions(personas)
        
        return {
            "personas": [{"name": p.name, "location": p.location, "voice": p.voice, 
                         "arendtian_mode": p.arendtian_mode, "concerns": p.environmental_concerns} 
                        for p in personas],
            "dialogues": dialogues,
            "environmental_summary": environmental_summary,
            "citizen_question": citizen_question,
            "zones_processed": len(personas),
            "zones_failed": len(failed_zones),
            "max_personas_limit": max_personas
        }
    
    def _generate_satellite_based_dialogues(self, personas: List[ImageBasedPersona], 
                                          question: str) -> List[Dict[str, str]]:
        """Generate dialogues based on satellite observations"""
        
        dialogues = []
        
        for i in range(len(personas)):
            for j in range(i + 1, min(i + 3, len(personas))):
                persona1, persona2 = personas[i], personas[j]
                
                dialogue = {
                    "participants": [persona1.name, persona2.name],
                    "locations": [persona1.location, persona2.location],
                    "satellite_contrast": f"{persona1.visual_characteristics} vs {persona2.visual_characteristics}",
                    "arendtian_tension": f"{persona1.arendtian_mode} confronts {persona2.arendtian_mode}",
                    "persona1_response": f"{persona1.name}: {persona1.voice} Regarding your question: we must address the {persona1.visual_characteristics} evident in our satellite observations.",
                    "persona2_response": f"{persona2.name}: {persona2.voice} From {persona2.location}, I observe {persona2.visual_characteristics} that requires {persona2.arendtian_mode} approach.",
                    "environmental_tension": f"Satellite data shows contrast between {persona1.location} and {persona2.location} land use patterns"
                }
                
                dialogues.append(dialogue)
        
        return dialogues
    
    def _summarize_environmental_conditions(self, personas: List[ImageBasedPersona]) -> Dict[str, any]:
        """Summarize environmental conditions across all zones"""
        
        # Aggregate spectral indices
        all_indices = {}
        for persona in personas:
            for index, value in persona.spectral_signature.items():
                if index not in all_indices:
                    all_indices[index] = []
                all_indices[index].append(value)
        
        # Calculate averages
        avg_indices = {index: sum(values)/len(values) for index, values in all_indices.items()}
        
        # Collect environmental concerns
        all_concerns = []
        for persona in personas:
            all_concerns.extend(persona.environmental_concerns)
        
        unique_concerns = list(set(all_concerns))
        
        return {
            "average_spectral_indices": avg_indices,
            "environmental_concerns": unique_concerns,
            "visual_diversity": list(set(p.visual_characteristics for p in personas)),
            "arendtian_modes_present": list(set(p.arendtian_mode for p in personas))
        }

def demo_integrated_image_personas():
    """Demonstrate the complete image-to-persona pipeline with 5 persona limit"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    print("🖼️ PRAGUE SATELLITE IMAGE PERSONA SYSTEM")
    print("=" * 55)
    print("Using REAL Sentinel-2 images from C:\\dev\\Satelite\\images")
    print("📊 Maximum personas per session: 5")
    
    # Initialize components
    persona_generator = ImagePersonaGenerator(api_key, "images")
    civic_assembly = ImageCivicAssembly(persona_generator)
    
    # Prague zones to analyze (limited to 5 maximum)
    prague_zones = ["letna_park", "old_town", "petrin_hill", "vltava_river", "vinohrady"]
    max_personas = 5
    limited_zones = prague_zones[:max_personas]
    
    print(f"\n🏙️ Analyzing {len(limited_zones)} Prague zones (max {max_personas}):")
    for i, zone in enumerate(limited_zones, 1):
        print(f"   {i}. {zone}")
    
    # Example citizen question
    citizen_question = "How do we balance urban development with environmental preservation in Prague?"
    
    try:
        # Generate civic assembly from satellite imagery
        print(f"\n🎭 Convening civic assembly from satellite analysis...")
        assembly_result = civic_assembly.convene_assembly_from_images(limited_zones, citizen_question)
        
        print(f"\n✨ ASSEMBLY RESULTS:")
        print(f"   📊 Personas generated: {assembly_result['zones_processed']}/{max_personas}")
        print(f"   ❌ Zones failed: {assembly_result['zones_failed']}")
        print(f"   🎯 Question: {citizen_question}")
        
        print(f"\n🎭 PERSONA CAST (Limited to {max_personas}):")
        for i, persona_info in enumerate(assembly_result['personas'], 1):
            print(f"\n   {i}. {persona_info['name']} ({persona_info['location']})")
            print(f"      Mode: {persona_info['arendtian_mode']}")
            print(f"      Voice: {persona_info['voice'][:100]}...")
            print(f"      Concerns: {', '.join(persona_info['concerns'][:2])}")
        
        print(f"\n🌍 ENVIRONMENTAL SUMMARY:")
        env_summary = assembly_result['environmental_summary']
        print(f"   Average NDVI: {env_summary['average_spectral_indices'].get('NDVI', 'N/A'):.3f}")
        print(f"   Unique concerns: {len(env_summary['environmental_concerns'])}")
        print(f"   Arendtian modes present: {', '.join(env_summary['arendtian_modes_present'])}")
        
        return assembly_result
        
    except Exception as e:
        print(f"\n❌ Error in demo: {e}")
        return None

if __name__ == "__main__":
    result = demo_integrated_image_personas() 