#!/usr/bin/env python3
"""
Unified Persona System for Prague Spectral Multiplicity Theater
Consolidates all persona generation approaches into a single, coherent system

This module provides a unified interface to all persona generation methods:
1. Spectral Multiplicity (Primary) - Sophisticated Prague district avatars
2. Arendtian Civic Assembly - Philosophical civic personas
3. Classic Mystical - Traditional spectral band entities
4. Image-Based - Direct satellite image analysis

The system automatically selects the best approach based on available data and user preferences.
"""

import os
import json
import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Import all persona systems
from .spectral_multiplicity_notebook import (
    SpectralMultiplicityPipeline, 
    GPT4oPersonaGenerator,
    GeneratedPersona as SpectralPersona,
    SpectralTile,
    PragueDistrictMapper
)
from .arendtian_personas import ArendtianPersonaGenerator, ArendtianPersona, CivicAssembly
from .classic_personas import ClassicPersonaGenerator, ClassicPersona, SpectralEnsemble
from .integrated_image_personas import ImagePersonaGenerator, ImageBasedPersona

# Import configuration
from ..config import get_config

# Import error handling system
from ..error_handling.unified_error_manager import (
    error_handler, 
    with_fallback, 
    PersonaGenerationError,
    APIError,
    EmergencyTheaterMode
)

logger = logging.getLogger(__name__)

@dataclass
class UnifiedPersona:
    """Unified persona representation that can hold any persona type"""
    name: str
    location: str
    voice: str
    mood: str
    arendtian_mode: str
    persona_type: str  # 'spectral_multiplicity', 'arendtian', 'classic', 'image_based'
    
    # Core attributes (present in all types)
    civic_conflict: str = ""
    dialogue_potential: str = ""
    temporal_status: str = "stable"
    
    # Extended attributes (from Spectral Multiplicity)
    district_soul: str = ""
    street_wisdom: str = ""
    urban_humor: str = ""
    arendtian_insight: str = ""
    city_memory: str = ""
    spectral_nickname: str = ""
    
    # Spectral data
    dominant_indices: Dict[str, float] = None
    spectral_signature: Dict[str, Any] = None
    
    # Original persona object for advanced operations
    original_persona: Any = None
    
    def __post_init__(self):
        if self.dominant_indices is None:
            self.dominant_indices = {}
        if self.spectral_signature is None:
            self.spectral_signature = {}

