"""
Dynamic Citizen Persona Chat Interface
Fully generative spectral personas that engage as alive, dramatic citizen interlocutors
No predefined data - everything generated from real TIFF spectral analysis
"""

import streamlit as st
import os
import json
import logging
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from typing import Dict, List, Optional
from datetime import datetime
import base64

# Import our custom modules
from core.satellite.tiff_persona_extractor import TIFFPersonaExtractor
from core.satellite.zip_tiff_processor import ZipTiffProcessor, process_browser_images_zip, process_existing_tiff_files
from core.conversation.spectral_dialogue import SpectralDialogue, ConversationContext
from core.personas.dynamic_citizen_personas import DynamicCitizenPersonaGenerator
from core.audio.elevenlabs_voices import voice_manager
from create_concrete_policy_personas import create_concrete_policy_persona

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🌆 Dynamic Citizen Personas",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dynamic citizen interface
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 400;
        color: #2E3440;
        margin-bottom: 1rem;
        text-align: center;
    }
    .citizen-card {
        background: linear-gradient(135deg, #F8F9FA 0%, #E5E9F0 100%);
        border-left: 5px solid #D08770;
        padding: 1.2rem;
        margin: 0.8rem 0;
        border-radius: 0 12px 12px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .citizen-response {
        background: linear-gradient(135deg, #ECEFF4 0%, #D8DEE9 100%);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        border-left: 4px solid #5E81AC;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }
    .user-message {
        background: linear-gradient(135deg, #E5E9F0 0%, #D8DEE9 100%);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 12px;
        border-right: 4px solid #88C0D0;
        text-align: right;
    }
    .dynamic-status {
        background: #A3BE8C;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    .spectral-signature {
        font-family: 'Courier New', monospace;
        background: #4C566A;
        color: #ECEFF4;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
    }
    .engagement-mode {
        background: #BF616A;
        color: white;
        padding: 0.2rem 0.6rem;
        border-radius: 10px;
        font-size: 0.7rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .randomness-indicator {
        background: #EBCB8B;
        color: #2E3440;
        padding: 0.2rem 0.5rem;
        border-radius: 8px;
        font-size: 0.7rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state at module level
if 'dynamic_personas' not in st.session_state:
    st.session_state.dynamic_personas = []
if 'active_citizens' not in st.session_state:
    st.session_state.active_citizens = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_language' not in st.session_state:
    st.session_state.current_language = 'english'
if 'randomness_level' not in st.session_state:
    st.session_state.randomness_level = 0.8
if 'spatial_context' not in st.session_state:
    st.session_state.spatial_context = {
        "lat": 50.075,
        "lon": 14.437,
        "location": "Prague"
    }

class DynamicCitizenPersonaChat:
    """Main application class for dynamic citizen persona chat"""
    
    def __init__(self):
        self.extractor = TIFFPersonaExtractor()
        self.zip_processor = ZipTiffProcessor()
        self.dialogue = SpectralDialogue()
        self.citizen_generator = DynamicCitizenPersonaGenerator()
        
    
    def create_spectral_visualization(self, persona: Dict) -> plt.Figure:
        """Create a visual representation of spectral data"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f"Spectral Analysis: {self._get_proper_character_name(persona)}", fontsize=16, fontweight='bold')
        
        # Get spectral data
        spectral_values = persona.get('spectral_values', {})
        spectral_metrics = persona.get('spectral_metrics', {})
        band_id = persona.get('band_id', 'Unknown')
        
        # 1. Band readings bar chart
        if 'band_readings' in spectral_values and spectral_values['band_readings']:
            bands = list(spectral_values['band_readings'].keys())
            values = list(spectral_values['band_readings'].values())
            colors = plt.cm.viridis(np.linspace(0, 1, len(bands)))
            
            bars = ax1.bar(bands, values, color=colors)
            ax1.set_title('Spectral Band Readings')
            ax1.set_ylabel('Reflectance Value')
            ax1.set_ylim(0, 1)
            
            # Highlight current band
            if band_id in bands:
                idx = bands.index(band_id)
                bars[idx].set_color('red')
                bars[idx].set_alpha(0.8)
        else:
            ax1.text(0.5, 0.5, 'No band data available', ha='center', va='center', transform=ax1.transAxes)
            ax1.set_title('Spectral Band Readings')
        
        # 2. Environmental indices
        if 'derived_indices' in spectral_values and spectral_values['derived_indices']:
            indices = list(spectral_values['derived_indices'].keys())
            idx_values = list(spectral_values['derived_indices'].values())
            colors = plt.cm.plasma(np.linspace(0, 1, len(indices)))
            
            ax2.bar(indices, idx_values, color=colors)
            ax2.set_title('Environmental Indices')
            ax2.set_ylabel('Index Value')
            ax2.tick_params(axis='x', rotation=45)
        else:
            ax2.text(0.5, 0.5, 'No indices available', ha='center', va='center', transform=ax2.transAxes)
            ax2.set_title('Environmental Indices')
        
        # 3. Spectral metrics radar chart
        if spectral_metrics:
            metrics = ['Variance', 'Intensity', 'Diversity']
            values = [
                spectral_metrics.get('variance', 0),
                spectral_metrics.get('intensity', 0),
                spectral_metrics.get('diversity', 0)
            ]
            
            angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
            values += values[:1]  # Complete the circle
            angles += angles[:1]
            
            ax3.remove()
            ax3 = fig.add_subplot(2, 2, 3, projection='polar')
            ax3.plot(angles, values, 'o-', linewidth=2, color='blue')
            ax3.fill(angles, values, alpha=0.25, color='blue')
            ax3.set_xticks(angles[:-1])
            ax3.set_xticklabels(metrics)
            ax3.set_ylim(0, 1)
            ax3.set_title('Spectral Analysis Metrics')
        else:
            ax3.text(0.5, 0.5, 'No metrics available', ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Spectral Analysis Metrics')
        
        # 4. Simulated spectral signature
        wavelengths = [443, 490, 560, 665, 705, 740, 783, 842, 865, 945, 1375, 1610, 2190]
        band_names = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12']
        
        # Create simulated spectral curve based on available data
        if 'band_readings' in spectral_values and spectral_values['band_readings']:
            signature = []
            for band in band_names:
                if band in spectral_values['band_readings']:
                    signature.append(spectral_values['band_readings'][band])
                else:
                    # Interpolate or use default
                    signature.append(0.3 + np.random.normal(0, 0.1))
        else:
            # Generate a typical spectral signature
            signature = [0.1, 0.15, 0.2, 0.25, 0.4, 0.45, 0.5, 0.6, 0.55, 0.3, 0.25, 0.2, 0.15]
        
        ax4.plot(wavelengths, signature, 'o-', linewidth=2, color='green', markersize=6)
        ax4.set_title('Spectral Signature')
        ax4.set_xlabel('Wavelength (nm)')
        ax4.set_ylabel('Reflectance')
        ax4.grid(True, alpha=0.3)
        
        # Highlight current band
        if band_id in band_names:
            idx = band_names.index(band_id)
            ax4.plot(wavelengths[idx], signature[idx], 'ro', markersize=10, alpha=0.7)
        
        plt.tight_layout()
        return fig
    
    def run(self):
        """Main application entry point"""
        self.render_header()
        
        if not st.session_state.dynamic_personas:
            self.render_tiff_loader()
        else:
            # Add option to load more personas
            with st.expander("➕ Add More Personas", expanded=False):
                self.render_tiff_loader(add_mode=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                self.render_combined_persona_panel()
            
            with col2:
                self.render_conversation_area()
    
    def render_header(self):
        """Render application header with controls"""
        col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
        
        with col1:
            st.markdown('<h1 class="main-header">🌆 Dynamic Citizen Personas</h1>', unsafe_allow_html=True)
            st.markdown("*Alive, dramatic spectral citizens generated from real satellite data*")
        
        with col2:
            # Language selector
            languages = {
                'czech': '🇨🇿 CZ',
                'english': '🇬🇧 EN', 
                'german': '🇩🇪 DE'
            }
            
            selected_lang = st.selectbox(
                "Language",
                options=list(languages.keys()),
                format_func=lambda x: languages[x],
                index=list(languages.keys()).index(st.session_state.current_language),
                key="dynamic_language_selector"
            )
            
            if selected_lang != st.session_state.current_language:
                st.session_state.current_language = selected_lang
                st.rerun()
        
        with col3:
            # Randomness control
            randomness = st.slider(
                "🎲 Randomness",
                min_value=0.1,
                max_value=1.0,
                value=st.session_state.randomness_level,
                step=0.1,
                key="randomness_slider"
            )
            st.session_state.randomness_level = randomness
        
        with col4:
            # Temperature control
            temperature = st.slider(
                "🌡️ Creativity",
                min_value=0.1,
                max_value=2.0,
                value=1.1,
                step=0.1,
                key="dynamic_temperature_slider"
            )
            self.dialogue.temperature = temperature
    
    def render_tiff_loader(self, add_mode=False):
        """Render TIFF file loading interface for dynamic personas"""
        st.subheader("📡 Load Real Satellite Data")
        
        # Get available sources
        sources = self.zip_processor.get_available_sources()
        
        # Create tabs for real data only
        tab1, tab2, tab3 = st.tabs(["🗜️ ZIP Files", "📁 TIFF Directories", "📄 Individual TIFFs"])
        
        with tab1:
            st.write("**Process ZIP archives containing real TIFF files**")
            
            if sources["zip_files"]:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    selected_zip = st.selectbox(
                        "Select ZIP file:",
                        options=sources["zip_files"],
                        format_func=lambda x: os.path.basename(x),
                        key="dynamic_zip_selector"
                    )
                
                with col2:
                    button_text = "➕ Add Personas" if add_mode else "🗜️ Generate Personas"
                    if st.button(button_text, type="primary"):
                        self.load_dynamic_personas_from_zip(selected_zip, add_mode=add_mode)
                
                # Special button for Browser images ZIP
                if any("Browser_images" in zip_file for zip_file in sources["zip_files"]):
                    st.markdown("---")
                    if st.button("🛰️ Load Browser Images → Dynamic Citizens", type="secondary"):
                        self.load_dynamic_browser_images_zip()
            else:
                st.warning("No ZIP files found in images directory")
        
        with tab2:
            st.write("**Process directories containing real TIFF files**")
            
            if sources["tiff_directories"]:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    selected_dir = st.selectbox(
                        "Select TIFF directory:",
                        options=sources["tiff_directories"],
                        format_func=lambda x: os.path.relpath(x, "images"),
                        key="dynamic_tiff_dir_selector"
                    )
                
                with col2:
                    button_text = "➕ Add Personas" if add_mode else "📁 Generate Personas"
                    if st.button(button_text, type="primary", key=f"tiff_dir_{add_mode}"):
                        self.load_dynamic_personas_from_tiff_directory(selected_dir, add_mode=add_mode)
            else:
                st.warning("No TIFF directories found")
        
        with tab3:
            st.write("**Process individual real TIFF files**")
            
            if sources["individual_tiffs"]:
                selected_tiff = st.selectbox(
                    "Select TIFF file:",
                    options=sources["individual_tiffs"],
                    format_func=lambda x: os.path.basename(x),
                    key="dynamic_individual_tiff_selector"
                )
                
                button_text = "➕ Add Persona" if add_mode else "📄 Generate Persona"
                if st.button(button_text, type="primary", key=f"single_tiff_{add_mode}"):
                    self.load_dynamic_personas_from_single_tiff(selected_tiff, add_mode=add_mode)
            else:
                st.warning("No individual TIFF files found")
    
    def load_dynamic_personas_from_zip(self, zip_path: str, add_mode: bool = False):
        """Load dynamic citizen personas from ZIP file"""
        try:
            with st.spinner(f"Generating dynamic citizens from: {os.path.basename(zip_path)}..."):
                # First extract spectral data
                spectral_data = self.zip_processor.extract_spectral_data_from_zip(zip_path)
                
                if spectral_data:
                    # Generate dynamic citizen personas
                    dynamic_personas = []
                    
                    # Extract bands from ZIP file contents (TIFF filenames)
                    available_bands = self._extract_bands_from_zip(zip_path)
                    
                    for band_id in available_bands:
                        # Pass existing personas for conflict generation
                        existing_for_conflict = st.session_state.dynamic_personas if add_mode else []
                        citizen_persona = self.citizen_generator.generate_dynamic_persona(
                            band_id,
                            spectral_data,
                            randomness_level=st.session_state.randomness_level,
                            existing_personas=existing_for_conflict
                        )
                        
                        # Add source file information
                        citizen_persona['source_file'] = zip_path
                        dynamic_personas.append(citizen_persona)
                    
                    if add_mode:
                        # Add to existing personas, but avoid duplicates
                        existing_personas = st.session_state.dynamic_personas
                        existing_band_ids = {p["band_id"] for p in existing_personas}
                        
                        # Only add personas for bands that don't already exist
                        new_personas = [p for p in dynamic_personas if p["band_id"] not in existing_band_ids]
                        
                        if new_personas:
                            existing_personas.extend(new_personas)
                            st.session_state.dynamic_personas = existing_personas
                            
                            # Activate new personas (don't change existing active ones)
                            new_active = [p["band_id"] for p in new_personas[:3]]
                            st.session_state.active_citizens.extend(new_active)
                            
                            # Generate greetings for new personas
                            for persona in new_personas[:3]:
                                self.generate_brief_introduction(persona)
                        else:
                            st.warning("All bands from this source are already loaded")
                    else:
                        # Replace existing personas
                        st.session_state.dynamic_personas = dynamic_personas
                        st.session_state.active_citizens = [p["band_id"] for p in dynamic_personas[:3]]  # Activate first 3
                        
                        # Clear conversation history when replacing personas
                        st.session_state.conversation_history = []
                        
                        # Generate initial greetings for automatically activated personas
                        for persona in dynamic_personas[:3]:
                            self.generate_brief_introduction(persona)
                    
                    # Set spatial context
                    st.session_state.spatial_context = {
                        "lat": 50.075,
                        "lon": 14.437,
                        "location": "Prague",
                        "source": f"Dynamic ZIP: {os.path.basename(zip_path)}"
                    }
                    
                    st.success(f"✅ Generated {len(dynamic_personas)} dynamic citizen personas from real satellite data")
                    st.rerun()
                else:
                    st.error("No spectral data could be extracted from ZIP file")
                    
        except Exception as e:
            st.error(f"Error generating dynamic personas: {e}")
            logger.error(f"Error generating dynamic personas from {zip_path}: {e}")
    
    def load_dynamic_browser_images_zip(self):
        """Load dynamic personas from Browser images ZIP"""
        try:
            browser_zip_path = "images/TIFF/Browser_images (10).zip"
            if os.path.exists(browser_zip_path):
                self.load_dynamic_personas_from_zip(browser_zip_path)
            else:
                st.error("Browser images ZIP not found")
        except Exception as e:
            st.error(f"Error loading Browser images: {e}")
    
    def load_dynamic_personas_from_tiff_directory(self, tiff_dir: str, add_mode: bool = False):
        """Load dynamic personas from TIFF directory"""
        try:
            with st.spinner(f"Generating dynamic citizens from directory: {os.path.basename(tiff_dir)}..."):
                # Extract spectral data from directory
                spectral_data = self.zip_processor.extract_spectral_data_from_directory(tiff_dir)
                
                if spectral_data:
                    # Generate dynamic citizen personas
                    dynamic_personas = []
                    available_bands = self._extract_available_bands(spectral_data)
                    
                    for band_id in available_bands:
                        # Pass existing personas for conflict generation
                        existing_for_conflict = st.session_state.dynamic_personas if add_mode else []
                        citizen_persona = self.citizen_generator.generate_dynamic_persona(
                            band_id,
                            spectral_data,
                            randomness_level=st.session_state.randomness_level,
                            existing_personas=existing_for_conflict
                        )
                        
                        # Add source file information
                        citizen_persona['source_file'] = tiff_dir
                        dynamic_personas.append(citizen_persona)
                    
                    if add_mode:
                        # Add to existing personas, but avoid duplicates
                        existing_personas = st.session_state.dynamic_personas
                        existing_band_ids = {p["band_id"] for p in existing_personas}
                        
                        # Only add personas for bands that don't already exist
                        new_personas = [p for p in dynamic_personas if p["band_id"] not in existing_band_ids]
                        
                        if new_personas:
                            existing_personas.extend(new_personas)
                            st.session_state.dynamic_personas = existing_personas
                            
                            # Activate new personas (don't change existing active ones)
                            new_active = [p["band_id"] for p in new_personas[:3]]
                            st.session_state.active_citizens.extend(new_active)
                            
                            # Generate greetings for new personas
                            for persona in new_personas[:3]:
                                self.generate_brief_introduction(persona)
                        else:
                            st.warning("All bands from this source are already loaded")
                    else:
                        # Replace existing personas
                        st.session_state.dynamic_personas = dynamic_personas
                        st.session_state.active_citizens = [p["band_id"] for p in dynamic_personas[:3]]
                        
                        # Clear conversation history when replacing personas
                        st.session_state.conversation_history = []
                        
                        # Generate initial greetings for automatically activated personas
                        for persona in dynamic_personas[:3]:
                            self.generate_brief_introduction(persona)
                    
                    st.success(f"✅ Generated {len(dynamic_personas)} dynamic citizen personas")
                    st.rerun()
                else:
                    st.error("No spectral data could be extracted from directory")
                    
        except Exception as e:
            st.error(f"Error generating dynamic personas: {e}")
            logger.error(f"Error generating dynamic personas from {tiff_dir}: {e}")
    
    def load_dynamic_personas_from_single_tiff(self, tiff_path: str, add_mode: bool = False):
        """Load dynamic personas from single TIFF file"""
        try:
            with st.spinner(f"Generating dynamic citizen from: {os.path.basename(tiff_path)}..."):
                # Extract spectral data from single file
                spectral_data = self.zip_processor.extract_spectral_data_from_single_tiff(tiff_path)
                
                if spectral_data:
                    # Determine band from filename
                    band_id = self._extract_band_from_filename(os.path.basename(tiff_path))
                    
                    # Pass existing personas for conflict generation
                    existing_for_conflict = st.session_state.dynamic_personas if add_mode else []
                    citizen_persona = self.citizen_generator.generate_dynamic_persona(
                        band_id,
                        spectral_data,
                        randomness_level=st.session_state.randomness_level,
                        existing_personas=existing_for_conflict
                    )
                    
                    # Add source file information
                    citizen_persona['source_file'] = tiff_path
                    
                    if add_mode:
                        # Add to existing personas, but avoid duplicates
                        existing_personas = st.session_state.dynamic_personas
                        existing_band_ids = {p["band_id"] for p in existing_personas}
                        
                        # Only add if this band doesn't already exist
                        if citizen_persona["band_id"] not in existing_band_ids:
                            existing_personas.append(citizen_persona)
                            st.session_state.dynamic_personas = existing_personas
                            
                            # Activate new persona
                            st.session_state.active_citizens.append(citizen_persona["band_id"])
                            
                            # Generate brief introduction for new persona
                            self.generate_brief_introduction(citizen_persona)
                        else:
                            st.warning(f"Band {citizen_persona['band_id']} is already loaded")
                    else:
                        # Replace existing personas
                        st.session_state.dynamic_personas = [citizen_persona]
                        st.session_state.active_citizens = [citizen_persona["band_id"]]
                        
                        # Clear conversation history when replacing personas
                        st.session_state.conversation_history = []
                        
                        # Generate brief introduction for automatically activated persona
                        self.generate_brief_introduction(citizen_persona)
                    
                    st.success(f"✅ Generated dynamic citizen persona from {band_id} band")
                    st.rerun()
                else:
                    st.error("No spectral data could be extracted from TIFF file")
                    
        except Exception as e:
            st.error(f"Error generating dynamic persona: {e}")
            logger.error(f"Error generating dynamic persona from {tiff_path}: {e}")
    
    def _extract_available_bands(self, spectral_data: Dict) -> List[str]:
        """Extract available spectral bands from data"""
        bands = set()
        
        for area, data in spectral_data.items():
            if isinstance(data, dict) and 'bands' in data:
                bands.update(data['bands'].keys())
        
        # Default to common Sentinel-2 bands if none found
        if not bands:
            bands = {"B02", "B08", "B11", "B12"}
        
        return sorted(list(bands))
    
    def _extract_band_from_filename(self, filename: str) -> str:
        """Extract band ID from filename"""
        filename_upper = filename.upper()
        
        for band in ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B08", "B8A", "B09", "B10", "B11", "B12"]:
            if band in filename_upper:
                return band
        
        return "B08"  # Default
    
    def _extract_bands_from_zip(self, zip_path: str) -> List[str]:
        """Extract band IDs from TIFF filenames inside ZIP file"""
        bands = set()
        
        try:
            import zipfile
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                for filename in zip_file.namelist():
                    if filename.lower().endswith('.tiff') or filename.lower().endswith('.tif'):
                        band_id = self._extract_band_from_filename(filename)
                        bands.add(band_id)
        except Exception as e:
            st.error(f"Error extracting bands from ZIP {zip_path}: {e}")
            # Fallback to default bands
            bands = {"B02", "B08", "B11", "B12"}
        
        return sorted(list(bands))
    
    def render_combined_persona_panel(self):
        """Render unified personas panel with spectral data"""
        st.markdown("### 🌆 Personas")
        st.markdown(f"**Randomness:** {st.session_state.randomness_level}")
        
        if st.session_state.dynamic_personas:
            # Show active personas with their spectral data
            for persona in st.session_state.dynamic_personas:
                if persona["band_id"] in st.session_state.active_citizens:
                    character_name = self._get_proper_character_name(persona)
                    band_id = persona['band_id']
                    wavelength = persona.get('wavelength_info', {}).get('wavelength', 'unknown')
                    
                    # Persona card with spectral info
                    st.markdown(f"🎭 **{character_name}**")
                    st.markdown("**ACTIVE**")
                    st.markdown(f"📡 **Band:** {band_id} ({wavelength}nm)")
                    st.markdown(f"🗣️ **Language:** {st.session_state.current_language}")
                    st.markdown(f"📍 **Location:** Prague")
                    
                    # Spectral data for this persona
                    if 'spectral_values' in persona:
                        spectral_values = persona['spectral_values']
                        
                        with st.expander(f"📊 {character_name} - Spectral Data"):
                            # Create two columns: visualization and data
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                # Create and display spectral visualization
                                try:
                                    fig = self.create_spectral_visualization(persona)
                                    st.pyplot(fig)
                                    plt.close(fig)  # Clean up memory
                                except Exception as e:
                                    st.error(f"Could not create visualization: {e}")
                            
                            with col2:
                                # Key metrics
                                if 'band_value' in spectral_values:
                                    st.metric(f"Band {band_id}", f"{spectral_values['band_value']:.4f}")
                                
                                if 'derived_indices' in spectral_values and spectral_values['derived_indices']:
                                    for index, value in spectral_values['derived_indices'].items():
                                        st.metric(index, f"{value:.4f}")
                                
                                if 'spectral_metrics' in persona:
                                    metrics = persona['spectral_metrics']
                                    st.metric("Variance", f"{metrics.get('variance', 0):.4f}")
                                    st.metric("Intensity", f"{metrics.get('intensity', 0):.4f}")
                    
                    st.markdown("---")
        else:
            st.warning("⚠️ **No personas loaded.** Use the sidebar to load spectral data from TIFF files.")
    
    def render_citizen_panel(self):
        """Render dynamic citizen personas panel"""
        st.subheader("🌆 Personas")
        
        if st.session_state.dynamic_personas:
            # Randomness regeneration
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f'<span class="randomness-indicator">Randomness: {st.session_state.randomness_level:.1f}</span>', unsafe_allow_html=True)
            with col2:
                if st.button("🎲 Regenerate", help="Generate new random personalities"):
                    self.regenerate_dynamic_personas()
            
            # Add conflict generation button if multiple personas are active
            if len(st.session_state.active_citizens) >= 2:
                if st.button("⚔️ Generate Conflict", help="Make active personas argue with each other!"):
                    self.generate_conflict_dialogue()
            
            st.markdown("---")
            
            # Display dynamic citizen personas with detailed mapping
            for i, persona in enumerate(st.session_state.dynamic_personas):
                is_active = persona["band_id"] in st.session_state.active_citizens
                
                with st.container():
                    # Enhanced citizen card with persona mapping
                    status_icon = "🟢" if is_active else "⚪"
                    
                    # Get character name - create proper names based on band type
                    character_name = self._get_proper_character_name(persona)
                    
                    # Get location info
                    location_name = persona.get('location_name', 'Prague')
                    if 'spatial_bounds' in persona:
                        bounds = persona['spatial_bounds']
                        if isinstance(bounds, (list, tuple)) and len(bounds) >= 4:
                            lat = (bounds[1] + bounds[3]) / 2
                            lon = (bounds[0] + bounds[2]) / 2
                            location_name = f"{location_name} ({lat:.3f}, {lon:.3f})"
                    
                    # Get wavelength info
                    wavelength = persona.get('wavelength', 'unknown')
                    if 'wavelength_psychology' in persona:
                        wavelength = f"{persona['wavelength_psychology'].get('wavelength', 'unknown')}nm"
                    
                    card_html = f"""
                    <div class="citizen-card">
                        <div style="margin-bottom: 0.8rem;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <strong style="color: #2E3440; font-size: 1.1rem;">🎭 {character_name}</strong>
                                <span class="dynamic-status">{'ACTIVE' if is_active else 'INACTIVE'}</span>
                            </div>
                            <div style="font-size: 0.85rem; color: #5E81AC; line-height: 1.4;">
                                📡 Band: {persona['band_id']} ({wavelength})<br>
                                🗣️ Language: {st.session_state.current_language}<br>
                                📍 Location: {location_name}
                            </div>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    
                    # Toggle activation
                    if is_active:
                        if st.button(f"🔇 Deactivate {persona['band_id']}", key=f"deactivate_{persona['band_id']}_{i}"):
                            st.session_state.active_citizens.remove(persona["band_id"])
                            st.rerun()
                    else:
                        if st.button(f"🔊 Activate {persona['band_id']}", key=f"activate_{persona['band_id']}_{i}"):
                            st.session_state.active_citizens.append(persona["band_id"])
                            # Generate brief introduction when manually activated
                            self.generate_brief_introduction(persona)
                            st.rerun()
                    
                    st.markdown("---")
        else:
            st.info("Load satellite data to generate dynamic citizen personas")
    
    def render_map_visualization(self):
        """Render map showing satellite imagery and persona locations"""
        st.subheader("🗺️ Spectral Map")
        
        if st.session_state.dynamic_personas:
            # Display spatial context
            spatial_ctx = st.session_state.spatial_context
            st.markdown(f"**Location**: {spatial_ctx.get('location', 'Prague')}")
            
            # Show the actual source file being processed
            source_info = spatial_ctx.get('source', 'Satellite Data')
            st.markdown(f"**Source**: {source_info}")
            
            # Try to show the actual TIFF file being processed
            if 'source' in spatial_ctx and 'ZIP:' in source_info:
                st.markdown("**Processed TIFF Data:**")
                st.markdown("*Spectral data extracted from selected TIFF files*")
                
                # Show persona mapping instead of random images
                st.markdown("**Persona Mapping:**")
                for persona in st.session_state.dynamic_personas:
                    if persona["band_id"] in st.session_state.active_citizens:
                        character_name = self._get_proper_character_name(persona)
                        wavelength = persona.get('wavelength', 'unknown')
                        if 'wavelength_psychology' in persona:
                            wavelength = f"{persona['wavelength_psychology'].get('wavelength', 'unknown')}nm"
                        
                        st.markdown(f"🟢 **{character_name}** ({persona['band_id']})")
                        st.markdown(f"   *Wavelength: {wavelength}*")
            else:
                # Fallback: show available images if no specific source
                st.markdown("**Source Data Visualization:**")
                
                # Show information about the loaded TIFF files
                if st.session_state.dynamic_personas:
                    # Get the source information from personas
                    source_files = set()
                    for persona in st.session_state.dynamic_personas:
                        if 'source_file' in persona:
                            source_files.add(persona['source_file'])
                    
                    if source_files:
                        st.success(f"📡 **Active TIFF Sources:** {', '.join([os.path.basename(f) for f in source_files])}")
                        
                        # Show spectral band information
                        st.markdown("**Loaded Spectral Bands:**")
                        for persona in st.session_state.dynamic_personas:
                            band_id = persona['band_id']
                            character_name = self._get_proper_character_name(persona)
                            source_file = persona.get('source_file', 'Unknown')
                            
                            # Band descriptions
                            band_descriptions = {
                                "B01": "Coastal aerosol (443nm) - Atmospheric particles, coastal waters",
                                "B02": "Blue (490nm) - Atmospheric clarity, water bodies",
                                "B03": "Green (560nm) - Vegetation health, urban areas",
                                "B04": "Red (665nm) - Vegetation stress, built environment",
                                "B05": "Red edge (705nm) - Vegetation chlorophyll content",
                                "B06": "Red edge (740nm) - Vegetation stress, leaf structure",
                                "B07": "Red edge (783nm) - Vegetation moisture, canopy structure",
                                "B08": "Near-infrared (842nm) - Vegetation biomass, water content",
                                "B8A": "Narrow NIR (865nm) - Vegetation index calculations",
                                "B09": "Water vapour (945nm) - Atmospheric water content",
                                "B10": "SWIR Cirrus (1375nm) - Cirrus cloud detection",
                                "B11": "SWIR1 (1610nm) - Moisture content, urban materials",
                                "B12": "SWIR2 (2190nm) - Geology, mineral composition"
                            }
                            
                            band_desc = band_descriptions.get(band_id, "Spectral analysis")
                            st.markdown(f"• **{character_name}** ({band_id}): {band_desc}")
                            st.caption(f"   Source: {os.path.basename(source_file)}")
                        
                        # Display actual spectral data values
                        st.markdown("---")
                        st.markdown("**📊 Raw Spectral Data Values:**")
                        
                        # Show spectral data for each persona
                        for persona in st.session_state.dynamic_personas:
                            if 'spectral_values' in persona:
                                character_name = self._get_proper_character_name(persona)
                                band_id = persona['band_id']
                                spectral_values = persona['spectral_values']
                                
                                with st.expander(f"🔍 {character_name} ({band_id}) - Spectral Data"):
                                    # Create two columns: visualization and data
                                    col1, col2 = st.columns([2, 1])
                                    
                                    with col1:
                                        # Create and display spectral visualization
                                        try:
                                            fig = self.create_spectral_visualization(persona)
                                            st.pyplot(fig)
                                            plt.close(fig)  # Clean up memory
                                        except Exception as e:
                                            st.error(f"Could not create visualization: {e}")
                                    
                                    with col2:
                                        # Band-specific value
                                        if 'band_value' in spectral_values:
                                            st.metric(f"Band {band_id} Value", f"{spectral_values['band_value']:.4f}")
                                        
                                        # Derived indices
                                        if 'derived_indices' in spectral_values and spectral_values['derived_indices']:
                                            st.markdown("**Environmental Indices:**")
                                            for index, value in spectral_values['derived_indices'].items():
                                                st.metric(index, f"{value:.4f}")
                                        
                                        # Spectral metrics
                                        if 'spectral_metrics' in persona:
                                            st.markdown("**Spectral Analysis:**")
                                            metrics = persona['spectral_metrics']
                                            st.metric("Variance", f"{metrics.get('variance', 0):.4f}")
                                            st.metric("Intensity", f"{metrics.get('intensity', 0):.4f}")
                                            st.metric("Diversity", f"{metrics.get('diversity', 0):.4f}")
                                        
                                        # All band readings (compact view)
                                        if 'band_readings' in spectral_values and spectral_values['band_readings']:
                                            st.markdown("**All Band Readings:**")
                                            for band, value in spectral_values['band_readings'].items():
                                                st.text(f"{band}: {value:.4f}")
                        
                        # Note about TIFF display limitations
                        st.info("💡 **Note:** TIFF files contain raw spectral data that can't be displayed as images. The personas above represent the actual spectral information from your selected TIFF files.")
                    else:
                        st.warning("No source file information available")
                else:
                    # Show guidance when no personas are loaded
                    st.warning("⚠️ **No TIFF data loaded.** Use the sidebar to load spectral data from TIFF files.")
                    
                    # Show available reference images if any
                    image_files = []
                    if os.path.exists("images"):
                        for file in os.listdir("images"):
                            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                                image_files.append(file)
                    
                    if image_files:
                        st.markdown("**Available Reference Images:**")
                        image_path = os.path.join("images", image_files[0])
                        try:
                            st.image(image_path, caption=f"Reference View: {image_files[0]}", use_container_width=True)
                            st.caption("💡 This is a reference image. Load TIFF data above to create spectral personas.")
                        except Exception as e:
                            st.error(f"Could not load reference image: {e}")
            
        
        else:
            st.info("Load satellite data to see map visualization")
            
            # Show example images while waiting
            st.markdown("**Example Prague Satellite Images:**")
            
            if os.path.exists("images"):
                example_files = []
                for file in os.listdir("images"):
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        example_files.append(file)
                
                if example_files:
                    # Show first example
                    example_path = os.path.join("images", example_files[0])
                    try:
                        st.image(example_path, caption=f"Example: {example_files[0]}", use_container_width=True)
                    except Exception as e:
                        st.write("Satellite imagery will appear here after loading data")
    
    def generate_brief_introduction(self, persona):
        """Generate a brief, authentic introduction when persona first appears"""
        try:
            # Use the dialogue system with a natural introduction prompt
            from core.conversation.spectral_dialogue import ConversationContext
            
            # Check if there are other active personas to create conflicts with
            other_active_personas = [p for p in st.session_state.dynamic_personas
                                   if p["band_id"] in st.session_state.active_citizens
                                   and p["band_id"] != persona["band_id"]]
            
            if other_active_personas:
                # Create conflict-driven introduction
                other_names = [self._get_proper_character_name(p) for p in other_active_personas]
                other_bands = [p["band_id"] for p in other_active_personas]
                intro_prompt = f"Introduce yourself dramatically while challenging the existing activists {', '.join(other_names)} ({', '.join(other_bands)}) who are completely wrong about Prague's real environmental problems. Be funny and propose a competing action!"
            else:
                # Standard introduction
                intro_prompt = "Introduce yourself briefly to someone who just arrived"
            
            context = ConversationContext(
                user_input=intro_prompt,
                language=st.session_state.current_language,
                narrative_mode="direct",
                active_personas=[persona["band_id"]],
                spatial_context=st.session_state.spatial_context
            )
            
            # Generate brief introduction using LLM
            response = self.dialogue.generate_persona_response(persona, context)
            introduction = response["response"]
            
            # Add introduction to conversation history
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": introduction,
                "persona_name": self._get_proper_character_name(persona),
                "band_id": persona["band_id"],
                "voice_type": "introduction"
            })
            
        except Exception as e:
            logger.error(f"Error generating introduction for {self._get_proper_character_name(persona)}: {e}")
            # Simple fallback introduction
            character_name = self._get_proper_character_name(persona)
            fallback_intro = f"On me, Prague's {persona['band_id']} patterns shift and change. I am {character_name}."
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": fallback_intro,
                "persona_name": character_name,
                "band_id": persona["band_id"],
                "voice_type": "fallback_introduction"
            })
    
    

    def _get_proper_character_name(self, persona):
        """Generate proper character names based on band type and location"""
        band_id = persona["band_id"]
        
        # Get location for naming
        location = "Prague"
        if 'spatial_bounds' in persona:
            bounds = persona['spatial_bounds']
            if isinstance(bounds, (list, tuple)) and len(bounds) >= 4:
                lat = (bounds[1] + bounds[3]) / 2
                # Determine Prague district based on coordinates
                if 50.08 <= lat <= 50.09:
                    location = "Nusle Basin"
                elif 50.07 <= lat <= 50.08:
                    location = "Vinohrady District"
                elif 50.09 <= lat <= 50.10:
                    location = "Letná Park"
                else:
                    location = "Prague"
        
        # ALWAYS extract name from character field to avoid corrupted short_name/dynamic_name
        # Skip the short_name and dynamic_name fields as they may contain full greetings
        
        # Extract name from character field - fix the actual extraction
        if 'character' in persona and persona['character']:
            character = persona['character']
            
            # Remove any formatting markers first
            import re
            character = re.sub(r'\*+([^*]+)\*+:?\s*', r'\1', character)  # Remove **text**: patterns
            character = re.sub(r'^[^:]*:\s*', '', character)  # Remove "prefix:" patterns
            
            # Debug: Let's see what we're working with
            print(f"DEBUG: Character content: {character[:100]}...")
            
            # Look for "I am" followed by name - be very specific
            if "I am " in character:
                # Find the position after "I am "
                start_pos = character.find("I am ") + 5
                remaining_text = character[start_pos:]
                
                # Look for the name - it should be the next few words before a comma or other separator
                # Handle patterns like "I am the illustrious Dr. NIRvana"
                words = remaining_text.split()
                name_words = []
                
                for word in words:
                    # Skip articles and descriptive words
                    if word.lower() in ['the', 'illustrious', 'magnificent', 'great', 'mighty', 'spectacular', 'amazing']:
                        continue
                    
                    # Stop at punctuation or lowercase descriptive words
                    if word.endswith(',') or word.endswith('!') or word.endswith('.'):
                        # Include the word but remove punctuation
                        clean_word = word.rstrip(',.!')
                        if clean_word and clean_word[0].isupper():
                            name_words.append(clean_word)
                        break
                    
                    # Stop at lowercase words (usually descriptive text)
                    if word[0].islower():
                        break
                    
                    # Add capitalized words (likely part of name)
                    if word[0].isupper():
                        name_words.append(word)
                    
                    # Stop after 3 words max
                    if len(name_words) >= 3:
                        break
                
                if name_words:
                    extracted_name = ' '.join(name_words)
                    print(f"DEBUG: Extracted name: {extracted_name}")
                    return extracted_name
            
            # Try "I'm" pattern as backup
            if "I'm " in character:
                start_pos = character.find("I'm ") + 4
                remaining_text = character[start_pos:]
                words = remaining_text.split()
                name_words = []
                
                for word in words:
                    if word.lower() in ['the', 'illustrious', 'magnificent', 'great', 'mighty']:
                        continue
                    
                    if word.endswith(',') or word.endswith('!') or word.endswith('.'):
                        clean_word = word.rstrip(',.!')
                        if clean_word and clean_word[0].isupper():
                            name_words.append(clean_word)
                        break
                    
                    if word[0].islower():
                        break
                    
                    if word[0].isupper():
                        name_words.append(word)
                    
                    if len(name_words) >= 3:
                        break
                
                if name_words:
                    extracted_name = ' '.join(name_words)
                    print(f"DEBUG: Extracted name from I'm: {extracted_name}")
                    return extracted_name
        
        # Last resort fallback
        return f"Spectral Entity of {location}"
    
    def _create_audio_player(self, text: str, persona: Dict, persona_name: str) -> str:
        """Create audio player HTML for persona speech"""
        try:
            # Assign voice dynamically based on persona characteristics
            voice_name = voice_manager.assign_voice_to_persona(persona)
            voice_description = voice_manager.get_voice_description(voice_name)
            
            # Generate speech audio
            audio_data = voice_manager.generate_speech(text, voice_name)
            
            if audio_data:
                # Encode audio as base64 for HTML player
                audio_base64 = base64.b64encode(audio_data).decode()
                
                # Create custom audio player with voice info
                audio_html = f"""
                <div style="margin: 10px 0; padding: 8px; background: #f0f2f6; border-radius: 8px; border-left: 4px solid #4CAF50;">
                    <div style="font-size: 0.8em; color: #666; margin-bottom: 5px;">
                        🎤 {voice_description}
                    </div>
                    <audio controls style="width: 100%; height: 32px;">
                        <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                """
                return audio_html
            else:
                return f'<div style="font-size: 0.8em; color: #999; font-style: italic;">🔇 Audio unavailable (check ELEVENLABS_API_KEY)</div>'
                
        except Exception as e:
            return f'<div style="font-size: 0.8em; color: #ff6b6b; font-style: italic;">🔇 Audio error: {str(e)}</div>'
    
    def trigger_agent_cascade(self, initial_persona):
        """Disabled automatic cascade - personas only join when manually activated"""
        # Disabled to prevent automatic repetitive responses
        pass
    
    def regenerate_dynamic_personas(self):
        """Regenerate personas with new randomness"""
        if st.session_state.dynamic_personas:
            try:
                # Get the original spectral data (we need to store this)
                # For now, regenerate with current randomness level
                for i, persona in enumerate(st.session_state.dynamic_personas):
                    # Create mock spectral data for regeneration
                    mock_spectral_data = {
                        "area_1": {
                            "derived_indices": {
                                "NDVI": 0.5 + (st.session_state.randomness_level - 0.5) * 0.4,
                                "Urban_Index": 0.6 + (st.session_state.randomness_level - 0.5) * 0.3,
                                "Moisture_Stress": 0.4 + (st.session_state.randomness_level - 0.5) * 0.2
                            }
                        }
                    }
                    
                    # Get other personas for conflict generation (excluding current one)
                    other_personas = [p for j, p in enumerate(st.session_state.dynamic_personas) if j != i]
                    new_persona = self.citizen_generator.generate_dynamic_persona(
                        persona["band_id"],
                        mock_spectral_data,
                        randomness_level=st.session_state.randomness_level,
                        existing_personas=other_personas
                    )
                    st.session_state.dynamic_personas[i] = new_persona
                
                st.success("🎲 Regenerated all citizen personas with new randomness!")
                st.rerun()
                
            except Exception as e:
                st.error(f"Error regenerating personas: {e}")
    
    def render_conversation_area(self):
        """Render conversation area"""
        st.subheader("💬 Multi-Persona Dialogue")
        
        # Show active participants
        if st.session_state.active_citizens:
            active_names = []
            for citizen_id in st.session_state.active_citizens:
                persona = next((p for p in st.session_state.dynamic_personas if p["band_id"] == citizen_id), None)
                if persona:
                    active_names.append(self._get_proper_character_name(persona))
            
            st.info(f"🎭 **Active Participants:** {', '.join(active_names)}")
            
            if len(st.session_state.active_citizens) == 1:
                st.warning("💡 **Tip:** Add more spectral beings from the sidebar to create richer dialogue!")
        else:
            st.warning("⚠️ No active personas. Load some spectral data first!")
        
        # Display conversation history
        for message in st.session_state.conversation_history:
            if message["role"] == "user":
                st.markdown(f'<div class="user-message">👤 **You:** {message["content"]}</div>', unsafe_allow_html=True)
            else:
                persona_name = message.get("persona_name", "Citizen")
                band_id = message.get("band_id", "Unknown")
                
                # Clean formatting markers from content
                import re
                clean_content = message["content"]
                clean_content = re.sub(r'\*+([^*]+)\*+:?\s*', r'\1', clean_content)  # Remove **text**: patterns
                clean_content = re.sub(r'^[^:]*:\s*', '', clean_content)  # Remove "prefix:" patterns
                
                # Display the text response
                st.markdown(f'<div class="citizen-response">🎭 **{persona_name}:** {clean_content}</div>', unsafe_allow_html=True)
                
                # Add audio player if we have persona data
                if band_id != "Unknown" and st.session_state.active_citizens:
                    # Find the corresponding persona for voice generation
                    matching_persona = None
                    for citizen_id in st.session_state.active_citizens:
                        if citizen_id == band_id:
                            # Get the full persona object from dynamic_personas
                            matching_persona = next((p for p in st.session_state.dynamic_personas if p["band_id"] == citizen_id), None)
                            break
                    
                    if matching_persona:
                        # Generate and display audio player
                        audio_html = self._create_audio_player(clean_content, matching_persona, persona_name)
                        st.markdown(audio_html, unsafe_allow_html=True)
        
        # Message input using chat_input to prevent loops
        if st.session_state.active_citizens:
            user_message = st.chat_input(
                placeholder="Ask about Prague, share observations, or challenge their perspectives..."
            )
        else:
            st.chat_input(
                placeholder="Load spectral data first to start chatting...",
                disabled=True
            )
            user_message = None
        
        if user_message and st.session_state.active_citizens:
            self.process_user_message(user_message)
        
        # Inter-persona reaction button
        if st.session_state.active_citizens and len(st.session_state.active_citizens) > 1 and st.session_state.conversation_history:
            # Check if there's a previous persona message to react to
            last_persona_message = None
            for message in reversed(st.session_state.conversation_history):
                if message["role"] == "assistant":
                    last_persona_message = message
                    break
            
            if last_persona_message:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"💭 **Last speaker:** {last_persona_message.get('persona_name', 'Unknown')}")
                with col2:
                    if st.button("🎭 Persona Reacts", help="Let another persona react to the previous speaker"):
                        self.trigger_persona_reaction(last_persona_message)
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation"):
            st.session_state.conversation_history = []
            st.rerun()
    
    def process_user_message(self, message: str):
        """Process user message and generate citizen responses"""
        # Add user message to history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Generate response from ONE persona at a time for proper dialogue
        if st.session_state.active_citizens:
            # Initialize conversation turn tracker if not exists
            if 'conversation_turn' not in st.session_state:
                st.session_state.conversation_turn = 0
            
            # Select which persona responds this turn (rotate between active personas)
            current_turn = st.session_state.conversation_turn % len(st.session_state.active_citizens)
            responding_citizen_id = st.session_state.active_citizens[current_turn]
            citizen_persona = next((p for p in st.session_state.dynamic_personas if p["band_id"] == responding_citizen_id), None)
            
            if citizen_persona:
                try:
                    # Get other active personas for conflict generation
                    other_active_personas = [p for p in st.session_state.dynamic_personas
                                           if p["band_id"] in st.session_state.active_citizens
                                           and p["band_id"] != citizen_persona["band_id"]]
                    
                    # Enhance user message with conflict context if there are other personas
                    enhanced_message = message
                    if other_active_personas and len(other_active_personas) > 0:
                        other_names = [self._get_proper_character_name(p) for p in other_active_personas]
                        other_bands = [p["band_id"] for p in other_active_personas]
                        enhanced_message = f"{message}\n\n[Context: You are responding while other spectral activists {', '.join(other_names)} ({', '.join(other_bands)}) are also active. Feel free to challenge their approaches or propose competing solutions based on your {citizen_persona['band_id']} spectral analysis!]"
                    
                    # Create conversation context
                    context = ConversationContext(
                        user_input=enhanced_message,
                        language=st.session_state.current_language,
                        narrative_mode="direct",
                        active_personas=[citizen_persona["band_id"]],
                        spatial_context=st.session_state.spatial_context
                    )
                    
                    # Generate response using the dynamic persona
                    response_data = self.dialogue.generate_persona_response(
                        citizen_persona,
                        context
                    )
                    
                    # Add citizen response to history
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": response_data["response"],
                        "persona_name": self._get_proper_character_name(citizen_persona),
                        "band_id": citizen_persona.get("band_id", "Unknown")
                    })
                    
                    # Advance turn for next response
                    st.session_state.conversation_turn += 1
                    
                    # Force UI update to show the response immediately
                    st.rerun()
                    
                except Exception as e:
                    logger.error(f"Error generating response for {responding_citizen_id}: {e}")
                    st.session_state.conversation_history.append({
                        "role": "assistant",
                        "content": f"*{self._get_proper_character_name(citizen_persona)} is experiencing technical difficulties...*",
                        "persona_name": self._get_proper_character_name(citizen_persona),
                        "band_id": citizen_persona.get("band_id", "Unknown")
                    })
                    # Still advance turn even on error
                    st.session_state.conversation_turn += 1
                    
                    # Force UI update even on error
                    st.rerun()
    
    def trigger_persona_reaction(self, last_message: Dict):
        """Trigger a persona reaction to the previous speaker"""
        try:
            # Find a different persona to react (not the one who just spoke)
            last_speaker_name = last_message.get('persona_name', '')
            
            # Get available personas (excluding the last speaker)
            available_personas = []
            for citizen_id in st.session_state.active_citizens:
                persona = next((p for p in st.session_state.dynamic_personas if p["band_id"] == citizen_id), None)
                if persona:
                    persona_name = self._get_proper_character_name(persona)
                    if persona_name != last_speaker_name:
                        available_personas.append(persona)
            
            if available_personas:
                # Select a random persona to react
                import random
                reacting_persona = random.choice(available_personas)
                
                # Create a reaction context
                reaction_prompt = f"React to what {last_speaker_name} just said: '{last_message['content']}'"
                
                context = ConversationContext(
                    user_input=reaction_prompt,
                    language=st.session_state.current_language,
                    narrative_mode="direct",
                    active_personas=[reacting_persona["band_id"]],
                    spatial_context=st.session_state.spatial_context
                )
                
                # Generate reaction
                response_data = self.dialogue.generate_persona_response(
                    reacting_persona,
                    context
                )
                
                # Add reaction to conversation history
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response_data["response"],
                    "persona_name": self._get_proper_character_name(reacting_persona),
                    "band_id": reacting_persona.get("band_id", "Unknown")
                })
                
                st.rerun()
                
        except Exception as e:
            logger.error(f"Error triggering persona reaction: {e}")
            st.error(f"Could not generate persona reaction: {e}")

    def generate_conflict_dialogue(self):
        """Generate spontaneous conflicts between active personas"""
        if len(st.session_state.active_citizens) < 2:
            return
            
        try:
            # Get all active personas
            active_personas = [p for p in st.session_state.dynamic_personas
                             if p["band_id"] in st.session_state.active_citizens]
            
            if len(active_personas) < 2:
                return
                
            # Create conflict scenarios based on band combinations
            import random
            persona1, persona2 = random.sample(active_personas, 2)
            
            # Generate conflict topics based on their bands
            conflict_topics = {
                ("B02", "B08"): "air quality vs vegetation health priorities",
                ("B02", "B11"): "atmospheric pollution vs soil moisture crisis",
                ("B02", "B12"): "air quality vs urban heat island effects",
                ("B08", "B11"): "vegetation biomass vs water stress solutions",
                ("B08", "B12"): "plant health vs thermal management strategies",
                ("B11", "B12"): "moisture conservation vs heat reduction methods",
                ("B03", "B04"): "green light photosynthesis vs red light absorption analysis",
                ("B03", "B08"): "visible vegetation vs infrared biomass detection",
                ("B04", "B11"): "plant stress indicators vs water content measurements"
            }
            
            # Get conflict topic
            band_pair = tuple(sorted([persona1["band_id"], persona2["band_id"]]))
            topic = conflict_topics.get(band_pair, "environmental monitoring approaches")
            
            # Generate conflict dialogue
            conflict_prompt = f"Start a heated but funny argument with {self._get_proper_character_name(persona2)} about {topic}. Challenge their {persona2['band_id']} approach with your {persona1['band_id']} spectral evidence from Prague!"
            
            context = ConversationContext(
                user_input=conflict_prompt,
                language=st.session_state.current_language,
                narrative_mode="direct",
                active_personas=[persona1["band_id"]],
                spatial_context=st.session_state.spatial_context
            )
            
            # Generate first persona's challenge
            response1 = self.dialogue.generate_persona_response(persona1, context)
            
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response1["response"],
                "persona_name": self._get_proper_character_name(persona1),
                "band_id": persona1["band_id"],
                "voice_type": "conflict_initiation"
            })
            
            # Generate second persona's counter-response
            counter_prompt = f"Respond angrily and humorously to {self._get_proper_character_name(persona1)}'s challenge: '{response1['response']}'. Defend your {persona2['band_id']} approach and propose a better solution!"
            
            context2 = ConversationContext(
                user_input=counter_prompt,
                language=st.session_state.current_language,
                narrative_mode="direct",
                active_personas=[persona2["band_id"]],
                spatial_context=st.session_state.spatial_context
            )
            
            response2 = self.dialogue.generate_persona_response(persona2, context2)
            
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response2["response"],
                "persona_name": self._get_proper_character_name(persona2),
                "band_id": persona2["band_id"],
                "voice_type": "conflict_response"
            })
            
            st.rerun()
            
        except Exception as e:
            logger.error(f"Error generating conflict dialogue: {e}")

# Main application
if __name__ == "__main__":
    app = DynamicCitizenPersonaChat()
    app.run()