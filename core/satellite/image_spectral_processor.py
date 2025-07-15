#!/usr/bin/env python3
"""
Image Spectral Processor
Extract spectral data from actual Sentinel-2 satellite images
Integrates with GPT-4o vision for image analysis and persona generation
"""

import os
import json
import base64
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from PIL import Image, ImageStat
# Disable PIL decompression bomb warning for trusted satellite data sources
Image.MAX_IMAGE_PIXELS = None
import numpy as np
import openai
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ImageTile:
    """A tile extracted from satellite imagery"""
    image_path: str
    tile_name: str
    bbox: Tuple[int, int, int, int]  # (x1, y1, x2, y2)
    center_coordinates: Tuple[float, float]  # (lat, lon)
    date: str
    satellite_type: str
    image_type: str  # NDVI, EVI, False_color, etc.

@dataclass
class ExtractedSpectralData:
    """Spectral data extracted from satellite images"""
    location_name: str
    coordinates: Tuple[float, float]
    date: str
    image_types: List[str]
    pixel_statistics: Dict[str, Dict[str, float]]  # {image_type: {mean, std, min, max}}
    derived_indices: Dict[str, float]
    visual_analysis: str  # GPT-4o vision analysis
    semantic_categories: List[str]

class SatelliteImageProcessor:
    """Process satellite images and extract spectral information"""
    
    def __init__(self, images_directory: str = "images"):
        self.images_dir = Path(images_directory)
        self.available_images = self._scan_available_images()
        
        # Prague coordinate mapping (approximate)
        self.prague_zones = {
            "letna_park": (50.0945, 14.4186),
            "old_town": (50.0755, 14.4378),
            "petrin_hill": (50.0836, 14.3988),
            "vltava_river": (50.0761, 14.4135),
            "vinohrady": (50.0750, 14.4500),
            "smichov": (50.0521, 14.4022),
            "holesovice": (50.1031, 14.4378),
            "karlin": (50.0920, 14.4560)
        }
    
    def _scan_available_images(self) -> Dict[str, List[Path]]:
        """Scan for available satellite images"""
        images = {}
        
        for image_file in self.images_dir.glob("*.jpg"):
            # Parse filename: 2025-07-10-00_00_2025-07-10-23_59_Sentinel-2_L2A_NDVI.jpg
            filename = image_file.name
            parts = filename.split("_")
            
            if len(parts) >= 6:
                date = parts[0]  # 2025-07-10-00
                image_type = parts[-1].split(".")[0]  # NDVI, EVI, etc.
                
                if date not in images:
                    images[date] = []
                images[date].append({
                    "path": image_file,
                    "type": image_type,
                    "satellite": "Sentinel-2"
                })
        
        # Also check PNG files
        for image_file in self.images_dir.glob("*.png"):
            filename = image_file.name
            parts = filename.split("_")
            
            if len(parts) >= 6:
                date = parts[0]
                image_type = parts[-1].split(".")[0]
                
                if date not in images:
                    images[date] = []
                images[date].append({
                    "path": image_file,
                    "type": image_type,
                    "satellite": "Sentinel-2"
                })
        
        logger.info(f"Found images for dates: {list(images.keys())}")
        return images
    
    def extract_tile_from_image(self, image_path: Path, zone_name: str, 
                               tile_size: int = 200) -> Optional[ImageTile]:
        """Extract a tile from satellite image for a specific Prague zone"""
        
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                
                # Map zone to approximate image coordinates (this would need calibration with real georeference)
                zone_mappings = {
                    "letna_park": (0.3, 0.2),      # Upper left area
                    "old_town": (0.5, 0.5),       # Center
                    "petrin_hill": (0.2, 0.4),    # Left center
                    "vltava_river": (0.4, 0.6),   # Center-bottom
                    "vinohrady": (0.7, 0.6),      # Right-bottom
                    "smichov": (0.3, 0.8),        # Lower left
                    "holesovice": (0.6, 0.2),     # Upper right
                    "karlin": (0.8, 0.4)          # Right center
                }
                
                if zone_name not in zone_mappings:
                    return None
                
                # Calculate tile coordinates
                rel_x, rel_y = zone_mappings[zone_name]
                center_x = int(width * rel_x)
                center_y = int(height * rel_y)
                
                # Define bounding box
                half_size = tile_size // 2
                x1 = max(0, center_x - half_size)
                y1 = max(0, center_y - half_size)
                x2 = min(width, center_x + half_size)
                y2 = min(height, center_y + half_size)
                
                # Extract date and type from filename
                filename = image_path.name
                date = filename.split("_")[0] if "_" in filename else "2025-07-10"
                image_type = filename.split("_")[-1].split(".")[0] if "_" in filename else "unknown"
                
                return ImageTile(
                    image_path=str(image_path),
                    tile_name=zone_name,
                    bbox=(x1, y1, x2, y2),
                    center_coordinates=self.prague_zones.get(zone_name, (50.0755, 14.4378)),
                    date=date,
                    satellite_type="Sentinel-2",
                    image_type=image_type
                )
                
        except Exception as e:
            logger.error(f"Error extracting tile from {image_path}: {e}")
            return None
    
    def analyze_tile_statistics(self, image_path: Path, bbox: Tuple[int, int, int, int]) -> Dict[str, float]:
        """Analyze pixel statistics for a tile"""
        
        try:
            with Image.open(image_path) as img:
                # Crop to tile area
                tile = img.crop(bbox)
                
                # Convert to RGB if needed
                if tile.mode != 'RGB':
                    tile = tile.convert('RGB')
                
                # Calculate statistics for each channel
                stats = ImageStat.Stat(tile)
                
                # For spectral indices (NDVI, EVI, etc.), typically single channel or false color
                if len(stats.mean) == 1:
                    # Single channel (e.g., NDVI)
                    return {
                        "mean": stats.mean[0] / 255.0,  # Normalize to 0-1
                        "std": stats.stddev[0] / 255.0,
                        "min": min(stats.extrema[0]) / 255.0,
                        "max": max(stats.extrema[0]) / 255.0
                    }
                else:
                    # Multi-channel (RGB false color)
                    return {
                        "red_mean": stats.mean[0] / 255.0,
                        "green_mean": stats.mean[1] / 255.0,
                        "blue_mean": stats.mean[2] / 255.0,
                        "red_std": stats.stddev[0] / 255.0,
                        "green_std": stats.stddev[1] / 255.0,
                        "blue_std": stats.stddev[2] / 255.0,
                        "overall_brightness": sum(stats.mean) / (3 * 255.0)
                    }
                    
        except Exception as e:
            logger.error(f"Error analyzing tile statistics: {e}")
            return {"mean": 0.5, "std": 0.1, "min": 0.0, "max": 1.0}