class UnifiedPersonaSystem:
    """
    Unified system that manages all persona generation approaches
    Automatically selects the best method based on configuration and data availability
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.config = get_config()
        self.api_key = api_key or self.config.openai_api_key
        
        # Initialize all persona generators
        self._init_generators()
        
        # Track active personas
        self.active_personas: List[UnifiedPersona] = []
        self.session_history: List[Dict] = []
        
        logger.info(f"Unified Persona System initialized with mode: {self.config.persona_generation_mode}")
    
    def _init_generators(self):
        """Initialize all persona generation systems"""
        try:
            # Primary system: Spectral Multiplicity
            if self.api_key:
                self.spectral_multiplicity = SpectralMultiplicityPipeline(self.api_key)
                self.spectral_generator = GPT4oPersonaGenerator(self.api_key)
                logger.info("✅ Spectral Multiplicity system initialized")
            else:
                self.spectral_multiplicity = None
                self.spectral_generator = None
                logger.warning("⚠️ Spectral Multiplicity disabled - no API key")
            
            # Secondary systems
            self.arendtian_generator = ArendtianPersonaGenerator(self.api_key)
            self.classic_generator = ClassicPersonaGenerator(self.api_key)
            
            # Image-based system (requires images directory)
            if self.config.images_dir.exists():
                self.image_generator = ImagePersonaGenerator(
                    self.api_key or "", 
                    str(self.config.images_dir)
                )
                logger.info("✅ Image-based persona system initialized")
            else:
                self.image_generator = None
                logger.warning("⚠️ Image-based system disabled - no images directory")
                
        except Exception as e:
            logger.error(f"Error initializing persona generators: {e}")
            # Ensure we have at least basic functionality
            self.spectral_multiplicity = None
            self.spectral_generator = None
            self.arendtian_generator = ArendtianPersonaGenerator(None)  # Mock mode
            self.classic_generator = ClassicPersonaGenerator(None)  # Mock mode
            self.image_generator = None
    
    @error_handler(severity="medium", fallback_value=[])
    def generate_personas(self, 
                         spectral_data: Dict[str, Any], 
                         location: Dict[str, float],
                         persona_type: Optional[str] = None,
                         count: int = 1) -> List[UnifiedPersona]:
        """
        Generate personas using the unified system
        
        Args:
            spectral_data: Spectral band data and indices
            location: Geographic coordinates and location info
            persona_type: Force specific type ('spectral_multiplicity', 'arendtian', 'classic', 'image_based')
            count: Number of personas to generate
            
        Returns:
            List of unified personas
        """
        
        # Determine which system to use
        if persona_type:
            selected_type = persona_type
        else:
            selected_type = self._select_optimal_persona_type(spectral_data, location)
        
        logger.info(f"Generating {count} personas using {selected_type} system")
        
        personas = []
        
        try:
            if selected_type == "template" and self.spectral_generator:
                personas = self._generate_template_personas(spectral_data, location, count)
            
            elif selected_type == "spectral_multiplicity" and self.spectral_multiplicity:
                personas = self._generate_spectral_multiplicity_personas(spectral_data, location, count)
            
            elif selected_type == "arendtian":
                personas = self._generate_arendtian_personas(spectral_data, location, count)
            
            elif selected_type == "classic":
                personas = self._generate_classic_personas(spectral_data, location, count)
            
            elif selected_type == "image_based" and self.image_generator:
                personas = self._generate_image_based_personas(spectral_data, location, count)
            
            else:
                # Fallback to available system
                logger.warning(f"Requested type {selected_type} not available, using fallback")
                personas = self._generate_fallback_personas(spectral_data, location, count)
        
        except Exception as e:
            logger.error(f"Error generating {selected_type} personas: {e}")
            # Try fallback
            personas = self._generate_fallback_personas(spectral_data, location, count)
        
        # Add to active personas and session history
        self.active_personas.extend(personas)
        self._record_generation_session(personas, spectral_data, location, selected_type)
        
        return personas
    
    def _select_optimal_persona_type(self, spectral_data: Dict, location: Dict) -> str:
        """Intelligently select the best persona generation approach"""
        
        # Check configuration preference
        config_mode = self.config.persona_generation_mode.lower()
        
        if config_mode == "template" and self.spectral_generator:
            return "template"
        elif config_mode == "spectral_multiplicity" and self.spectral_multiplicity:
            return "spectral_multiplicity"
        
        # Check if we have Prague-specific location data
        location_name = location.get("name", "").lower()
        prague_keywords = ["prague", "praha", "letna", "vinohrady", "vltava", "wenceslas", "charles"]
        
        if any(keyword in location_name for keyword in prague_keywords):
            # For Prague locations, prefer template system for cleaner generation
            if self.spectral_generator:
                return "template"
            elif self.spectral_multiplicity:
                return "spectral_multiplicity"
        
        # Check data richness
        if isinstance(spectral_data, dict):
            band_count = len([k for k in spectral_data.keys() if k.startswith('B')])
            indices_count = len([k for k in spectral_data.keys() if k in ['NDVI', 'NDWI', 'UI', 'MSI']])
            
            if band_count >= 8 and indices_count >= 3:
                # Rich data - prefer template system for better results
                if self.spectral_generator:
                    return "template"
                elif self.spectral_multiplicity:
                    return "spectral_multiplicity"
                else:
                    return "arendtian"
            elif band_count >= 4:
                return "classic"
        
        # Default fallback - prefer template if available
        if self.spectral_generator:
            return "template"
        elif self.api_key:
            return "arendtian"
        else:
            return "classic"
    
    def _generate_spectral_multiplicity_personas(self, spectral_data: Dict, location: Dict, count: int) -> List[UnifiedPersona]:
        """Generate personas using the sophisticated Spectral Multiplicity system"""
        
        # Convert data to format expected by Spectral Multiplicity
        location_name = location.get("name", "unknown_location")
        lat = location.get("lat", 50.0755)
        lon = location.get("lon", 14.4378)
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract bands from spectral data
        bands = {}
        for key, value in spectral_data.items():
            if key.startswith('B') and isinstance(value, (int, float)):
                bands[key] = float(value)
        
        # Require real spectral bands - no approximation from indices
        if not bands:
            logger.error(f"No real spectral bands available for {location_name}")
            return self._generate_fallback_personas(spectral_data, location, count)
        
        # Create district data for processing
        district_data = [{
            "location": location_name,
            "lat": lat,
            "lon": lon,
            "date": date,
            "bands": bands
        }]
        
        # Generate using Spectral Multiplicity pipeline
        spectral_personas = self.spectral_multiplicity.process_prague_districts(district_data)
        
        # Convert to unified format
        unified_personas = []
        for sp in spectral_personas[:count]:
            unified = UnifiedPersona(
                name=sp.name,
                location=sp.location,
                voice=sp.voice,
                mood=sp.mood,
                arendtian_mode=sp.arendtian_mode,
                persona_type="spectral_multiplicity",
                civic_conflict=sp.civic_conflict,
                dialogue_potential=sp.dialogue_potential,
                temporal_status=sp.temporal_status,
                district_soul=sp.district_soul,
                street_wisdom=sp.street_wisdom,
                urban_humor=sp.urban_humor,
                arendtian_insight=sp.arendtian_insight,
                city_memory=sp.city_memory,
                spectral_nickname=sp.spectral_nickname,
                dominant_indices=sp.dominant_indices,
                spectral_signature={"bands": bands, "type": "spectral_multiplicity"},
                original_persona=sp
            )
            unified_personas.append(unified)
        
        return unified_personas
    
    def _generate_template_personas(self, spectral_data: Dict, location: Dict, count: int) -> List[UnifiedPersona]:
        """Generate personas using the elegant template-based system"""
        
        if not self.spectral_generator:
            logger.warning("Template generation requires spectral generator with API key")
            return self._generate_fallback_personas(spectral_data, location, count)
        
        # Convert data to format expected by template system
        location_name = location.get("name", "unknown_location")
        lat = location.get("lat", 50.0755)
        lon = location.get("lon", 14.4378)
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Extract bands from spectral data
        bands = {}
        for key, value in spectral_data.items():
            if key.startswith('B') and isinstance(value, (int, float)):
                bands[key] = float(value)
        
        # Require real spectral bands - no approximation from indices
        if not bands:
            logger.error(f"No real spectral bands available for template generation at {location_name}")
            return self._generate_fallback_personas(spectral_data, location, count)
        
        try:
            # Create spectral tile for template generation
            tile = self.spectral_generator.create_spectral_tile(
                location=location_name,
                lat=lat,
                lon=lon,
                date=date,
                bands=bands
            )
            
            # Generate using template system
            template_personas = self.spectral_generator.generate_template_persona(tile)
            
            # Convert to unified format
            unified_personas = []
            for tp in template_personas[:count]:
                unified = UnifiedPersona(
                    name=tp.name,
                    location=tp.location,
                    voice=tp.voice,
                    mood=tp.mood,
                    arendtian_mode=tp.arendtian_mode,
                    persona_type="template",
                    civic_conflict=tp.civic_conflict,
                    dialogue_potential=tp.dialogue_potential,
                    temporal_status=tp.temporal_status,
                    district_soul=tp.district_soul,
                    street_wisdom=tp.street_wisdom,
                    urban_humor=tp.urban_humor,
                    arendtian_insight=tp.arendtian_insight,
                    city_memory=tp.city_memory,
                    spectral_nickname=tp.spectral_nickname,
                    dominant_indices=tp.dominant_indices,
                    spectral_signature={"bands": bands, "type": "template"},
                    original_persona=tp
                )
                unified_personas.append(unified)
            
            logger.info(f"Generated {len(unified_personas)} template personas for {location_name}")
            return unified_personas
            
        except Exception as e:
            logger.error(f"Template generation failed for {location_name}: {e}")
            return self._generate_fallback_personas(spectral_data, location, count)
    
    def _generate_arendtian_personas(self, spectral_data: Dict, location: Dict, count: int) -> List[UnifiedPersona]:
        """Generate personas using the enhanced Arendtian civic system with image integration"""
        
        # Check if we have image-based spectral data for enhanced generation
        if hasattr(spectral_data, 'image_types') or 'image_types' in spectral_data:
            # Use the new image-based Arendtian generation
            try:
                assembly = self.arendtian_generator.generate_civic_assembly_from_image_data(
                    spectral_data, location, datetime.now().strftime("%Y-%m-%d")
                )
            except Exception as e:
                logger.warning(f"Image-based Arendtian generation failed: {e}, falling back to standard")
                assembly = self.arendtian_generator.generate_civic_assembly(spectral_data, location)
        else:
            # Use standard Arendtian generation
            assembly = self.arendtian_generator.generate_civic_assembly(spectral_data, location)
        
        # Convert assembly members to unified format
        unified_personas = []
        members = [assembly.plurality_leader, assembly.dissenting_voice, assembly.mediating_presence]
        
        # Add spectral witnesses if available
        if hasattr(assembly, 'spectral_witnesses') and assembly.spectral_witnesses:
            members.extend(assembly.spectral_witnesses[:count-3])  # Add remaining slots
        
        for i, member in enumerate(members[:count]):
            if member:
                # Enhanced conversion with image-based data
                dominant_indices = {}
                spectral_signature = {"type": "arendtian"}
                
                # Extract spectral data if available from image-based generation
                if hasattr(member, 'dominant_band') and member.dominant_band:
                    if member.dominant_band in spectral_data:
                        dominant_indices[member.dominant_band] = spectral_data[member.dominant_band]
                    spectral_signature["dominant_band"] = member.dominant_band
                
                # Enhanced persona with image metadata integration
                unified = UnifiedPersona(
                    name=member.name,
                    location=location.get("name", "Unknown"),
                    voice=member.voice,
                    mood=member.utterance if hasattr(member, 'utterance') else "Contemplative civic engagement",
                    arendtian_mode=member.arendtian_mode,
                    persona_type="arendtian_enhanced",
                    civic_conflict=member.political_stance if hasattr(member, 'political_stance') else "Environmental stewardship",
                    dialogue_potential=f"Engages through {member.arendtian_mode} mode with spectral awareness",
                    temporal_presence=member.temporal_presence if hasattr(member, 'temporal_presence') else "stable",
                    district_soul=f"Civic representative of {member.arendtian_mode} consciousness",
                    street_wisdom=member.utterance if hasattr(member, 'utterance') else member.voice,
                    urban_humor="Philosophical wit with environmental awareness",
                    arendtian_insight=f"Deep {member.arendtian_mode} perspective on civic ecology",
                    city_memory="Historical civic memory integrated with spectral data",
                    spectral_nickname=f"The {member.arendtian_mode} Guardian",
                    dominant_indices=dominant_indices,
                    spectral_signature=spectral_signature,
                    original_persona=member
                )
                unified_personas.append(unified)
        
        return unified_personas
    
    def _generate_classic_personas(self, spectral_data: Dict, location: Dict, count: int) -> List[UnifiedPersona]:
        """Generate personas using the classic mystical system"""
        
        # Generate spectral ensemble
        ensemble = self.classic_generator.generate_spectral_ensemble(spectral_data, location)
        
        # Convert ensemble members to unified format
        unified_personas = []
        members = [ensemble.dominant_agent, ensemble.conflicting_agent, ensemble.supporting_agent]
        
        for i, member in enumerate(members[:count]):
            if member:
                unified = UnifiedPersona(
                    name=member.name,
                    location=location.get("name", "Unknown"),
                    voice=member.voice,
                    mood=member.temporal_role,
                    arendtian_mode="Thinking",  # Default for mystical entities
                    persona_type="classic",
                    civic_conflict=member.micro_warning,
                    dialogue_potential=f"Mystical communication through {member.spectral_band}",
                    temporal_status=member.temporal_role,
                    district_soul=f"Mystical essence of {member.spectral_band}",
                    street_wisdom=member.micro_memory,
                    urban_humor="Mystical humor",
                    arendtian_insight="Spectral contemplation",
                    city_memory=member.micro_memory,
                    spectral_nickname=f"The {member.spectral_band} Spirit",
                    dominant_indices={member.spectral_band: member.band_intensity},
                    spectral_signature={"type": "classic", "band": member.spectral_band},
                    original_persona=member
                )
                unified_personas.append(unified)
        
        return unified_personas
    
    def _generate_image_based_personas(self, spectral_data: Dict, location: Dict, count: int) -> List[UnifiedPersona]:
        """Generate personas using the image-based system"""
        
        # This would require actual image data - simplified for now
        logger.warning("Image-based persona generation not fully implemented in unified system")
        return self._generate_fallback_personas(spectral_data, location, count)
    
    def _generate_fallback_personas(self, spectral_data: Dict, location: Dict, count: int) -> List[UnifiedPersona]:
        """Generate basic fallback personas when other systems fail"""
        
        location_name = location.get("name", "Unknown Location")
        
        fallback_personas = []
        for i in range(count):
            persona = UnifiedPersona(
                name=f"Avatar of {location_name} #{i+1}",
                location=location_name,
                voice=f"I am the spectral consciousness of {location_name}, speaking through electromagnetic wisdom.",
                mood="Contemplative and observant",
                arendtian_mode="Thinking",
                persona_type="fallback",
                civic_conflict="Balancing urban development with natural harmony",
                dialogue_potential="Engages through spectral awareness",
                temporal_status="stable",
                district_soul=f"The essential character of {location_name}",
                street_wisdom="Knowledge gained through spectral observation",
                urban_humor="Witty observations about urban life",
                arendtian_insight="Deep contemplative perspective",
                city_memory="Historical memory of this place",
                spectral_nickname="The Fallback Spirit",
                dominant_indices={"fallback_index": 0.5},
                spectral_signature={"type": "fallback"}
            )
            fallback_personas.append(persona)
        
        return fallback_personas
    
    def generate_dialogue(self, 
                         personas: List[UnifiedPersona], 
                         citizen_question: str,
                         dialogue_type: str = "group") -> Dict[str, Any]:
        """Generate dialogue between personas using the appropriate system"""
        
        if not personas:
            return {"error": "No personas provided for dialogue"}
        
        # Determine which dialogue system to use based on persona types
        primary_type = personas[0].persona_type
        
        try:
            if primary_type == "spectral_multiplicity" and len(personas) >= 2:
                # Use sophisticated Spectral Multiplicity dialogue
                original_personas = [p.original_persona for p in personas if p.original_persona]
                if len(original_personas) >= 2:
                    dialogue_system = self.spectral_multiplicity.dialogue_system
                    if dialogue_type == "group":
                        return dialogue_system.generate_group_dialogue(original_personas, citizen_question)
                    else:
                        return dialogue_system.generate_inter_district_dialogue(
                            original_personas[0], original_personas[1], citizen_question
                        )
            
            elif primary_type == "arendtian" and self.arendtian_generator:
                # Use Arendtian assembly deliberation
                # This would require reconstructing the assembly - simplified for now
                pass
            
            elif primary_type == "classic" and self.classic_generator:
                # Use classic ensemble dialogue
                # This would require reconstructing the ensemble - simplified for now
                pass
        
        except Exception as e:
            logger.error(f"Error generating {primary_type} dialogue: {e}")
        
        # Fallback: Generate simple dialogue
        return self._generate_simple_dialogue(personas, citizen_question)
    
    def _generate_simple_dialogue(self, personas: List[UnifiedPersona], citizen_question: str) -> Dict[str, Any]:
        """Generate simple dialogue when advanced systems aren't available"""
        
        dialogue_turns = []
        for i, persona in enumerate(personas[:4]):  # Limit to 4 speakers
            response = f"{persona.name}: {persona.voice} Regarding your question about '{citizen_question}', I believe we must consider {persona.civic_conflict}."
            dialogue_turns.append({
                "speaker": persona.name,
                "dialogue": response
            })
        
        return {
            "group_conversation": dialogue_turns,
            "group_dynamic": f"Collaborative discussion between {len(personas)} personas",
            "collective_insight": "Unified perspective on the citizen's question",
            "humor_highlights": "Gentle humor throughout the conversation"
        }
    
    def _record_generation_session(self, personas: List[UnifiedPersona], spectral_data: Dict, location: Dict, persona_type: str):
        """Record the generation session for analytics and export"""
        
        session_record = {
            "timestamp": datetime.now().isoformat(),
            "persona_type": persona_type,
            "location": location,
            "spectral_data_summary": {
                "band_count": len([k for k in spectral_data.keys() if k.startswith('B')]),
                "has_indices": any(k in spectral_data for k in ['NDVI', 'NDWI', 'UI']),
                "data_richness": "high" if len(spectral_data) > 10 else "medium" if len(spectral_data) > 5 else "low"
            },
            "personas_generated": len(personas),
            "persona_names": [p.name for p in personas],
            "arendtian_modes": [p.arendtian_mode for p in personas]
        }
        
        self.session_history.append(session_record)
    
    def get_active_personas(self, persona_type: Optional[str] = None) -> List[UnifiedPersona]:
        """Get currently active personas, optionally filtered by type"""
        
        if persona_type:
            return [p for p in self.active_personas if p.persona_type == persona_type]
        return self.active_personas.copy()
    
    def clear_active_personas(self):
        """Clear all active personas"""
        self.active_personas.clear()
        logger.info("Cleared all active personas")
    
    def export_session(self, filename: Optional[str] = None) -> str:
        """Export current session data"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"unified_persona_session_{timestamp}.json"
        
        export_data = {
            "session_metadata": {
                "timestamp": datetime.now().isoformat(),
                "system_version": "unified_persona_system_v1.0",
                "total_personas": len(self.active_personas),
                "persona_types": list(set(p.persona_type for p in self.active_personas)),
                "configuration": {
                    "persona_mode": self.config.persona_generation_mode,
                    "api_available": bool(self.api_key),
                    "systems_available": {
                        "spectral_multiplicity": bool(self.spectral_multiplicity),
                        "arendtian": bool(self.arendtian_generator),
                        "classic": bool(self.classic_generator),
                        "image_based": bool(self.image_generator)
                    }
                }
            },
            "active_personas": [asdict(p) for p in self.active_personas],
            "session_history": self.session_history
        }
        
        filepath = Path(filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Session exported to {filepath}")
        return str(filepath)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status and capabilities"""
        
        return {
            "unified_system_version": "1.0",
            "configuration": {
                "persona_mode": self.config.persona_generation_mode,
                "api_key_configured": bool(self.api_key),
                "images_directory": str(self.config.images_dir),
                "max_personas": self.config.max_personas_per_session
            },
            "available_systems": {
                "template": {
                    "available": bool(self.spectral_generator),
                    "description": "Elegant template-based Prague personas with naming directive and clean JSON output",
                    "requires_api": True,
                    "features": ["Prague toponyms", "Historical anchors", "Spectral aliases", "Arendtian modes"]
                },
                "spectral_multiplicity": {
                    "available": bool(self.spectral_multiplicity),
                    "description": "Sophisticated Prague district avatars with humor and philosophy",
                    "requires_api": True
                },
                "arendtian": {
                    "available": bool(self.arendtian_generator),
                    "description": "Philosophical civic personas based on Arendtian framework",
                    "requires_api": False
                },
                "classic": {
                    "available": bool(self.classic_generator),
                    "description": "Traditional mystical spectral band entities",
                    "requires_api": False
                },
                "image_based": {
                    "available": bool(self.image_generator),
                    "description": "Direct satellite image analysis personas",
                    "requires_api": True
                }
            },
            "active_personas": {
                "total": len(self.active_personas),
                "by_type": {
                    persona_type: len([p for p in self.active_personas if p.persona_type == persona_type])
                    for persona_type in set(p.persona_type for p in self.active_personas)
                } if self.active_personas else {}
            },
            "session_history": {
                "total_sessions": len(self.session_history),
                "recent_activity": self.session_history[-3:] if self.session_history else []
            }
        }

# Convenience functions for backward compatibility
def create_unified_system(api_key: Optional[str] = None) -> UnifiedPersonaSystem:
    """Create a unified persona system instance"""
    return UnifiedPersonaSystem(api_key)

def generate_personas_unified(spectral_data: Dict[str, Any], 
                            location: Dict[str, float],
                            persona_type: Optional[str] = None,
                            count: int = 1,
                            api_key: Optional[str] = None) -> List[UnifiedPersona]:
    """Convenience function to generate personas using the unified system"""
    
    system = UnifiedPersonaSystem(api_key)
    return system.generate_personas(spectral_data, location, persona_type, count)

# Export the main classes and functions
__all__ = [
    'UnifiedPersonaSystem',
    'UnifiedPersona', 
    'create_unified_system',
    'generate_personas_unified'
]
