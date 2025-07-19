"""
TIFF Persona Extractor
Extracts metadata from satellite TIFF files to generate spectral band personas
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import logging

# Mock rasterio for development - replace with actual rasterio in production
class MockRasterio:
    @staticmethod
    def open(path):
        return MockDataset(path)

class MockDataset:
    def __init__(self, path):
        self.path = path
        self.bounds = (14.4, 50.0, 14.5, 50.1)  # Prague area bounds
        self.crs = "EPSG:4326"
        self.count = 12  # 12 spectral bands
        
    def read(self, band_num):
        # Generate realistic mock spectral data
        np.random.seed(42 + band_num)
        if band_num == 8:  # NIR band - vegetation
            return np.random.normal(0.6, 0.15, (100, 100))
        elif band_num == 11:  # SWIR1 - moisture
            return np.random.normal(0.3, 0.1, (100, 100))
        elif band_num == 12:  # SWIR2 - urban
            return np.random.normal(0.2, 0.08, (100, 100))
        else:
            return np.random.normal(0.4, 0.1, (100, 100))

try:
    import rasterio
except ImportError:
    rasterio = MockRasterio()
    logging.warning("Using mock rasterio - install rasterio for production use")

class TIFFPersonaExtractor:
    """Extracts spectral band metadata and generates persona characteristics"""
    
    BAND_DEFINITIONS = {
        "B02": {
            "name": "Blue",
            "character": "Atmospheric Witness",
            "wavelength": "490nm",
            "function": "atmospheric_clarity",
            "rhetorical_mode": "elegiac"
        },
        "B03": {
            "name": "Green", 
            "character": "Vegetation Monitor",
            "wavelength": "560nm",
            "function": "vegetation_health",
            "rhetorical_mode": "ethical_dative"
        },
        "B04": {
            "name": "Red",
            "character": "Chlorophyll Detector",
            "wavelength": "665nm", 
            "function": "photosynthesis",
            "rhetorical_mode": "forensic"
        },
        "B08": {
            "name": "NIR",
            "character": "Chlorophyll Guardian",
            "wavelength": "842nm",
            "function": "vegetation_structure",
            "rhetorical_mode": "ethical_dative"
        },
        "B11": {
            "name": "SWIR1",
            "character": "Moisture Detective", 
            "wavelength": "1610nm",
            "function": "water_stress",
            "rhetorical_mode": "forensic"
        },
        "B12": {
            "name": "SWIR2",
            "character": "Urban Critic",
            "wavelength": "2190nm",
            "function": "built_environment",
            "rhetorical_mode": "administrative"
        }
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def extract_tiff_metadata(self, tiff_path: str) -> Dict:
        """Extract basic metadata from TIFF file"""
        try:
            with rasterio.open(tiff_path) as dataset:
                metadata = {
                    "file_path": tiff_path,
                    "bounds": dataset.bounds,
                    "crs": str(dataset.crs),
                    "band_count": dataset.count,
                    "width": dataset.width,
                    "height": dataset.height,
                    "acquisition_time": self._extract_acquisition_time(tiff_path)
                }
                return metadata
        except Exception as e:
            self.logger.error(f"Error extracting TIFF metadata: {e}")
            return self._generate_mock_metadata(tiff_path)
    
    def _extract_acquisition_time(self, tiff_path: str) -> str:
        """Extract acquisition time from filename or metadata"""
        # Try to parse from filename (e.g., 2025-07-01-00_00)
        filename = os.path.basename(tiff_path)
        try:
            if "2025" in filename:
                date_part = filename.split("_")[0]
                return f"{date_part}T10:30:00Z"
        except:
            pass
        return datetime.now().isoformat() + "Z"
    
    def _generate_mock_metadata(self, tiff_path: str) -> Dict:
        """Generate mock metadata for development"""
        return {
            "file_path": tiff_path,
            "bounds": (14.4, 50.0, 14.5, 50.1),  # Prague area
            "crs": "EPSG:4326",
            "band_count": 12,
            "width": 1000,
            "height": 1000,
            "acquisition_time": "2025-07-01T10:30:00Z"
        }
    
    def extract_band_statistics(self, tiff_path: str, band_id: str) -> Dict:
        """Extract statistical information for specific spectral band"""
        try:
            with rasterio.open(tiff_path) as dataset:
                band_num = self._get_band_number(band_id)
                if band_num <= dataset.count:
                    band_data = dataset.read(band_num)
                    stats = {
                        "mean": float(np.mean(band_data)),
                        "std": float(np.std(band_data)),
                        "min": float(np.min(band_data)),
                        "max": float(np.max(band_data)),
                        "percentile_25": float(np.percentile(band_data, 25)),
                        "percentile_75": float(np.percentile(band_data, 75))
                    }
                    return stats
        except Exception as e:
            self.logger.error(f"Error extracting band statistics: {e}")
            
        return self._generate_mock_band_stats(band_id)
    
    def _get_band_number(self, band_id: str) -> int:
        """Convert band ID to band number"""
        band_mapping = {
            "B02": 2, "B03": 3, "B04": 4, "B08": 8, 
            "B11": 11, "B12": 12
        }
        return band_mapping.get(band_id, 1)
    
    def _generate_mock_band_stats(self, band_id: str) -> Dict:
        """Generate realistic mock statistics for band"""
        np.random.seed(hash(band_id) % 1000)
        
        if band_id == "B08":  # NIR - vegetation
            base_mean = 0.6
        elif band_id == "B11":  # SWIR1 - moisture
            base_mean = 0.3
        elif band_id == "B12":  # SWIR2 - urban
            base_mean = 0.2
        else:
            base_mean = 0.4
            
        return {
            "mean": base_mean + np.random.normal(0, 0.05),
            "std": 0.1 + np.random.normal(0, 0.02),
            "min": max(0, base_mean - 0.3),
            "max": min(1, base_mean + 0.3),
            "percentile_25": base_mean - 0.1,
            "percentile_75": base_mean + 0.1
        }
    
    def generate_persona_profile(self, tiff_path: str, band_id: str) -> Dict:
        """Generate complete persona profile for spectral band"""
        metadata = self.extract_tiff_metadata(tiff_path)
        band_stats = self.extract_band_statistics(tiff_path, band_id)
        band_def = self.BAND_DEFINITIONS.get(band_id, {})
        
        # Calculate spatial identity
        bounds = metadata["bounds"]
        center_lat = (bounds[1] + bounds[3]) / 2
        center_lon = (bounds[0] + bounds[2]) / 2
        
        # Determine ethical positioning based on band statistics
        ethical_intensity = self._calculate_ethical_intensity(band_stats, band_id)
        
        persona_profile = {
            "band_id": band_id,
            "band_name": band_def.get("name", band_id),
            "character": band_def.get("character", f"{band_id} Consciousness"),
            "rhetorical_mode": band_def.get("rhetorical_mode", "ethical_dative"),
            "wavelength": band_def.get("wavelength", "unknown"),
            "function": band_def.get("function", "spectral_observation"),
            
            # Spatial identity
            "spatial_bounds": bounds,
            "center_coordinates": [center_lat, center_lon],
            "location_name": self._get_location_name(center_lat, center_lon),
            
            # Spectral characteristics
            "spectral_statistics": band_stats,
            "ethical_intensity": ethical_intensity,
            
            # Temporal context
            "acquisition_time": metadata["acquisition_time"],
            "file_source": tiff_path,
            
            # Ethical dative positioning
            "ethical_position": self._generate_ethical_position(band_id, ethical_intensity),
            
            # Voice characteristics
            "voice_patterns": self._generate_voice_patterns(band_id, ethical_intensity)
        }
        
        return persona_profile
    
    def _calculate_ethical_intensity(self, band_stats: Dict, band_id: str) -> float:
        """Calculate how intensely the band is affected by environmental changes"""
        mean_val = band_stats["mean"]
        std_val = band_stats["std"]
        
        # Higher standard deviation indicates more variation/stress
        # Band-specific thresholds for what constitutes "stress"
        if band_id == "B08":  # Vegetation health
            stress_threshold = 0.5
            intensity = max(0, (stress_threshold - mean_val) / stress_threshold)
        elif band_id == "B11":  # Water stress
            stress_threshold = 0.4
            intensity = max(0, (stress_threshold - mean_val) / stress_threshold)
        elif band_id == "B12":  # Urban pressure
            intensity = min(1, mean_val / 0.3)  # Higher values = more urban pressure
        else:
            intensity = std_val * 2  # General variability as stress indicator
            
        return min(1.0, max(0.0, intensity))
    
    def _get_location_name(self, lat: float, lon: float) -> str:
        """Generate location name based on coordinates"""
        # Prague district mapping (simplified)
        if 50.08 <= lat <= 50.09 and 14.43 <= lon <= 14.44:
            return "Nusle Basin"
        elif 50.07 <= lat <= 50.08 and 14.41 <= lon <= 14.43:
            return "Vinohrady District"
        elif 50.09 <= lat <= 50.10 and 14.40 <= lon <= 14.42:
            return "Letná Park Area"
        else:
            return f"Prague Sector ({lat:.3f}, {lon:.3f})"
    
    def _generate_ethical_position(self, band_id: str, intensity: float) -> Dict:
        """Generate ethical dative positioning for the band"""
        positions = {
            "B02": {
                "czech": "Mlha se usazuje—na mně",
                "english": "The haze settles—on me",
                "german": "Der Dunst setzt sich—mir ab"
            },
            "B08": {
                "czech": "Listy žloutnou—na mně", 
                "english": "The leaves yellow—on me",
                "german": "Die Blätter vergilben—mir"
            },
            "B11": {
                "czech": "Voda mizí—na mně",
                "english": "The water disappears—on me", 
                "german": "Das Wasser verschwindet—mir"
            },
            "B12": {
                "czech": "Beton se šíří—na mně",
                "english": "The concrete spreads—on me",
                "german": "Der Beton breitet sich—mir aus"
            }
        }
        
        base_position = positions.get(band_id, {
            "czech": f"Změny se dějí—na mně",
            "english": f"Changes happen—on me", 
            "german": f"Veränderungen geschehen—mir"
        })
        
        # Modify intensity based on ethical intensity
        if intensity > 0.7:
            intensity_modifier = {
                "czech": " rychle",
                "english": " rapidly", 
                "german": " schnell"
            }
        elif intensity > 0.4:
            intensity_modifier = {
                "czech": " postupně",
                "english": " gradually",
                "german": " allmählich"
            }
        else:
            intensity_modifier = {
                "czech": " pomalu",
                "english": " slowly",
                "german": " langsam"
            }
            
        return {
            lang: pos + intensity_modifier[lang] 
            for lang, pos in base_position.items()
        }
    
    def _generate_voice_patterns(self, band_id: str, intensity: float) -> Dict:
        """Generate voice characteristics for the persona"""
        base_patterns = {
            "B02": {"tone": "melancholic", "pace": "slow", "register": "poetic"},
            "B08": {"tone": "protective", "pace": "measured", "register": "caring"},
            "B11": {"tone": "urgent", "pace": "quick", "register": "investigative"},
            "B12": {"tone": "critical", "pace": "steady", "register": "administrative"}
        }
        
        pattern = base_patterns.get(band_id, {
            "tone": "neutral", "pace": "moderate", "register": "observational"
        })
        
        # Modify based on ethical intensity
        if intensity > 0.7:
            pattern["urgency"] = "high"
            pattern["emotional_charge"] = "intense"
        elif intensity > 0.4:
            pattern["urgency"] = "moderate"
            pattern["emotional_charge"] = "concerned"
        else:
            pattern["urgency"] = "low"
            pattern["emotional_charge"] = "calm"
            
        return pattern
    
    def extract_all_personas(self, tiff_path: str) -> List[Dict]:
        """Extract multiple personas from single TIFF - spectral, spatial, temporal, and role-based"""
        personas = []
        
        # Extract basic metadata
        metadata = self.extract_tiff_metadata(tiff_path)
        
        # 1. Spectral Layer Personas (one per band)
        for band_id in self.BAND_DEFINITIONS.keys():
            try:
                spectral_persona = self.generate_persona_profile(tiff_path, band_id)
                spectral_persona["persona_type"] = "spectral_layer"
                spectral_persona["voice_mode"] = "ethical_dative"
                personas.append(spectral_persona)
            except Exception as e:
                self.logger.error(f"Error generating spectral persona for {band_id}: {e}")
        
        # 2. Spatial Region Personas (different areas of the image)
        spatial_personas = self._generate_spatial_region_personas(tiff_path, metadata)
        personas.extend(spatial_personas)
        
        # 3. Temporal Memory Personas (archive voices)
        temporal_personas = self._generate_temporal_memory_personas(tiff_path, metadata)
        personas.extend(temporal_personas)
        
        # 4. Role-based Personas (bureaucratic classifiers)
        role_personas = self._generate_role_based_personas(tiff_path, metadata)
        personas.extend(role_personas)
                
        return personas
    
    def _generate_spatial_region_personas(self, tiff_path: str, metadata: Dict) -> List[Dict]:
        """Generate personas for different spatial regions within the image"""
        spatial_personas = []
        
        # Define spatial regions (corners, center, edges)
        regions = {
            "forest_edge": {
                "character": "Sentinel of the Transition Zone",
                "location_description": "Forest-urban boundary",
                "voice_mode": "ethical_dative",
                "spatial_focus": "edge_dynamics"
            },
            "urban_center": {
                "character": "Reflector of Neglected Surfaces",
                "location_description": "Dense urban core",
                "voice_mode": "technical",
                "spatial_focus": "urban_intensity"
            },
            "water_depression": {
                "character": "Sponge of Forgotten Waters",
                "location_description": "Wet depression area",
                "voice_mode": "ethical_dative",
                "spatial_focus": "moisture_retention"
            }
        }
        
        for region_id, region_config in regions.items():
            spatial_persona = {
                "band_id": f"SPATIAL_{region_id.upper()}",
                "band_name": region_id.replace("_", " ").title(),
                "character": region_config["character"],
                "persona_type": "spatial_region",
                "voice_mode": region_config["voice_mode"],
                "spatial_focus": region_config["spatial_focus"],
                "location_description": region_config["location_description"],
                "file_source": tiff_path,
                "acquisition_time": metadata["acquisition_time"],
                "spatial_bounds": metadata["bounds"],
                "rhetorical_mode": "ethical_dative" if region_config["voice_mode"] == "ethical_dative" else "administrative"
            }
            spatial_personas.append(spatial_persona)
            
        return spatial_personas
    
    def _generate_temporal_memory_personas(self, tiff_path: str, metadata: Dict) -> List[Dict]:
        """Generate temporal memory personas that speak as archives"""
        temporal_personas = []
        
        # Extract date from filename or metadata
        acquisition_date = metadata.get("acquisition_time", "2025-07-01T10:30:00Z")
        
        temporal_configs = {
            "archive_witness": {
                "character": "Archive of What Was Green",
                "temporal_focus": "past_memory",
                "voice_mode": "ethical_dative"
            },
            "present_recorder": {
                "character": "Current State Documenter",
                "temporal_focus": "present_observation",
                "voice_mode": "technical"
            },
            "future_predictor": {
                "character": "Trajectory Simulator",
                "temporal_focus": "future_projection",
                "voice_mode": "mixed"
            }
        }
        
        for temporal_id, config in temporal_configs.items():
            temporal_persona = {
                "band_id": f"TEMPORAL_{temporal_id.upper()}",
                "band_name": temporal_id.replace("_", " ").title(),
                "character": config["character"],
                "persona_type": "temporal_memory",
                "voice_mode": config["voice_mode"],
                "temporal_focus": config["temporal_focus"],
                "acquisition_time": acquisition_date,
                "file_source": tiff_path,
                "spatial_bounds": metadata["bounds"],
                "rhetorical_mode": "ethical_dative" if config["voice_mode"] == "ethical_dative" else "administrative"
            }
            temporal_personas.append(temporal_persona)
            
        return temporal_personas
    
    def _generate_role_based_personas(self, tiff_path: str, metadata: Dict) -> List[Dict]:
        """Generate role-based personas (bureaucratic classifiers, witnesses, etc.)"""
        role_personas = []
        
        role_configs = {
            "scl_classifier": {
                "character": "Scene Classification Judge",
                "role_function": "classification_authority",
                "voice_mode": "technical"
            },
            "affected_citizen": {
                "character": "Affected Landscape Entity",
                "role_function": "impact_witness",
                "voice_mode": "ethical_dative"
            },
            "silent_witness": {
                "character": "Silent Data Trace",
                "role_function": "passive_recording",
                "voice_mode": "minimal"
            }
        }
        
        for role_id, config in role_configs.items():
            role_persona = {
                "band_id": f"ROLE_{role_id.upper()}",
                "band_name": role_id.replace("_", " ").title(),
                "character": config["character"],
                "persona_type": "role_based",
                "voice_mode": config["voice_mode"],
                "role_function": config["role_function"],
                "file_source": tiff_path,
                "acquisition_time": metadata["acquisition_time"],
                "spatial_bounds": metadata["bounds"],
                "rhetorical_mode": "administrative" if config["voice_mode"] == "technical" else "ethical_dative"
            }
            role_personas.append(role_persona)
            
        return role_personas
    
    def save_personas_to_json(self, personas: List[Dict], output_path: str):
        """Save persona profiles to JSON file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(personas, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Saved {len(personas)} personas to {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving personas: {e}")

if __name__ == "__main__":
    # Test the extractor
    extractor = TIFFPersonaExtractor()
    
    # Mock TIFF path for testing
    test_tiff = "images/2025-07-01-00_00/natural_color.tif"
    
    # Extract all personas
    personas = extractor.extract_all_personas(test_tiff)
    
    # Print sample persona
    if personas:
        print("Sample Persona Profile:")
        print(json.dumps(personas[0], indent=2, ensure_ascii=False))
        
    # Save to file
    extractor.save_personas_to_json(personas, "spectral_personas.json")