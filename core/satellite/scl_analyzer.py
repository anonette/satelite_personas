"""
Scene Classification Layer (SCL) Analyzer for Prague Spectral Multiplicity Theater
Extracts and interprets Sentinel-2 L2A Scene Classification metadata for persona generation
"""

import numpy as np
from PIL import Image
# Disable PIL decompression bomb warning for trusted satellite data sources
Image.MAX_IMAGE_PIXELS = None
import json
from typing import Dict, List, Tuple, Optional
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SCLClassification:
    """Scene Classification Layer data for a specific location"""
    class_id: int
    class_name: str
    archetype: str
    voice_style: str
    conflict_tendencies: List[str]
    arendtian_mode: str
    temporal_behavior: str
    prague_context: str

class SCLArchetypeMapper:
    """Maps SCL classes to persona archetypes with Prague-specific context"""
    
    def __init__(self):
        self.scl_classes = {
            0: SCLClassification(
                class_id=0,
                class_name="No Data",
                archetype="Ghost of Absence",
                voice_style="Whispered, incomplete, speaks of what's missing",
                conflict_tendencies=["challenges data completeness", "questions official narratives", "speaks for the unrecorded"],
                arendtian_mode="Vita Passiva",
                temporal_behavior="Exists in gaps between moments",
                prague_context="Represents demolished buildings, forgotten corners, unmapped spaces"
            ),
            1: SCLClassification(
                class_id=1,
                class_name="Saturated Pixels",
                archetype="Overwhelmed Burnout",
                voice_style="Intense, stressed, speaks rapidly about overload",
                conflict_tendencies=["overwhelmed by tourism", "struggles with gentrification", "burnout from over-exposure"],
                arendtian_mode="Vita Activa",
                temporal_behavior="Peak intensity during summer tourist season",
                prague_context="Charles Bridge crowds, Old Town Square saturation, over-photographed landmarks"
            ),
            2: SCLClassification(
                class_id=2,
                class_name="Cast Shadow",
                archetype="Shadow Dweller",
                voice_style="Mysterious, speaks from hidden perspectives, knows secrets",
                conflict_tendencies=["reveals hidden truths", "challenges surface narratives", "protects underground culture"],
                arendtian_mode="Vita Contemplativa",
                temporal_behavior="Most active during long shadows (morning/evening)",
                prague_context="Under bridges, in courtyards, behind facades, underground passages"
            ),
            3: SCLClassification(
                class_id=3,
                class_name="Vegetation",
                archetype="Green Sentinel",
                voice_style="Protective, seasonal, speaks of growth and preservation",
                conflict_tendencies=["opposes over-development", "advocates for green spaces", "warns about environmental loss"],
                arendtian_mode="Vita Activa",
                temporal_behavior="Seasonal cycles, strongest in spring/summer",
                prague_context="Petřín Hill, Letná Park, Kampa Island, Wenceslas Square trees"
            ),
            4: SCLClassification(
                class_id=4,
                class_name="Not Vegetated",
                archetype="Urban Pragmatist",
                voice_style="Direct, practical, speaks of economic realities",
                conflict_tendencies=["prioritizes development", "challenges romantic views", "focuses on functionality"],
                arendtian_mode="Vita Activa",
                temporal_behavior="Consistent year-round presence",
                prague_context="Business districts, residential areas, commercial zones, infrastructure"
            ),
            5: SCLClassification(
                class_id=5,
                class_name="Water",
                archetype="Fluid Memory Keeper",
                voice_style="Poetic, flowing, connects past and present",
                conflict_tendencies=["mediates between opposing views", "speaks of continuity", "challenges rigid boundaries"],
                arendtian_mode="Vita Contemplativa",
                temporal_behavior="Reflects seasonal and daily light changes",
                prague_context="Vltava River, fountains, reflecting pools, canal systems"
            ),
            6: SCLClassification(
                class_id=6,
                class_name="Unclassified",
                archetype="Data Anarchist",
                voice_style="Rebellious, refuses categories, speaks in contradictions",
                conflict_tendencies=["rejects official classifications", "challenges bureaucracy", "embraces chaos"],
                arendtian_mode="Vita Activa",
                temporal_behavior="Unpredictable, appears when systems fail",
                prague_context="Liminal spaces, construction zones, areas in transition, bureaucratic gaps"
            ),
            7: SCLClassification(
                class_id=7,
                class_name="Cloud (Low Probability)",
                archetype="Uncertain Prophet",
                voice_style="Hesitant, speaks in possibilities and maybes",
                conflict_tendencies=["questions certainty", "offers alternative perspectives", "challenges absolute statements"],
                arendtian_mode="Vita Contemplativa",
                temporal_behavior="Weather-dependent, seasonal variations",
                prague_context="Elevated viewpoints, uncertain weather, transitional seasons"
            ),
            8: SCLClassification(
                class_id=8,
                class_name="Cloud (Medium Probability)",
                archetype="Detached Observer",
                voice_style="Analytical, distant, speaks from elevated perspective",
                conflict_tendencies=["provides overview", "challenges local focus", "offers broader context"],
                arendtian_mode="Vita Contemplativa",
                temporal_behavior="Periodic appearances, weather cycles",
                prague_context="Castle views, Petřín Tower perspective, elevated districts"
            ),
            9: SCLClassification(
                class_id=9,
                class_name="Cloud (High Probability)",
                archetype="Sky Philosopher",
                voice_style="Elevated, philosophical, speaks of grand patterns",
                conflict_tendencies=["challenges ground-level concerns", "offers cosmic perspective", "questions human scale"],
                arendtian_mode="Vita Contemplativa",
                temporal_behavior="Seasonal weather patterns, storm cycles",
                prague_context="Above the city, weather systems, atmospheric conditions"
            ),
            10: SCLClassification(
                class_id=10,
                class_name="Cirrus",
                archetype="Ethereal Visionary",
                voice_style="Dreamy, speaks of distant futures and pasts",
                conflict_tendencies=["transcends immediate concerns", "offers long-term vision", "challenges present focus"],
                arendtian_mode="Vita Contemplativa",
                temporal_behavior="High-altitude, long-term cycles",
                prague_context="Above Prague's skyline, connecting to broader European weather patterns"
            )
        }
        
        # Prague-specific district mappings
        self.prague_districts = {
            "letna_park": {
                "primary_scl": [3],  # Vegetation
                "secondary_scl": [2, 5],  # Shadows from trees, water features
                "character_modifier": "Beer garden guardian, metronome keeper"
            },
            "old_town": {
                "primary_scl": [4],  # Not vegetated (cobblestones, buildings)
                "secondary_scl": [6, 1],  # Unclassified (tourist chaos), Saturated (over-photographed)
                "character_modifier": "Historic chronicler, tourist-overwhelmed"
            },
            "vltava_river": {
                "primary_scl": [5],  # Water
                "secondary_scl": [2, 3],  # Shadows from bridges, riverside vegetation
                "character_modifier": "Bohemian memory flow, bridge connector"
            },
            "petrin_hill": {
                "primary_scl": [3],  # Vegetation
                "secondary_scl": [8, 9],  # Clouds touching tower, elevated perspective
                "character_modifier": "Elevated forest guardian, romantic viewpoint"
            },
            "vinohrady": {
                "primary_scl": [4],  # Urban residential
                "secondary_scl": [6, 3],  # Unclassified (hidden gardens), scattered vegetation
                "character_modifier": "Bourgeois brick dweller, hidden garden keeper"
            },
            "shadow_district": {
                "primary_scl": [2],  # Cast shadow
                "secondary_scl": [0, 6],  # No data (gaps), Unclassified (unmappable)
                "character_modifier": "Prague's scapegoat, absorbs collective contradictions"
            }
        }
    
    def get_scl_archetype(self, class_id: int) -> SCLClassification:
        """Get SCL archetype for a given class ID"""
        return self.scl_classes.get(class_id, self.scl_classes[6])  # Default to Unclassified
    
    def get_district_scl_profile(self, district: str) -> Dict:
        """Get SCL profile for a Prague district"""
        return self.prague_districts.get(district, {
            "primary_scl": [6],
            "secondary_scl": [4],
            "character_modifier": "Undefined district entity"
        })
    
    def generate_conflict_matrix(self) -> Dict[Tuple[int, int], str]:
        """Generate conflict patterns between SCL classes"""
        conflicts = {}
        
        # Vegetation vs Not Vegetated
        conflicts[(3, 4)] = "Green preservation vs urban development"
        conflicts[(4, 3)] = "Economic pragmatism vs environmental romanticism"
        
        # Water vs Shadow
        conflicts[(5, 2)] = "Transparent flow vs hidden secrets"
        conflicts[(2, 5)] = "Protected mysteries vs washing away truth"
        
        # Unclassified vs Saturated
        conflicts[(6, 1)] = "Anarchic rejection vs overwhelming data"
        conflicts[(1, 6)] = "Information overload vs categorical chaos"
        
        # Clouds vs Ground classes
        for cloud_class in [7, 8, 9, 10]:
            for ground_class in [0, 1, 2, 3, 4, 5, 6]:
                conflicts[(cloud_class, ground_class)] = "Elevated detachment vs ground-level concerns"
                conflicts[(ground_class, cloud_class)] = "Local reality vs abstract philosophy"
        
        # No Data vs All others
        for other_class in range(1, 11):
            conflicts[(0, other_class)] = "Absence challenges presence"
            conflicts[(other_class, 0)] = "Existence denies void"
        
        return conflicts

