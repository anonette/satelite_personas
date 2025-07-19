"""
Spectral Persona Chat Interface
Main Streamlit application for conversing with satellite-derived spectral band personas
"""

import streamlit as st
import os
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

# Import our custom modules
from core.satellite.tiff_persona_extractor import TIFFPersonaExtractor
from core.satellite.zip_tiff_processor import ZipTiffProcessor, process_browser_images_zip, process_existing_tiff_files
from core.conversation.spectral_dialogue import SpectralDialogue, ConversationContext
from core.language.ethical_dative import EthicalDativeGenerator, RhetoricalMode
from core.personas.dynamic_citizen_personas import DynamicCitizenPersonaGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🛰️ Spectral Persona Chat",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimalist design
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 300;
        color: #2E3440;
        margin-bottom: 1rem;
    }
    .persona-card {
        background: #F8F9FA;
        border-left: 4px solid #5E81AC;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0 8px 8px 0;
    }
    .persona-response {
        background: #ECEFF4;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        border-left: 3px solid #88C0D0;
    }
    .user-message {
        background: #E5E9F0;
        padding: 0.8rem;
        margin: 0.3rem 0;
        border-radius: 8px;
        border-left: 3px solid #D08770;
    }
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .active { background-color: #A3BE8C; }
    .inactive { background-color: #BF616A; }
    .whisper { background-color: #EBCB8B; }
</style>
""", unsafe_allow_html=True)

class SpectralPersonaInterface:
    """Main interface class for spectral persona chat"""
    
    def __init__(self):
        self.extractor = TIFFPersonaExtractor()
        self.zip_processor = ZipTiffProcessor()
        self.dialogue = SpectralDialogue(temperature=1.1)
        self.ethical_dative = EthicalDativeGenerator()
        
        # Initialize session state
        if 'personas' not in st.session_state:
            st.session_state.personas = []
        if 'active_personas' not in st.session_state:
            st.session_state.active_personas = []
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []
        if 'current_language' not in st.session_state:
            st.session_state.current_language = 'czech'
        if 'narrative_mode' not in st.session_state:
            st.session_state.narrative_mode = 'direct'
        if 'spatial_context' not in st.session_state:
            st.session_state.spatial_context = None
    
    def render_header(self):
        """Render the main header with language selection"""
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown('<h1 class="main-header">🛰️ Spectral Persona Chat</h1>', unsafe_allow_html=True)
        
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
                key="language_selector"
            )
            
            if selected_lang != st.session_state.current_language:
                st.session_state.current_language = selected_lang
                st.rerun()
        
        with col3:
            # Temperature control
            temperature = st.slider(
                "🌡️ Creativity",
                min_value=0.1,
                max_value=2.0,
                value=1.1,
                step=0.1,
                key="temperature_slider"
            )
            self.dialogue.temperature = temperature
    
    def render_tiff_loader(self):
        """Render TIFF file loading interface"""
        st.subheader("📁 Load Satellite Image")
        
        # Get available sources
        sources = self.zip_processor.get_available_sources()
        
        # Create tabs for different loading options
        tab1, tab2, tab3, tab4 = st.tabs(["🗜️ ZIP Files", "📁 TIFF Directories", "📄 Individual TIFFs", "🎭 Mock Personas"])
        
        with tab1:
            st.write("**Process ZIP archives containing TIFF files**")
            
            if sources["zip_files"]:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    selected_zip = st.selectbox(
                        "Select ZIP file:",
                        options=sources["zip_files"],
                        format_func=lambda x: os.path.basename(x),
                        key="zip_selector"
                    )
                
                with col2:
                    if st.button("🗜️ Process ZIP", type="primary"):
                        self.load_personas_from_zip(selected_zip)
                
                # Special button for Browser images ZIP
                if any("Browser_images" in zip_file for zip_file in sources["zip_files"]):
                    st.markdown("---")
                    if st.button("🛰️ Load Browser Images (Recommended)", type="secondary"):
                        self.load_browser_images_zip()
            else:
                st.info("No ZIP files found in images directory")
        
        with tab2:
            st.write("**Process directories containing TIFF files**")
            
            if sources["tiff_directories"]:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    selected_dir = st.selectbox(
                        "Select TIFF directory:",
                        options=sources["tiff_directories"],
                        format_func=lambda x: os.path.relpath(x, "images"),
                        key="tiff_dir_selector"
                    )
                
                with col2:
                    if st.button("📁 Process Directory", type="primary"):
                        self.load_personas_from_tiff_directory(selected_dir)
                
                # Show TIFF files in selected directory
                if selected_dir:
                    tiff_files = [f for f in os.listdir(selected_dir) if f.lower().endswith(('.tif', '.tiff'))]
                    if tiff_files:
                        st.write(f"**Found {len(tiff_files)} TIFF files:**")
                        for tiff_file in tiff_files[:5]:  # Show first 5
                            st.write(f"• {tiff_file}")
                        if len(tiff_files) > 5:
                            st.write(f"• ... and {len(tiff_files) - 5} more")
            else:
                st.info("No TIFF directories found")
        
        with tab3:
            st.write("**Process individual TIFF files**")
            
            if sources["individual_tiffs"]:
                selected_tiff = st.selectbox(
                    "Select TIFF file:",
                    options=sources["individual_tiffs"],
                    format_func=lambda x: os.path.basename(x),
                    key="individual_tiff_selector"
                )
                
                if st.button("📄 Process Single TIFF", type="primary"):
                    self.load_personas_from_single_tiff(selected_tiff)
            else:
                st.info("No individual TIFF files found")
        
        with tab4:
            st.write("**Generate mock personas for demonstration**")
            st.info("Use this option if no real TIFF data is available")
            
            if st.button("🎭 Generate Mock Personas", type="primary"):
                self.generate_mock_personas()
    
    def load_personas_from_directory(self, image_dir: str):
        """Load personas from satellite image directory"""
        try:
            # Look for TIFF files in the directory
            image_path = os.path.join("images", image_dir)
            tiff_files = [f for f in os.listdir(image_path) if f.endswith('.tif')]
            
            if tiff_files:
                # Use the first TIFF file found
                tiff_path = os.path.join(image_path, tiff_files[0])
                personas = self.extractor.extract_all_personas(tiff_path)
                
                st.session_state.personas = personas
                st.session_state.active_personas = [p["band_id"] for p in personas[:3]]  # Activate first 3
                
                # Set spatial context
                if personas:
                    coords = personas[0].get("center_coordinates", [50.075, 14.437])
                    st.session_state.spatial_context = {
                        "lat": coords[0],
                        "lon": coords[1],
                        "location": personas[0].get("location_name", "Prague")
                    }
                
                st.success(f"✅ Loaded {len(personas)} spectral personas from {image_dir}")
                st.rerun()
            else:
                st.error("No TIFF files found in selected directory")
                
        except Exception as e:
            st.error(f"Error loading personas: {e}")
            logger.error(f"Error loading personas from {image_dir}: {e}")
    
    def generate_mock_personas(self):
        """Generate mock personas for demonstration"""
        try:
            mock_tiff_path = "images/mock/satellite_data.tif"
            personas = self.extractor.extract_all_personas(mock_tiff_path)
            
            st.session_state.personas = personas
            st.session_state.active_personas = [p["band_id"] for p in personas[:3]]
            
            # Set mock spatial context
            st.session_state.spatial_context = {
                "lat": 50.075,
                "lon": 14.437,
                "location": "Nusle Basin, Prague"
            }
            
            st.success(f"✅ Generated {len(personas)} mock spectral personas")
            st.rerun()
            
        except Exception as e:
            st.error(f"Error generating mock personas: {e}")
            logger.error(f"Error generating mock personas: {e}")
    def load_personas_from_zip(self, zip_path: str):
        """Load personas from ZIP file"""
        try:
            with st.spinner(f"Processing ZIP file: {os.path.basename(zip_path)}..."):
                personas = self.zip_processor.process_zip_to_personas(zip_path)
                
                if personas:
                    st.session_state.personas = personas
                    st.session_state.active_personas = [p["band_id"] for p in personas[:4]]  # Activate first 4
                    
                    # Set spatial context from first persona
                    coords = personas[0].get("center_coordinates", [50.075, 14.437])
                    st.session_state.spatial_context = {
                        "lat": coords[0],
                        "lon": coords[1],
                        "location": personas[0].get("location_name", "Prague"),
                        "source": f"ZIP: {os.path.basename(zip_path)}"
                    }
                    
                    st.success(f"✅ Loaded {len(personas)} spectral personas from ZIP file")
                    
                    # Show loaded personas
                    st.write("**Loaded personas:**")
                    for persona in personas:
                        st.write(f"• {persona['character']} ({persona['band_id']}) - {persona.get('source_file', 'unknown')}")
                    
                    st.rerun()
                else:
                    st.warning("No valid spectral bands found in ZIP file")
                    
        except Exception as e:
            st.error(f"Error processing ZIP file: {e}")
            logger.error(f"Error processing ZIP file {zip_path}: {e}")
    
    def load_browser_images_zip(self):
        """Load personas from Browser images ZIP file"""
        try:
            with st.spinner("Processing Browser images ZIP file..."):
                personas = process_browser_images_zip()
                
                if personas:
                    st.session_state.personas = personas
                    st.session_state.active_personas = [p["band_id"] for p in personas[:4]]
                    
                    # Set spatial context
                    coords = personas[0].get("center_coordinates", [50.075, 14.437])
                    st.session_state.spatial_context = {
                        "lat": coords[0],
                        "lon": coords[1],
                        "location": personas[0].get("location_name", "Prague"),
                        "source": "Browser Images ZIP"
                    }
                    
                    st.success(f"✅ Loaded {len(personas)} spectral personas from Browser images")
                    
                    # Show loaded personas
                    st.write("**Loaded personas:**")
                    for persona in personas:
                        st.write(f"• {persona['character']} ({persona['band_id']}) - {persona.get('source_file', 'unknown')}")
                    
                    st.rerun()
                else:
                    st.warning("No valid spectral bands found in Browser images ZIP")
                    
        except Exception as e:
            st.error(f"Error processing Browser images ZIP: {e}")
            logger.error(f"Error processing Browser images ZIP: {e}")
    
    def load_personas_from_tiff_directory(self, tiff_dir: str):
        """Load personas from TIFF directory"""
        try:
            with st.spinner(f"Processing TIFF directory: {os.path.basename(tiff_dir)}..."):
                personas = self.zip_processor.process_existing_tiff_directory(tiff_dir)
                
                if personas:
                    st.session_state.personas = personas
                    st.session_state.active_personas = [p["band_id"] for p in personas[:4]]
                    
                    # Set spatial context
                    coords = personas[0].get("center_coordinates", [50.075, 14.437])
                    st.session_state.spatial_context = {
                        "lat": coords[0],
                        "lon": coords[1],
                        "location": personas[0].get("location_name", "Prague"),
                        "source": f"Directory: {os.path.basename(tiff_dir)}"
                    }
                    
                    st.success(f"✅ Loaded {len(personas)} spectral personas from TIFF directory")
                    
                    # Show loaded personas
                    st.write("**Loaded personas:**")
                    for persona in personas:
                        st.write(f"• {persona['character']} ({persona['band_id']}) - {persona.get('source_file', 'unknown')}")
                    
                    st.rerun()
                else:
                    st.warning("No valid spectral bands found in TIFF directory")
                    
        except Exception as e:
            st.error(f"Error processing TIFF directory: {e}")
            logger.error(f"Error processing TIFF directory {tiff_dir}: {e}")
    
    def load_personas_from_single_tiff(self, tiff_path: str):
        """Load personas from single TIFF file"""
        try:
            with st.spinner(f"Processing TIFF file: {os.path.basename(tiff_path)}..."):
                # Determine band ID from filename
                filename = os.path.basename(tiff_path).lower()
                band_id = "B08"  # Default
                
                if 'b02' in filename or '_02_' in filename:
                    band_id = "B02"
                elif 'b03' in filename or '_03_' in filename:
                    band_id = "B03"
                elif 'b04' in filename or '_04_' in filename:
                    band_id = "B04"
                elif 'b08' in filename or '_08_' in filename:
                    band_id = "B08"
                elif 'b11' in filename or '_11_' in filename:
                    band_id = "B11"
                elif 'b12' in filename or '_12_' in filename:
                    band_id = "B12"
                
                persona = self.extractor.generate_persona_profile(tiff_path, band_id)
                persona['source_file'] = os.path.basename(tiff_path)
                
                st.session_state.personas = [persona]
                st.session_state.active_personas = [persona["band_id"]]
                
                # Set spatial context
                coords = persona.get("center_coordinates", [50.075, 14.437])
                st.session_state.spatial_context = {
                    "lat": coords[0],
                    "lon": coords[1],
                    "location": persona.get("location_name", "Prague"),
                    "source": f"Single TIFF: {os.path.basename(tiff_path)}"
                }
                
                st.success(f"✅ Loaded persona: {persona['character']} ({persona['band_id']})")
                st.rerun()
                
        except Exception as e:
            st.error(f"Error processing single TIFF: {e}")
            logger.error(f"Error processing single TIFF {tiff_path}: {e}")

    
    def render_persona_controls(self):
        """Render persona activation and mode controls"""
        if not st.session_state.personas:
            return
        
        st.subheader("🎭 Active Personas")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Persona activation checkboxes
            persona_options = {p["band_id"]: f"{p['character']} ({p['band_id']})" 
                             for p in st.session_state.personas}
            
            selected_personas = st.multiselect(
                "Select active personas:",
                options=list(persona_options.keys()),
                default=st.session_state.active_personas,
                format_func=lambda x: persona_options[x],
                key="persona_selector"
            )
            
            st.session_state.active_personas = selected_personas
        
        with col2:
            # Narrative mode selector
            narrative_modes = {
                'whisper': '🌬️ Whisper',
                'direct': '💬 Direct',
                'trial': '⚖️ Trial',
                'conflict': '⚔️ Conflict'
            }
            
            selected_mode = st.selectbox(
                "Narrative Mode:",
                options=list(narrative_modes.keys()),
                format_func=lambda x: narrative_modes[x],
                index=list(narrative_modes.keys()).index(st.session_state.narrative_mode),
                key="narrative_mode_selector"
            )
            
            st.session_state.narrative_mode = selected_mode
    
    def render_spatial_info(self):
        """Render spatial context information"""
        if st.session_state.spatial_context:
            spatial = st.session_state.spatial_context
            
            st.markdown(f"""
            📍 **Location:** {spatial.get('location', 'Unknown')}
            🌐 **Coordinates:** {spatial.get('lat', 0):.4f}, {spatial.get('lon', 0):.4f}
            📅 **Image:** {datetime.now().strftime('%Y-%m-%d')}
            🗂️ **Source:** {spatial.get('source', 'Unknown')}
            """)
    
    def render_conversation_interface(self):
        """Render the main conversation interface"""
        if not st.session_state.active_personas:
            st.info("Select personas above to start conversation")
            return
        
        st.subheader("💬 Conversation")
        
        # Display conversation history
        self.render_conversation_history()
        
        # User input
        user_input = st.chat_input(
            placeholder=f"Type your message to the spectral personas... (Language: {st.session_state.current_language})"
        )
        
        if user_input:
            self.process_user_input(user_input)
    
    def render_conversation_history(self):
        """Render conversation history"""
        if not st.session_state.conversation_history:
            st.info("Start a conversation by typing a message below")
            return
        
        # Create scrollable container for conversation
        with st.container():
            for exchange in st.session_state.conversation_history[-10:]:  # Show last 10 exchanges
                # User message
                if exchange.get("user_input"):
                    st.markdown(f"""
                    <div class="user-message">
                        <strong>You:</strong> {exchange["user_input"]}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Persona responses
                for response in exchange.get("responses", []):
                    persona_name = response.get("character", response.get("persona_id", "Unknown"))
                    persona_response = response.get("response", "")
                    emotional_state = response.get("emotional_state", "calm")
                    
                    # Status indicator based on emotional state
                    status_class = "active" if emotional_state in ["protective", "curious"] else \
                                  "inactive" if emotional_state in ["distressed", "angry"] else "whisper"
                    
                    st.markdown(f"""
                    <div class="persona-response">
                        <span class="status-indicator {status_class}"></span>
                        <strong>{persona_name}:</strong> {persona_response}
                        <br><small style="color: #666;">({emotional_state} • {response.get('language', 'czech')})</small>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
    
    def process_user_input(self, user_input: str):
        """Process user input and generate persona responses"""
        try:
            # Get active persona profiles
            active_persona_profiles = [
                p for p in st.session_state.personas 
                if p["band_id"] in st.session_state.active_personas
            ]
            
            if not active_persona_profiles:
                st.warning("No active personas selected")
                return
            
            # Create conversation context
            context = ConversationContext(
                user_input=user_input,
                language=st.session_state.current_language,
                narrative_mode=st.session_state.narrative_mode,
                active_personas=st.session_state.active_personas,
                spatial_context=st.session_state.spatial_context,
                conversation_history=st.session_state.conversation_history
            )
            
            # Generate responses
            with st.spinner("Spectral personas are responding..."):
                responses = self.dialogue.generate_multi_persona_conversation(
                    active_persona_profiles, context
                )
            
            # Add to conversation history
            exchange = {
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "responses": responses,
                "narrative_mode": st.session_state.narrative_mode,
                "language": st.session_state.current_language
            }
            
            st.session_state.conversation_history.append(exchange)
            
            # Rerun to update display
            st.rerun()
            
        except Exception as e:
            st.error(f"Error processing input: {e}")
            logger.error(f"Error processing user input: {e}")
    
    def render_persona_status(self):
        """Render status of active personas"""
        if not st.session_state.active_personas:
            return
        
        st.subheader("📊 Persona Status")
        
        active_profiles = [
            p for p in st.session_state.personas 
            if p["band_id"] in st.session_state.active_personas
        ]
        
        cols = st.columns(len(active_profiles))
        
        for i, persona in enumerate(active_profiles):
            with cols[i]:
                # Get persona memory if available
                memory = self.dialogue.persona_memories.get(persona["band_id"])
                
                st.markdown(f"""
                <div class="persona-card">
                    <h4>{persona['character']}</h4>
                    <p><strong>Band:</strong> {persona['band_id']}</p>
                    <p><strong>Function:</strong> {persona.get('function', 'observation')}</p>
                    <p><strong>Mode:</strong> {persona.get('rhetorical_mode', 'ethical_dative')}</p>
                    {f"<p><strong>State:</strong> {memory.current_emotional_state.value}</p>" if memory else ""}
                    {f"<p><strong>Observations:</strong> {len(memory.observations)}</p>" if memory else ""}
                </div>
                """, unsafe_allow_html=True)
    
    def render_sidebar_controls(self):
        """Render sidebar with additional controls"""
        with st.sidebar:
            st.header("🛠️ Controls")
            
            # Export conversation
            if st.button("💾 Export Conversation"):
                self.export_conversation()
            
            # Clear conversation
            if st.button("🗑️ Clear Conversation"):
                st.session_state.conversation_history = []
                st.rerun()
            
            # Show conversation stats
            if st.session_state.conversation_history:
                st.subheader("📈 Statistics")
                total_exchanges = len(st.session_state.conversation_history)
                total_responses = sum(
                    len(exchange.get("responses", [])) 
                    for exchange in st.session_state.conversation_history
                )
                
                st.metric("Total Exchanges", total_exchanges)
                st.metric("Total Responses", total_responses)
                st.metric("Active Personas", len(st.session_state.active_personas))
            
            # Debug information
            if st.checkbox("🔍 Debug Mode"):
                st.subheader("Debug Info")
                st.json({
                    "current_language": st.session_state.current_language,
                    "narrative_mode": st.session_state.narrative_mode,
                    "active_personas": st.session_state.active_personas,
                    "spatial_context": st.session_state.spatial_context,
                    "total_personas": len(st.session_state.personas)
                })
    
    def export_conversation(self):
        """Export conversation history to JSON"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "conversation_history": st.session_state.conversation_history,
                "personas": st.session_state.personas,
                "spatial_context": st.session_state.spatial_context,
                "settings": {
                    "language": st.session_state.current_language,
                    "narrative_mode": st.session_state.narrative_mode,
                    "temperature": self.dialogue.temperature
                }
            }
            
            filename = f"spectral_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            st.download_button(
                label="📥 Download Conversation",
                data=json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=filename,
                mime="application/json"
            )
            
        except Exception as e:
            st.error(f"Error exporting conversation: {e}")
    
    def run(self):
        """Main application runner"""
        # Render main interface
        self.render_header()
        
        # Render sidebar
        self.render_sidebar_controls()
        
        # Main content area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # TIFF loader
            self.render_tiff_loader()
            
            # Persona controls
            self.render_persona_controls()
            
            # Spatial info
            self.render_spatial_info()
            
            # Conversation interface
            self.render_conversation_interface()
        
        with col2:
            # Persona status
            self.render_persona_status()

def main():
    """Main application entry point"""
    try:
        interface = SpectralPersonaInterface()
        interface.run()
        
    except Exception as e:
        st.error(f"Application error: {e}")
        logger.error(f"Application error: {e}")
        
        # Show error details in debug mode
        if st.checkbox("Show Error Details"):
            st.exception(e)

if __name__ == "__main__":
    main()