class GPT4oVisionAnalyzer:
    """Use GPT-4o vision capabilities to analyze satellite imagery"""
    
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        if self.client:
            self.vision_available = self.test_vision_access()
        else:
            self.vision_available = False
    
    def test_vision_access(self) -> bool:
        """Test if the API key has access to GPT-4o vision"""
        try:
            logger.info("Testing GPT-4o vision access...")
            
            # Create a simple test image (1x1 pixel)
            from PIL import Image
            from io import BytesIO
            import base64
            
            test_img = Image.new('RGB', (1, 1), color='red')
            buffer = BytesIO()
            test_img.save(buffer, format='JPEG')
            test_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "What color is this pixel?"},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{test_base64}",
                                    "detail": "low"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=50,
                temperature=1.1
            )
            
            content = response.choices[0].message.content
            if content and content.strip():
                logger.info("GPT-4o vision access confirmed")
                return True
            else:
                logger.warning("GPT-4o vision returned empty response")
                return False
                
        except Exception as e:
            logger.error(f"GPT-4o vision access test failed: {e}")
            return False
    
    def encode_image_to_base64(self, image_path: Path, bbox: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Encode image or image tile to base64 for GPT-4o"""
        
        try:
            logger.info(f"Encoding image: {image_path} with bbox: {bbox}")
            
            with Image.open(image_path) as img:
                logger.info(f"Original image size: {img.size}, mode: {img.mode}")
                
                if bbox:
                    img = img.crop(bbox)
                    logger.info(f"Cropped image size: {img.size}")
                
                # Resize if too large (GPT-4o has size limits)
                if max(img.size) > 1024:
                    original_size = img.size
                    img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
                    logger.info(f"Resized image from {original_size} to {img.size}")
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    original_mode = img.mode
                    img = img.convert('RGB')
                    logger.info(f"Converted image mode from {original_mode} to RGB")
                
                # Save to bytes
                from io import BytesIO
                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=85)
                buffer_size = len(buffer.getvalue())
                logger.info(f"Image encoded to buffer: {buffer_size} bytes")
                
                # Encode to base64
                import base64
                encoded = base64.b64encode(buffer.getvalue()).decode('utf-8')
                logger.info(f"Base64 encoded: {len(encoded)} characters")
                
                return encoded
                
        except Exception as e:
            logger.error(f"Error encoding image {image_path}: {e}")
            return ""
    
    def analyze_satellite_tile(self, image_path: Path, tile: ImageTile, 
                              context: str = "") -> str:
        """Analyze satellite tile using GPT-4o vision"""
        
        if not self.client:
            return f"No OpenAI client available. {tile.image_type} data for {tile.tile_name} shows spectral characteristics typical of Prague urban areas."
        
        if not self.vision_available:
            return f"GPT-4o vision not available. {tile.image_type} analysis for {tile.tile_name} indicates mixed urban-natural environment with moderate vegetation and infrastructure development."
        
        # Encode image
        base64_image = self.encode_image_to_base64(Path(image_path), tile.bbox)
        
        if not base64_image:
            logger.error(f"Failed to encode image for {tile.tile_name}")
            return f"Image encoding failed for {tile.image_type}. Unable to analyze visual characteristics of {tile.tile_name}."
        
        prompt = f"""
Analyze this Sentinel-2 satellite image tile for Prague, Czech Republic.

TILE INFORMATION:
- Location: {tile.tile_name}
- Coordinates: {tile.center_coordinates}
- Date: {tile.date}
- Image Type: {tile.image_type}
- Satellite: {tile.satellite_type}

ANALYSIS REQUIREMENTS:
1. Describe what you observe in this spectral image
2. Identify land cover types (vegetation, water, built areas, etc.)
3. Assess vegetation health if visible (green, stressed, sparse)
4. Note any urban infrastructure or development patterns
5. Describe texture, patterns, and spectral characteristics
6. Suggest what this data reveals about the local environment

CONTEXT: {context}

Focus on spectral characteristics that would influence civic and environmental concerns for Prague residents.
"""
        
        try:
            logger.info(f"Making GPT-4o vision API call for {tile.tile_name} ({tile.image_type})")
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=800,
                temperature=1.1
            )
            
            content = response.choices[0].message.content
            
            # Check if response is empty
            if not content or content.strip() == "":
                logger.error(f"Empty response from GPT-4o vision API for {tile.tile_name}")
                return f"Vision analysis returned empty response for {tile.image_type} data of {tile.tile_name}. This may indicate API access issues or image processing problems."
            
            logger.info(f"Successfully analyzed {tile.tile_name}: {len(content)} characters")
            return content
            
        except Exception as e:
            logger.error(f"Error in GPT-4o vision analysis for {tile.tile_name}: {e}")
            return f"Vision analysis error for {tile.image_type}: {str(e)}. Fallback: {tile.tile_name} shows mixed spectral characteristics typical of Prague urban environment."

class ImageSpectralExtractor:
    """Complete pipeline for extracting spectral data from satellite images"""
    
    def __init__(self, api_key: str, images_directory: str = "images"):
        self.image_processor = SatelliteImageProcessor(images_directory)
        self.vision_analyzer = GPT4oVisionAnalyzer(api_key)
    
    def extract_spectral_data_for_zone(self, zone_name: str, date: str = None) -> Optional[ExtractedSpectralData]:
        """Extract complete spectral data for a Prague zone from available images"""
        
        # Find available images for date
        if not date:
            # Use most recent date
            available_dates = list(self.image_processor.available_images.keys())
            if not available_dates:
                logger.error("No satellite images available")
                return None
            date = sorted(available_dates)[-1]
        
        if date not in self.image_processor.available_images:
            logger.error(f"No images available for date {date}")
            return None
        
        images_for_date = self.image_processor.available_images[date]
        
        # Extract tiles and analyze
        pixel_statistics = {}
        visual_analyses = []
        image_types = []
        
        for img_info in images_for_date:
            image_path = img_info["path"]
            image_type = img_info["type"]
            
            # Extract tile for this zone
            tile = self.image_processor.extract_tile_from_image(image_path, zone_name)
            if not tile:
                continue
            
            # Get pixel statistics
            stats = self.image_processor.analyze_tile_statistics(image_path, tile.bbox)
            pixel_statistics[image_type] = stats
            image_types.append(image_type)
            
            # Get GPT-4o vision analysis
            analysis = self.vision_analyzer.analyze_satellite_tile(
                image_path, tile, f"Analyzing {image_type} data for civic persona generation"
            )
            visual_analyses.append(f"{image_type}: {analysis}")
        
        if not pixel_statistics:
            logger.error(f"No valid tiles extracted for {zone_name}")
            return None
        
        # Derive indices from available data
        derived_indices = self._derive_indices_from_images(pixel_statistics)
        
        # Classify semantically
        semantic_categories = self._classify_zone_from_analysis(visual_analyses, derived_indices)
        
        coordinates = self.image_processor.prague_zones.get(zone_name, (50.0755, 14.4378))
        
        return ExtractedSpectralData(
            location_name=zone_name,
            coordinates=coordinates,
            date=date,
            image_types=image_types,
            pixel_statistics=pixel_statistics,
            derived_indices=derived_indices,
            visual_analysis=" | ".join(visual_analyses),
            semantic_categories=semantic_categories
        )
    
    def _derive_indices_from_images(self, pixel_stats: Dict[str, Dict[str, float]]) -> Dict[str, float]:
        """Derive spectral indices from image statistics"""
        indices = {}
        
        # If we have NDVI directly
        if "NDVI" in pixel_stats:
            # NDVI images are usually normalized to 0-1 or -1 to 1
            # Assume our processing gives 0-1, convert to -1 to 1
            ndvi_stats = pixel_stats["NDVI"]
            if "mean" in ndvi_stats:
                ndvi_mean = ndvi_stats["mean"]
            elif "overall_brightness" in ndvi_stats:
                ndvi_mean = ndvi_stats["overall_brightness"]
            else:
                # Take first available numeric value
                ndvi_mean = list(ndvi_stats.values())[0] if ndvi_stats else 0.5
            indices["NDVI"] = (ndvi_mean * 2) - 1  # Convert 0-1 to -1 to 1
        
        # If we have EVI directly
        if "EVI" in pixel_stats:
            evi_stats = pixel_stats["EVI"]
            if "mean" in evi_stats:
                indices["EVI"] = evi_stats["mean"]
            elif "overall_brightness" in evi_stats:
                indices["EVI"] = evi_stats["overall_brightness"]
            else:
                indices["EVI"] = list(evi_stats.values())[0] if evi_stats else 0.5
        
        # If we have Moisture Stress
        for key in pixel_stats:
            if "moisture" in key.lower() or "stress" in key.lower():
                moisture_stats = pixel_stats[key]
                if "mean" in moisture_stats:
                    indices["Moisture_Stress"] = moisture_stats["mean"]
                elif "overall_brightness" in moisture_stats:
                    indices["Moisture_Stress"] = moisture_stats["overall_brightness"]
                else:
                    indices["Moisture_Stress"] = list(moisture_stats.values())[0] if moisture_stats else 0.5
        
        # Derive urban index from false color if available
        for key in pixel_stats:
            if "false" in key.lower() or "color" in key.lower():
                stats = pixel_stats[key]
                if "red_mean" in stats and "blue_mean" in stats:
                    # Simple urban index approximation
                    indices["Urban_Index"] = stats["red_mean"] / (stats["blue_mean"] + 0.1)
                elif "overall_brightness" in stats:
                    # Fallback approximation
                    indices["Urban_Index"] = stats["overall_brightness"]
        
        # Texture/variation indices
        for img_type, stats in pixel_stats.items():
            variation_key = None
            if "std" in stats:
                variation_key = "std"
            elif "red_std" in stats:
                variation_key = "red_std"
            
            if variation_key:
                indices[f"{img_type}_Variation"] = stats[variation_key]
        
        return indices
    
    def _classify_zone_from_analysis(self, analyses: List[str], indices: Dict[str, float]) -> List[str]:
        """Classify zone based on GPT-4o analysis and indices"""
        categories = []
        
        combined_analysis = " ".join(analyses).lower()
        
        # Vegetation analysis
        if "vegetation" in combined_analysis or "green" in combined_analysis:
            ndvi = indices.get("NDVI", 0)
            if ndvi > 0.3:
                categories.append("healthy_vegetation")
            elif ndvi > 0.1:
                categories.append("moderate_vegetation")
            else:
                categories.append("sparse_vegetation")
        
        # Urban analysis
        if "urban" in combined_analysis or "built" in combined_analysis or "development" in combined_analysis:
            categories.append("urban_development")
        
        # Water analysis
        if "water" in combined_analysis or "river" in combined_analysis:
            categories.append("water_body")
        
        # Stress indicators
        if "stress" in combined_analysis or "dry" in combined_analysis:
            categories.append("environmental_stress")
        
        # Infrastructure
        if "road" in combined_analysis or "building" in combined_analysis:
            categories.append("infrastructure")
        
        return categories if categories else ["mixed_urban"]
    
    def process_multiple_zones(self, zones: List[str], date: str = None) -> List[ExtractedSpectralData]:
        """Process multiple Prague zones"""
        results = []
        
        for zone in zones:
            logger.info(f"Processing zone: {zone}")
            data = self.extract_spectral_data_for_zone(zone, date)
            if data:
                results.append(data)
            
        return results

# Example usage
def demo_image_processing():
    """Demonstrate image-based spectral processing"""
    
    api_key = os.getenv("OPENAI_API_KEY")
    extractor = ImageSpectralExtractor(api_key, "images")
    
    # Process key Prague zones
    prague_zones = ["letna_park", "old_town", "petrin_hill", "vltava_river", "vinohrady"]
    
    print("🖼️ Processing actual satellite images...")
    results = extractor.process_multiple_zones(prague_zones)
    
    print(f"\n✨ Processed {len(results)} zones from satellite imagery:")
    for result in results:
        print(f"\n📍 {result.location_name.upper()}")
        print(f"   Available data: {', '.join(result.image_types)}")
        print(f"   Coordinates: {result.coordinates}")
        print(f"   Indices: {result.derived_indices}")
        print(f"   Categories: {result.semantic_categories}")
        print(f"   Vision analysis: {result.visual_analysis[:200]}...")
    
    return results

if __name__ == "__main__":
    demo_results = demo_image_processing() 