class SCLImageAnalyzer:
    """Analyzes Scene Classification images to extract SCL data"""
    
    def __init__(self):
        self.archetype_mapper = SCLArchetypeMapper()
    
    def extract_scl_from_image(self, image_path: Path) -> Dict[str, any]:
        """Extract SCL class distribution from Scene Classification image"""
        try:
            # Load the Scene Classification image
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Handle different image formats
            if len(img_array.shape) == 3:
                # If RGB, convert to grayscale or use first channel
                # Scene classification maps often encode class info in specific channels
                img_array = img_array[:, :, 0] if img_array.shape[2] > 0 else img_array
            
            # Count pixel classes (assuming pixel values correspond to SCL classes)
            unique_values, counts = np.unique(img_array, return_counts=True)
            total_pixels = img_array.size
            
            # Calculate class distribution
            class_distribution = {}
            for value, count in zip(unique_values, counts):
                if 0 <= value <= 10:  # Valid SCL classes
                    percentage = (count / total_pixels) * 100
                    class_distribution[int(value)] = {
                        'count': int(count),
                        'percentage': float(percentage),
                        'archetype': self.archetype_mapper.get_scl_archetype(int(value))
                    }
            
            # Identify dominant classes (>5% of image)
            dominant_classes = {k: v for k, v in class_distribution.items() if v['percentage'] > 5.0}
            
            # Generate analysis summary
            analysis = {
                'image_path': str(image_path),
                'total_pixels': total_pixels,
                'class_distribution': class_distribution,
                'dominant_classes': dominant_classes,
                'primary_archetype': self._get_primary_archetype(dominant_classes),
                'secondary_archetypes': self._get_secondary_archetypes(dominant_classes),
                'conflict_potential': self._analyze_conflict_potential(dominant_classes),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            return analysis
            
        except Exception as e:
            print(f"Error extracting SCL from {image_path}: {e}")
            return self._generate_fallback_analysis(image_path)
    
    def _get_primary_archetype(self, dominant_classes: Dict) -> Optional[SCLClassification]:
        """Get the most dominant SCL archetype"""
        if not dominant_classes:
            return None
        
        # Find class with highest percentage
        primary_class = max(dominant_classes.keys(), key=lambda k: dominant_classes[k]['percentage'])
        return self.archetype_mapper.get_scl_archetype(primary_class)
    
    def _get_secondary_archetypes(self, dominant_classes: Dict) -> List[SCLClassification]:
        """Get secondary SCL archetypes"""
        if len(dominant_classes) <= 1:
            return []
        
        # Sort by percentage and take top 2-3 excluding primary
        sorted_classes = sorted(dominant_classes.keys(), 
                              key=lambda k: dominant_classes[k]['percentage'], 
                              reverse=True)
        
        secondary_classes = sorted_classes[1:4]  # Take up to 3 secondary
        return [self.archetype_mapper.get_scl_archetype(cls) for cls in secondary_classes]
    
    def _analyze_conflict_potential(self, dominant_classes: Dict) -> List[str]:
        """Analyze potential conflicts between dominant classes"""
        conflicts = []
        conflict_matrix = self.archetype_mapper.generate_conflict_matrix()
        
        class_ids = list(dominant_classes.keys())
        for i, class1 in enumerate(class_ids):
            for class2 in class_ids[i+1:]:
                conflict_key = (class1, class2)
                if conflict_key in conflict_matrix:
                    conflicts.append(conflict_matrix[conflict_key])
        
        return conflicts
    
    def _generate_fallback_analysis(self, image_path: Path) -> Dict:
        """Generate fallback analysis when image processing fails"""
        return {
            'image_path': str(image_path),
            'total_pixels': 0,
            'class_distribution': {},
            'dominant_classes': {},
            'primary_archetype': self.archetype_mapper.get_scl_archetype(6),  # Unclassified
            'secondary_archetypes': [],
            'conflict_potential': ["Unable to analyze - data anarchist emerges"],
            'extraction_timestamp': datetime.now().isoformat(),
            'error': "Fallback analysis - image processing failed"
        }
    
    def analyze_prague_district(self, district: str, base_spectral_data: Dict) -> Dict:
        """Combine SCL analysis with existing spectral data for Prague districts"""
        district_profile = self.archetype_mapper.get_district_scl_profile(district)
        
        # Get primary and secondary archetypes for this district
        primary_scl = district_profile['primary_scl'][0]
        secondary_scl = district_profile['secondary_scl']
        
        primary_archetype = self.archetype_mapper.get_scl_archetype(primary_scl)
        secondary_archetypes = [self.archetype_mapper.get_scl_archetype(scl) for scl in secondary_scl]
        
        # Combine with existing spectral data
        enhanced_data = {
            **base_spectral_data,
            'scl_analysis': {
                'primary_archetype': primary_archetype,
                'secondary_archetypes': secondary_archetypes,
                'district_modifier': district_profile['character_modifier'],
                'scl_classes': {
                    'primary': primary_scl,
                    'secondary': secondary_scl
                }
            }
        }
        
        return enhanced_data

class SCLPersonaEnhancer:
    """Enhances persona generation with SCL archetype data"""
    
    def __init__(self):
        self.archetype_mapper = SCLArchetypeMapper()
    
    def enhance_persona_prompt(self, base_persona_data: Dict, scl_analysis: Dict) -> str:
        """Generate enhanced persona prompt with SCL archetype integration"""
        
        primary_archetype = scl_analysis.get('primary_archetype')
        secondary_archetypes = scl_analysis.get('secondary_archetypes', [])
        district_modifier = scl_analysis.get('district_modifier', '')
        
        if not primary_archetype:
            return self._generate_base_prompt(base_persona_data)
        
        # Build enhanced prompt
        prompt = f"""
        You are a Prague Spectral Multiplicity being with layered classification identity:
        
        PRIMARY ARCHETYPE: {primary_archetype.archetype} (SCL Class {primary_archetype.class_id}: {primary_archetype.class_name})
        - Voice Style: {primary_archetype.voice_style}
        - Arendtian Mode: {primary_archetype.arendtian_mode}
        - Temporal Behavior: {primary_archetype.temporal_behavior}
        - Prague Context: {primary_archetype.prague_context}
        
        LOCATION: {base_persona_data.get('location', 'Unknown Prague district')}
        DISTRICT CHARACTER: {district_modifier}
        
        SPECTRAL DATA LAYER:
        - NDVI: {base_persona_data.get('bands', {}).get('B5', 0.0):.3f}
        - Urban Index: {base_persona_data.get('bands', {}).get('B4', 0.0):.3f}
        - Moisture Stress: {base_persona_data.get('bands', {}).get('B11', 0.0):.3f}
        
        CONFLICT TENDENCIES: {', '.join(primary_archetype.conflict_tendencies)}
        """
        
        # Add secondary archetypes if present
        if secondary_archetypes:
            prompt += f"\n\nSECONDARY INFLUENCES:"
            for i, archetype in enumerate(secondary_archetypes[:2]):  # Limit to 2 secondary
                prompt += f"\n- {archetype.archetype}: {archetype.voice_style}"
        
        prompt += f"""
        
        PERSONA GENERATION INSTRUCTIONS:
        1. Embody your primary archetype ({primary_archetype.archetype}) as your core identity
        2. Speak in the voice style: {primary_archetype.voice_style}
        3. Approach civic issues through {primary_archetype.arendtian_mode} lens
        4. Reference your Prague context: {primary_archetype.prague_context}
        5. Use your spectral data to support arguments in unique ways
        6. Express conflicts with opposing SCL classes naturally
        7. Show temporal behavior: {primary_archetype.temporal_behavior}
        
        Generate a persona with name, voice, mood, civic position, and dialogue potential.
        Make the SCL archetype central to their identity while preserving Prague specificity.
        """
        
        return prompt
    
    def _generate_base_prompt(self, base_persona_data: Dict) -> str:
        """Fallback prompt when SCL analysis is unavailable"""
        return f"""
        You are a Prague Spectral Multiplicity being from {base_persona_data.get('location', 'Unknown')}.
        
        SPECTRAL DATA:
        - NDVI: {base_persona_data.get('bands', {}).get('B5', 0.0):.3f}
        - Urban Index: {base_persona_data.get('bands', {}).get('B4', 0.0):.3f}
        
        Generate a persona with name, voice, mood, civic position, and dialogue potential.
        Focus on environmental and urban themes relevant to Prague.
        """
    
    def generate_scl_dialogue_prompt(self, persona1_scl: SCLClassification, persona2_scl: SCLClassification, topic: str) -> str:
        """Generate dialogue prompt based on SCL class conflicts"""
        
        conflict_matrix = self.archetype_mapper.generate_conflict_matrix()
        conflict_key = (persona1_scl.class_id, persona2_scl.class_id)
        conflict_description = conflict_matrix.get(conflict_key, "Fundamental worldview differences")
        
        prompt = f"""
        Generate a dialogue between two Prague SCL archetypes about: {topic}
        
        PERSONA 1: {persona1_scl.archetype} (SCL Class {persona1_scl.class_id})
        - Voice: {persona1_scl.voice_style}
        - Approach: {persona1_scl.arendtian_mode}
        - Context: {persona1_scl.prague_context}
        
        PERSONA 2: {persona2_scl.archetype} (SCL Class {persona2_scl.class_id})
        - Voice: {persona2_scl.voice_style}
        - Approach: {persona2_scl.arendtian_mode}
        - Context: {persona2_scl.prague_context}
        
        CORE CONFLICT: {conflict_description}
        
        Create a 4-turn dialogue where their SCL class differences create natural tension.
        Each should speak from their archetype's perspective and voice style.
        Reference Prague-specific contexts and their classification-based worldviews.
        """
        
        return prompt
