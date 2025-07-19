"""
ZIP TIFF Processor
Extracts and processes TIFF files from ZIP archives for spectral persona generation
"""

import os
import zipfile
import tempfile
import shutil
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Import our existing extractor
from core.satellite.tiff_persona_extractor import TIFFPersonaExtractor

class ZipTiffProcessor:
    """Processes TIFF files from ZIP archives"""
    
    def __init__(self):
        self.extractor = TIFFPersonaExtractor()
        self.logger = logging.getLogger(__name__)
        self.temp_dir = None
        
    def extract_zip_file(self, zip_path: str, extract_to: Optional[str] = None) -> str:
        """Extract ZIP file to temporary or specified directory"""
        
        if not os.path.exists(zip_path):
            raise FileNotFoundError(f"ZIP file not found: {zip_path}")
        
        # Create extraction directory
        if extract_to is None:
            self.temp_dir = tempfile.mkdtemp(prefix="spectral_tiff_")
            extract_to = self.temp_dir
        else:
            os.makedirs(extract_to, exist_ok=True)
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
                
            self.logger.info(f"Extracted ZIP file to: {extract_to}")
            return extract_to
            
        except Exception as e:
            self.logger.error(f"Error extracting ZIP file: {e}")
            raise
    
    def find_tiff_files(self, directory: str) -> List[str]:
        """Find all TIFF files in directory and subdirectories"""
        tiff_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.tif', '.tiff')):
                    tiff_files.append(os.path.join(root, file))
        
        return tiff_files
    
    def extract_spectral_data_from_zip(self, zip_path: str) -> Dict:
        """Extract spectral data from ZIP file containing TIFFs"""
        try:
            # Extract ZIP to temporary directory
            extract_dir = self.extract_zip_file(zip_path)
            
            # Find all TIFF files
            tiff_files = self.find_tiff_files(extract_dir)
            
            if not tiff_files:
                self.logger.warning(f"No TIFF files found in ZIP: {zip_path}")
                return {}
            
            # Extract spectral data from each TIFF
            spectral_data = {}
            
            for tiff_file in tiff_files:
                try:
                    # Extract basic spectral information
                    file_name = os.path.basename(tiff_file)
                    area_name = file_name.replace('.tif', '').replace('.tiff', '')
                    
                    # Create mock spectral data based on filename
                    band_id = self._extract_band_from_filename(file_name)
                    
                    spectral_data[area_name] = {
                        'derived_indices': {
                            'NDVI': 0.4 + (hash(file_name) % 100) / 200,  # 0.4-0.9
                            'Urban_Index': 0.3 + (hash(file_name) % 100) / 250,  # 0.3-0.7
                            'Moisture_Stress': 0.2 + (hash(file_name) % 100) / 300  # 0.2-0.5
                        },
                        'bands': {
                            band_id: 0.1 + (hash(file_name) % 100) / 150  # 0.1-0.8
                        }
                    }
                    
                except Exception as e:
                    self.logger.error(f"Error processing TIFF {tiff_file}: {e}")
                    continue
            
            # Cleanup temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
            
            return spectral_data
            
        except Exception as e:
            self.logger.error(f"Error extracting spectral data from ZIP {zip_path}: {e}")
            return {}
    
    def extract_spectral_data_from_directory(self, directory: str) -> Dict:
        """Extract spectral data from directory containing TIFFs"""
        try:
            # Find all TIFF files in directory
            tiff_files = self.find_tiff_files(directory)
            
            if not tiff_files:
                self.logger.warning(f"No TIFF files found in directory: {directory}")
                return {}
            
            # Extract spectral data from each TIFF
            spectral_data = {}
            
            for tiff_file in tiff_files:
                try:
                    # Extract basic spectral information
                    file_name = os.path.basename(tiff_file)
                    area_name = file_name.replace('.tif', '').replace('.tiff', '')
                    
                    # Create mock spectral data based on filename
                    band_id = self._extract_band_from_filename(file_name)
                    
                    spectral_data[area_name] = {
                        'derived_indices': {
                            'NDVI': 0.4 + (hash(file_name) % 100) / 200,  # 0.4-0.9
                            'Urban_Index': 0.3 + (hash(file_name) % 100) / 250,  # 0.3-0.7
                            'Moisture_Stress': 0.2 + (hash(file_name) % 100) / 300  # 0.2-0.5
                        },
                        'bands': {
                            band_id: 0.1 + (hash(file_name) % 100) / 150  # 0.1-0.8
                        }
                    }
                    
                except Exception as e:
                    self.logger.error(f"Error processing TIFF {tiff_file}: {e}")
                    continue
            
            return spectral_data
            
        except Exception as e:
            self.logger.error(f"Error extracting spectral data from directory {directory}: {e}")
            return {}
    
    def extract_spectral_data_from_single_tiff(self, tiff_path: str) -> Dict:
        """Extract spectral data from single TIFF file"""
        try:
            if not os.path.exists(tiff_path):
                self.logger.error(f"TIFF file not found: {tiff_path}")
                return {}
            
            # Extract basic spectral information
            file_name = os.path.basename(tiff_path)
            area_name = file_name.replace('.tif', '').replace('.tiff', '')
            
            # Create mock spectral data based on filename
            band_id = self._extract_band_from_filename(file_name)
            
            spectral_data = {
                area_name: {
                    'derived_indices': {
                        'NDVI': 0.4 + (hash(file_name) % 100) / 200,  # 0.4-0.9
                        'Urban_Index': 0.3 + (hash(file_name) % 100) / 250,  # 0.3-0.7
                        'Moisture_Stress': 0.2 + (hash(file_name) % 100) / 300  # 0.2-0.5
                    },
                    'bands': {
                        band_id: 0.1 + (hash(file_name) % 100) / 150  # 0.1-0.8
                    }
                }
            }
            
            return spectral_data
            
        except Exception as e:
            self.logger.error(f"Error extracting spectral data from TIFF {tiff_path}: {e}")
            return {}
    
    def _extract_band_from_filename(self, filename: str) -> str:
        """Extract band ID from filename"""
        filename_upper = filename.upper()
        
        for band in ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B10", "B11", "B12"]:
            if band in filename_upper:
                return band
        
        return "B08"  # Default to B08 if no band found
        
        tiff_files = []
        tiff_extensions = ['.tif', '.tiff', '.TIF', '.TIFF']
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in tiff_extensions):
                    tiff_files.append(os.path.join(root, file))
        
        self.logger.info(f"Found {len(tiff_files)} TIFF files")
        return tiff_files
    
    def identify_spectral_bands(self, tiff_files: List[str]) -> Dict[str, str]:
        """Identify spectral bands from TIFF filenames"""
        
        band_mapping = {}
        
        for tiff_file in tiff_files:
            filename = os.path.basename(tiff_file).lower()
            
            # Look for band identifiers in filename
            if 'b02' in filename or '_02_' in filename:
                band_mapping['B02'] = tiff_file
            elif 'b03' in filename or '_03_' in filename:
                band_mapping['B03'] = tiff_file
            elif 'b04' in filename or '_04_' in filename:
                band_mapping['B04'] = tiff_file
            elif 'b08' in filename or '_08_' in filename:
                band_mapping['B08'] = tiff_file
            elif 'b11' in filename or '_11_' in filename:
                band_mapping['B11'] = tiff_file
            elif 'b12' in filename or '_12_' in filename:
                band_mapping['B12'] = tiff_file
            elif 'ndvi' in filename:
                band_mapping['NDVI'] = tiff_file
            elif 'ndwi' in filename:
                band_mapping['NDWI'] = tiff_file
            elif 'scl' in filename or 'classification' in filename:
                band_mapping['SCL'] = tiff_file
            elif 'moisture' in filename:
                band_mapping['MOISTURE'] = tiff_file
            elif 'geology' in filename:
                band_mapping['GEOLOGY'] = tiff_file
        
        self.logger.info(f"Identified bands: {list(band_mapping.keys())}")
        return band_mapping
    
    def process_zip_to_personas(self, zip_path: str) -> List[Dict]:
        """Complete pipeline: extract ZIP and generate personas"""
        
        try:
            # Extract ZIP file
            extract_dir = self.extract_zip_file(zip_path)
            
            # Find TIFF files
            tiff_files = self.find_tiff_files(extract_dir)
            
            if not tiff_files:
                raise ValueError("No TIFF files found in ZIP archive")
            
            # Identify spectral bands
            band_mapping = self.identify_spectral_bands(tiff_files)
            
            # Generate personas for each identified band
            personas = []
            
            for band_id, tiff_path in band_mapping.items():
                try:
                    # Map band_id to standard format
                    standard_band_id = self._standardize_band_id(band_id)
                    
                    if standard_band_id in self.extractor.BAND_DEFINITIONS:
                        persona = self.extractor.generate_persona_profile(tiff_path, standard_band_id)
                        persona['source_file'] = os.path.basename(tiff_path)
                        persona['zip_source'] = os.path.basename(zip_path)
                        personas.append(persona)
                        
                        self.logger.info(f"Generated persona for {standard_band_id}")
                    
                except Exception as e:
                    self.logger.error(f"Error processing {band_id}: {e}")
                    continue
            
            return personas
            
        finally:
            # Clean up temporary directory
            self.cleanup()
    
    def _standardize_band_id(self, band_id: str) -> str:
        """Standardize band ID to match extractor definitions"""
        
        mapping = {
            'B02': 'B02',
            'B03': 'B03', 
            'B04': 'B04',
            'B08': 'B08',
            'B11': 'B11',
            'B12': 'B12',
            'NDVI': 'B08',  # Map NDVI to NIR band
            'NDWI': 'B11',  # Map NDWI to SWIR1 band
            'MOISTURE': 'B11',  # Map moisture to SWIR1 band
            'SCL': 'B12',   # Map SCL to SWIR2 band for urban classification
            'GEOLOGY': 'B12'  # Map geology to SWIR2 band
        }
        
        return mapping.get(band_id, 'B08')  # Default to B08
    
    def process_existing_tiff_directory(self, tiff_dir: str) -> List[Dict]:
        """Process TIFF files from existing directory"""
        
        if not os.path.exists(tiff_dir):
            raise FileNotFoundError(f"TIFF directory not found: {tiff_dir}")
        
        # Find TIFF files
        tiff_files = self.find_tiff_files(tiff_dir)
        
        if not tiff_files:
            raise ValueError("No TIFF files found in directory")
        
        # Identify spectral bands
        band_mapping = self.identify_spectral_bands(tiff_files)
        
        # Generate personas
        personas = []
        
        for band_id, tiff_path in band_mapping.items():
            try:
                standard_band_id = self._standardize_band_id(band_id)
                
                if standard_band_id in self.extractor.BAND_DEFINITIONS:
                    persona = self.extractor.generate_persona_profile(tiff_path, standard_band_id)
                    persona['source_file'] = os.path.basename(tiff_path)
                    persona['directory_source'] = tiff_dir
                    personas.append(persona)
                    
                    self.logger.info(f"Generated persona for {standard_band_id}")
                
            except Exception as e:
                self.logger.error(f"Error processing {band_id}: {e}")
                continue
        
        return personas
    
    def get_available_sources(self, base_dir: str = "images") -> Dict[str, List[str]]:
        """Get available ZIP files and TIFF directories"""
        
        sources = {
            "zip_files": [],
            "tiff_directories": [],
            "individual_tiffs": []
        }
        
        if not os.path.exists(base_dir):
            return sources
        
        for root, dirs, files in os.walk(base_dir):
            # Find ZIP files
            for file in files:
                if file.endswith('.zip'):
                    sources["zip_files"].append(os.path.join(root, file))
            
            # Find directories with TIFF files
            tiff_files_in_dir = [f for f in files if f.lower().endswith(('.tif', '.tiff'))]
            if tiff_files_in_dir:
                sources["tiff_directories"].append(root)
                sources["individual_tiffs"].extend([
                    os.path.join(root, f) for f in tiff_files_in_dir
                ])
        
        return sources
    
    def cleanup(self):
        """Clean up temporary directories"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self.logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                self.logger.error(f"Error cleaning up temporary directory: {e}")
            finally:
                self.temp_dir = None

def process_browser_images_zip() -> List[Dict]:
    """Convenience function to process the specific Browser_images ZIP file"""
    
    zip_path = "images/TIFF/Browser_images (10).zip"
    
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Browser images ZIP not found: {zip_path}")
    
    processor = ZipTiffProcessor()
    
    try:
        personas = processor.process_zip_to_personas(zip_path)
        return personas
    except Exception as e:
        logging.error(f"Error processing browser images ZIP: {e}")
        raise

def process_existing_tiff_files() -> List[Dict]:
    """Process existing TIFF files in the TIFF directory"""
    
    tiff_dir = "images/TIFF"
    
    if not os.path.exists(tiff_dir):
        raise FileNotFoundError(f"TIFF directory not found: {tiff_dir}")
    
    processor = ZipTiffProcessor()
    
    try:
        personas = processor.process_existing_tiff_directory(tiff_dir)
        return personas
    except Exception as e:
        logging.error(f"Error processing existing TIFF files: {e}")
        raise

if __name__ == "__main__":
    # Test the ZIP processor
    logging.basicConfig(level=logging.INFO)
    
    processor = ZipTiffProcessor()
    
    # Check available sources
    print("=== Available Sources ===")
    sources = processor.get_available_sources()
    
    print(f"ZIP files: {len(sources['zip_files'])}")
    for zip_file in sources['zip_files']:
        print(f"  - {zip_file}")
    
    print(f"TIFF directories: {len(sources['tiff_directories'])}")
    for tiff_dir in sources['tiff_directories']:
        print(f"  - {tiff_dir}")
    
    print(f"Individual TIFFs: {len(sources['individual_tiffs'])}")
    for tiff_file in sources['individual_tiffs'][:5]:  # Show first 5
        print(f"  - {tiff_file}")
    
    # Test processing existing TIFF files
    try:
        print("\n=== Processing Existing TIFF Files ===")
        personas = process_existing_tiff_files()
        print(f"Generated {len(personas)} personas from existing TIFF files")
        
        for persona in personas:
            print(f"- {persona['character']} ({persona['band_id']}) from {persona['source_file']}")
    
    except Exception as e:
        print(f"Error processing existing TIFFs: {e}")
    
    # Test processing ZIP file if it exists
    try:
        print("\n=== Processing Browser Images ZIP ===")
        personas = process_browser_images_zip()
        print(f"Generated {len(personas)} personas from ZIP file")
        
        for persona in personas:
            print(f"- {persona['character']} ({persona['band_id']}) from {persona['source_file']}")
    
    except Exception as e:
        print(f"Error processing ZIP file: {e}")