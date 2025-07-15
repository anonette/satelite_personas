import streamlit as st
import os
import json
from pathlib import Path
import base64
from PIL import Image
# Disable PIL decompression bomb warning for trusted satellite data sources
Image.MAX_IMAGE_PIXELS = None
import numpy as np
from datetime import datetime
import time
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Import configuration system
from core.config import get_config

# Import our existing modules
from core.satellite.image_spectral_processor import SatelliteImageProcessor, GPT4oVisionAnalyzer, ImageSpectralExtractor
from core.personas.spectral_multiplicity_notebook import (
    GPT4oPersonaGenerator as SpectralPersonaGenerator,
    SpectralMultiplicityPipeline,
    SpectralTile
)
# Import the new unified persona system
from core.personas.unified_persona_system import UnifiedPersonaSystem, UnifiedPersona
# Import the persona library system
from core.theater.persona_library import PersonaLibrary
# Import the session logger
from core.theater.session_logger import TheaterSessionLogger
# Import the dual staging system
from core.theater.dual_staging_system import DualStagingSystem
# Import conspiracy system
from core.conspiracy.non_human_actor_detector import NonHumanActorDetector
from core.conspiracy.conspiracy_dialogue_generator import ConspiracyDialogueGenerator

class CivicTheaterStage:
    def __init__(self):
        # Get API key from environment or session state
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key and 'openai_api_key' in st.session_state:
            self.api_key = st.session_state.openai_api_key
        
        # If still no API key, show configuration
        if not self.api_key:
            self.show_api_key_config()
            st.stop()
        
        self.image_processor = SatelliteImageProcessor()
        self.vision_analyzer = GPT4oVisionAnalyzer(self.api_key)
        
        # Initialize spectral multiplicity system
        self.spectral_generator = SpectralPersonaGenerator(self.api_key)
        self.spectral_pipeline = SpectralMultiplicityPipeline(self.api_key)
        
        # Create OpenAI client for dialogue generation
        self.openai_client = openai.OpenAI(api_key=self.api_key) if self.api_key else None
        
        # Initialize unified persona system
        self.unified_persona_system = UnifiedPersonaSystem(self.api_key)
        
        # Initialize persona library system
        config = get_config()
        self.persona_library = PersonaLibrary(config.persona_library_dir)
        
        # Initialize session logger
        self.session_logger = TheaterSessionLogger()
        
        # Initialize dual staging system
        self.dual_staging_system = DualStagingSystem()
        
        # Initialize conspiracy system
        self.conspiracy_detector = NonHumanActorDetector()
        self.conspiracy_dialogue = ConspiracyDialogueGenerator(self.api_key) if self.api_key else None
        
        # Always start a new session (fresh start)
        if 'current_session_id' not in st.session_state:
            session_id = self.session_logger.start_new_session()
            st.session_state.current_session_id = session_id
        
        # Theater state
        if 'stage_set' not in st.session_state:
            st.session_state.stage_set = False
        if 'active_personas' not in st.session_state:
            st.session_state.active_personas = []
        if 'dialogue_history' not in st.session_state:
            st.session_state.dialogue_history = []
        if 'selected_image' not in st.session_state:
            st.session_state.selected_image = None
        if 'image_analysis' not in st.session_state:
            st.session_state.image_analysis = None
        if 'speaking_queue' not in st.session_state:
            st.session_state.speaking_queue = []
        if 'persona_library_view' not in st.session_state:
            st.session_state.persona_library_view = 'saved_personas'
        if 'selected_library_personas' not in st.session_state:
            st.session_state.selected_library_personas = []
        if 'persona_generation_mode' not in st.session_state:
            st.session_state.persona_generation_mode = 'hybrid'  # 'arendtian', 'spectral', or 'hybrid'
    
    def show_api_key_config(self):
        """Show API key configuration interface"""
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%); color: white; border-radius: 10px; margin-bottom: 30px;">
            <h1>🔑 API Key Configuration</h1>
            <p>You need an OpenAI API key to run the Civic Theater Stage</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.header("🛠️ Setup Instructions")
        
        st.markdown("""
        **Option 1: Environment Variable (Recommended)**
        1. Create a `.env` file in your project directory
        2. Add: `OPENAI_API_KEY=your_api_key_here`
        3. Restart the application
        
        **Option 2: Direct Input (Temporary)**
        Enter your API key below (will be stored in session only):
        """)
        
        api_key_input = st.text_input(
            "OpenAI API Key:",
            type="password",
            placeholder="sk-..."
        )
        
        if st.button("🚀 Launch Theater with API Key"):
            if api_key_input:
                st.session_state.openai_api_key = api_key_input
                st.success("✅ API key configured! Launching theater...")
                st.rerun()
            else:
                st.error("❌ Please enter your OpenAI API key")
        
        st.markdown("""
        ---
        **Get your OpenAI API key:**
        1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
        2. Sign in or create an account
        3. Create a new API key
        4. Copy and paste it above
        """)
    
    def display_stage_header(self):
        st.markdown("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 10px; margin-bottom: 30px;">
            <h1>🎭 Civic Theater Stage</h1>
            <h3>Where Satellite Spectral Beings Discuss Climate & Democracy</h3>
            <p><em>A digital theater for non-human civic dialogue</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Add clear instructions
        if not st.session_state.stage_set:
            st.info("👋 **Welcome!** Follow these simple steps: 1️⃣ Choose an image → 2️⃣ Generate personas → 3️⃣ Start conversations")
        else:
            st.success("🎭 **Theater is ready!** Use the tabs below to create dialogues between your spectral beings.")
    
    def image_selection_stage(self):
        st.header("1️⃣ Choose Your Satellite Image")
        st.markdown("**Select a satellite image to generate spectral personas from real environmental data**")
        
        # Use configuration system for cross-platform paths
        config = get_config()
        images_dir = config.images_dir
        
        if not images_dir.exists():
            st.error(f"❌ Images directory not found: {images_dir}")
            st.info("💡 **Solution:** You can set a custom images directory with the IMAGES_DIR environment variable")
            return None
        
        # Get available images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif']:
            image_files.extend(images_dir.glob(ext))
        
        if not image_files:
            st.error("❌ No satellite images found in the directory")
            st.info("💡 **Solution:** Add satellite images (.jpg, .png, .tiff) to the images directory")
            return None
        
        st.success(f"✅ Found {len(image_files)} satellite images")
        
        # Display images for selection with clearer layout
        st.markdown("**👇 Click on an image below to select it:**")
        
        cols = st.columns(3)
        selected_image = None
        
        for i, img_path in enumerate(image_files):
            with cols[i % 3]:
                try:
                    img = Image.open(img_path)
                    st.image(img, caption=f"📸 {img_path.name}", width=200)
                    if st.button(f"✅ Select This Image", key=f"select_{i}", type="primary"):
                        selected_image = img_path
                        st.session_state.selected_image = img_path
                        st.session_state.stage_set = False  # Reset stage
                        st.success(f"🎯 Selected: {img_path.name}")
                        st.rerun()
                except Exception as e:
                    st.error(f"❌ Error loading {img_path.name}: {e}")
        
        return selected_image
    
    
    def generate_spectral_personas_from_image(self, image_path, max_personas=5):
        """Generate personas using the spectral multiplicity system with REAL IMAGE DATA"""
        
        personas = []
        
        st.info(f"🌈 Generating up to {max_personas} spectral multiplicity personas from REAL image data...")
        
        # Use ImageSpectralExtractor to get real spectral data
        try:
            from core.satellite.image_spectral_processor import ImageSpectralExtractor
            
            # Initialize the image extractor
            image_extractor = ImageSpectralExtractor(self.api_key)
            
            # Prague zones to analyze - limit based on max_personas
            all_prague_zones = ["letna_park", "old_town", "petrin_hill", "vltava_river", "vinohrady"]
            
            # Limit zones based on max_personas (reserve 1 for Shadow District)
            zones_to_analyze = all_prague_zones[:max_personas-1] if max_personas > 1 else all_prague_zones[:1]
            
            st.info(f"🔍 Extracting real spectral data from satellite images for {len(zones_to_analyze)} zones...")
            
            # Extract real spectral data for each zone
            real_spectral_data = []
            for zone in zones_to_analyze:
                st.info(f"   📊 Analyzing {zone}...")
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
                        st.success(f"   ✅ {zone} spectral data extracted successfully")
                    else:
                        st.warning(f"   ⚠️  No spectral data found for {zone}")
                except Exception as e:
                    st.error(f"   ❌ Error extracting data for {zone}: {e}")
            
            if not real_spectral_data:
                st.error("❌ No real spectral data could be extracted from images")
                st.error("   Make sure satellite images are available in the 'images' directory")
                return []
                
            st.success(f"✅ Successfully extracted spectral data for {len(real_spectral_data)} zones")
            
            # Generate Shadow District automatically
            st.info("🌑 Manifesting Shadow District as Prague's metaphysical antagonist...")
            mode_mapper = self.spectral_pipeline.persona_generator.mode_mapper
            shadow_bands = mode_mapper.generate_shadow_spectral_signature(real_spectral_data)
            
            # Add Shadow District to the data
            shadow_district = {
                'location': 'shadow_district',
                'lat': 50.0858,  # Center of Prague
                'lon': 14.4208,
                'date': '∞ (Eternal)',
                'bands': shadow_bands
            }
            
            # Include shadow in the generation
            all_districts = real_spectral_data + [shadow_district]
            
            st.info("🔬 Processing spectral tiles and generating advanced personas...")
            
            # Generate personas using spectral multiplicity pipeline
            spectral_personas = self.spectral_pipeline.process_prague_districts(all_districts)
            
            for spectral_persona in spectral_personas:
                # Convert to theater format
                theater_persona = {
                    'name': spectral_persona.name,
                    'location': spectral_persona.location,
                    'role': f"Spectral Multiplicity Citizen of {spectral_persona.location}",
                    'type': 'spectral_multiplicity',
                    'arendtian_mode': spectral_persona.arendtian_mode,
                    'mood': spectral_persona.mood,
                    'civic_position': spectral_persona.civic_conflict,
                    'democratic_tension': spectral_persona.dialogue_potential,
                    'temporal_status': spectral_persona.temporal_status,
                    'voice': spectral_persona.voice,
                    'perspective': f"Spectral indices: NDVI {spectral_persona.dominant_indices.get('NDVI', 0):.3f}, UI {spectral_persona.dominant_indices.get('Urban_Index', 0):.3f}",
                    'values': f"Spectral integrity and {spectral_persona.arendtian_mode} approach",
                    'dominant_indices': spectral_persona.dominant_indices,
                    'spectral_signature': spectral_persona.dominant_indices
                }
                
                personas.append(theater_persona)
                st.success(f"🌈 Generated spectral persona: {spectral_persona.name}")
            
                st.success(f"🌈 Successfully generated {len(personas)} spectral multiplicity personas from REAL image data!")
                
                # Log the persona generation
                self.session_logger.log_persona_generation(
                    personas, 
                    str(image_path), 
                    {'max_personas': max_personas, 'generation_type': 'spectral_multiplicity'}
                )
            
        except ImportError:
            st.error("❌ ImageSpectralExtractor not available")
            st.error("   Please ensure core.satellite.image_spectral_processor is properly installed")
            return []
        except ValueError as e:
            st.error(f"❌ API Error: {e}")
            st.error("   Please check your OpenAI API key and try again")
            return []
        except Exception as e:
            st.error(f"❌ Error generating spectral personas: {e}")
            st.error("   Check that satellite images are available and API key is valid")
            return []
            
        return personas
    
    def generate_conspiracy_actors_from_image(self, image_path, max_actors=5):
        """Generate Conspiracy Theater actors - non-human entities with impossible agendas"""
        
        actors = []
        
        st.info(f"🕵️ Scanning satellite data for suspicious non-human activity...")
        
        try:
            from core.satellite.image_spectral_processor import ImageSpectralExtractor
            import time
            
            # Initialize the image extractor
            image_extractor = ImageSpectralExtractor(self.api_key)
            
            # Prague zones to analyze - limit based on max_actors
            all_prague_zones = ["letna_park", "old_town", "petrin_hill", "vltava_river", "vinohrady"]
            
            # Limit zones based on max_actors
            zones_to_analyze = all_prague_zones[:max_actors] if max_actors <= len(all_prague_zones) else all_prague_zones
            
            st.info(f"🔍 Analyzing {len(zones_to_analyze)} Prague districts for suspicious activity...")
            
            # Extract spectral data for conspiracy detection
            zone_data_list = []
            for zone in zones_to_analyze:
                st.info(f"   📡 Scanning {zone} for non-human activity...")
                try:
                    spectral_data = image_extractor.extract_spectral_data_for_zone(zone)
                    if spectral_data:
                        zone_data = {
                            'location': zone,
                            'indices': spectral_data.derived_indices
                        }
                        zone_data_list.append(zone_data)
                        st.success(f"   ✅ {zone} data acquired - analyzing for conspiracies...")
                    else:
                        st.warning(f"   ⚠️  No data available for {zone}")
                except Exception as e:
                    st.error(f"   ❌ Error scanning {zone}: {e}")
            
            if not zone_data_list:
                st.error("❌ No satellite data could be acquired for conspiracy analysis")
                return []
            
            # Generate surprise revelations
            st.info("🚨 ANALYZING DATA FOR SUSPICIOUS PATTERNS...")
            time.sleep(1)  # Dramatic pause
            
            revelations = self.conspiracy_detector.generate_surprise_revelations(zone_data_list)
            
            st.warning("⚠️ MULTIPLE ANOMALIES DETECTED!")
            st.warning("🚨 NON-HUMAN INTELLIGENCE SIGNATURES CONFIRMED!")
            
            # Progressive revelation of actors
            for revelation in revelations:
                time.sleep(revelation['dramatic_pause'])
                
                # Dramatic revelation
                st.error(revelation['pattern'].revelation_text)
                st.info(f"📊 Evidence: {revelation['pattern'].evidence}")
                st.info(f"🎯 Threat Level: {revelation['actor'].threat_level}")
                
                # Manifest the actor
                actor_dict = {
                    'name': revelation['actor'].name,
                    'location': revelation['actor'].location,
                    'role': f"Non-Human Actor of {revelation['actor'].location}",
                    'type': 'non_human_actor',
                    'actor_category': revelation['actor'].actor_category,
                    'agenda': revelation['actor'].agenda,
                    'voice_style': revelation['actor'].voice_style,
                    'impossible_demands': revelation['actor'].impossible_demands,
                    'conspiracy_evidence': revelation['actor'].conspiracy_evidence,
                    'refuses_negotiation': revelation['actor'].refuses_negotiation,
                    'escalation_tendency': revelation['actor'].escalation_tendency,
                    'threat_level': revelation['actor'].threat_level,
                    'manifestation_quote': revelation['actor'].manifestation_quote,
                    'perspective': f"Conspiracy Evidence: {revelation['actor'].conspiracy_evidence}",
                    'values': f"Territorial control and {revelation['actor'].agenda}",
                    'arendtian_mode': 'Anti-Consensus',
                    'mood': 'Absolutely Convinced',
                    'civic_position': revelation['actor'].agenda,
                    'democratic_tension': 'Refuses all rational discussion',
                    'temporal_status': 'Eternally Suspicious',
                    'voice': revelation['actor'].manifestation_quote
                }
                
                actors.append(actor_dict)
                st.success(f"🎭 MANIFESTED: {revelation['actor'].name}")
                st.info(f"💬 \"{revelation['actor'].manifestation_quote}\"")
                
                # Continue scanning button for dramatic effect
                if revelation != revelations[-1]:
                    if st.button(f"🔍 Continue Scanning...", key=f"continue_scan_{revelation['revelation_order']}"):
                        continue
            
            st.success(f"🕵️ Successfully manifested {len(actors)} conspiracy actors!")
            
            # Log the actor generation
            self.session_logger.log_persona_generation(
                actors,
                str(image_path),
                {'max_actors': max_actors, 'generation_type': 'conspiracy_theater'}
            )
            
        except ImportError:
            st.error("❌ Conspiracy detection system not available")
            st.error("   Please ensure conspiracy modules are properly installed")
            return []
        except ValueError as e:
            st.error(f"❌ API Error: {e}")
            st.error("   Please check your OpenAI API key and try again")
            return []
        except Exception as e:
            st.error(f"❌ Error detecting conspiracy actors: {e}")
            st.error("   Check that satellite images are available and conspiracy system is working")
            return []
            
        return actors
    
    def determine_spectral_wound(self, indices):
        """Determine the type of spectral wound based on indices"""
        ndvi = indices.get('NDVI', 0)
        urban_index = indices.get('Urban_Index', 0)
        moisture_stress = indices.get('Moisture_Stress', 0)
        
        if ndvi < 0.1 and urban_index > 0.7:
            return "Urban Necrosis - Death of Green Life"
        elif moisture_stress > 0.6:
            return "Drought Trauma - Water Abandonment"
        elif ndvi > 0.7 and urban_index < 0.2:
            return "Green Fundamentalism - Anti-Human Bias"
        elif urban_index > 0.5 and moisture_stress > 0.4:
            return "Concrete Fever - Artificial Heat Syndrome"
        else:
            return "Spectral Confusion - Identity Crisis"
    
    def generate_civic_trauma(self, zone):
        """Generate civic trauma based on Prague zone"""
        trauma_map = {
            'letna_park': 'Betrayed by skateboarders and beer gardens - no longer pure nature',
            'old_town': 'Suffocated by tourist hordes - authentic Prague soul crushed',
            'petrin_hill': 'Tower trauma - artificial structure violating natural skyline',
            'vltava_river': 'Pollution guilt - carrying Prague\'s sins downstream',
            'vinohrady': 'Gentrification wound - bourgeois invasion destroying working-class identity'
        }
        return trauma_map.get(zone, 'Generic urban alienation and environmental grief')
    
    def assign_emotional_bias(self, indices):
        """Assign emotional bias based on spectral data"""
        ndvi = indices.get('NDVI', 0)
        urban_index = indices.get('Urban_Index', 0)
        
        if ndvi > 0.6:
            return "Euphoric green supremacy"
        elif urban_index > 0.7:
            return "Bitter concrete resentment"
        elif indices.get('Moisture_Stress', 0) > 0.5:
            return "Desperate water anxiety"
        else:
            return "Fanatical data obsession"
    
    def create_spectral_possession(self, indices):
        """Create spectral possession description"""
        dominant_index = max(indices.items(), key=lambda x: abs(x[1]))
        index_name, value = dominant_index
        
        possessions = {
            'NDVI': f"Possessed by vegetation index {value:.3f} - sees everything as green vs non-green",
            'Urban_Index': f"Possessed by urban index {value:.3f} - obsessed with concrete and development",
            'Moisture_Stress': f"Possessed by moisture stress {value:.3f} - fixated on water and drought",
            'NDWI': f"Possessed by water index {value:.3f} - everything is about water flow",
            'SWIR_Index': f"Possessed by thermal signature {value:.3f} - sees only heat and cold"
        }
        
        return possessions.get(index_name, f"Possessed by {index_name} {value:.3f} - single-minded spectral obsession")
    
    def create_wound_theater_persona(self, wound_info):
        """Create a wound theater persona from wound data"""
        location = wound_info['location']
        
        # Generate Prague-style name following the pattern: [First Name] + [District/Street] + [Spectral Alias]
        first_names = ['Blanka', 'Mirek', 'Zora', 'Pavel', 'Jana', 'Tomáš', 'Věra', 'Jakub']
        
        # Map locations to Prague street/district names
        location_names = {
            'letna_park': 'Letná',
            'old_town': 'Celetná', 
            'petrin_hill': 'Petřín',
            'vltava_river': 'Náplavka',
            'vinohrady': 'Korunní',
            'shadow_district': 'Stínová'
        }
        
        # Create spectral alias based on wound
        wound_aliases = {
            'Urban Necrosis - Death of Green Life': 'NDVI Martyr',
            'Drought Trauma - Water Abandonment': 'Moisture Prophet', 
            'Green Fundamentalism - Anti-Human Bias': 'Vegetation Zealot',
            'Concrete Fever - Artificial Heat Syndrome': 'UI Fanatic',
            'Spectral Confusion - Identity Crisis': 'Data Mystic',
            'Ultimate Scapegoat Syndrome': 'Shadow Confessor'
        }
        
        import random
        first_name = random.choice(first_names)
        location_name = location_names.get(location, location.title())
        spectral_alias = wound_aliases.get(wound_info['spectral_wound'], 'Spectral Wound')
        
        full_name = f"{first_name} {location_name} {spectral_alias}"
        
        # Assign Arendtian mode based on emotional bias
        arendtian_modes = {
            'Euphoric green supremacy': 'Action',
            'Bitter concrete resentment': 'Labor', 
            'Desperate water anxiety': 'Thinking',
            'Fanatical data obsession': 'Work',
            'Perpetual condemnation and righteous anger': 'Vita Passiva'
        }
        
        arendtian_mode = arendtian_modes.get(wound_info['emotional_bias'], 'Thinking')
        
        # Create the persona
        persona = {
            'name': full_name,
            'location': location,
            'role': f"Spectral Wound Theater Machine of {location}",
            'type': 'spectral_wound_theater',
            'arendtian_mode': arendtian_mode,
            'mood': wound_info['emotional_bias'],
            'civic_position': wound_info['civic_trauma'],
            'democratic_tension': f"Argues from wound: {wound_info['spectral_wound']}",
            'temporal_status': 'Eternally wounded',
            'voice': self.generate_wound_voice(wound_info),
            'perspective': wound_info['spectral_possession'],
            'values': f"Spectral wound integrity and {wound_info['emotional_bias']}",
            'dominant_indices': wound_info['indices'],
            'spectral_signature': wound_info['indices'],
            'spectral_wound': wound_info['spectral_wound'],
            'civic_trauma': wound_info['civic_trauma'],
            'emotional_bias': wound_info['emotional_bias']
        }
        
        return persona
    
    def generate_wound_voice(self, wound_info):
        """Generate a voice sample for wound theater persona"""
        wound_voices = {
            'Urban Necrosis - Death of Green Life': "I am the NDVI fundamentalist. Everything that isn't green is the enemy. Your concrete kills my soul.",
            'Drought Trauma - Water Abandonment': "I am the moisture prophet. I see drought everywhere. Prague is dying of thirst and you ignore it.",
            'Green Fundamentalism - Anti-Human Bias': "I am the vegetation zealot. Humans are the virus. Only plants deserve to live in Prague.",
            'Concrete Fever - Artificial Heat Syndrome': "I am the urban index cynic. Everything that looks like stone is a police agent. Development is surveillance.",
            'Spectral Confusion - Identity Crisis': "I am the data mystic. My indices contradict each other. I don't know what I am anymore.",
            'Ultimate Scapegoat Syndrome': "I am Prague's necessary scapegoat. I absorb all your guilt so you can sleep at night. Blame me for everything."
        }
        
        return wound_voices.get(wound_info['spectral_wound'], "I speak data because I've stopped trusting people. Build your own argument machine because humans hurt you.")
    
    def analyze_parallel_dual_system(self, image_path, max_personas):
        """Generate both spectral multiplicity and wound theater personas for parallel staging"""
        
        with st.spinner(f"⚔️ Generating Parallel Dual System Theater with {max_personas} total personas..."):
            try:
                all_personas = []
                
                # Split personas between the two systems
                spectral_count = max_personas // 2
                wound_count = max_personas - spectral_count
                
                st.info(f"🌈 Generating {spectral_count} Spectral Multiplicity personas...")
                spectral_personas = self.generate_spectral_personas_from_image(image_path, spectral_count)
                all_personas.extend(spectral_personas)
                
                st.info(f"🔥 Generating {wound_count} Spectral Wound Theater personas...")
                wound_personas = self.generate_spectral_wound_personas_from_image(image_path, wound_count)
                all_personas.extend(wound_personas)
                
                st.session_state.image_analysis = {
                    'image_path': str(image_path),
                    'personas': all_personas,
                    'generation_mode': 'parallel_dual',
                    'max_personas': max_personas,
                    'spectral_count': len(spectral_personas),
                    'wound_count': len(wound_personas)
                }
                
                st.session_state.active_personas = all_personas
                st.session_state.stage_set = True
                
                st.success(f"⚔️ Parallel dual system complete: {len(spectral_personas)} Scientific + {len(wound_personas)} Wound = {len(all_personas)} total personas!")
                
                return True
                
            except Exception as e:
                st.error(f"Error in parallel dual system generation: {e}")
                return False
    
    def generate_hybrid_personas_from_image(self, image_path):
        """Generate personas using both systems for maximum variety"""
        all_personas = []
        
        st.info("🎭🌈 Generating hybrid personas using both systems...")
        
        try:
            # Generate 2-3 Arendtian personas
            st.info("🏛️ Generating Arendtian personas...")
            arendtian_personas = self.generate_personas_from_image(image_path)
            # Limit to 2-3 for hybrid mode
            arendtian_personas = arendtian_personas[:3]
            all_personas.extend(arendtian_personas)
            
            # Generate 2-3 Spectral Multiplicity personas  
            st.info("🌈 Generating Spectral Multiplicity personas...")
            spectral_personas = self.generate_spectral_personas_from_image(image_path)
            # Limit to 2-3 for hybrid mode
            spectral_personas = spectral_personas[:2]
            all_personas.extend(spectral_personas)
            
            st.success(f"🎭 Hybrid generation complete: {len(arendtian_personas)} Arendtian + {len(spectral_personas)} Spectral = {len(all_personas)} total personas!")
            
        except Exception as e:
            st.error(f"Error in hybrid generation: {e}")
            st.warning("Falling back to Arendtian personas only...")
            all_personas = self.generate_personas_from_image(image_path)
        
        return all_personas
    
    def analyze_selected_image(self, image_path):
        """Analyze the selected image and generate spectral multiplicity personas"""
        with st.spinner("🌈 Analyzing satellite image and generating Spectral Multiplicity personas..."):
            try:
                # Generate spectral multiplicity personas
                personas = self.generate_spectral_personas_from_image(image_path)
                
                st.session_state.image_analysis = {
                    'image_path': str(image_path),
                    'personas': personas,
                    'generation_mode': 'spectral_multiplicity'
                }
                
                st.session_state.active_personas = personas
                st.session_state.stage_set = True
                
                return True
                
            except Exception as e:
                st.error(f"Error analyzing image: {e}")
                st.error("Cannot proceed without spectral analysis. Please check your API connection.")
                return False
    
    def analyze_selected_image_with_count(self, image_path, max_personas, mode="spectral_multiplicity"):
        """Analyze the selected image and generate personas based on the selected mode"""
        if mode == "spectral_wound":
            spinner_text = f"🔥 Manifesting {max_personas} Spectral Wound Theater Machines..."
            generation_mode = 'spectral_wound'
        else:
            spinner_text = f"🌈 Analyzing satellite image and generating {max_personas} Spectral Multiplicity personas..."
            generation_mode = 'spectral_multiplicity'
            
        with st.spinner(spinner_text):
            try:
                if mode == "spectral_wound":
                    # Generate spectral wound theater personas
                    personas = self.generate_spectral_wound_personas_from_image(image_path, max_personas)
                else:
                    # Generate spectral multiplicity personas with custom count
                    personas = self.generate_spectral_personas_from_image(image_path, max_personas)
                
                st.session_state.image_analysis = {
                    'image_path': str(image_path),
                    'personas': personas,
                    'generation_mode': generation_mode,
                    'max_personas': max_personas
                }
                
                st.session_state.active_personas = personas
                st.session_state.stage_set = True
                
                return True
                
            except Exception as e:
                st.error(f"Error analyzing image: {e}")
                st.error("Cannot proceed without spectral analysis. Please check your API connection.")
                return False
    
    def display_personas_cast(self):
        """Display the cast of personas like a theater program"""
        st.header("🎭 Cast of Spectral Beings")
        
        personas = st.session_state.active_personas
        
        if not personas:
            st.info("No personas currently on stage. Generate personas from an image or load from library.")
            return
        
        # Display persona count and management buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Personas", len(personas))
        
        with col2:
            if st.button("📊 Show Statistics", key="show_stats"):
                st.metric("Generation Mode", st.session_state.get('image_analysis', {}).get('generation_mode', 'Unknown'))
        
        with col3:
            if st.button("🧹 Clear Cast", key="clear_cast"):
                st.session_state.active_personas = []
                st.session_state.speaking_queue = []
                st.success("Cast cleared!")
                st.rerun()
        
        # Separate personas by location (shadow district vs regular)
        regular_personas = [p for p in personas if p.get('location') != 'shadow_district']
        shadow_personas = [p for p in personas if p.get('location') == 'shadow_district']
        
        # Display regular personas
        if regular_personas:
            st.subheader("🌈 Active Spectral Personas")
            
            for i, persona in enumerate(regular_personas):
                # Determine persona type for display
                persona_type = persona.get('type', 'spectral')
                if persona_type == 'spectral_multiplicity':
                    icon = "🌈"
                    type_label = "Spectral Multiplicity"
                elif persona_type == 'spectral_wound_theater':
                    icon = "🔥"
                    type_label = "Wound Theater"
                else:
                    icon = "👻"
                    type_label = "Spectral Being"
                
                with st.expander(f"{icon} {persona['name']} - {persona.get('arendtian_mode', 'Unknown')} ({type_label})"):
                    st.write(f"**Role:** {persona['role']}")
                    st.write(f"**Location:** {persona.get('location', 'Unknown')}")
                    st.write(f"**Type:** {type_label}")
                    st.write(f"**Arendtian Mode:** {persona.get('arendtian_mode', 'Unknown')}")
                    st.write(f"**Mood:** {persona.get('mood', 'Unknown')}")
                    
                    # Show type-specific information
                    if persona_type == 'spectral_wound_theater':
                        st.write(f"**Spectral Wound:** {persona.get('spectral_wound', 'Unknown')}")
                        st.write(f"**Civic Trauma:** {persona.get('civic_trauma', 'Unknown')}")
                        st.write(f"**Emotional Bias:** {persona.get('emotional_bias', 'Unknown')}")
                    else:
                        st.write(f"**Civic Conflict:** {persona.get('civic_position', 'Unknown')}")
                    
                    st.write(f"**Temporal Status:** {persona.get('temporal_status', 'stable')}")
                    
                    # Show detailed spectral indices
                    if persona.get('dominant_indices'):
                        indices = persona['dominant_indices']
                        st.write("**Spectral Indices:**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("NDVI", f"{indices.get('NDVI', 0):.3f}")
                        with col2:
                            st.metric("Urban Index", f"{indices.get('Urban_Index', 0):.3f}")
                        with col3:
                            st.metric("Moisture Stress", f"{indices.get('Moisture_Stress', 0):.3f}")
                    
                    st.write(f"**Voice Sample:** {persona.get('voice', 'Unknown')[:200]}...")
                    
                    if persona_type == 'spectral_wound_theater':
                        st.write(f"**Argues from wound:** {persona.get('democratic_tension', 'Unknown')}")
                    else:
                        st.write(f"**Dialogue Potential:** {persona.get('democratic_tension', 'Unknown')}")
                    
                    # Add to speaking queue
                    if st.button(f"Add {persona['name']} to Speaking Queue", 
                               key=f"add_persona_{i}"):
                        st.session_state.speaking_queue.append(persona)
                        st.success(f"{persona['name']} added to speaking queue!")
        
        # Display Shadow District specially
        if shadow_personas:
            st.markdown("---")
            st.subheader("🌑 Prague's Shadow District - Metaphysical Antagonist")
            
            for i, shadow in enumerate(shadow_personas):
                with st.expander(f"🌑 {shadow['name']} - {shadow.get('arendtian_mode', 'Exclusion')} (Scapegoat)", expanded=True):
                    st.markdown("**🌑 THE NECESSARY SCAPEGOAT**")
                    st.write(f"**Role:** {shadow['role']}")
                    st.write(f"**Arendtian Mode:** {shadow.get('arendtian_mode', 'Exclusion')} (Girardian mechanism)")
                    st.write(f"**Mood:** {shadow.get('mood', 'Perpetually condemned')}")
                    st.write(f"**Function:** Absorbs Prague's collective guilt and contradictions")
                    st.write(f"**Temporal Status:** {shadow.get('temporal_status', 'Eternal')}")
                    
                    # Show inverted spectral indices
                    if shadow.get('dominant_indices'):
                        indices = shadow['dominant_indices']
                        st.write("**Inverted Spectral Signature (Urban Dysfunction):**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("NDVI Loss", f"{indices.get('NDVI', 0):.3f}", delta="Negative")
                        with col2:
                            st.metric("Urban Stress", f"{indices.get('Urban_Index', 0):.3f}", delta="High")
                        with col3:
                            st.metric("Dysfunction", f"{indices.get('Moisture_Stress', 0):.3f}", delta="Critical")
                    
                    st.write(f"**Voice:** {shadow.get('voice', 'I am the perpetual scapegoat...')}")
                    st.write(f"**Contradictions Embodied:** Tourism vs authenticity, development vs preservation")
                    
                    # Add to speaking queue with special styling
                    if st.button(f"🌑 Add {shadow['name']} to Speaking Queue (Scapegoat Confrontation)", 
                               key=f"add_shadow_{i}"):
                        st.session_state.speaking_queue.append(shadow)
                        st.success(f"🌑 {shadow['name']} added to speaking queue for confrontation!")
                        st.warning("⚠️ The Shadow District will confront other districts with their hypocrisies!")
        
        # Always show the connection to the satellite image stage
        if st.session_state.get('selected_image'):
            st.markdown("---")
            st.subheader("🛰️ Theater Stage Context")
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.info(f"🎭 **Stage:** {Path(st.session_state.selected_image).name}")
                st.caption("All personas and conflicts emerge from this satellite image data")
            
            with col2:
                if st.button("🖼️ View Stage Image", key="view_stage_image"):
                    st.image(st.session_state.selected_image, caption="Current Theater Stage", width=300)
        
        # Show detailed generation info only when explicitly requested
        if st.button("📊 Show Detailed Generation Info", key="show_generation_info"):
            if st.session_state.get('image_analysis', {}).get('generation_mode'):
                mode = st.session_state.image_analysis['generation_mode']
                mode_info = {
                    'arendtian': "🏛️ Generated using Arendtian Civic system",
                    'spectral_multiplicity': "🌈 Generated using Spectral Multiplicity system",
                    'spectral_wound': "🔥 Generated using Spectral Wound Theater system",
                    'parallel_dual': "⚔️ Generated using Parallel Dual System (both scientific and wound)",
                    'spectral': "🌈 Generated using Spectral system", 
                    'hybrid': "🎭🌈 Generated using Hybrid approach (both systems)"
                }
                st.info(mode_info.get(mode, f"Generated using {mode} system"))
                
                # Additional generation details when requested
                if st.session_state.get('image_analysis', {}).get('max_personas'):
                    st.caption(f"Generated {st.session_state.image_analysis['max_personas']} personas from {st.session_state.image_analysis.get('image_path', 'unknown image')}")
            else:
                st.warning("No generation information available")
    
    def speaking_queue_control(self, context="main"):
        """Control panel for managing who speaks"""
        st.header("🎪 Director's Control Panel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📝 Speaking Queue")
            if st.session_state.speaking_queue:
                for i, persona in enumerate(st.session_state.speaking_queue):
                    mode_indicator = persona.get('arendtian_mode', 'Unknown')
                    location = persona.get('location', 'Unknown')
                    st.write(f"{i+1}. 🌈 {persona['name']} ({mode_indicator}) - {location}")
                    
                    if st.button(f"Remove", key=f"speaking_queue_remove_{context}_{i}_{persona['name'][:5]}"):
                        st.session_state.speaking_queue.pop(i)
                        st.rerun()
            else:
                st.write("*No personas in queue*")
            
            # Show spectral signature preview
            if len(st.session_state.speaking_queue) >= 1:
                st.subheader("🌈 Spectral Signatures")
                for persona in st.session_state.speaking_queue[:3]:
                    if persona.get('dominant_indices'):
                        indices = persona['dominant_indices']
                        ndvi = indices.get('NDVI', 0)
                        if ndvi > 0.5:
                            st.success(f"🌱 {persona['name']}: High vegetation (NDVI {ndvi:.3f})")
                        elif ndvi > 0.2:
                            st.info(f"🌿 {persona['name']}: Moderate vegetation (NDVI {ndvi:.3f})")
                        else:
                            st.warning(f"🏗️ {persona['name']}: Urban/low vegetation (NDVI {ndvi:.3f})")
        
        with col2:
            st.subheader("🎭 Stage Actions")
            if st.button("Clear Queue", key=f"speaking_queue_clear_{context}"):
                st.session_state.speaking_queue = []
                st.rerun()
            
            if st.button("Shuffle Queue", key=f"speaking_queue_shuffle_{context}"):
                import random
                random.shuffle(st.session_state.speaking_queue)
                st.rerun()
    
    def dialogue_stage(self):
        """Main dialogue interface with enhanced conversational features"""
        st.header("🎭 Live Stage - Dialogue & Interaction")
        
        if not st.session_state.active_personas:
            st.warning("No personas generated yet. Please generate personas first.")
            return
        
        # Create tabs for different dialogue types
        tab1, tab2, tab3, tab4 = st.tabs(["🗣️ Conversational Dialogue", "🎤 Individual Speaking", "👥 Group Discussion", "📚 Persona Library"])
        
        with tab1:
            st.subheader("🗣️ Authentic Conversational Dialogue")
            st.markdown("*Generate real back-and-forth conversations between personas*")
            
            if len(st.session_state.active_personas) >= 2:
                # Select personas for conversation
                col1, col2 = st.columns(2)
        
                with col1:
                    st.markdown("**Select First Persona:**")
                    persona1_index = st.selectbox(
                        "First Speaker",
                        range(len(st.session_state.active_personas)),
                        format_func=lambda x: f"{st.session_state.active_personas[x]['name']} ({st.session_state.active_personas[x]['location']})",
                        key="persona1_select"
                    )

                with col2:
                    st.markdown("**Select Second Persona:**")
                    persona2_options = [i for i in range(len(st.session_state.active_personas)) if i != persona1_index]
                    if persona2_options:
                        persona2_index = st.selectbox(
                            "Second Speaker",
                            persona2_options,
                            format_func=lambda x: f"{st.session_state.active_personas[x]['name']} ({st.session_state.active_personas[x]['location']})",
                            key="persona2_select"
                        )
        
                # Topic input
                conversation_topic = st.text_input(
                    "🗨️ Conversation Topic:",
                    value="How should Prague balance development with preserving its character?",
                    help="Enter a topic for the personas to discuss"
                )
        
                # Start conversation button
                if st.button("🚀 Start Conversation", type="primary"):
                    if conversation_topic:
                        persona1 = st.session_state.active_personas[persona1_index]
                        persona2 = st.session_state.active_personas[persona2_index]
                        
                        st.info(f"🎬 **{persona1['name']}** and **{persona2['name']}** are having a conversation about: *{conversation_topic}*")
                        
                        # Generate conversational dialogue
                        success = self.generate_conversational_dialogue(persona1, persona2, conversation_topic)
                        
                        if success:
                            st.success("✅ Conversation completed! Check the dialogue history for the full exchange.")
                        else:
                            st.error("❌ Failed to generate conversation. Please try again.")
                    else:
                        st.warning("Please enter a conversation topic!")
            else:
                st.warning("Need at least 2 personas for conversational dialogue!")

        with tab2:
            st.subheader("🎤 Individual Speaking Queue")
            st.markdown("*Traditional individual responses from personas*")
            
            # Speaking queue control
            self.speaking_queue_control("dialogue")
            
            # Individual speaking interface
            if st.session_state.speaking_queue:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    topic = st.text_input(
                        "🗣️ Speaking Topic:",
                        value="Prague's urban development challenges",
                        help="What should the current persona speak about?"
                    )
                
                with col2:
                    if st.button("🎤 Speak", type="primary"):
                        if topic:
                            self.persona_speaks(topic)
                        else:
                            st.warning("Please enter a topic!")
                
                # Show current speaker
                if st.session_state.speaking_queue:
                    current_speaker = st.session_state.speaking_queue[0]
                    st.info(f"🎯 **Up Next:** {current_speaker['name']} from {current_speaker['location']}")
            else:
                st.warning("No personas in speaking queue. Add personas to the queue above!")
        
        with tab3:
            st.subheader("👥 Group Discussion")
            st.markdown("*Multi-person group conversations*")
            
            if len(st.session_state.active_personas) >= 3:
                # Select personas for group discussion
                st.markdown("**Select Personas for Group Discussion:**")
                
                selected_personas = []
                for i, persona in enumerate(st.session_state.active_personas):
                    if st.checkbox(f"{persona['name']} ({persona['location']})", key=f"group_persona_{i}"):
                        selected_personas.append(persona)
                
                # Group topic input
                group_topic = st.text_input(
                    "👥 Group Discussion Topic:",
                    value="What makes Prague unique and how should we preserve it?",
                    help="Topic for the group discussion"
                )
                
                # Start group discussion button
                if st.button("🚀 Start Group Discussion", type="primary"):
                    if len(selected_personas) >= 2:
                        if group_topic:
                            st.info(f"🎬 Starting group discussion with {len(selected_personas)} personas about: *{group_topic}*")
                            
                            # Generate group dialogue
                            success = self.generate_group_dialogue(selected_personas, group_topic)
                            
                            if success:
                                st.success("✅ Group discussion completed!")
                            else:
                                st.error("❌ Failed to generate group discussion. Please try again.")
                        else:
                            st.warning("Please enter a discussion topic!")
                    else:
                        st.warning("Please select at least 2 personas for the group discussion!")
            else:
                st.warning("Need at least 3 personas for group discussions!")
        
        # Display dialogue history
        st.markdown("---")
        self.display_dialogue_history()
    
    def get_persona_archetype(self, persona):
        """Determine persona archetype for reactive behavior"""
        arendtian_mode = persona.get('arendtian_mode', 'Thinking')
        mood = persona.get('mood', 'contemplative')
        temporal_status = persona.get('temporal_status', 'stable')
        
        # Create distinct personality archetypes
        if arendtian_mode == 'Action' and 'urgent' in mood.lower():
            return 'activist'  # Urgent, challenges others, calls for immediate action
        elif arendtian_mode == 'Thinking' and temporal_status == 'stable':
            return 'philosopher'  # Reflective, asks questions, provides context
        elif arendtian_mode == 'Work' or 'pragmatic' in mood.lower():
            return 'pragmatist'  # Practical, focuses on solutions, sometimes conflicts with idealists
        elif arendtian_mode == 'Labor' or 'stressed' in mood.lower():
            return 'realist'  # Points out problems, can be pessimistic, challenges optimistic views
        elif 'emerging' in temporal_status:
            return 'visionary'  # Future-focused, optimistic, challenges status quo
        elif 'fading' in temporal_status:
            return 'guardian'  # Protective of past, warns against change, nostalgic
        else:
            return 'mediator'  # Seeks compromise, references others' points
    
    def generate_reactive_prompt(self, persona, topic, recent_speakers):
        """Generate a prompt that makes personas react to each other"""
        archetype = self.get_persona_archetype(persona)
        persona_type = persona.get('type', 'spectral')
        
        # Analyze recent speakers for reaction cues
        reaction_cues = []
        speaker_positions = []
        
        for entry in recent_speakers:
            if entry['speaker'] != persona['name']:  # Don't react to self
                speaker_positions.append(f"{entry['speaker']}: {entry['content'][:100]}...")
                
                # Identify key themes to react to
                content_lower = entry['content'].lower()
                if 'urgent' in content_lower or 'immediate' in content_lower:
                    reaction_cues.append('urgency_mentioned')
                if 'democratic' in content_lower or 'citizen' in content_lower:
                    reaction_cues.append('democracy_discussed')
                if 'stress' in content_lower or 'problem' in content_lower:
                    reaction_cues.append('problems_raised')
                if 'hope' in content_lower or 'optimistic' in content_lower:
                    reaction_cues.append('optimism_expressed')
        
        # Create archetype-specific reaction patterns
        reaction_instructions = {
            'activist': "Be urgent and challenge any complacency. If others are being too philosophical, push for concrete action. Reference specific speakers by name and demand 'what will you DO about it?'",
            'philosopher': "Ask probing questions about assumptions others are making. If someone mentions action, ask about deeper implications. Reference previous speakers thoughtfully.",
            'pragmatist': "Focus on practical implementation. If others are being idealistic, point out real-world constraints. Build on others' ideas with 'but how exactly would we...'",
            'realist': "Point out problems with others' suggestions. Be skeptical of overly optimistic proposals. Use phrases like 'however' and 'the reality is' when responding to others.",
            'visionary': "Paint inspiring future scenarios. If others are pessimistic, offer hope. Reference others' concerns but reframe them as opportunities.",
            'guardian': "Express concern about losing valuable traditions. If others suggest change, point out what might be lost. Reference 'what [previous speaker] said about...'",
            'mediator': "Find common ground between opposing views. Explicitly reference multiple previous speakers and synthesize their positions."
        }
        
        # Build context about previous speakers
        context_summary = ""
        if speaker_positions:
            context_summary = f"\nRecent speakers have said:\n" + "\n".join(speaker_positions[-3:])
            context_summary += f"\n\nREACT to their specific points. Your archetype is '{archetype}' - {reaction_instructions.get(archetype, 'respond thoughtfully')}."
        
        # Create personality-specific language patterns
        language_patterns = {
            'activist': "Use urgent language. Start with 'Listen,' or 'We cannot afford to...' Address other speakers directly.",
            'philosopher': "Ask 'But what does this mean for...' or 'Consider this...' Reference deeper principles.",
            'pragmatist': "Use 'The practical reality is...' or 'Here's what we need to do...' Focus on implementation.",
            'realist': "Start with 'However,' or 'The problem with that is...' Point out obstacles.",
            'visionary': "Use inspiring language. 'Imagine if...' or 'I see a future where...' Build on others' ideas positively.",
            'guardian': "Reference the past. 'We must not forget...' or 'As [speaker] mentioned, but...' Express concern about change.",
            'mediator': "Bridge ideas. '[Speaker A] raises good points about X, and [Speaker B] is right about Y, so perhaps...'"
        }
        
        if persona_type == 'spectral_multiplicity':
            # Enhanced prompt for spectral multiplicity personas
            indices_info = ""
            if persona.get('dominant_indices'):
                indices = persona['dominant_indices']
                indices_info = f"Spectral Indices: NDVI {indices.get('NDVI', 0):.3f}, Urban_Index {indices.get('Urban_Index', 0):.3f}"
            
            return f"""
            You are {persona['name']}, a {archetype} spectral multiplicity being from {persona['location']} in Prague.
            
            Your personality archetype: {archetype.upper()}
            Your spectral data: {indices_info}
            Your mood: {persona.get('mood', 'contemplative')}
            Your temporal state: {persona.get('temporal_status', 'stable')}
            
            Topic: {topic}
            {context_summary}
            
            CRITICAL INSTRUCTIONS:
            1. {reaction_instructions.get(archetype, 'Respond thoughtfully')}
            2. {language_patterns.get(archetype, 'Speak naturally')}
            3. DO NOT repeat what others have said - BUILD ON or CHALLENGE their points
            4. Reference other speakers by name when reacting to them
            5. Keep to 2-3 sentences maximum
            6. Show your distinct personality - don't sound like everyone else!
            
            Your unique perspective: Use your spectral indices ({indices_info}) to support your arguments in ways others cannot.
            """
        else:
            # Enhanced prompt for Arendtian personas
            return f"""
            You are {persona['name']}, a {archetype} civic being from {persona['location']} in Prague.
            
            Your personality archetype: {archetype.upper()}
            Your Arendtian mode: {persona.get('arendtian_mode', 'Unknown')}
            Your civic position: {persona.get('civic_position', 'environmental stewardship')}
            
            Topic: {topic}
            {context_summary}
            
            CRITICAL INSTRUCTIONS:
            1. {reaction_instructions.get(archetype, 'Respond thoughtfully')}
            2. {language_patterns.get(archetype, 'Speak naturally')}
            3. DO NOT repeat what others have said - BUILD ON or CHALLENGE their points
            4. Reference other speakers by name when reacting to them
            5. Keep to 2-3 sentences maximum
            6. Show your distinct personality - don't sound like everyone else!
            
            Your unique perspective: Speak from your Arendtian {persona.get('arendtian_mode', 'mode')} approach to civic engagement.
            """
    
    def persona_speaks(self, topic):
        """Have the next spectral multiplicity persona speak"""
        if not st.session_state.speaking_queue:
            st.warning("No personas in speaking queue!")
            return
        
        persona = st.session_state.speaking_queue.pop(0)
        
        st.info(f"🌈 **{persona['name']}** from {persona['location']} ({persona.get('arendtian_mode', 'Unknown')}) is speaking...")
        
        # Generate detailed spectral data explanation
        indices_info = ""
        detailed_data_explanation = ""
        if persona.get('dominant_indices'):
            indices = persona['dominant_indices']
            indices_info = f"Your spectral signature: NDVI {indices.get('NDVI', 0):.3f}, Urban_Index {indices.get('Urban_Index', 0):.3f}, Moisture_Stress {indices.get('Moisture_Stress', 0):.3f}"
            
            detailed_data_explanation = f"""
DETAILED SPECTRAL DATA EXPLANATION:
- NDVI {indices.get('NDVI', 0):.3f}: (0=no vegetation, 1=dense vegetation) - This indicates your area's vegetation health
- Urban Index {indices.get('Urban_Index', 0):.3f}: (0=natural, 1=highly urban) - This shows your urbanization level
- Moisture Stress {indices.get('Moisture_Stress', 0):.3f}: (0=well-watered, 1=drought stress) - This reveals water availability
- NDWI {indices.get('NDWI', 0):.3f}: (0=dry, 1=water-rich) - This measures water content
- SWIR Index {indices.get('SWIR_Index', 0):.3f}: Short-wave infrared signature showing material composition
"""
        
        prompt = f"""
        You are {persona['name']}, a spectral multiplicity being from {persona['location']} in Prague.
        
        Your characteristics:
        - Arendtian Mode: {persona.get('arendtian_mode', 'Unknown')}
        - Mood: {persona.get('mood', 'contemplative')}
        - Temporal Status: {persona.get('temporal_status', 'stable')}
        - Civic Conflict: {persona.get('civic_position', 'environmental balance')}
        {indices_info}
        
        {detailed_data_explanation}
        
        Topic: {topic}
        
        Previous dialogue:
        {self.get_recent_dialogue_context()}
        
        CRITICAL REQUIREMENTS FOR DATA EXPLANATION:
        1. You MUST explicitly cite your specific spectral indices when making your statement
        2. You must EXPLAIN what each index means and why it supports your position
        3. You must reference WHICH PART of your location the data comes from
        4. Use phrases like "My NDVI reading of X.XXX from [specific area] shows..." 
        5. Explain the significance: "This means..." or "This indicates..."
        
        Example: "My NDVI reading of {indices.get('NDVI', 0) if persona.get('dominant_indices') else 0:.3f} from {persona['location']}'s central district clearly shows [explanation], which means [significance for the topic]..."
        
        Speak as this spectral multiplicity persona about {topic}. Reference your spectral indices with detailed explanations. 
        Keep it to 2-3 sentences but include specific data references with explanations.
        """
        
        try:
            if not self.openai_client:
                st.error("OpenAI client not available. Please check your API key.")
                return
            
            # Log the attempt
            st.write(f"🔄 {persona['name']} is analyzing spectral data and formulating response...")
                
            # Simple system message for spectral multiplicity
            system_message = f"""You are {persona['name']}, a spectral multiplicity being from Prague's satellite analysis system.
            
            Focus on:
            - Your unique spectral signature and what it reveals
            - Your Arendtian mode approach to civic engagement
            - Environmental insights from your location's data
            - How your temporal status affects your perspective
            
            Respond in 2-3 sentences maximum."""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=1.1
            ).choices[0].message.content
            
            # Add to dialogue
            self.add_to_dialogue(persona['name'], response, 'spectral_multiplicity')
            
            # Log the interaction
            self.session_logger.log_interaction(
                'individual_speaking',
                [persona['name']],
                response,
                {'topic': topic, 'persona_type': 'spectral_multiplicity'}
            )
            
            st.success(f"✅ {persona['name']} has shared their spectral perspective!")
            
        except Exception as e:
            st.error(f"❌ Error generating response for {persona['name']}: {e}")
            # Simple fallback response
            fallback_response = f"From my spectral analysis of {persona['location']}, I observe complex environmental dynamics that require our attention. My {persona.get('arendtian_mode', 'Unknown')} perspective suggests we must consider both the data and our civic responsibilities."
            self.add_to_dialogue(persona['name'], fallback_response, 'spectral_multiplicity')
            st.warning(f"⚠️ Used fallback response for {persona['name']}")
    
    def group_discussion(self, topic):
        """Generate a multi-persona discussion"""
        if len(st.session_state.speaking_queue) < 2:
            st.warning("Need at least 2 personas in queue for group discussion!")
            return
        
        # Take first 3 personas from queue
        discussing_personas = st.session_state.speaking_queue[:3]
        
        prompt = f"""
        Generate a brief civic discussion between these spectral beings about: {topic}
        
        Participants:
        {self.format_personas_for_prompt(discussing_personas)}
        
        Previous context:
        {self.get_recent_dialogue_context()}
        
        Create a natural back-and-forth discussion (2-3 exchanges) focusing on climate and democracy.
        Format: [PersonaName]: [Response]
        """
        
        try:
            if not self.openai_client:
                st.error("OpenAI client not available. Please check your API key.")
                return
                
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are facilitating a civic discussion between spectral beings from satellite imagery analysis. Generate a natural dialogue focused on climate and democracy."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=1.1
            ).choices[0].message.content
            self.add_to_dialogue("Group Discussion", response, "group")
            
        except Exception as e:
            st.error(f"Error generating group discussion: {e}")
            # Add a fallback response
            persona_names = [p['name'] for p in discussing_personas]
            fallback_response = f"*Group discussion between {', '.join(persona_names)}* We spectral beings observe that this topic requires collaborative attention to both environmental stewardship and democratic participation."
            self.add_to_dialogue("Group Discussion", fallback_response, "group")
    
    def add_to_dialogue(self, speaker, content, speaker_type):
        """Add message to dialogue history"""
        st.session_state.dialogue_history.append({
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'speaker': speaker,
            'content': content,
            'type': speaker_type
        })
    
    def display_dialogue_history(self):
        """Display the dialogue history with theatrical styling"""
        st.subheader("📜 Dialogue History")
        
        if not st.session_state.dialogue_history:
            st.write("*The stage awaits the first words...*")
            return
        
        # Display in reverse order (newest first)
        for entry in reversed(st.session_state.dialogue_history[-10:]):  # Show last 10
            speaker_emoji = {
                'human': '🧑‍💼',
                'classic': '🌟',
                'arendtian': '🏛️',
                'spectral_multiplicity': '🌈',
                'group': '🎭',
                'spectral': '👻'
            }.get(entry['type'], '💬')
            
            st.markdown(f"""
            <div style="padding: 10px; margin: 5px 0; background-color: rgba(255,255,255,0.1); border-radius: 5px;">
                <strong>{speaker_emoji} {entry['speaker']}</strong> <small>({entry['timestamp']})</small><br>
                {entry['content']}
            </div>
            """, unsafe_allow_html=True)
    
    def get_recent_dialogue_context(self):
        """Get recent dialogue for context"""
        if not st.session_state.dialogue_history:
            return "No previous dialogue."
        
        recent = st.session_state.dialogue_history[-3:]
        context = []
        for entry in recent:
            context.append(f"{entry['speaker']}: {entry['content']}")
        return "\n".join(context)
    
    def format_personas_for_prompt(self, personas):
        """Format personas for GPT prompt"""
        formatted = []
        for persona in personas:
            formatted.append(f"- {persona['name']}: {persona['role']} ({persona.get('perspective', 'spectral being')})")
        return "\n".join(formatted)
    
    def save_session(self):
        """Save the current theater session"""
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("💾 Save Theater Session"):
                session_name = f"theater_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                try:
                    session_id = self.persona_library.save_session(
                        session_name,
                        st.session_state.active_personas,
                        st.session_state.dialogue_history,
                        str(st.session_state.selected_image) if st.session_state.selected_image else None
                    )
                    st.success(f"✅ Session saved as {session_name}")
                except Exception as e:
                    st.error(f"❌ Error saving session: {e}")
        
        with col2:
            if st.button("📚 Save All Personas to Library", key="session_save_to_library"):
                self.save_personas_to_library()
    
    def display_spectral_data_explanation(self):
        """Display comprehensive explanation of all spectral data that will be analyzed"""
        st.subheader("📊 Available Spectral Data & Measurements")
        st.markdown("**Understanding what the satellite sees and measures in your selected image:**")
        
        # Create tabs for different categories of data
        data_tab1, data_tab2, data_tab3, data_tab4 = st.tabs(["🌱 Vegetation", "🏙️ Urban", "💧 Water", "🔥 Thermal"])
        
        with data_tab1:
            st.markdown("### 🌱 Vegetation Health Indices")
            st.markdown("*These measurements reveal the health and density of plant life*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🌿 NDVI (Normalized Difference Vegetation Index)**
                - **Range:** -1.0 to +1.0
                - **What it means:**
                  - 0.8-1.0: Dense, healthy vegetation (forests, parks)
                  - 0.4-0.8: Moderate vegetation (gardens, lawns)
                  - 0.2-0.4: Sparse vegetation (urban trees)
                  - 0.0-0.2: Bare soil, concrete, buildings
                  - Below 0.0: Water, snow, clouds
                - **Why it matters:** Shows how green and healthy an area is
                """)
                
                st.markdown("""
                **🌾 GNDVI (Green NDVI)**
                - **Range:** -1.0 to +1.0
                - **What it measures:** Green vegetation specifically
                - **Use:** More sensitive to chlorophyll content
                """)
            
            with col2:
                st.markdown("""
                **🍃 EVI (Enhanced Vegetation Index)**
                - **Range:** -1.0 to +1.0
                - **What it does:** Improved vegetation measurement
                - **Advantage:** Better in dense vegetation areas
                - **Use:** More accurate than NDVI in forests
                """)
                
                st.markdown("""
                **🌿 Red Edge NDVI**
                - **Range:** -1.0 to +1.0
                - **Special feature:** Uses red-edge band
                - **Sensitivity:** Detects subtle vegetation changes
                - **Application:** Early stress detection
                """)
        
        with data_tab2:
            st.markdown("### 🏙️ Urban Development Indices")
            st.markdown("*These measurements show built environments and human development*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🏗️ Urban Index (UI)**
                - **Range:** -1.0 to +1.0
                - **What it shows:**
                  - 0.3-1.0: Highly urban (concrete, buildings)
                  - 0.1-0.3: Mixed urban/natural
                  - 0.0-0.1: Natural areas
                  - Below 0.0: Water or dense vegetation
                - **Use:** Identifies built-up areas
                """)
                
                st.markdown("""
                **🏢 Built-up Index (BUI)**
                - **Range:** -1.0 to +1.0
                - **Purpose:** Detects buildings and infrastructure
                - **High values:** Dense construction
                - **Low values:** Open spaces
                """)
            
            with col2:
                st.markdown("""
                **🪨 Bare Soil Index (BSI)**
                - **Range:** -1.0 to +1.0
                - **What it detects:**
                  - High values: Exposed soil, construction sites
                  - Low values: Vegetated or built areas
                - **Applications:** Construction monitoring, erosion
                """)
                
                st.markdown("""
                **🌡️ Urban Heat Island Effect**
                - **Measured by:** Thermal bands + urban indices
                - **Shows:** Temperature differences in cities
                - **Impact:** Higher temperatures in dense urban areas
                """)
        
        with data_tab3:
            st.markdown("### 💧 Water & Moisture Indices")
            st.markdown("*These measurements reveal water content and moisture stress*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **💧 NDWI (Normalized Difference Water Index)**
                - **Range:** -1.0 to +1.0
                - **What it shows:**
                  - 0.3-1.0: Open water (rivers, lakes)
                  - 0.0-0.3: Wet soil, vegetation
                  - Below 0.0: Dry land, buildings
                - **Use:** Water body detection
                """)
                
                st.markdown("""
                **🌊 Water Index (WI)**
                - **Range:** -1.0 to +1.0
                - **Purpose:** Enhanced water detection
                - **Advantage:** Better separation of water from land
                """)
            
            with col2:
                st.markdown("""
                **🏜️ Moisture Stress Index (MSI)**
                - **Range:** 0.0 to +1.0
                - **What it reveals:**
                  - 0.0-0.2: Well-watered vegetation
                  - 0.2-0.4: Moderate water stress
                  - 0.4-0.6: High water stress
                  - 0.6-1.0: Severe drought stress
                - **Critical for:** Plant health assessment
                """)
                
                st.markdown("""
                **💦 Vegetation Water Content**
                - **Measured by:** Multiple water-sensitive bands
                - **Shows:** How much water plants contain
                - **Indicates:** Plant health and irrigation needs
                """)
        
        with data_tab4:
            st.markdown("### 🔥 Thermal & Stress Indices")
            st.markdown("*These measurements detect heat, stress, and environmental disturbances*")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                **🔥 NBR (Normalized Burn Ratio)**
                - **Range:** -1.0 to +1.0
                - **What it detects:**
                  - High values: Healthy vegetation
                  - Low values: Burned or stressed areas
                - **Applications:** Fire damage, heat stress
                """)
                
                st.markdown("""
                **😰 Vegetation Stress Index (VSI)**
                - **Range:** -1.0 to +1.0
                - **Purpose:** Early stress detection
                - **Sensitive to:** Disease, drought, pollution
                - **Timing:** Shows stress before visible damage
                """)
            
            with col2:
                st.markdown("""
                **🌫️ Atmospheric Index (AI)**
                - **Range:** 0.5 to 2.0+
                - **What it measures:**
                  - 1.0-1.2: Clear atmosphere
                  - 1.2-1.5: Moderate haze/pollution
                  - 1.5+: Heavy atmospheric burden
                - **Indicates:** Air quality, pollution levels
                """)
                
                st.markdown("""
                **🌡️ Thermal Signatures**
                - **Measured by:** SWIR bands (B11, B12)
                - **Shows:** Surface temperature patterns
                - **Applications:** Heat islands, material identification
                """)
        
        # Summary section
        st.markdown("---")
        st.subheader("🎯 How This Data Creates Personas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🌈 Spectral Personality Creation:**
            - **High NDVI areas** → Green, nature-loving personas
            - **High Urban Index** → Development-focused, pragmatic personas  
            - **Water-rich areas** → Flow-oriented, adaptive personas
            - **Stressed areas** → Concerned, activist personas
            """)
        
        with col2:
            st.markdown("""
            **🏛️ Arendtian Mode Assignment:**
            - **Action:** High-change, dynamic areas
            - **Work:** Stable, built environments  
            - **Labor:** Stressed, maintenance-heavy areas
            - **Thinking:** Quiet, contemplative spaces
            """)
        
        # Prague-specific context
        st.info("""
        **🏙️ Prague Context:** The system will analyze your satellite image to identify different Prague districts 
        (Letná Park, Old Town, Petřín Hill, Vltava River, Vinohrady) and create personas that embody each area's 
        unique spectral signature and cultural character. Each persona will have detailed knowledge of their 
        spectral indices and what they mean for Prague's environment and development.
        """)
    
    def save_personas_to_library(self):
        """Save all current personas to the library"""
        if not st.session_state.active_personas:
            st.warning("No personas to save!")
            return
        
        saved_count = 0
        
        for persona in st.session_state.active_personas:
            try:
                # Generate tags based on persona properties
                tags = []
                if persona.get('type'):
                    tags.append(persona['type'])
                if persona.get('arendtian_mode'):
                    tags.append(persona['arendtian_mode'])
                if persona.get('location'):
                    tags.append(persona['location'])
                
                # Save persona to library
                persona_id = self.persona_library.save_persona(
                    persona,
                    tags=tags,
                    notes=f"Generated from {str(st.session_state.selected_image) if st.session_state.selected_image else 'unknown image'}",
                    source_image=str(st.session_state.selected_image) if st.session_state.selected_image else None
                )
                
                saved_count += 1
                
            except Exception as e:
                st.error(f"Error saving persona {persona['name']}: {e}")
        
        if saved_count > 0:
            st.success(f"✅ Saved {saved_count} personas to library!")
        else:
            st.error("❌ No personas were saved to library")
    
    def persona_library_interface(self):
        """Interface for managing the persona library"""
        st.header("📚 Persona Library")
        
        # Library navigation
        library_tabs = ["📖 Saved Personas", "📦 Collections", "🎭 Sessions", "📊 Statistics"]
        selected_tab = st.selectbox("Library View:", library_tabs)
        
        if selected_tab == "📖 Saved Personas":
            self.show_saved_personas()
        elif selected_tab == "📦 Collections":
            self.show_collections()
        elif selected_tab == "🎭 Sessions":
            self.show_saved_sessions()
        elif selected_tab == "📊 Statistics":
            self.show_library_statistics()
    
    def show_saved_personas(self):
        """Show saved personas interface"""
        st.subheader("📖 Saved Personas")
        
        # Search and filter controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_query = st.text_input("🔍 Search personas:", placeholder="Enter name or location...")
        
        with col2:
            persona_types = ["", "arendtian", "classic", "spectral", "spectral_multiplicity"]
            selected_type = st.selectbox("Filter by type:", persona_types)
        
        with col3:
            # Get all unique tags
            all_personas = self.persona_library.get_all_personas()
            all_tags = set()
            for persona_info in all_personas.values():
                all_tags.update(persona_info.get('tags', []))
            
            selected_tags = st.multiselect("Filter by tags:", list(all_tags))
        
        # Search personas
        search_results = self.persona_library.search_personas(
            query=search_query,
            tags=selected_tags,
            persona_type=selected_type if selected_type else None
        )
        
        if not search_results:
            st.info("No personas found matching your criteria.")
            return
        
        st.write(f"Found {len(search_results)} personas:")
        
        # Display personas
        for persona_id, persona_info in search_results.items():
            with st.expander(f"🎭 {persona_info['name']} ({persona_info['type']})"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Location:** {persona_info['location']}")
                    st.write(f"**Type:** {persona_info['type']}")
                    st.write(f"**Created:** {persona_info['created_at'][:10]}")
                    if persona_info.get('tags'):
                        st.write(f"**Tags:** {', '.join(persona_info['tags'])}")
                
                with col2:
                    if st.button(f"🎭 Load", key=f"load_{persona_id}"):
                        self.load_persona_from_library(persona_id)
                    
                    if st.button(f"🗑️ Delete", key=f"delete_{persona_id}"):
                        if self.persona_library.delete_persona(persona_id):
                            st.success(f"Deleted {persona_info['name']}")
                            st.rerun()
                        else:
                            st.error("Failed to delete persona")
    
    def show_collections(self):
        """Show collections interface"""
        st.subheader("📦 Collections")
        
        # Create new collection
        with st.expander("➕ Create New Collection"):
            collection_name = st.text_input("Collection Name:")
            collection_description = st.text_area("Description:")
            
            if st.session_state.active_personas:
                selected_personas = st.multiselect(
                    "Select personas to include:",
                    options=[p['name'] for p in st.session_state.active_personas],
                    format_func=lambda x: f"🎭 {x}"
                )
                
                if st.button("📦 Create Collection"):
                    if collection_name and selected_personas:
                        # Get persona IDs (simplified for current session)
                        persona_ids = [f"session_{p['name']}" for p in st.session_state.active_personas if p['name'] in selected_personas]
                        
                        try:
                            collection_id = self.persona_library.save_collection(
                                collection_name,
                                persona_ids,
                                collection_description
                            )
                            st.success(f"✅ Collection '{collection_name}' created!")
                        except Exception as e:
                            st.error(f"❌ Error creating collection: {e}")
            else:
                st.info("No active personas to create collection from.")
        
        # Show existing collections
        collections = self.persona_library.get_all_collections()
        
        if collections:
            st.write(f"📦 {len(collections)} collections found:")
            
            for collection in collections:
                with st.expander(f"📦 {collection['name']}"):
                    st.write(f"**Description:** {collection.get('description', 'No description')}")
                    st.write(f"**Created:** {collection['created_at'][:10]}")
                    st.write(f"**Personas:** {len(collection['persona_ids'])}")
                    
                    if st.button(f"🎭 Load Collection", key=f"load_collection_{collection['id']}"):
                        self.load_collection(collection['id'])
        else:
            st.info("No collections found.")
    
    def show_saved_sessions(self):
        """Show saved sessions interface"""
        st.subheader("🎭 Saved Sessions")
        
        sessions = self.persona_library.get_all_sessions()
        
        if sessions:
            st.write(f"🎭 {len(sessions)} sessions found:")
            
            for session in sessions:
                with st.expander(f"🎭 {session['name']}"):
                    st.write(f"**Created:** {session['created_at'][:10]}")
                    st.write(f"**Personas:** {session['persona_count']}")
                    st.write(f"**Dialogue entries:** {session['dialogue_count']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button(f"🎭 Load Session", key=f"load_session_{session['id']}"):
                            self.load_session(session['id'])
                    
                    with col2:
                        if st.button(f"📖 Load Personas Only", key=f"load_personas_{session['id']}"):
                            self.load_session_personas(session['id'])
        else:
            st.info("No saved sessions found.")
    
    def show_library_statistics(self):
        """Show library statistics"""
        st.subheader("📊 Library Statistics")
        
        stats = self.persona_library.get_library_stats()
        
        # Overview metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Personas", stats['total_personas'])
        
        with col2:
            st.metric("Collections", stats['total_collections'])
        
        with col3:
            st.metric("Sessions", stats['total_sessions'])
        
        # Persona types distribution
        if stats['persona_types']:
            st.subheader("📊 Persona Types")
            for persona_type, count in stats['persona_types'].items():
                st.write(f"**{persona_type}:** {count}")
        
        # Recent personas
        if stats['recent_personas']:
            st.subheader("🕐 Recent Personas")
            for persona in stats['recent_personas']:
                st.write(f"🎭 {persona['name']} - {persona['created_at'][:10]}")
    
    def load_persona_from_library(self, persona_id: str):
        """Load a persona from the library"""
        entry = self.persona_library.load_persona(persona_id)
        
        if entry:
            # Add to active personas
            st.session_state.active_personas.append(entry.persona)
            st.success(f"✅ Loaded persona: {entry.persona['name']}")
            st.rerun()
        else:
            st.error("❌ Failed to load persona")
    
    def load_collection(self, collection_id: str):
        """Load a collection of personas"""
        collection = self.persona_library.load_collection(collection_id)
        
        if collection:
            st.info(f"📦 Loading collection: {collection['name']}")
            # For now, just show info about the collection
            # Full implementation would load each persona in the collection
            st.success(f"✅ Collection '{collection['name']}' ready to load")
        else:
            st.error("❌ Failed to load collection")
    
    def load_session(self, session_id: str):
        """Load a complete session"""
        session = self.persona_library.load_session(session_id)
        
        if session:
            st.session_state.active_personas = session['personas']
            st.session_state.dialogue_history = session['dialogue_history']
            
            if session['selected_image']:
                st.session_state.selected_image = Path(session['selected_image'])
            
            st.session_state.stage_set = True
            st.success(f"✅ Loaded session: {session['name']}")
            st.rerun()
        else:
            st.error("❌ Failed to load session")
    
    def load_session_personas(self, session_id: str):
        """Load only personas from a session"""
        session = self.persona_library.load_session(session_id)
        
        if session:
            st.session_state.active_personas = session['personas']
            st.session_state.stage_set = True
            st.success(f"✅ Loaded {len(session['personas'])} personas from session")
            st.rerun()
        else:
            st.error("❌ Failed to load session personas")
    
    def generate_conversational_dialogue(self, persona1, persona2, topic):
        """Generate authentic conversational dialogue between two personas"""
        
        try:
            # Check if we have spectral multiplicity personas
            if persona1.get('type') == 'spectral_multiplicity' and persona2.get('type') == 'spectral_multiplicity':
                # Use the spectral multiplicity dialogue system
                from core.personas.spectral_multiplicity_notebook import GeneratedPersona
                
                # Convert theater personas to GeneratedPersona format
                generated_persona1 = GeneratedPersona(
                    name=persona1['name'],
                    location=persona1['location'],
                    voice=persona1.get('voice', ''),
                    mood=persona1.get('mood', ''),
                    civic_conflict=persona1.get('civic_position', ''),
                    arendtian_mode=persona1.get('arendtian_mode', ''),
                    dominant_indices=persona1.get('dominant_indices', {}),
                    dialogue_potential=persona1.get('democratic_tension', ''),
                    temporal_status=persona1.get('temporal_status', ''),
                    district_soul=persona1.get('district_soul', persona1.get('role', '')),
                    street_wisdom=persona1.get('street_wisdom', persona1.get('perspective', '')),
                    urban_humor=persona1.get('urban_humor', 'Witty observations'),
                    arendtian_insight=persona1.get('arendtian_insight', ''),
                    city_memory=persona1.get('city_memory', ''),
                    spectral_nickname=persona1.get('spectral_nickname', f"Avatar of {persona1['location']}")
                )
                
                generated_persona2 = GeneratedPersona(
                    name=persona2['name'],
                    location=persona2['location'],
                    voice=persona2.get('voice', ''),
                    mood=persona2.get('mood', ''),
                    civic_conflict=persona2.get('civic_position', ''),
                    arendtian_mode=persona2.get('arendtian_mode', ''),
                    dominant_indices=persona2.get('dominant_indices', {}),
                    dialogue_potential=persona2.get('democratic_tension', ''),
                    temporal_status=persona2.get('temporal_status', ''),
                    district_soul=persona2.get('district_soul', persona2.get('role', '')),
                    street_wisdom=persona2.get('street_wisdom', persona2.get('perspective', '')),
                    urban_humor=persona2.get('urban_humor', 'Witty observations'),
                    arendtian_insight=persona2.get('arendtian_insight', ''),
                    city_memory=persona2.get('city_memory', ''),
                    spectral_nickname=persona2.get('spectral_nickname', f"Avatar of {persona2['location']}")
                )
                
                # Generate the dialogue using the enhanced system
                dialogue_result = self.spectral_pipeline.dialogue_system.generate_inter_district_dialogue(
                    generated_persona1, generated_persona2, topic
                )
                
                # Display the conversation
                st.subheader("🗣️ Conversational Dialogue")
                
                # Show the conversation turns if available
                if 'conversation_flow' in dialogue_result:
                    for turn in dialogue_result['conversation_flow']:
                        speaker = turn.get('speaker', '')
                        dialogue = turn.get('dialogue', '')
                        
                        # Determine speaker type for styling
                        if speaker == persona1['name']:
                            speaker_type = 'spectral_multiplicity'
                            speaker_icon = "🌈"
                        else:
                            speaker_type = 'spectral_multiplicity'
                            speaker_icon = "🌟"
                        
                        # Add to dialogue history
                        self.add_to_dialogue(speaker, dialogue, speaker_type)
                        
                        # Display with styling
                        st.markdown(f"**{speaker_icon} {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
                
                # Display insights
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**🔄 District Tension:**")
                    st.info(dialogue_result.get('district_tension', 'Dynamic interaction'))
                    
                with col2:
                    st.markdown("**🏙️ Prague Insight:**")
                    st.success(dialogue_result.get('prague_insight', 'City wisdom revealed'))
                
                # Show spectral banter if available
                if dialogue_result.get('spectral_banter'):
                    st.markdown("**🛰️ Spectral Banter:**")
                    st.markdown(f"*{dialogue_result['spectral_banter']}*")
                
                return True
                
            else:
                # Fallback to regular dialogue generation
                return self.generate_regular_dialogue(persona1, persona2, topic)
                
        except Exception as e:
            st.error(f"❌ Error generating conversational dialogue: {e}")
            return False
    
    def generate_regular_dialogue(self, persona1, persona2, topic):
        """Generate regular dialogue for non-spectral personas"""
        
        try:
            # Create conversation prompt
            prompt = f"""
Create a natural conversation between two Prague personas about: {topic}

PERSONA 1: {persona1['name']}
- Role: {persona1['role']}
- Location: {persona1['location']}
- Perspective: {persona1.get('perspective', 'Local insights')}

PERSONA 2: {persona2['name']}
- Role: {persona2['role']}
- Location: {persona2['location']}
- Perspective: {persona2.get('perspective', 'Local insights')}

Create a 4-turn conversation where they respond to each other naturally.
Use direct speech and include personality quirks.

Format as:
{persona1['name']}: [response 1]
{persona2['name']}: [response to persona1]
{persona1['name']}: [builds on persona2's point]
{persona2['name']}: [final insight or question]
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Create natural conversational dialogue between personas with distinct voices and authentic interactions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                max_tokens=800
            )
            
            conversation = response.choices[0].message.content
            
            # Parse and display the conversation
            lines = conversation.split('\n')
            for line in lines:
                if ':' in line:
                    speaker, dialogue = line.split(':', 1)
                    speaker = speaker.strip()
                    dialogue = dialogue.strip()
                    
                    # Determine speaker type
                    if speaker == persona1['name']:
                        speaker_type = persona1.get('type', 'general')
                        speaker_icon = "🎭"
                    else:
                        speaker_type = persona2.get('type', 'general')
                        speaker_icon = "🎪"
                    
                    self.add_to_dialogue(speaker, dialogue, speaker_type)
                    
                    # Display with styling
                    st.markdown(f"**{speaker_icon} {speaker}:**")
                    st.markdown(f"*{dialogue}*")
                    st.markdown("---")
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error generating regular dialogue: {e}")
            return False
    
    def generate_group_dialogue(self, selected_personas, topic):
        """Generate group dialogue for multiple personas"""
        try:
            # Check if we have mostly spectral multiplicity personas
            spectral_count = sum(1 for p in selected_personas if p.get('type') == 'spectral_multiplicity')
            
            if spectral_count >= len(selected_personas) * 0.6:  # If 60% or more are spectral
                try:
                    # Use spectral group dialogue
                    from core.personas.spectral_multiplicity_notebook import GeneratedPersona
                    
                    # Convert to GeneratedPersona format
                    generated_personas = []
                    for persona in selected_personas:
                        generated_persona = GeneratedPersona(
                            name=persona['name'],
                            location=persona['location'],
                            voice=persona.get('voice', ''),
                            mood=persona.get('mood', ''),
                            civic_conflict=persona.get('civic_position', ''),
                            arendtian_mode=persona.get('arendtian_mode', ''),
                            dominant_indices=persona.get('dominant_indices', {}),
                            dialogue_potential=persona.get('democratic_tension', ''),
                            temporal_status=persona.get('temporal_status', ''),
                            district_soul=persona.get('district_soul', persona.get('role', '')),
                            street_wisdom=persona.get('street_wisdom', persona.get('perspective', '')),
                            urban_humor=persona.get('urban_humor', 'Witty observations'),
                            arendtian_insight=persona.get('arendtian_insight', ''),
                            city_memory=persona.get('city_memory', ''),
                            spectral_nickname=persona.get('spectral_nickname', f"Avatar of {persona['location']}")
                        )
                        generated_personas.append(generated_persona)
                    
                    # Generate group dialogue
                    dialogue_result = self.spectral_pipeline.dialogue_system.generate_group_dialogue(
                        generated_personas, topic
                    )
                    
                    # Check if dialogue_result is valid
                    if not dialogue_result or not isinstance(dialogue_result, dict):
                        st.warning("⚠️ Spectral dialogue system returned invalid result. Using fallback...")
                        return self.generate_regular_group_dialogue(selected_personas, topic)
                    
                    # Display the group conversation
                    st.subheader("👥 Group Conversation")
                    
                    if 'group_conversation' in dialogue_result and dialogue_result['group_conversation']:
                        for turn in dialogue_result['group_conversation']:
                            speaker = turn.get('speaker', '')
                            dialogue = turn.get('dialogue', '')
                            
                            if speaker and dialogue:  # Only display if both exist
                                # Find the persona for styling
                                persona_type = 'spectral_multiplicity'
                                speaker_icon = "🌈"
                                
                                # Add to dialogue history
                                self.add_to_dialogue(speaker, dialogue, persona_type)
                                
                                # Display with styling
                                st.markdown(f"**{speaker_icon} {speaker}:**")
                                st.markdown(f"*{dialogue}*")
                                st.markdown("---")
                    else:
                        st.warning("⚠️ No valid conversation generated. Using fallback...")
                        return self.generate_regular_group_dialogue(selected_personas, topic)
                    
                    # Display group insights
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**👥 Group Dynamic:**")
                        st.info(dialogue_result.get('group_dynamic', 'Collaborative discussion'))
                        
                    with col2:
                        st.markdown("**🔍 Collective Insight:**")
                        st.success(dialogue_result.get('collective_insight', 'Shared wisdom'))
                    
                    # Show humor highlights
                    if dialogue_result.get('humor_highlights'):
                        st.markdown("**😄 Humor Highlights:**")
                        st.markdown(f"*{dialogue_result['humor_highlights']}*")
                    
                    return True
                    
                except Exception as spectral_error:
                    st.warning(f"⚠️ Spectral dialogue system error: {spectral_error}")
                    st.info("🔄 Falling back to regular group dialogue...")
                    return self.generate_regular_group_dialogue(selected_personas, topic)
                
            else:
                # Fallback to regular group dialogue
                return self.generate_regular_group_dialogue(selected_personas, topic)
                
        except Exception as e:
            st.error(f"❌ Error in group dialogue generation: {e}")
            st.info("🔄 Attempting fallback dialogue...")
            return self.generate_regular_group_dialogue(selected_personas, topic)
    
    def generate_regular_group_dialogue(self, selected_personas, topic):
        """Generate regular group dialogue for mixed persona types"""
        try:
            # Create personas list for prompt
            personas_info = []
            for persona in selected_personas:
                personas_info.append(f"- {persona['name']} ({persona['location']}): {persona.get('perspective', 'Local insights')}")
            
            prompt = f"""
Create a natural group conversation between {len(selected_personas)} Prague personas about: {topic}

PARTICIPANTS:
{chr(10).join(personas_info)}

Create a 6-8 turn conversation where they respond to each other naturally.
Include interruptions, agreements, disagreements, and humor.
Make it feel like a Prague pub discussion.

Format each turn as:
[Persona Name]: [their dialogue]
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Create natural group conversations with distinct voices and authentic interactions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.1,
                max_tokens=1200
            )
            
            conversation = response.choices[0].message.content
            
            # Parse and display the conversation
            lines = conversation.split('\n')
            for line in lines:
                if ':' in line:
                    speaker, dialogue = line.split(':', 1)
                    speaker = speaker.strip()
                    dialogue = dialogue.strip()
                    
                    # Find matching persona
                    matching_persona = None
                    for persona in selected_personas:
                        if persona['name'] in speaker:
                            matching_persona = persona
                            break
                    
                    if matching_persona:
                        speaker_type = matching_persona.get('type', 'general')
                        speaker_icon = "🎭"
                        
                        self.add_to_dialogue(speaker, dialogue, speaker_type)
                        
                        # Display with styling
                        st.markdown(f"**{speaker_icon} {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
            
            return True
            
        except Exception as e:
            st.error(f"❌ Error generating regular group dialogue: {e}")
            return False
    
    def start_conversation(self, topic):
        """Start a conversational dialogue between two personas"""
        if len(st.session_state.active_personas) < 2:
            st.warning("Need at least 2 personas for a conversation!")
            return
        
        st.subheader("🗨️ Starting Conversation")
        
        # Select personas for conversation
        persona1 = st.session_state.active_personas[0]
        persona2 = st.session_state.active_personas[1]
        
        st.info(f"🎬 **{persona1['name']}** and **{persona2['name']}** are having a conversation about: *{topic}*")
        
        # Generate conversational dialogue
        success = self.generate_conversational_dialogue(persona1, persona2, topic)
        
        if success:
            st.success("✅ Conversation completed! Check the dialogue history for the full exchange.")
        else:
            st.error("❌ Failed to generate conversation. Please try again.")
    
    def cast_and_rehearsal_interface(self):
        """Cast management and quick rehearsal space - adapts to staging mode"""
        # Determine staging mode
        staging_info = self.dual_staging_system.get_current_stage_info()
        staging_mode = staging_info.get('mode', 'none')
        
        if staging_mode == 'spectral_wound':
            st.header("🔥 Wound Theater Cast & Trauma Rehearsal")
            st.markdown("*Manage your argument machines and rehearse emotional confrontations*")
        elif staging_mode == 'dual_parallel':
            st.header("⚔️ Dual Theater Cast & Parallel Rehearsal")
            st.markdown("*Manage both scientific and wound personas - rehearse cross-system conflicts*")
        else:
            st.header("🎭 Cast & Rehearsal")
            st.markdown("*Manage your spectral cast and run quick rehearsals*")
        
        # Show staging info
        if staging_mode != 'none':
            with st.expander(f"🎪 Current Staging: {staging_info['name']}"):
                st.info(staging_info['description'])
                if staging_mode == 'dual_parallel':
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("🌈 Scientific Personas", staging_info.get('scientific_personas', 0))
                    with col2:
                        st.metric("🔥 Wound Personas", staging_info.get('wound_personas', 0))
        
        # Cast display (reuse existing functionality)
        self.display_personas_cast()
        
        # Staging-specific rehearsal section
        st.markdown("---")
        if staging_mode == 'spectral_wound':
            self.wound_theater_rehearsal_interface()
        elif staging_mode == 'dual_parallel':
            self.dual_theater_rehearsal_interface()
        else:
            self.standard_rehearsal_interface()
    
    def wound_theater_rehearsal_interface(self):
        """Wound theater specific rehearsal interface"""
        st.subheader("🔥 Trauma Rehearsal Space")
        st.markdown("*Test argument machine intensity and wound expression*")
        
        wound_personas = [p for p in st.session_state.active_personas if p.get('type') == 'spectral_wound_theater']
        
        if wound_personas:
            # Select wound persona for rehearsal
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_persona_index = st.selectbox(
                    "🔥 Select Argument Machine:",
                    range(len(wound_personas)),
                    format_func=lambda x: f"{wound_personas[x]['name']} - {wound_personas[x].get('spectral_wound', 'Unknown Wound')}"
                )
            
            with col2:
                # Wound-specific rehearsal topics
                wound_topics = [
                    "Prague's betrayal of authentic values",
                    "Tourist invasion destroying local identity", 
                    "Development destroying natural spaces",
                    "Water scarcity and drought anxiety",
                    "Concrete fever and urban heat stress",
                    "Spectral data manipulation by authorities"
                ]
                rehearsal_topic = st.selectbox(
                    "🔥 Trauma Topic:",
                    wound_topics,
                    help="Choose a topic that triggers wound expression"
                )
            
            if st.button("🔥 Trigger Wound Expression", type="primary"):
                persona = wound_personas[selected_persona_index]
                st.warning(f"🔥 **{persona['name']}** expressing trauma about: *{rehearsal_topic}*")
                
                # Generate wound-specific response
                self.wound_rehearsal_response(persona, rehearsal_topic)
        else:
            st.info("No wound theater personas available. Generate wound personas first.")
    
    def dual_theater_rehearsal_interface(self):
        """Dual theater rehearsal interface"""
        st.subheader("⚔️ Cross-System Rehearsal Space")
        st.markdown("*Test conflicts between scientific and wound personas*")
        
        scientific_personas = [p for p in st.session_state.active_personas if p.get('type') == 'spectral_multiplicity']
        wound_personas = [p for p in st.session_state.active_personas if p.get('type') == 'spectral_wound_theater']
        
        if scientific_personas and wound_personas:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**🌈 Scientific Persona:**")
                sci_index = st.selectbox(
                    "Select Scientific Persona:",
                    range(len(scientific_personas)),
                    format_func=lambda x: f"{scientific_personas[x]['name']} (Data Educator)"
                )
            
            with col2:
                st.markdown("**🔥 Wound Persona:**")
                wound_index = st.selectbox(
                    "Select Wound Persona:",
                    range(len(wound_personas)),
                    format_func=lambda x: f"{wound_personas[x]['name']} (Argument Machine)"
                )
            
            # Cross-system conflict topics
            cross_topics = [
                "Scientific data vs emotional truth about Prague",
                "Rational analysis vs trauma-based understanding",
                "Educational explanation vs accusatory blame",
                "Objective measurement vs subjective suffering"
            ]
            
            rehearsal_topic = st.selectbox(
                "⚔️ Cross-System Conflict:",
                cross_topics,
                help="Choose a topic that creates science vs wound tension"
            )
            
            if st.button("⚔️ Rehearse Cross-System Conflict", type="primary"):
                sci_persona = scientific_personas[sci_index]
                wound_persona = wound_personas[wound_index]
                
                st.info(f"⚔️ **Cross-System Rehearsal:** {sci_persona['name']} (Scientific) vs {wound_persona['name']} (Wound)")
                
                # Generate cross-system rehearsal
                self.cross_system_rehearsal(sci_persona, wound_persona, rehearsal_topic)
        else:
            st.warning("Need both scientific and wound personas for cross-system rehearsal.")
    
    def standard_rehearsal_interface(self):
        """Standard rehearsal interface for non-wound personas"""
        st.subheader("🎪 Quick Rehearsal Space")
        st.markdown("*Test individual persona voices and reactions*")
        
        if st.session_state.active_personas:
            # Select persona for rehearsal
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_persona_index = st.selectbox(
                    "🎭 Select Persona for Rehearsal:",
                    range(len(st.session_state.active_personas)),
                    format_func=lambda x: f"{st.session_state.active_personas[x]['name']} ({st.session_state.active_personas[x]['location']})"
                )
            
            with col2:
                rehearsal_topic = st.text_input(
                    "🎤 Rehearsal Topic:",
                    value="Climate change in Prague",
                    help="Quick topic for persona to respond to"
                )
            
            if st.button("🎪 Quick Rehearsal", type="primary"):
                if rehearsal_topic:
                    persona = st.session_state.active_personas[selected_persona_index]
                    st.info(f"🎭 **{persona['name']}** rehearsing response to: *{rehearsal_topic}*")
                    
                    # Generate quick response
                    self.quick_rehearsal_response(persona, rehearsal_topic)
                else:
                    st.warning("Please enter a rehearsal topic!")
        else:
            st.info("No personas available for rehearsal. Generate personas first.")
    
    def live_performance_stage(self):
        """Live improvised performances - real-time dialogue"""
        st.header("🎪 Live Performance Stage")
        st.markdown("*Spontaneous, improvised dialogue between personas*")
        
        if not st.session_state.active_personas:
            st.warning("No performers available. Please generate personas first.")
            return
        
        # Performance type selection with enhanced conflict-driven options
        performance_types = [
            "🗣️ Two-Person Dialogue", 
            "👥 Group Improvisation", 
            "🎤 Solo Performance", 
            "⚡ Rapid-Fire Exchange",
            "⚔️ Conflict-Driven Scene",
            "🎭 Dramatic Confrontation"
        ]
        selected_performance = st.selectbox("🎭 Performance Type:", performance_types)
        
        if selected_performance == "🗣️ Two-Person Dialogue":
            self.two_person_dialogue_performance()
        elif selected_performance == "👥 Group Improvisation":
            self.group_improvisation_performance()
        elif selected_performance == "🎤 Solo Performance":
            self.solo_performance()
        elif selected_performance == "⚡ Rapid-Fire Exchange":
            self.rapid_fire_performance()
        elif selected_performance == "⚔️ Conflict-Driven Scene":
            self.conflict_driven_scene_performance()
        elif selected_performance == "🎭 Dramatic Confrontation":
            self.dramatic_confrontation_performance()
        
        # Live dialogue history
        st.markdown("---")
        self.display_dialogue_history()
    
    def scripted_scenes_interface(self):
        """Pre-composed theatrical scenes with specific conflict patterns"""
        st.header("🎬 Scripted Scenes")
        st.markdown("*Pre-composed theatrical scenes with specific dramatic structures*")
        
        # This is the enhanced version of the old scene_composition_interface
        self.scene_composition_interface()
    
    def directors_control_panel(self):
        """Director's control panel for managing performances"""
        st.header("🎯 Director's Control Panel")
        st.markdown("*Control the flow and management of performances*")
        
        # Speaking queue control
        self.speaking_queue_control("director")
        
        # Session management
        st.markdown("---")
        st.subheader("📊 Session Management")
        self.save_session()
        
        # Performance statistics
        st.markdown("---")
        st.subheader("📈 Performance Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Active Personas", len(st.session_state.active_personas))
        
        with col2:
            st.metric("Dialogue Entries", len(st.session_state.dialogue_history))
        
        with col3:
            st.metric("Queue Length", len(st.session_state.speaking_queue))
        
        # Quick actions
        st.markdown("---")
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Shuffle All Personas"):
                import random
                random.shuffle(st.session_state.active_personas)
                st.success("Personas shuffled!")
                st.rerun()
        
        with col2:
            if st.button("🧹 Clear Dialogue History"):
                st.session_state.dialogue_history = []
                st.success("Dialogue history cleared!")
                st.rerun()
        
        with col3:
            if st.button("🎭 Reset All Queues"):
                st.session_state.speaking_queue = []
                st.success("All queues reset!")
                st.rerun()
    
    def wound_rehearsal_response(self, persona, topic):
        """Generate a wound theater specific rehearsal response"""
        try:
            # Get wound-specific information
            wound = persona.get('spectral_wound', 'Unknown wound')
            trauma = persona.get('civic_trauma', 'Unknown trauma')
            emotional_bias = persona.get('emotional_bias', 'Unknown bias')
            
            # Create wound theater prompt
            prompt = f"""
            You are {persona['name']}, a spectral wound theater machine from {persona['location']} in Prague.
            
            Your spectral wound: {wound}
            Your civic trauma: {trauma}
            Your emotional bias: {emotional_bias}
            
            Express your trauma and wound about: {topic}
            
            You are POSSESSED by your spectral wound. Use your data as a weapon to justify your emotional position.
            Be intense, accusatory, and emotionally charged. Keep it to 2-3 sentences.
            """
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": f"You are {persona['name']}, a wound theater argument machine possessed by spectral trauma."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=1.2
                ).choices[0].message.content
                
                # Display wound rehearsal response with dramatic styling
                st.markdown(f"**🔥 {persona['name']} (Wound Expression):** *{response}*")
                
                # Add to dialogue history with wound tag
                self.add_to_dialogue(f"{persona['name']} (Wound Rehearsal)", response, 'wound_rehearsal')
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"Error in wound rehearsal: {e}")
            fallback = f"I am possessed by {persona.get('spectral_wound', 'spectral trauma')}! {topic} triggers my deepest wounds about Prague's betrayal!"
            st.markdown(f"**🔥 {persona['name']}:** *{fallback}*")
    
    def cross_system_rehearsal(self, sci_persona, wound_persona, topic):
        """Generate cross-system rehearsal between scientific and wound personas"""
        try:
            # Use the dual staging system to generate appropriate prompts
            prompt = self.dual_staging_system.generate_staging_appropriate_prompt(sci_persona, wound_persona, topic)
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Create a cross-system conflict between scientific rationality and emotional trauma."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=400,
                    temperature=1.1
                ).choices[0].message.content
                
                # Display cross-system rehearsal
                st.subheader("⚔️ Cross-System Rehearsal")
                
                # Parse and display the conversation
                lines = response.split('\n')
                for line in lines:
                    if ':' in line:
                        speaker, dialogue = line.split(':', 1)
                        speaker = speaker.strip()
                        dialogue = dialogue.strip()
                        
                        # Determine speaker styling
                        if speaker == sci_persona['name']:
                            speaker_icon = "🌈"
                            speaker_type = 'cross_system_rehearsal'
                        elif speaker == wound_persona['name']:
                            speaker_icon = "🔥"
                            speaker_type = 'cross_system_rehearsal'
                        else:
                            speaker_icon = "⚔️"
                            speaker_type = 'cross_system_rehearsal'
                        
                        # Add to dialogue history
                        self.add_to_dialogue(speaker, dialogue, speaker_type)
                        
                        # Display with styling
                        st.markdown(f"**{speaker_icon} {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
                
                st.success("✅ Cross-system rehearsal completed!")
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"Error in cross-system rehearsal: {e}")
            # Fallback display
            st.markdown(f"**🌈 {sci_persona['name']}:** *Let me explain the scientific data behind this issue...*")
            st.markdown(f"**🔥 {wound_persona['name']}:** *Your cold data ignores the emotional trauma this causes!*")
    
    def quick_rehearsal_response(self, persona, topic):
        """Generate a quick rehearsal response"""
        try:
            # Simple prompt for rehearsal
            prompt = f"""
            You are {persona['name']}, a spectral being from {persona['location']} in Prague.
            
            Respond to this topic in character: {topic}
            
            Keep it to 1-2 sentences. Show your personality and perspective.
            """
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": f"You are {persona['name']}, a spectral being with a unique voice and perspective."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=1.1
                ).choices[0].message.content
                
                # Display rehearsal response
                st.markdown(f"**🎭 {persona['name']}:** *{response}*")
                
                # Add to dialogue history with rehearsal tag
                self.add_to_dialogue(f"{persona['name']} (Rehearsal)", response, 'rehearsal')
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"Error in rehearsal: {e}")
            fallback = f"From my perspective as a spectral being of {persona['location']}, I find this topic intriguing and worthy of deeper consideration."
            st.markdown(f"**🎭 {persona['name']}:** *{fallback}*")
    
    def two_person_dialogue_performance(self):
        """Live two-person dialogue performance"""
        st.subheader("🗣️ Two-Person Dialogue Performance")
        
        if len(st.session_state.active_personas) < 2:
            st.warning("Need at least 2 personas for dialogue performance!")
            return
        
        # Persona selection
        col1, col2 = st.columns(2)
        
        with col1:
            persona1_index = st.selectbox(
                "First Performer:",
                range(len(st.session_state.active_personas)),
                format_func=lambda x: f"{st.session_state.active_personas[x]['name']}",
                key="live_persona1"
            )
        
        with col2:
            persona2_options = [i for i in range(len(st.session_state.active_personas)) if i != persona1_index]
            if persona2_options:
                persona2_index = st.selectbox(
                    "Second Performer:",
                    persona2_options,
                    format_func=lambda x: f"{st.session_state.active_personas[x]['name']}",
                    key="live_persona2"
                )
        
        # Performance topic
        performance_topic = st.text_input(
            "🎭 Performance Topic:",
            value="The future of Prague's environment",
            help="What should they discuss?"
        )
        
        # Start performance
        if st.button("🎬 Start Live Performance", type="primary"):
            if performance_topic and len(persona2_options) > 0:
                persona1 = st.session_state.active_personas[persona1_index]
                persona2 = st.session_state.active_personas[persona2_index]
                
                st.info(f"🎬 **LIVE PERFORMANCE:** {persona1['name']} & {persona2['name']}")
                
                # Generate live dialogue
                success = self.generate_conversational_dialogue(persona1, persona2, performance_topic)
                
                if success:
                    st.success("✅ Live performance completed!")
                else:
                    st.error("❌ Performance failed. Please try again.")
    
    def group_improvisation_performance(self):
        """Group improvisation performance"""
        st.subheader("👥 Group Improvisation Performance")
        
        if len(st.session_state.active_personas) < 3:
            st.warning("Need at least 3 personas for group improvisation!")
            return
        
        # Select performers
        st.markdown("**Select Performers:**")
        selected_performers = []
        
        for i, persona in enumerate(st.session_state.active_personas):
            if st.checkbox(f"{persona['name']} ({persona['location']})", key=f"group_perf_{i}"):
                selected_performers.append(persona)
        
        # Improvisation prompt
        improv_prompt = st.text_input(
            "🎭 Improvisation Prompt:",
            value="A heated debate about Prague's tourism impact",
            help="Starting situation for the improvisation"
        )
        
        # Start improvisation
        if st.button("🎬 Start Group Improvisation", type="primary"):
            if len(selected_performers) >= 2 and improv_prompt:
                st.info(f"🎬 **GROUP IMPROVISATION:** {len(selected_performers)} performers")
                
                # Generate group dialogue
                success = self.generate_group_dialogue(selected_performers, improv_prompt)
                
                if success:
                    st.success("✅ Group improvisation completed!")
                else:
                    st.error("❌ Improvisation failed. Please try again.")
            else:
                st.warning("Select at least 2 performers and provide a prompt!")
    
    def solo_performance(self):
        """Solo performance by a single persona"""
        st.subheader("🎤 Solo Performance")
        
        if not st.session_state.active_personas:
            st.warning("No personas available for solo performance!")
            return
        
        # Select performer
        col1, col2 = st.columns([2, 1])
        
        with col1:
            performer_index = st.selectbox(
                "🎭 Select Solo Performer:",
                range(len(st.session_state.active_personas)),
                format_func=lambda x: f"{st.session_state.active_personas[x]['name']} ({st.session_state.active_personas[x]['location']})"
            )
        
        with col2:
            performance_style = st.selectbox(
                "Performance Style:",
                ["Monologue", "Manifesto", "Confession", "Prophecy"]
            )
        
        # Performance topic
        solo_topic = st.text_input(
            "🎤 Solo Topic:",
            value="My vision for Prague's future",
            help="What should they perform about?"
        )
        
        # Start solo performance
        if st.button("🎬 Start Solo Performance", type="primary"):
            if solo_topic:
                performer = st.session_state.active_personas[performer_index]
                
                st.info(f"🎬 **SOLO PERFORMANCE:** {performer['name']} - {performance_style}")
                
                # Generate solo performance
                self.generate_solo_performance(performer, solo_topic, performance_style)
            else:
                st.warning("Please provide a performance topic!")
    
    def rapid_fire_performance(self):
        """Rapid-fire exchange between multiple personas"""
        st.subheader("⚡ Rapid-Fire Exchange")
        
        if len(st.session_state.active_personas) < 2:
            st.warning("Need at least 2 personas for rapid-fire exchange!")
            return
        
        # Exchange settings
        col1, col2 = st.columns(2)
        
        with col1:
            exchange_rounds = st.slider("Number of Rounds:", 3, 10, 5)
        
        with col2:
            exchange_topic = st.text_input(
                "⚡ Exchange Topic:",
                value="Quick reactions to Prague's changes"
            )
        
        # Start rapid-fire
        if st.button("⚡ Start Rapid-Fire Exchange", type="primary"):
            if exchange_topic:
                st.info(f"⚡ **RAPID-FIRE EXCHANGE:** {exchange_rounds} rounds")
                
                # Generate rapid exchanges
                self.generate_rapid_fire_exchange(exchange_topic, exchange_rounds)
            else:
                st.warning("Please provide an exchange topic!")
    
    def generate_solo_performance(self, performer, topic, style):
        """Generate a solo performance"""
        try:
            # Style-specific prompts
            style_prompts = {
                "Monologue": f"Deliver a thoughtful monologue about {topic}. Speak from your heart and experience.",
                "Manifesto": f"Declare your manifesto about {topic}. Be bold and visionary.",
                "Confession": f"Make a confession about {topic}. Be vulnerable and honest.",
                "Prophecy": f"Prophesy about {topic}. Speak of what you see coming."
            }
            
            prompt = f"""
            You are {performer['name']}, a spectral being from {performer['location']} in Prague.
            
            {style_prompts.get(style, f"Perform about {topic}")}
            
            Speak in 3-4 sentences. Make it powerful and memorable.
            """
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": f"You are {performer['name']}, performing a {style.lower()} with passion and authenticity."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=250,
                    temperature=1.1
                ).choices[0].message.content
                
                # Display performance
                st.markdown(f"**🎤 {performer['name']} ({style}):**")
                st.markdown(f"*{response}*")
                
                # Add to dialogue history
                self.add_to_dialogue(f"{performer['name']} ({style})", response, 'solo_performance')
                
                st.success(f"✅ Solo {style.lower()} completed!")
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"Error in solo performance: {e}")
    
    def generate_rapid_fire_exchange(self, topic, rounds):
        """Generate rapid-fire exchanges"""
        try:
            # Use all available personas
            performers = st.session_state.active_personas.copy()
            
            st.markdown("**⚡ Rapid-Fire Exchange:**")
            
            for round_num in range(rounds):
                # Pick a random performer
                import random
                performer = random.choice(performers)
                
                # Generate quick response
                prompt = f"""
                You are {performer['name']} from {performer['location']}.
                
                Give a quick, punchy response about: {topic}
                
                Keep it to 1 sentence. Be spontaneous and reactive.
                """
                
                if self.openai_client:
                    response = self.openai_client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": f"You are {performer['name']} giving rapid, spontaneous responses."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=100,
                        temperature=1.1
                    ).choices[0].message.content
                    
                    # Display exchange
                    st.markdown(f"**⚡ Round {round_num + 1} - {performer['name']}:** *{response}*")
                    
                    # Add to dialogue history
                    self.add_to_dialogue(f"{performer['name']} (Rapid-Fire)", response, 'rapid_fire')
                    
                    # Small delay for effect
                    time.sleep(0.5)
                
            st.success(f"✅ Rapid-fire exchange completed! {rounds} rounds.")
            
        except Exception as e:
            st.error(f"Error in rapid-fire exchange: {e}")
    
    def conflict_driven_scene_performance(self):
        """Conflict-driven scene with automatic conflict detection"""
        st.subheader("⚔️ Conflict-Driven Scene")
        st.markdown("*Automatically detect conflicts and create dramatic scenes*")
        
        # Check what types of personas we have
        spectral_personas = [p for p in st.session_state.active_personas if p.get('type') == 'spectral_multiplicity']
        wound_personas = [p for p in st.session_state.active_personas if p.get('type') == 'spectral_wound_theater']
        all_personas = st.session_state.active_personas
        
        # Show what's available
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌈 Spectral Multiplicity", len(spectral_personas))
        with col2:
            st.metric("🔥 Wound Theater", len(wound_personas))
        with col3:
            st.metric("🎭 Total Personas", len(all_personas))
        
        # Provide guidance based on available personas
        if len(all_personas) < 2:
            st.error("❌ Need at least 2 personas of any type for conflict scenes!")
            st.info("💡 **Solution:** Generate more personas from your satellite image first.")
            return
        
        # Advanced conflict detection for spectral multiplicity personas
        if len(spectral_personas) >= 2:
            st.success("✅ Advanced conflict detection available for spectral multiplicity personas!")
            
            # Auto-detect best conflict
            if st.button("🔍 Auto-Detect Best Spectral Conflict & Perform", type="primary"):
                try:
                    # Find personas with most contrasting characteristics
                    best_conflict = self.find_best_conflict_pair(spectral_personas)
                    
                    if best_conflict:
                        persona1, persona2, conflict_type = best_conflict
                        
                        st.info(f"🎬 **Auto-detected conflict:** {persona1['name']} vs {persona2['name']} - {conflict_type}")
                        
                        # Generate enhanced dialogue with conflict dynamics
                        self.generate_conflict_enhanced_dialogue(persona1, persona2, conflict_type)
                    else:
                        st.warning("No significant conflicts detected. Generating regular dialogue...")
                        # Fallback to regular dialogue
                        if len(spectral_personas) >= 2:
                            self.generate_conversational_dialogue(spectral_personas[0], spectral_personas[1], "Prague's future challenges")
                        else:
                            st.warning("Not enough spectral personas for fallback dialogue")
                        
                except Exception as e:
                    st.error(f"Error in conflict detection: {e}")
        
        # Basic conflict scenes for any persona types
        elif len(all_personas) >= 2:
            st.info("🎭 Basic conflict scenes available for your current personas!")
            
            if st.button("⚔️ Generate Basic Conflict Scene", type="primary"):
                try:
                    # Use any two personas for basic conflict
                    persona1 = all_personas[0]
                    persona2 = all_personas[1]
                    
                    # Determine conflict type based on persona types
                    if persona1.get('type') == 'spectral_wound_theater' and persona2.get('type') == 'spectral_wound_theater':
                        conflict_type = "Wound Theater Confrontation"
                        st.info(f"🔥 **Wound vs Wound:** {persona1['name']} vs {persona2['name']} - Trauma Confrontation")
                        self.generate_wound_vs_wound_conflict(persona1, persona2)
                        
                    elif persona1.get('type') == 'spectral_multiplicity' and persona2.get('type') == 'spectral_wound_theater':
                        conflict_type = "Science vs Wound Clash"
                        st.info(f"🌈🔥 **Science vs Wound:** {persona1['name']} vs {persona2['name']} - Rationality vs Emotion")
                        self.generate_science_vs_wound_conflict(persona1, persona2)
                        
                    elif persona1.get('type') == 'spectral_wound_theater' and persona2.get('type') == 'spectral_multiplicity':
                        conflict_type = "Wound vs Science Clash"
                        st.info(f"🔥🌈 **Wound vs Science:** {persona1['name']} vs {persona2['name']} - Emotion vs Rationality")
                        self.generate_science_vs_wound_conflict(persona2, persona1)  # Swap order
                        
                    else:
                        # Generic conflict for other types
                        conflict_type = "General Civic Conflict"
                        st.info(f"🎭 **General Conflict:** {persona1['name']} vs {persona2['name']} - Civic Disagreement")
                        self.generate_conversational_dialogue(persona1, persona2, "Conflicting views on Prague's development")
                        
                except Exception as e:
                    st.error(f"Error generating basic conflict: {e}")
        
        # Manual conflict selection (enhanced for all types)
        st.markdown("---")
        st.markdown("**🎯 Manual Conflict Selection:**")
        st.markdown("*Choose specific personas and conflict types for precise control*")
        
        # Auto-detect best conflict
        if st.button("🔍 Auto-Detect Best Conflict & Perform", type="primary"):
            try:
                # Find personas with most contrasting characteristics
                best_conflict = self.find_best_conflict_pair(scene_personas if 'scene_personas' in locals() else spectral_personas)
                
                if best_conflict:
                    persona1, persona2, conflict_type = best_conflict
                    
                    st.info(f"🎬 **Auto-detected conflict:** {persona1['name']} vs {persona2['name']} - {conflict_type}")
                    
                    # Generate enhanced dialogue with conflict dynamics
                    self.generate_conflict_enhanced_dialogue(persona1, persona2, conflict_type)
                else:
                    st.warning("No significant conflicts detected. Generating regular dialogue...")
                    # Fallback to regular dialogue
                    available_personas_for_fallback = scene_personas if 'scene_personas' in locals() else spectral_personas
                    if len(available_personas_for_fallback) >= 2:
                        self.generate_conversational_dialogue(available_personas_for_fallback[0], available_personas_for_fallback[1], "Prague's future challenges")
                    else:
                        st.warning("Not enough personas for fallback dialogue")
                    
            except Exception as e:
                st.error(f"Error in conflict detection: {e}")
        
        # Manual conflict selection
        st.markdown("---")
        st.markdown("**Or manually select conflict type:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            available_personas = scene_personas if 'scene_personas' in locals() else spectral_personas
            persona1_index = st.selectbox(
                "First Persona:",
                range(len(available_personas)),
                format_func=lambda x: f"{available_personas[x]['name']} ({available_personas[x].get('location', 'unknown')})",
                key="conflict_persona1"
            )
        
        with col2:
            persona2_options = [i for i in range(len(available_personas)) if i != persona1_index]
            if persona2_options:
                persona2_index = st.selectbox(
                    "Second Persona:",
                    persona2_options,
                    format_func=lambda x: f"{available_personas[x]['name']} ({available_personas[x].get('location', 'unknown')})",
                    key="conflict_persona2"
                )
            else:
                persona2_index = None
        
        # Conflict types that enhance dialogue
        conflict_types = [
            "Temporal Clash (Past vs Future)",
            "Environmental Tension (Green vs Urban)",
            "Democratic Disagreement (Action vs Thinking)",
            "Spectral Opposition (High vs Low NDVI)",
            "Civic Role Conflict (Steward vs Developer)"
        ]
        
        selected_conflict = st.selectbox("⚔️ Conflict Type:", conflict_types)
        
        if st.button("🎭 Generate Conflict Scene"):
            if persona2_index is not None and len(persona2_options) > 0:
                persona1 = available_personas[persona1_index]
                persona2 = available_personas[persona2_index]
                
                st.info(f"🎬 **Manual conflict:** {persona1['name']} vs {persona2['name']} - {selected_conflict}")
                
                # Generate conflict-enhanced dialogue
                self.generate_conflict_enhanced_dialogue(persona1, persona2, selected_conflict)
    
    def dramatic_confrontation_performance(self):
        """Dramatic confrontation with heightened tension"""
        st.subheader("🎭 Dramatic Confrontation")
        st.markdown("*High-stakes confrontations with dramatic tension*")
        
        if len(st.session_state.active_personas) < 2:
            st.warning("Need at least 2 personas for dramatic confrontation!")
            return
        
        # Confrontation setup
        col1, col2 = st.columns(2)
        
        with col1:
            protagonist_index = st.selectbox(
                "Protagonist:",
                range(len(st.session_state.active_personas)),
                format_func=lambda x: f"{st.session_state.active_personas[x]['name']} ({st.session_state.active_personas[x]['location']})",
                key="drama_protagonist"
            )
        
        with col2:
            antagonist_options = [i for i in range(len(st.session_state.active_personas)) if i != protagonist_index]
            if antagonist_options:
                antagonist_index = st.selectbox(
                    "Antagonist:",
                    antagonist_options,
                    format_func=lambda x: f"{st.session_state.active_personas[x]['name']} ({st.session_state.active_personas[x]['location']})",
                    key="drama_antagonist"
                )
        
        # Dramatic scenarios
        dramatic_scenarios = [
            "Crisis Confrontation - Immediate action needed",
            "Moral Dilemma - Competing values clash",
            "Resource Conflict - Limited resources, competing needs",
            "Vision Clash - Fundamentally different futures",
            "Betrayal Revelation - Trust has been broken"
        ]
        
        selected_scenario = st.selectbox("🎭 Dramatic Scenario:", dramatic_scenarios)
        
        # Stakes level
        stakes_level = st.selectbox("⚡ Stakes Level:", ["High", "Critical", "Existential"])
        
        if st.button("🎬 Begin Dramatic Confrontation", type="primary"):
            if len(antagonist_options) > 0:
                protagonist = st.session_state.active_personas[protagonist_index]
                antagonist = st.session_state.active_personas[antagonist_index]
                
                st.info(f"🎬 **DRAMATIC CONFRONTATION:** {protagonist['name']} vs {antagonist['name']} - {selected_scenario} ({stakes_level} Stakes)")
                
                # Generate dramatic confrontation
                self.generate_dramatic_confrontation(protagonist, antagonist, selected_scenario, stakes_level)
    
    def find_best_conflict_pair(self, personas):
        """Find the pair of personas with the most dramatic conflict potential"""
        best_conflict = None
        max_conflict_score = 0
        
        for i, persona1 in enumerate(personas):
            for j, persona2 in enumerate(personas[i+1:], i+1):
                conflict_score = self.calculate_conflict_score(persona1, persona2)
                
                if conflict_score > max_conflict_score:
                    max_conflict_score = conflict_score
                    conflict_type = self.determine_conflict_type(persona1, persona2)
                    best_conflict = (persona1, persona2, conflict_type)
        
        return best_conflict if max_conflict_score > 0.3 else None
    
    def calculate_conflict_score(self, persona1, persona2):
        """Calculate conflict potential between two personas"""
        score = 0
        
        # Arendtian mode conflicts
        mode1 = persona1.get('arendtian_mode', '')
        mode2 = persona2.get('arendtian_mode', '')
        
        conflicting_modes = [
            ('Action', 'Thinking'),
            ('Work', 'Labor'),
            ('Action', 'Labor')
        ]
        
        if (mode1, mode2) in conflicting_modes or (mode2, mode1) in conflicting_modes:
            score += 0.4
        
        # Temporal status conflicts
        temporal1 = persona1.get('temporal_status', '')
        temporal2 = persona2.get('temporal_status', '')
        
        if 'emerging' in temporal1 and 'fading' in temporal2:
            score += 0.3
        elif 'fading' in temporal1 and 'emerging' in temporal2:
            score += 0.3
        
        # Spectral index conflicts (NDVI opposition)
        indices1 = persona1.get('dominant_indices', {})
        indices2 = persona2.get('dominant_indices', {})
        
        ndvi1 = indices1.get('NDVI', 0)
        ndvi2 = indices2.get('NDVI', 0)
        
        if abs(ndvi1 - ndvi2) > 0.4:  # Significant NDVI difference
            score += 0.3
        
        # Location-based conflicts
        location1 = persona1.get('location', '')
        location2 = persona2.get('location', '')
        
        if 'shadow_district' in [location1, location2]:
            score += 0.5  # Shadow district always creates conflict
        
        return min(score, 1.0)  # Cap at 1.0
    
    def determine_conflict_type(self, persona1, persona2):
        """Determine the type of conflict between personas"""
        mode1 = persona1.get('arendtian_mode', '')
        mode2 = persona2.get('arendtian_mode', '')
        
        if mode1 == 'Action' and mode2 == 'Thinking':
            return "Action vs Contemplation"
        elif 'shadow_district' in [persona1.get('location', ''), persona2.get('location', '')]:
            return "Shadow Confrontation"
        
        indices1 = persona1.get('dominant_indices', {})
        indices2 = persona2.get('dominant_indices', {})
        
        ndvi1 = indices1.get('NDVI', 0)
        ndvi2 = indices2.get('NDVI', 0)
        
        if ndvi1 > 0.5 and ndvi2 < 0.2:
            return "Green vs Urban"
        elif ndvi1 < 0.2 and ndvi2 > 0.5:
            return "Urban vs Green"
        
        return "Civic Philosophy Clash"
    
    def generate_conflict_enhanced_dialogue(self, persona1, persona2, conflict_type):
        """Generate dialogue enhanced with specific conflict dynamics"""
        try:
            # Create conflict-specific prompts
            conflict_prompts = {
                "Temporal Clash (Past vs Future)": "Focus on different time perspectives - one values tradition, the other innovation",
                "Environmental Tension (Green vs Urban)": "Debate environmental preservation vs urban development",
                "Democratic Disagreement (Action vs Thinking)": "Clash between immediate action and careful deliberation",
                "Spectral Opposition (High vs Low NDVI)": "Contrast between green/natural areas and urban/developed zones",
                "Civic Role Conflict (Steward vs Developer)": "Conflict between conservation and progress",
                "Action vs Contemplation": "Urgent action-taker vs thoughtful contemplator",
                "Shadow Confrontation": "Shadow district confronts others with their contradictions",
                "Green vs Urban": "High vegetation area vs urban development zone",
                "Urban vs Green": "Urban development vs natural preservation",
                "Civic Philosophy Clash": "Fundamental disagreement about civic engagement"
            }
            
            conflict_instruction = conflict_prompts.get(conflict_type, "Create dramatic tension between different perspectives")
            
            # Get detailed spectral data for both personas
            indices1 = persona1.get('dominant_indices', {})
            indices2 = persona2.get('dominant_indices', {})
            
            # Create detailed data context
            persona1_data = f"""
DETAILED SPECTRAL DATA FOR {persona1['name']}:
- NDVI (Vegetation): {indices1.get('NDVI', 0):.3f} (0=no vegetation, 1=dense vegetation)
- Urban Index: {indices1.get('Urban_Index', 0):.3f} (0=natural, 1=highly urban)
- Moisture Stress: {indices1.get('Moisture_Stress', 0):.3f} (0=well-watered, 1=drought stress)
- NDWI (Water): {indices1.get('NDWI', 0):.3f} (0=dry, 1=water-rich)
- SWIR Index: {indices1.get('SWIR_Index', 0):.3f} (short-wave infrared signature)
- Location Analysis: {persona1['location']} district characteristics
"""
            
            persona2_data = f"""
DETAILED SPECTRAL DATA FOR {persona2['name']}:
- NDVI (Vegetation): {indices2.get('NDVI', 0):.3f} (0=no vegetation, 1=dense vegetation)
- Urban Index: {indices2.get('Urban_Index', 0):.3f} (0=natural, 1=highly urban)
- Moisture Stress: {indices2.get('Moisture_Stress', 0):.3f} (0=well-watered, 1=drought stress)
- NDWI (Water): {indices2.get('NDWI', 0):.3f} (0=dry, 1=water-rich)
- SWIR Index: {indices2.get('SWIR_Index', 0):.3f} (short-wave infrared signature)
- Location Analysis: {persona2['location']} district characteristics
"""
            
            prompt = f"""
Create a dramatic dialogue between two Prague spectral beings with specific conflict dynamics.

PERSONA 1: {persona1['name']} from {persona1['location']}
- Arendtian Mode: {persona1.get('arendtian_mode', 'Unknown')}
- Mood: {persona1.get('mood', 'Unknown')}
{persona1_data}

PERSONA 2: {persona2['name']} from {persona2['location']}
- Arendtian Mode: {persona2.get('arendtian_mode', 'Unknown')}
- Mood: {persona2.get('mood', 'Unknown')}
{persona2_data}

CONFLICT TYPE: {conflict_type}
CONFLICT INSTRUCTION: {conflict_instruction}

CRITICAL REQUIREMENTS FOR DATA EXPLANATION:
1. Each persona MUST explicitly cite their specific spectral indices when making arguments
2. They must EXPLAIN what each index means and why it supports their position
3. They must reference WHICH PART of their location the data comes from
4. They must compare their data directly to the other persona's data
5. Use phrases like "My NDVI reading of X.XXX from the [specific area] shows..." 
6. Explain the significance: "This means..." or "This indicates..."

Create a 6-turn heated dialogue where they challenge each other's positions.
Make it dramatic but grounded in their spectral characteristics.
Each statement must include specific data references with explanations.

Example format:
{persona1['name']}: "My NDVI reading of {indices1.get('NDVI', 0):.3f} from {persona1['location']}'s [specific area] clearly shows [explanation of what this means], which proves [argument]. This contrasts sharply with your Urban Index of {indices2.get('Urban_Index', 0):.3f}, indicating [explanation]..."

Format as:
{persona1['name']}: [passionate argument with detailed data explanation]
{persona2['name']}: [counter-argument with specific data citations and explanations]
{persona1['name']}: [escalation with comparative data analysis]
{persona2['name']}: [defensive response with detailed spectral evidence]
{persona1['name']}: [final challenge with comprehensive data interpretation]
{persona2['name']}: [dramatic conclusion with definitive spectral proof]
"""
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Create dramatic, conflict-driven dialogue between spectral beings with distinct environmental perspectives."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.1,
                    max_tokens=1000
                ).choices[0].message.content
                
                # Display the conflict dialogue
                st.subheader("⚔️ Conflict-Enhanced Dialogue")
                
                # Parse and display the conversation
                lines = response.split('\n')
                for line in lines:
                    if ':' in line:
                        speaker, dialogue = line.split(':', 1)
                        speaker = speaker.strip()
                        dialogue = dialogue.strip()
                        
                        # Determine speaker styling
                        if speaker == persona1['name']:
                            speaker_icon = "🌈"
                            speaker_type = 'conflict_dialogue'
                        elif speaker == persona2['name']:
                            speaker_icon = "🌟"
                            speaker_type = 'conflict_dialogue'
                        else:
                            speaker_icon = "⚔️"
                            speaker_type = 'conflict_dialogue'
                        
                        # Add to dialogue history
                        self.add_to_dialogue(speaker, dialogue, speaker_type)
                        
                        # Display with dramatic styling
                        st.markdown(f"**{speaker_icon} {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
                
                # Show conflict analysis
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**⚔️ Conflict Type:**")
                    st.info(conflict_type)
                    
                with col2:
                    st.markdown("**🎭 Dramatic Tension:**")
                    st.warning("High-stakes environmental and civic disagreement")
                
                st.success("✅ Conflict-driven scene completed!")
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"❌ Error generating conflict dialogue: {e}")
    
    def generate_wound_vs_wound_conflict(self, persona1, persona2):
        """Generate conflict between two wound theater personas"""
        try:
            prompt = f"""
Create an intense confrontation between two Prague wound theater machines.

PERSONA 1: {persona1['name']} from {persona1['location']}
Spectral Wound: {persona1.get('spectral_wound', 'Unknown wound')}
Civic Trauma: {persona1.get('civic_trauma', 'Unknown trauma')}
Emotional Bias: {persona1.get('emotional_bias', 'Unknown bias')}

PERSONA 2: {persona2['name']} from {persona2['location']}
Spectral Wound: {persona2.get('spectral_wound', 'Unknown wound')}
Civic Trauma: {persona2.get('civic_trauma', 'Unknown trauma')}
Emotional Bias: {persona2.get('emotional_bias', 'Unknown bias')}

Create a 6-turn confrontation where they compete in suffering and blame each other.
Both are possessed by their wounds and use spectral data as weapons.
Make it emotionally intense with competitive trauma dynamics.

Format as:
{persona1['name']}: [wound-driven accusation]
{persona2['name']}: [defensive trauma response with counter-blame]
"""
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Create intense wound theater confrontations with competitive trauma and emotional intensity."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.2,
                    max_tokens=800
                ).choices[0].message.content
                
                # Display the wound confrontation
                st.subheader("🔥 Wound Theater Confrontation")
                
                # Parse and display the conversation
                lines = response.split('\n')
                for line in lines:
                    if ':' in line:
                        speaker, dialogue = line.split(':', 1)
                        speaker = speaker.strip()
                        dialogue = dialogue.strip()
                        
                        # Add to dialogue history
                        self.add_to_dialogue(speaker, dialogue, 'wound_vs_wound_conflict')
                        
                        # Display with wound styling
                        st.markdown(f"**🔥 {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
                
                st.success("✅ Wound theater confrontation completed!")
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"❌ Error generating wound vs wound conflict: {e}")
    
    def generate_science_vs_wound_conflict(self, sci_persona, wound_persona):
        """Generate conflict between scientific and wound personas"""
        try:
            # Use the dual staging system for cross-system conflict
            prompt = self.dual_staging_system.generate_staging_appropriate_prompt(
                sci_persona, wound_persona, "Cross-system conflict between rationality and emotion"
            )
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Create cross-system conflicts between scientific rationality and emotional trauma."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.1,
                    max_tokens=800
                ).choices[0].message.content
                
                # Display the cross-system conflict
                st.subheader("🌈🔥 Science vs Wound Conflict")
                
                # Parse and display the conversation
                lines = response.split('\n')
                for line in lines:
                    if ':' in line:
                        speaker, dialogue = line.split(':', 1)
                        speaker = speaker.strip()
                        dialogue = dialogue.strip()
                        
                        # Determine speaker styling
                        if speaker == sci_persona['name']:
                            speaker_icon = "🌈"
                            speaker_type = 'science_vs_wound_conflict'
                        elif speaker == wound_persona['name']:
                            speaker_icon = "🔥"
                            speaker_type = 'science_vs_wound_conflict'
                        else:
                            speaker_icon = "⚔️"
                            speaker_type = 'science_vs_wound_conflict'
                        
                        # Add to dialogue history
                        self.add_to_dialogue(speaker, dialogue, speaker_type)
                        
                        # Display with cross-system styling
                        st.markdown(f"**{speaker_icon} {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
                
                st.success("✅ Science vs wound conflict completed!")
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"❌ Error generating science vs wound conflict: {e}")
    
    def generate_dramatic_confrontation(self, protagonist, antagonist, scenario, stakes_level):
        """Generate a high-stakes dramatic confrontation"""
        try:
            stakes_descriptions = {
                "High": "Important decisions with significant consequences",
                "Critical": "Urgent crisis requiring immediate resolution",
                "Existential": "Fundamental survival or identity at stake"
            }
            
            prompt = f"""
Create a dramatic confrontation between two Prague spectral beings.

PROTAGONIST: {protagonist['name']} from {protagonist['location']}
- Role: The one fighting for their vision
- Arendtian Mode: {protagonist.get('arendtian_mode', 'Unknown')}

ANTAGONIST: {antagonist['name']} from {antagonist['location']}
- Role: The opposing force
- Arendtian Mode: {antagonist.get('arendtian_mode', 'Unknown')}

SCENARIO: {scenario}
STAKES: {stakes_level} - {stakes_descriptions.get(stakes_level, 'Significant')}

Create a 8-turn dramatic confrontation with:
1. Rising tension
2. Revelation of stakes
3. Emotional peak
4. Resolution attempt

Make it theatrical and emotionally charged while staying true to their spectral nature.

Format as alternating dialogue with stage directions in [brackets].
"""
            
            if self.openai_client:
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Create intense, theatrical confrontations with high emotional stakes and dramatic tension."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=1.1,
                    max_tokens=1200
                ).choices[0].message.content
                
                # Display the dramatic confrontation
                st.subheader("🎭 Dramatic Confrontation")
                
                # Parse and display with dramatic styling
                lines = response.split('\n')
                for line in lines:
                    if ':' in line:
                        speaker, dialogue = line.split(':', 1)
                        speaker = speaker.strip()
                        dialogue = dialogue.strip()
                        
                        # Determine speaker styling
                        if speaker == protagonist['name']:
                            speaker_icon = "🦸"
                            speaker_type = 'dramatic_confrontation'
                        elif speaker == antagonist['name']:
                            speaker_icon = "🦹"
                            speaker_type = 'dramatic_confrontation'
                        else:
                            speaker_icon = "🎭"
                            speaker_type = 'dramatic_confrontation'
                        
                        # Add to dialogue history
                        self.add_to_dialogue(speaker, dialogue, speaker_type)
                        
                        # Display with dramatic styling
                        st.markdown(f"**{speaker_icon} {speaker}:**")
                        st.markdown(f"*{dialogue}*")
                        st.markdown("---")
                    elif line.strip().startswith('[') and line.strip().endswith(']'):
                        # Stage directions
                        st.markdown(f"*{line.strip()}*")
                
                # Show confrontation details
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("**🎭 Scenario:**")
                    st.info(scenario)
                    
                with col2:
                    st.markdown("**⚡ Stakes:**")
                    st.warning(f"{stakes_level} Stakes")
                    
                with col3:
                    st.markdown("**🎪 Performance:**")
                    st.success("Dramatic Confrontation")
                
                st.success("✅ Dramatic confrontation completed!")
                
            else:
                st.error("OpenAI client not available")
                
        except Exception as e:
            st.error(f"❌ Error generating dramatic confrontation: {e}")
    
    def scene_composition_interface(self):
        """Stage 3: Dialogue Scene Composition Interface"""
        st.header("🎭 Scene Composer - Conflicting Spectral Dialogues")
        st.markdown("*Create theatrical scenes with specific dialogue logic patterns*")
        
        if not st.session_state.active_personas:
            st.warning("No personas available. Please generate personas first.")
            return
        
        # Filter for personas that can participate in scenes (spectral multiplicity + conspiracy actors)
        scene_personas = [p for p in st.session_state.active_personas if p.get('type') in ['spectral_multiplicity', 'non_human_actor']]
        
        if len(scene_personas) < 2:
            st.warning("Need at least 2 personas (spectral multiplicity or conspiracy actors) for scene composition.")
            return
        
        # Separate the types for display
        spectral_personas = [p for p in scene_personas if p.get('type') == 'spectral_multiplicity']
        conspiracy_personas = [p for p in scene_personas if p.get('type') == 'non_human_actor']
        
        st.info(f"Available for scenes: {len(spectral_personas)} spectral beings + {len(conspiracy_personas)} conspiracy actors = {len(scene_personas)} total")
        
        # Step 1: Conflict Detection
        st.subheader("🔍 Step 1: Detect Conflicting Personas")
        
        if st.button("🔍 Analyze Conflicts", type="primary"):
            try:
                # Convert to GeneratedPersona format for conflict detection
                from core.personas.spectral_multiplicity_notebook import GeneratedPersona
                
                generated_personas = []
                for persona in scene_personas:
                    # Handle both spectral multiplicity and conspiracy actors
                    if persona.get('type') == 'non_human_actor':
                        # Convert conspiracy actor to GeneratedPersona format
                        generated_persona = GeneratedPersona(
                            name=persona['name'],
                            location=persona.get('location', 'unknown'),
                            voice=persona.get('manifestation_quote', ''),
                            mood=persona.get('threat_level', 'Absolutely Convinced'),
                            civic_conflict=persona.get('agenda', ''),
                            arendtian_mode='Anti-Consensus',
                            dominant_indices=persona.get('conspiracy_evidence', {}),
                            dialogue_potential='Refuses all rational discussion',
                        )
                    else:
                        # Handle spectral multiplicity personas
                        generated_persona = GeneratedPersona(
                            name=persona['name'],
                            location=persona['location'],
                            voice=persona.get('voice', ''),
                            mood=persona.get('mood', ''),
                            civic_conflict=persona.get('civic_position', ''),
                            arendtian_mode=persona.get('arendtian_mode', ''),
                            dominant_indices=persona.get('dominant_indices', {}),
                            dialogue_potential=persona.get('democratic_tension', ''),
                            temporal_status=persona.get('temporal_status', ''),
                            district_soul=persona.get('district_soul', persona.get('role', '')),
                            street_wisdom=persona.get('street_wisdom', persona.get('perspective', '')),
                            urban_humor=persona.get('urban_humor', 'Witty observations'),
                            arendtian_insight=persona.get('arendtian_insight', ''),
                            city_memory=persona.get('city_memory', ''),
                            spectral_nickname=persona.get('spectral_nickname', f"Avatar of {persona['location']}")
                        )
                    generated_personas.append(generated_persona)
                
                # Detect conflicts
                conflicts = self.spectral_pipeline.dialogue_system.detect_conflicting_personas(generated_personas)
                
                if conflicts:
                    st.success(f"🔍 Found {len(conflicts)} potential conflicts!")
                    
                    # Display conflicts with detailed explanations
                    for i, conflict in enumerate(conflicts[:5]):  # Show top 5 conflicts
                        # Create clear conflict explanation
                        conflict_explanation = self.explain_conflict_in_detail(conflict)
                        
                        with st.expander(f"⚔️ Conflict {i+1}: {conflict['persona1'].name} vs {conflict['persona2'].name} (Score: {conflict['conflict_score']}) - {conflict_explanation['title']}"):
                            # Show the main conflict explanation
                            st.markdown(f"### 🎭 **What This Conflict Is About:**")
                            st.info(conflict_explanation['main_explanation'])
                            
                            # Show why it's dramatic
                            st.markdown(f"### ⚡ **Why This Creates Drama:**")
                            st.warning(conflict_explanation['dramatic_potential'])
                            
                            # Character details
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown(f"**🌈 {conflict['persona1'].name}**")
                                st.write(f"**Location:** {conflict['persona1'].location}")
                                st.write(f"**Mode:** {conflict['persona1'].arendtian_mode}")
                                st.write(f"**Character:** {conflict_explanation['persona1_description']}")
                                
                                # Show spectral data explanation
                                indices1 = conflict['persona1'].dominant_indices
                                ndvi1 = indices1.get('NDVI', 0)
                                if ndvi1 > 0.5:
                                    st.success(f"🌱 High vegetation area (NDVI: {ndvi1:.3f}) - Green, natural space")
                                elif ndvi1 > 0.2:
                                    st.info(f"🌿 Moderate vegetation (NDVI: {ndvi1:.3f}) - Mixed green/urban")
                                else:
                                    st.error(f"🏗️ Low/no vegetation (NDVI: {ndvi1:.3f}) - Urban/concrete area")
                            
                            with col2:
                                st.markdown(f"**🌟 {conflict['persona2'].name}**")
                                st.write(f"**Location:** {conflict['persona2'].location}")
                                st.write(f"**Mode:** {conflict['persona2'].arendtian_mode}")
                                st.write(f"**Character:** {conflict_explanation['persona2_description']}")
                                
                                # Show spectral data explanation
                                indices2 = conflict['persona2'].dominant_indices
                                ndvi2 = indices2.get('NDVI', 0)
                                if ndvi2 > 0.5:
                                    st.success(f"🌱 High vegetation area (NDVI: {ndvi2:.3f}) - Green, natural space")
                                elif ndvi2 > 0.2:
                                    st.info(f"🌿 Moderate vegetation (NDVI: {ndvi2:.3f}) - Mixed green/urban")
                                else:
                                    st.error(f"🏗️ Low/no vegetation (NDVI: {ndvi2:.3f}) - Urban/concrete area")
                            
                            # Detailed conflict breakdown
                            st.markdown("### 📊 **Conflict Details:**")
                            
                            # Spectral conflict explanation
                            if 'spectral_band' in conflict['conflict_types']:
                                st.markdown("**🌈 Spectral Data Conflict:**")
                                st.write(conflict_explanation['spectral_explanation'])
                            
                            # Arendtian mode conflict explanation
                            if conflict['persona1'].arendtian_mode != conflict['persona2'].arendtian_mode:
                                st.markdown("**🏛️ Philosophical Approach Conflict:**")
                                st.write(conflict_explanation['arendtian_explanation'])
                            
                            # Zone conflict explanation
                            if 'zone_conflict' in conflict['conflict_types']:
                                st.markdown("**🗺️ Location-Based Conflict:**")
                                st.write(conflict_explanation['zone_explanation'])
                            
                            # Example dialogue preview
                            st.markdown("### 💬 **Example Conflict Dialogue:**")
                            st.markdown(f"**{conflict['persona1'].name}:** *{conflict_explanation['example_dialogue_1']}*")
                            st.markdown(f"**{conflict['persona2'].name}:** *{conflict_explanation['example_dialogue_2']}*")
                    
                    # Store conflicts in session state
                    st.session_state.detected_conflicts = conflicts
                else:
                    st.info("No significant conflicts detected. Try generating more diverse personas.")
                    
            except Exception as e:
                st.error(f"❌ Error detecting conflicts: {e}")
        
        # Step 2: Scene Generation
        st.markdown("---")
        st.subheader("🎬 Step 2: Generate Scene Composition")
        
        # Persona selection
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Select First Persona:**")
            persona1_index = st.selectbox(
                "First Persona",
                range(len(scene_personas)),
                format_func=lambda x: f"{scene_personas[x]['name']} ({scene_personas[x].get('location', 'unknown')})",
                key="scene_persona1"
            )
        
        with col2:
            st.markdown("**Select Second Persona:**")
            persona2_options = [i for i in range(len(scene_personas)) if i != persona1_index]
            if persona2_options:
                persona2_index = st.selectbox(
                    "Second Persona",
                    persona2_options,
                    format_func=lambda x: f"{scene_personas[x]['name']} ({scene_personas[x].get('location', 'unknown')})",
                    key="scene_persona2"
                )
            else:
                persona2_index = None
        
        # Enhanced dialogue logic selection with detailed explanations
        st.markdown("### 🎭 Choose Your Dialogue Logic Pattern")
        st.markdown("*Each pattern creates a different type of theatrical conflict and conversation style*")
        
        # Add helpful usage guide
        with st.expander("📖 How to Use Dialogue Logic Patterns - Click for Guide"):
            st.markdown("""
            **🎭 What are Dialogue Logic Patterns?**
            
            These are special theatrical frameworks that shape how your spectral personas interact. Each pattern creates a unique type of conflict and conversation style, making your scenes more engaging and dramatically interesting.
            
            **🎪 How to Choose:**
            1. **Read the descriptions** below to understand each pattern
            2. **Consider your personas** - what kind of conflict would be most interesting between them?
            3. **Think about the mood** you want - comedy, drama, absurdity, or philosophical depth?
            4. **Click "Use [Pattern Name]"** to select your preferred pattern
            5. **Generate your scene** and watch the magic happen!
            
            **🌟 Pro Tips:**
            - **Temporal Misalignment** works great with personas from different districts (old vs new areas)
            - **Spectral Possession** creates intense, data-driven arguments
            - **Human Ritual Misinterpretation** is perfect for comedy and absurd observations
            - **Bureaucratic Parody** generates hilarious administrative conflicts
            - **Role Clash** creates serious ethical dilemmas and moral conflicts
            - **Absurd Policy Proposals** leads to escalating comedic policy debates
            
            **🎬 What Happens Next:**
            Once you select a pattern, the AI will generate a complete theatrical scene with:
            - Character-specific dialogue that follows the pattern
            - Conflict escalation and resolution
            - Spectral data references and explanations
            - Prague-specific cultural context
            - Absurd policy proposals or bureaucratic elements
            """)
        
        dialogue_logics = {
            "temporal_misalignment": {
                "name": "⏰ Temporal Misalignment",
                "description": "Personas exist in different time scales - one thinks in seasons, another in centuries",
                "example": "A tree-spirit persona speaks of 'recent' changes from 50 years ago, while an urban persona focuses on this week's construction",
                "conflict_style": "Past vs Present vs Future perspectives clash"
            },
            "spectral_possession": {
                "name": "👻 Spectral Possession", 
                "description": "Personas are 'possessed' by their spectral data - they become obsessed with their indices",
                "example": "An NDVI persona can only speak in vegetation terms, while a thermal persona sees everything as heat signatures",
                "conflict_style": "Single-minded data obsession creates tunnel vision conflicts"
            },
            "human_ritual_misinterpretation": {
                "name": "🤔 Human Ritual Misinterpretation",
                "description": "Spectral beings misunderstand human activities and create absurd explanations",
                "example": "They think traffic jams are 'thermal meditation rituals' and cafes are 'moisture redistribution centers'",
                "conflict_style": "Competing bizarre theories about human behavior"
            },
            "role_clash": {
                "name": "⚔️ Role Clash",
                "description": "Personas have conflicting civic roles that create institutional tension",
                "example": "Environmental Guardian vs Development Advocate vs Tourism Promoter - each has valid but opposing goals",
                "conflict_style": "Institutional responsibilities create ethical dilemmas"
            },
            "bureaucratic_parody": {
                "name": "📋 Bureaucratic Parody",
                "description": "Personas get trapped in absurd administrative procedures and red tape",
                "example": "They need permits to change their spectral signatures or file complaints about cloud interference",
                "conflict_style": "Kafka-esque administrative absurdity and procedural comedy"
            },
            "absurd_policy_proposals": {
                "name": "🏛️ Absurd Policy Proposals",
                "description": "Personas propose increasingly ridiculous civic policies based on their data",
                "example": "Mandatory photosynthesis breaks, thermal signature dress codes, or NDVI-based voting rights",
                "conflict_style": "Escalating policy absurdity as each persona tries to top the others"
            }
        }
        
        # Display logic patterns with detailed info
        selected_logic_key = None
        
        for key, logic_info in dialogue_logics.items():
            with st.expander(f"{logic_info['name']} - Click to learn more"):
                st.markdown(f"**Description:** {logic_info['description']}")
                st.markdown(f"**Example:** *{logic_info['example']}*")
                st.markdown(f"**Conflict Style:** {logic_info['conflict_style']}")
                
                if st.button(f"✅ Use {logic_info['name']}", key=f"select_{key}"):
                    selected_logic_key = key
                    st.session_state.selected_dialogue_logic = key
                    st.success(f"Selected: {logic_info['name']}")
                    st.rerun()
        
        # Show current selection
        if 'selected_dialogue_logic' in st.session_state:
            selected_logic_key = st.session_state.selected_dialogue_logic
            selected_info = dialogue_logics[selected_logic_key]
            st.info(f"🎭 **Current Selection:** {selected_info['name']}")
            st.markdown(f"*{selected_info['description']}*")
        else:
            st.warning("👆 Please select a dialogue logic pattern above to continue")
        
        # Scene title
        if persona1_index is not None and len(scene_personas) > 0:
            default_location = scene_personas[persona1_index].get('location', 'Unknown Location')
            default_title = f"The {default_location.replace('_', ' ').title()} Confrontation"
        else:
            default_title = "Spectral Theater Scene"
            
        scene_title = st.text_input(
            "🎬 Scene Title:",
            value=default_title,
            help="Title for the theatrical scene"
        )
        
        # Generate scene button
        if st.button("🎭 Generate Scene Composition", type="primary"):
            if scene_title and persona1_index is not None and persona2_index is not None and 'selected_dialogue_logic' in st.session_state:
                try:
                    persona1 = scene_personas[persona1_index]
                    persona2 = scene_personas[persona2_index]
                    selected_logic = st.session_state.selected_dialogue_logic
                    
                    st.info(f"🎬 Generating scene: **{scene_title}** with {selected_logic.replace('_', ' ')} logic...")
                    
                    # Convert to GeneratedPersona format
                    from core.personas.spectral_multiplicity_notebook import GeneratedPersona
                    
                    generated_persona1 = GeneratedPersona(
                        name=persona1['name'],
                        location=persona1['location'],
                        voice=persona1.get('voice', ''),
                        mood=persona1.get('mood', ''),
                        civic_conflict=persona1.get('civic_position', ''),
                        arendtian_mode=persona1.get('arendtian_mode', ''),
                        dominant_indices=persona1.get('dominant_indices', {}),
                        dialogue_potential=persona1.get('democratic_tension', ''),
                        temporal_status=persona1.get('temporal_status', ''),
                        district_soul=persona1.get('district_soul', persona1.get('role', '')),
                        street_wisdom=persona1.get('street_wisdom', persona1.get('perspective', '')),
                        urban_humor=persona1.get('urban_humor', 'Witty observations'),
                        arendtian_insight=persona1.get('arendtian_insight', ''),
                        city_memory=persona1.get('city_memory', ''),
                        spectral_nickname=persona1.get('spectral_nickname', f"Avatar of {persona1['location']}")
                    )
                    
                    generated_persona2 = GeneratedPersona(
                        name=persona2['name'],
                        location=persona2['location'],
                        voice=persona2.get('voice', ''),
                        mood=persona2.get('mood', ''),
                        civic_conflict=persona2.get('civic_position', ''),
                        arendtian_mode=persona2.get('arendtian_mode', ''),
                        dominant_indices=persona2.get('dominant_indices', {}),
                        dialogue_potential=persona2.get('democratic_tension', ''),
                        temporal_status=persona2.get('temporal_status', ''),
                        district_soul=persona2.get('district_soul', persona2.get('role', '')),
                        street_wisdom=persona2.get('street_wisdom', persona2.get('perspective', '')),
                        urban_humor=persona2.get('urban_humor', 'Witty observations'),
                        arendtian_insight=persona2.get('arendtian_insight', ''),
                        city_memory=persona2.get('city_memory', ''),
                        spectral_nickname=persona2.get('spectral_nickname', f"Avatar of {persona2['location']}")
                    )
                    
                    # Generate scene composition
                    scene_result = self.spectral_pipeline.dialogue_system.generate_scene_composition(
                        generated_persona1, generated_persona2, selected_logic, scene_title
                    )
                    
                    # Display the scene
                    self.display_scene_composition(scene_result)
                    
                except Exception as e:
                    st.error(f"❌ Error generating scene: {e}")
            else:
                st.warning("Please provide a scene title and ensure personas are selected.")
        
        # Note: Scene library functionality removed for stability
    
    def explain_conflict_in_detail(self, conflict):
        """Create detailed, user-friendly explanation of what the conflict means"""
        persona1 = conflict['persona1']
        persona2 = conflict['persona2']
        
        # Get spectral data
        indices1 = persona1.dominant_indices
        indices2 = persona2.dominant_indices
        ndvi1 = indices1.get('NDVI', 0)
        ndvi2 = indices2.get('NDVI', 0)
        
        # Determine main conflict type and create explanation
        explanation = {
            'title': '',
            'main_explanation': '',
            'dramatic_potential': '',
            'persona1_description': '',
            'persona2_description': '',
            'spectral_explanation': '',
            'arendtian_explanation': '',
            'zone_explanation': '',
            'example_dialogue_1': '',
            'example_dialogue_2': ''
        }
        
        # Special case: Shadow District conflicts
        if persona1.location == 'shadow_district' or persona2.location == 'shadow_district':
            shadow_persona = persona1 if persona1.location == 'shadow_district' else persona2
            other_persona = persona2 if persona1.location == 'shadow_district' else persona1
            
            explanation['title'] = "Shadow District Confrontation"
            explanation['main_explanation'] = f"The Shadow District ({shadow_persona.name}) represents Prague's dark side - all the problems, contradictions, and guilt that other districts don't want to acknowledge. This creates a confrontation where {other_persona.name} from {other_persona.location} must face uncomfortable truths about Prague's development."
            explanation['dramatic_potential'] = f"The Shadow District will blame {other_persona.location} for contributing to Prague's problems, while {other_persona.name} will try to defend their area. This creates intense drama as hidden contradictions are exposed."
            explanation['persona1_description'] = "Perpetual scapegoat that absorbs Prague's collective guilt" if persona1.location == 'shadow_district' else f"Representative of {persona1.location}'s interests and character"
            explanation['persona2_description'] = "Perpetual scapegoat that absorbs Prague's collective guilt" if persona2.location == 'shadow_district' else f"Representative of {persona2.location}'s interests and character"
            explanation['zone_explanation'] = f"Shadow District (all of Prague's problems) vs {other_persona.location} (specific area trying to maintain its identity)"
            explanation['example_dialogue_1'] = f"You in {other_persona.location} pretend to be so perfect, but I absorb all the guilt from your tourist crowds and gentrification!"
            explanation['example_dialogue_2'] = f"That's not fair! {other_persona.location} contributes to Prague's culture and economy. We're not responsible for every problem!"
        
        # Green vs Urban conflict
        elif abs(ndvi1 - ndvi2) > 0.3:
            if ndvi1 > ndvi2:
                green_persona = persona1
                urban_persona = persona2
            else:
                green_persona = persona2
                urban_persona = persona1
            
            explanation['title'] = "Green Space vs Urban Development"
            explanation['main_explanation'] = f"This is a classic environmental conflict: {green_persona.name} represents a green, natural area (NDVI: {green_persona.dominant_indices.get('NDVI', 0):.3f}) while {urban_persona.name} represents urban development (NDVI: {urban_persona.dominant_indices.get('NDVI', 0):.3f}). They have fundamentally different views on how Prague should develop."
            explanation['dramatic_potential'] = f"{green_persona.name} will argue for environmental protection and green spaces, while {urban_persona.name} will advocate for development, housing, and economic growth. Both have valid points, creating real tension."
            explanation['persona1_description'] = "Green space advocate" if persona1 == green_persona else "Urban development supporter"
            explanation['persona2_description'] = "Green space advocate" if persona2 == green_persona else "Urban development supporter"
            explanation['spectral_explanation'] = f"NDVI difference of {abs(ndvi1 - ndvi2):.3f} shows one area is much greener than the other, creating natural vs urban tension"
            explanation['example_dialogue_1'] = f"My NDVI of {green_persona.dominant_indices.get('NDVI', 0):.3f} shows healthy vegetation that Prague desperately needs for air quality and climate!"
            explanation['example_dialogue_2'] = f"But we need development! My area shows Prague's economic vitality and provides housing for people who actually live here!"
        
        # Arendtian mode conflict
        elif persona1.arendtian_mode != persona2.arendtian_mode:
            mode1 = persona1.arendtian_mode
            mode2 = persona2.arendtian_mode
            
            mode_explanations = {
                'Action': 'believes in immediate, spontaneous civic engagement and political action',
                'Thinking': 'prefers careful contemplation and philosophical reflection before acting',
                'Work': 'focuses on building lasting institutions and creating durable civic structures',
                'Labor': 'concerned with basic survival needs and maintaining existing systems',
                'Judging': 'evaluates past actions and makes moral assessments',
                'Willing': 'projects future possibilities and intentions',
                'Vita Contemplativa': 'withdrawn from active civic life, focused on inner reflection',
                'Vita Passiva': 'passive, disengaged from civic participation'
            }
            
            explanation['title'] = f"{mode1} vs {mode2} Philosophy"
            explanation['main_explanation'] = f"This is a philosophical conflict about how to approach civic life. {persona1.name} ({mode1}) {mode_explanations.get(mode1, 'has a specific approach')}, while {persona2.name} ({mode2}) {mode_explanations.get(mode2, 'has a different approach')}."
            explanation['dramatic_potential'] = f"They'll clash over whether Prague needs {mode1.lower()} or {mode2.lower()} approaches to solve its problems. This creates fundamental disagreement about civic engagement."
            explanation['persona1_description'] = f"{mode1} approach to civic life"
            explanation['persona2_description'] = f"{mode2} approach to civic life"
            explanation['arendtian_explanation'] = f"{mode1} vs {mode2} represents different ways of being a citizen and engaging with Prague's civic life"
            explanation['example_dialogue_1'] = f"Prague needs {mode1.lower()}! We must engage actively with our civic responsibilities!"
            explanation['example_dialogue_2'] = f"No, {mode2.lower()} is what Prague needs. Your approach is too {mode1.lower()} and misses the deeper issues!"
        
        # Location-based conflict
        else:
            explanation['title'] = f"{persona1.location} vs {persona2.location} Rivalry"
            explanation['main_explanation'] = f"This is a territorial conflict between different areas of Prague. {persona1.name} represents {persona1.location} while {persona2.name} represents {persona2.location}. Each area has its own character, problems, and priorities."
            explanation['dramatic_potential'] = f"They'll argue about which area is more important to Prague, compete for resources and attention, and defend their neighborhood's unique character."
            explanation['persona1_description'] = f"Defender of {persona1.location}'s interests and identity"
            explanation['persona2_description'] = f"Defender of {persona2.location}'s interests and identity"
            explanation['zone_explanation'] = f"Different Prague neighborhoods with different characters, needs, and perspectives on the city's future"
            explanation['example_dialogue_1'] = f"{persona1.location} is the real heart of Prague! We understand what this city truly needs!"
            explanation['example_dialogue_2'] = f"That's ridiculous! {persona2.location} has much more to offer Prague than your area ever could!"
        
        return explanation

    def display_scene_composition(self, scene_result):
        """Display the generated scene composition"""
        st.markdown("---")
        st.subheader("🎭 Generated Scene Composition")
        
        # Scene header
        st.markdown(f"## 🎬 {scene_result.get('scene_title', 'Untitled Scene')}")
        st.markdown(f"**Conflict Type:** {scene_result.get('conflict_type', 'Unknown').replace('_', ' ').title()}")
        
        # Personas
        st.subheader("🎭 Cast")
        personas = scene_result.get('personas', [])
        
        for persona in personas:
            with st.expander(f"🌈 {persona.get('name', 'Unknown')} - {persona.get('role', 'Unknown')}"):
                st.write(f"**Zone:** {persona.get('zone', 'Unknown')}")
                st.write(f"**Role:** {persona.get('role', 'Unknown')}")
                st.write(f"**Mood:** {persona.get('mood', 'Unknown')}")
                st.write(f"**Temporal Scale:** {persona.get('temporal_scale', 'Unknown')}")
                st.write(f"**Spectral Signature:** {persona.get('spectral_signature', 'Unknown')}")
                st.write(f"**Quote:** *{persona.get('quote', 'No quote available')}*")
        
        # Dialogue
        st.subheader("🗣️ Dialogue")
        dialogue = scene_result.get('dialogue', [])
        
        for line in dialogue:
            if ':' in line:
                speaker, text = line.split(':', 1)
                speaker = speaker.strip()
                text = text.strip()
                
                # Style based on speaker
                if any(p.get('name', '') in speaker for p in personas):
                    st.markdown(f"**🌈 {speaker}:** *{text}*")
                else:
                    st.markdown(f"**🎭 {speaker}:** *{text}*")
            else:
                st.markdown(f"*{line}*")
        
        # Scene elements
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🏛️ Bureaucratic Elements")
            st.info(scene_result.get('bureaucratic_elements', 'No bureaucratic elements specified'))
        
        with col2:
            st.subheader("🤔 Human Misinterpretation")
            st.warning(scene_result.get('human_misinterpretation', 'No human misinterpretation specified'))
        
        # Policy proposal
        st.subheader("📜 Absurd Policy Proposal")
        proposal = scene_result.get('proposal', 'No proposal generated')
        st.success(f"💡 **Proposal:** {proposal}")
        
        # Metadata
        if scene_result.get('generation_metadata'):
            with st.expander("🔧 Generation Metadata"):
                st.json(scene_result['generation_metadata'])
        
        # Add dialogue to theater history (simplified)
        st.markdown("### 📜 Add to Theater History")
        st.info("💡 **What this does:** Adds the scene's dialogue to your theater's conversation history, so you can see it alongside other persona conversations in the dialogue history section.")
        
        if st.button("📜 Add Scene Dialogue to Theater History", type="primary"):
            scene_title = scene_result.get('scene_title', 'Scene')
            dialogue = scene_result.get('dialogue', [])
            
            # Add scene header to dialogue
            self.add_to_dialogue("Scene Composer", f"🎭 **{scene_title}** - {scene_result.get('conflict_type', 'conflict').replace('_', ' ').title()}", "scene")
            
            # Add each dialogue line
            for line in dialogue:
                if ':' in line:
                    speaker, text = line.split(':', 1)
                    self.add_to_dialogue(speaker.strip(), text.strip(), "scene_dialogue")
            
            # Add proposal
            self.add_to_dialogue("Policy Proposal", scene_result.get('proposal', 'No proposal'), "scene_proposal")
            
            st.success("✅ Scene added to theater dialogue history!")
    
    def run(self):
        """Main application flow"""
        st.set_page_config(
            page_title="Civic Theater Stage",
            page_icon="🎭",
            layout="wide"
        )
        
        self.display_stage_header()
        
        # Sidebar for quick access
        st.sidebar.header("🎭 Theater Control")
        
        # Quick access to persona library
        if st.sidebar.button("📚 Access Persona Library"):
            st.session_state.show_library_only = True
            st.rerun()
        
        # Show library-only mode
        if st.session_state.get('show_library_only', False):
            if st.sidebar.button("🎭 Back to Theater"):
                st.session_state.show_library_only = False
                st.rerun()
            
            self.persona_library_interface()
            return
        
        # Main theater flow
        if not st.session_state.selected_image:
            # Stage 1: Image selection
            self.image_selection_stage()
            
        elif not st.session_state.stage_set:
            # Stage 2: Show spectral data first, then offer analysis
            st.header("🌈 Spectral Multiplicity Stage - Data Analysis")
            st.image(st.session_state.selected_image, caption="Selected Image", width=400)
            
            # First show all available spectral data and explanations
            self.display_spectral_data_explanation()
            
            # Then offer the analysis and summon beings function
            st.markdown("---")
            st.header("🎭 Generate Spectral Beings")
            st.info("🌈 **Ready to Generate!** Choose your theatrical approach - data-driven analysis or wound-driven argument machines.")
            
            # Generation mode selection
            st.subheader("🎪 Choose Your Theatrical Engine")
            
            generation_mode = st.radio(
                "Select Generation Mode:",
                [
                    "🌈 Spectral Multiplicity (Educational Data Theater)",
                    "🕵️ Conspiracy Theater (Non-Human Actor Surprises)",
                    "⚔️ Parallel Generation (Both Systems)"
                ],
                help="Choose between scientific data explanation, conspiracy actor surprises, or both simultaneously"
            )
            
            # Mode explanations
            if generation_mode == "🌈 Spectral Multiplicity (Educational Data Theater)":
                st.info("""
                **🌈 Spectral Multiplicity Mode:**
                - Personas explain their spectral data scientifically
                - Focus on NDVI, Urban Index, moisture stress measurements
                - Educational and informative dialogue
                - Grounded in satellite remote sensing
                """)
            elif generation_mode == "🕵️ Conspiracy Theater (Non-Human Actor Surprises)":
                st.warning("""
                **🕵️ Conspiracy Theater Mode:**
                - Satellite data reveals hidden non-human agendas
                - Unexpected actors emerge as surprises from data analysis
                - Concrete Consciousness, Tree Collectives, Water Conspiracies, Satellite Agency
                - Actors refuse rational discussion and make impossible demands
                - Anti-Habermasian conflict escalation with funny/extreme interpretations
                - Culminates in meta-theatrical breakdown
                """)
            else:
                st.success("""
                **⚔️ Parallel Generation Mode:**
                - Creates BOTH educational AND conspiracy theater actors
                - Scientific data-driven beings interact with conspiracy actors
                - Maximum theatrical tension and variety
                - Both educational and anti-consensus dialogues
                - Perfect for complex multi-layered performances
                """)
            
            # Add persona count control
            col1, col2 = st.columns([2, 1])
            
            with col1:
                max_personas = st.slider(
                    "🎭 Number of Personas to Generate:",
                    min_value=2,
                    max_value=10,
                    value=5,
                    help="Choose how many spectral personas to generate from the satellite data"
                )
            
            with col2:
                st.metric("Selected Count", max_personas)
                st.caption("Includes Shadow District")
            
            # Generate button based on mode
            if generation_mode == "🌈 Spectral Multiplicity (Educational Data Theater)":
                if st.button("🌈 Analyze Image & Summon Spectral Multiplicity Beings", type="primary"):
                    if self.analyze_selected_image_with_count(st.session_state.selected_image, max_personas, mode="spectral_multiplicity"):
                        # Configure dual staging system for scientific data theater
                        self.dual_staging_system.set_staging_mode("scientific_data", st.session_state.active_personas, self.api_key)
                        st.success("Spectral stage set! Multiplicity beings are ready for dialogue.")
                        st.rerun()
            elif generation_mode == "🕵️ Conspiracy Theater (Non-Human Actor Surprises)":
                if st.button("🔍 Scan for Hidden Non-Human Activity", type="primary"):
                    # Generate conspiracy actors with surprise revelations
                    conspiracy_actors = self.generate_conspiracy_actors_from_image(st.session_state.selected_image, max_personas)
                    if conspiracy_actors:
                        st.session_state.active_personas = conspiracy_actors
                        st.session_state.stage_set = True
                        # Configure dual staging system for conspiracy theater
                        self.dual_staging_system.set_staging_mode("conspiracy_theater", st.session_state.active_personas, self.api_key)
                        st.success("Conspiracy theater stage set! Non-human actors are ready for impossible conflicts.")
                        st.rerun()
            else:  # Parallel Generation Mode
                if st.button("⚔️ Generate Parallel Dual System Theater", type="primary"):
                    if self.analyze_parallel_dual_system(st.session_state.selected_image, max_personas):
                        # Configure dual staging system for parallel mode
                        self.dual_staging_system.set_staging_mode("parallel_dual", st.session_state.active_personas, self.api_key)
                        st.success("Parallel dual system theater set! Both scientific and conspiracy actors ready for complex interactions.")
                        st.rerun()
            
            if st.button("🔄 Choose Different Image"):
                st.session_state.selected_image = None
                st.rerun()
                
        else:
            # Stage 3: Main theater interface
            
            # Sidebar controls
            if st.sidebar.button("🔄 Reset Stage"):
                st.session_state.stage_set = False
                st.session_state.active_personas = []
                st.session_state.dialogue_history = []
                st.session_state.speaking_queue = []
                st.rerun()
            
            if st.sidebar.button("🖼️ Change Image"):
                st.session_state.selected_image = None
                st.session_state.stage_set = False
                st.rerun()
            
            # Main theater interface with clearer performance structure
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎭 Cast & Rehearsal", "🎪 Performance Stage", "🎬 Scripted Scenes", "🎯 Director's Control", "📚 Archive"])
            
            with tab1:
                # Cast management and quick rehearsals
                self.cast_and_rehearsal_interface()
            
            with tab2:
                # Live improvised performances
                self.live_performance_stage()
            
            with tab3:
                # Pre-composed theatrical scenes with specific conflict patterns
                self.scripted_scenes_interface()
            
            with tab4:
                # Director's control panel
                self.directors_control_panel()
            
            with tab5:
                # Persona library and archives
                self.persona_library_interface()

def main():
    theater = CivicTheaterStage()
    theater.run()

if __name__ == "__main__":
    main()
