"""
Mock Data Generator
Enhanced simulation of realistic satellite spectral data
"""

import random
import json
from typing import Dict, List, Optional
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockDataGenerator:
    """Generator for realistic mock satellite data"""
    
    def __init__(self):
        self.prague_districts = {
            (50.0755, 14.4378): "Old Town Square - Historical center",
            (50.0865, 14.4114): "Prague Castle - Royal complex",
            (50.0736, 14.4606): "Vinohrady - Residential district",
            (50.0521, 14.4022): "Smíchov - Industrial heritage",
            (50.1031, 14.4378): "Holešovice - Cultural revival",
            (50.0899, 14.4172): "Petřín Park - Large green space",
            (50.0761, 14.4135): "Vltava River - Water body",
        }
    
    def generate_spectral_data(self, lat: float, lon: float, date: str) -> Dict[str, float]:
        """Generate realistic mock spectral data"""
        
        # Base variation based on location
        base_variation = (hash(f"{lat:.3f}{lon:.3f}") % 100) / 100
        
        # Seasonal effects
        season_variation = self._get_seasonal_variation(date)
        
        # Land cover type effects
        land_cover_modifier = self._get_land_cover_modifier(lat, lon)
        
        # Base spectral values
        base_data = {
            "B1": 0.1 + base_variation * 0.3,
            "B2": 0.2 + base_variation * 0.4,
            "B3": 0.3 + base_variation * 0.5,
            "B4": 0.25 + base_variation * 0.4,
            "B5": 0.4 + base_variation * 0.6,
            "B6": 0.45 + base_variation * 0.5,
            "B7": 0.5 + base_variation * 0.4,
            "B8": 0.6 + base_variation * 0.3,
            "B8A": 0.65 + base_variation * 0.25,
            "B9": 0.1 + base_variation * 0.2,
            "B11": 0.3 + base_variation * 0.5,
            "B12": 0.2 + base_variation * 0.4
        }
        
        # Apply seasonal modifiers
        for band in base_data:
            if band in season_variation:
                base_data[band] = min(1.0, base_data[band] * season_variation[band])
        
        # Apply land cover modifiers
        for band in base_data:
            if band in land_cover_modifier:
                base_data[band] = min(1.0, base_data[band] * land_cover_modifier[band])
        
        # Add some realistic noise
        for band in base_data:
            noise = (random.random() - 0.5) * 0.1
            base_data[band] = max(0.0, min(1.0, base_data[band] + noise))
        
        return base_data
    
    def _get_seasonal_variation(self, date: str) -> Dict[str, float]:
        """Get seasonal modifiers for spectral bands"""
        try:
            month = int(date.split('-')[1])
        except:
            month = 6  # Default to summer
        
        if month in [12, 1, 2]:  # Winter
            return {
                "B3": 0.6,   # Less green vegetation
                "B8": 0.5,   # Lower NIR from vegetation
                "B11": 1.2,  # More visible soil/built surfaces
                "B12": 1.1   # More mineral signatures
            }
        elif month in [3, 4, 5]:  # Spring
            return {
                "B3": 1.3,   # Spring greening
                "B8": 1.1,   # Increasing vegetation
                "B5": 1.2,   # Red edge activity
                "B6": 1.15,  # Red edge activity
                "B7": 1.1    # Red edge activity
            }
        elif month in [6, 7, 8]:  # Summer
            return {
                "B8": 1.4,   # Peak vegetation
                "B3": 1.2,   # Green vegetation
                "B11": 0.7,  # Less visible soil
                "B9": 1.3    # More water vapor
            }
        else:  # Autumn
            return {
                "B4": 1.2,   # Autumn reds
                "B8": 0.8,   # Declining vegetation
                "B3": 0.9,   # Less green
                "B11": 1.1   # More visible soil
            }
    
    def _get_land_cover_modifier(self, lat: float, lon: float) -> Dict[str, float]:
        """Get land cover modifiers based on location"""
        
        # Determine land cover type based on proximity to known landmarks
        land_cover_type = self._classify_land_cover(lat, lon)
        
        if land_cover_type == "water":
            return {
                "B2": 1.5,   # High blue reflectance
                "B3": 1.3,   # High green reflectance
                "B8": 0.3,   # Very low NIR
                "B11": 0.2,  # Very low SWIR
                "B12": 0.2   # Very low SWIR
            }
        elif land_cover_type == "urban":
            return {
                "B11": 1.3,  # High SWIR from buildings
                "B12": 1.4,  # High SWIR from concrete
                "B8": 0.7,   # Lower NIR
                "B3": 0.8,   # Less vegetation
                "B4": 1.1    # Urban red signatures
            }
        elif land_cover_type == "vegetation":
            return {
                "B8": 1.6,   # Very high NIR
                "B3": 1.4,   # High green
                "B5": 1.3,   # High red edge
                "B6": 1.25,  # High red edge
                "B7": 1.2,   # High red edge
                "B11": 0.6,  # Low SWIR (high water content)
                "B4": 0.8    # Lower red (chlorophyll absorption)
            }
        else:  # mixed urban
            return {
                "B8": 1.1,   # Moderate NIR
                "B3": 1.0,   # Moderate green
                "B11": 1.1,  # Moderate SWIR
                "B4": 1.0    # Moderate red
            }
    
    def _classify_land_cover(self, lat: float, lon: float) -> str:
        """Classify land cover type based on coordinates"""
        
        # Distance to Vltava River
        river_distance = ((lat - 50.0761)**2 + (lon - 14.4135)**2)**0.5
        if river_distance < 0.005:
            return "water"
        
        # Distance to Petřín Park
        park_distance = ((lat - 50.0899)**2 + (lon - 14.4172)**2)**0.5
        if park_distance < 0.01:
            return "vegetation"
        
        # Distance to Old Town (high density urban)
        oldtown_distance = ((lat - 50.0755)**2 + (lon - 14.4378)**2)**0.5
        if oldtown_distance < 0.008:
            return "urban"
        
        # Default to mixed urban
        return "mixed"
    
    def get_enhanced_metadata(self, lat: float, lon: float, date: str) -> Dict[str, str]:
        """Get enhanced metadata for mock data"""
        
        # Find closest landmark
        closest_landmark = None
        min_distance = float('inf')
        
        for coords, description in self.prague_districts.items():
            distance = ((lat - coords[0])**2 + (lon - coords[1])**2)**0.5
            if distance < min_distance:
                min_distance = distance
                closest_landmark = description
        
        return {
            "source": "enhanced_mock",
            "data_quality": "simulated",
            "closest_landmark": closest_landmark,
            "land_cover": self._classify_land_cover(lat, lon),
            "seasonal_context": self._get_seasonal_context(date),
            "generation_method": "algorithmic_simulation"
        }
    
    def _get_seasonal_context(self, date: str) -> str:
        """Get seasonal context description"""
        try:
            month = int(date.split('-')[1])
        except:
            return "unknown_season"
        
        if month in [12, 1, 2]:
            return "winter_dormancy"
        elif month in [3, 4, 5]:
            return "spring_awakening"
        elif month in [6, 7, 8]:
            return "summer_peak"
        else:
            return "autumn_transition" 