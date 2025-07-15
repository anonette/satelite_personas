#!/usr/bin/env python3
"""
Regenerate Parallel Personas - Ensures Both Systems Work
Creates both Spectral Multiplicity AND Spectral Wound Theater personas
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import logging

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Generate both types of personas to ensure parallel staging works"""
    
    print("🔥 PARALLEL PERSONA GENERATION SYSTEM")
    print("=" * 50)
    print("This script ensures you get BOTH types of personas:")
    print("🌈 Spectral Multiplicity (Scientific Data)")
    print("🔥 Spectral Wound Theater (Argument Machines)")
    print("=" * 50)
    
    try:
        # Import required modules
        from core.config import get_config
        from core.satellite.image_spectral_processor import ImageSpectralExtractor
        from core.personas.spectral_multiplicity_notebook import SpectralMultiplicityPipeline
        from core.theater.dual_staging_system import DualStagingSystem
        
        # Get configuration
        config = get_config()
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ ERROR: OPENAI_API_KEY not found in environment")
            print("💡 SOLUTION: Create a .env file with your OpenAI API key")
            return False
        
        print(f"✅ API key found: {api_key[:10]}...")
        
        # Check for images
        images_dir = config.images_dir
        if not images_dir.exists():
            print(f"❌ ERROR: Images directory not found: {images_dir}")
            return False
        
        # Get available images
        image_files = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.tiff', '*.tif']:
            image_files.extend(images_dir.glob(ext))
        
        if not image_files:
            print(f"❌ ERROR: No satellite images found in {images_dir}")
            return False
        
        print(f"✅ Found {len(image_files)} satellite images")
        
        # Select first image for generation
        selected_image = image_files[0]
        print(f"🖼️ Using image: {selected_image.name}")
        
        # Initialize systems
        print("\n🔧 Initializing generation systems...")
        image_extractor = ImageSpectralExtractor(api_key)
        spectral_pipeline = SpectralMultiplicityPipeline(api_key)
        dual_staging = DualStagingSystem()
        
        # Generate spectral data for Prague zones
        print("\n🌈 STEP 1: Generating Spectral Multiplicity Personas")
        print("-" * 30)
        
        prague_zones = ["letna_park", "old_town", "petrin_hill", "vltava_river", "vinohrady"]
        spectral_data = []
        
        for zone in prague_zones[:3]:  # Generate 3 scientific personas
            print(f"📊 Extracting spectral data for {zone}...")
            try:
                zone_data = image_extractor.extract_spectral_data_for_zone(zone)
                if zone_data:
                    spectral_data.append({
                        'location': zone,
                        'lat': zone_data.coordinates[0],
                        'lon': zone_data.coordinates[1],
                        'date': zone_data.date,
                        'bands': {
                            'B1': zone_data.derived_indices.get('Blue_Index', 0.1),
                            'B2': zone_data.derived_indices.get('Green_Index', 0.1),
                            'B3': zone_data.derived_indices.get('Red_Index', 0.1),
                            'B4': zone_data.derived_indices.get('NIR_Index', 0.1),
                            'B5': zone_data.derived_indices.get('NDVI', 0.1),
                            'B8': zone_data.derived_indices.get('NDVI', 0.1) * 2,
                            'B8A': zone_data.derived_indices.get('NDVI', 0.1) * 1.8,
                            'B11': zone_data.derived_indices.get('NDWI', 0.1),
                            'B12': zone_data.derived_indices.get('SWIR_Index', 0.1)
                        }
                    })
                    print(f"✅ {zone} spectral data extracted")
                else:
                    print(f"⚠️ No data for {zone}")
            except Exception as e:
                print(f"❌ Error extracting {zone}: {e}")
        
        # Generate scientific personas
        scientific_personas = []
        if spectral_data:
            print(f"\n🔬 Generating {len(spectral_data)} scientific personas...")
            generated_personas = spectral_pipeline.process_prague_districts(spectral_data)
            
            for persona in generated_personas:
                scientific_persona = {
                    'name': persona.name,
                    'location': persona.location,
                    'role': f"Spectral Multiplicity Scientist of {persona.location}",
                    'type': 'spectral_multiplicity',
                    'arendtian_mode': persona.arendtian_mode,
                    'mood': persona.mood,
                    'civic_position': persona.civic_conflict,
                    'democratic_tension': persona.dialogue_potential,
                    'temporal_status': persona.temporal_status,
                    'voice': persona.voice,
                    'perspective': f"Scientific analysis: NDVI {persona.dominant_indices.get('NDVI', 0):.3f}",
                    'values': f"Scientific integrity and {persona.arendtian_mode} approach",
                    'dominant_indices': persona.dominant_indices,
                    'spectral_signature': persona.dominant_indices
                }
                scientific_personas.append(scientific_persona)
                print(f"🌈 Generated: {persona.name}")
        
        # Generate wound theater personas
        print(f"\n🔥 STEP 2: Generating Spectral Wound Theater Personas")
        print("-" * 30)
        
        wound_personas = []
        wound_zones = ["letna_park", "old_town", "vinohrady"]  # Generate 3 wound personas
        
        for zone in wound_zones:
            print(f"🩸 Creating wound persona for {zone}...")
            
            # Create wound-specific data
            wound_info = create_wound_persona_data(zone)
            wound_persona = create_wound_theater_persona(wound_info)
            wound_personas.append(wound_persona)
            print(f"🔥 Generated: {wound_persona['name']}")
        
        # Add Shadow District
        print(f"\n🌑 STEP 3: Adding Shadow District Scapegoat")
        print("-" * 30)
        
        shadow_wound = {
            'location': 'shadow_district',
            'spectral_wound': 'Ultimate Scapegoat Syndrome',
            'civic_trauma': 'Absorbs all of Prague\'s collective guilt and contradictions',
            'emotional_bias': 'Perpetual condemnation and righteous anger',
            'spectral_possession': 'Possessed by inverted spectral data - sees only dysfunction',
            'indices': {'NDVI': -0.8, 'Urban_Index': 0.95, 'Moisture_Stress': 0.9}
        }
        
        shadow_persona = create_wound_theater_persona(shadow_wound)
        wound_personas.append(shadow_persona)
        print(f"🌑 Generated: {shadow_persona['name']}")
        
        # Combine all personas
        all_personas = scientific_personas + wound_personas
        
        print(f"\n✅ PARALLEL GENERATION COMPLETE!")
        print("=" * 50)
        print(f"🌈 Scientific Personas: {len(scientific_personas)}")
        print(f"🔥 Wound Theater Personas: {len(wound_personas)}")
        print(f"🎭 Total Personas: {len(all_personas)}")
        print("=" * 50)
        
        # Save personas to file
        output_file = f"parallel_personas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        output_data = {
            'generation_timestamp': datetime.now().isoformat(),
            'generation_mode': 'parallel_dual_system',
            'source_image': str(selected_image),
            'scientific_personas': scientific_personas,
            'wound_personas': wound_personas,
            'all_personas': all_personas,
            'generation_stats': {
                'total_personas': len(all_personas),
                'scientific_count': len(scientific_personas),
                'wound_count': len(wound_personas)
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Personas saved to: {output_file}")
        
        # Display personas
        print(f"\n🌈 SCIENTIFIC PERSONAS:")
        for persona in scientific_personas:
            print(f"  • {persona['name']} - {persona['arendtian_mode']} - {persona['location']}")
        
        print(f"\n🔥 WOUND THEATER PERSONAS:")
        for persona in wound_personas:
            print(f"  • {persona['name']} - {persona.get('spectral_wound', 'Unknown wound')}")
        
        print(f"\n🎭 NEXT STEPS:")
        print("1. Launch the theater: ./launch.bat")
        print("2. Load these personas from the Archive tab")
        print("3. Use both scientific and wound theater features")
        print("4. Try cross-system conflicts in Performance Stage")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_wound_persona_data(zone):
    """Create wound-specific data for a zone"""
    
    wound_map = {
        'letna_park': {
            'spectral_wound': 'Green Fundamentalism - Anti-Human Bias',
            'civic_trauma': 'Betrayed by skateboarders and beer gardens - no longer pure nature',
            'emotional_bias': 'Euphoric green supremacy',
            'indices': {'NDVI': 0.8, 'Urban_Index': 0.1, 'Moisture_Stress': 0.2}
        },
        'old_town': {
            'spectral_wound': 'Urban Necrosis - Death of Green Life',
            'civic_trauma': 'Suffocated by tourist hordes - authentic Prague soul crushed',
            'emotional_bias': 'Bitter concrete resentment',
            'indices': {'NDVI': 0.1, 'Urban_Index': 0.9, 'Moisture_Stress': 0.3}
        },
        'vinohrady': {
            'spectral_wound': 'Concrete Fever - Artificial Heat Syndrome',
            'civic_trauma': 'Gentrification wound - bourgeois invasion destroying working-class identity',
            'emotional_bias': 'Desperate water anxiety',
            'indices': {'NDVI': 0.3, 'Urban_Index': 0.7, 'Moisture_Stress': 0.6}
        }
    }
    
    return {
        'location': zone,
        **wound_map.get(zone, {
            'spectral_wound': 'Spectral Confusion - Identity Crisis',
            'civic_trauma': 'Generic urban alienation and environmental grief',
            'emotional_bias': 'Fanatical data obsession',
            'indices': {'NDVI': 0.4, 'Urban_Index': 0.5, 'Moisture_Stress': 0.4}
        })
    }

def create_wound_theater_persona(wound_info):
    """Create a wound theater persona from wound data"""
    
    # Generate Prague-style name
    first_names = ['Blanka', 'Mirek', 'Zora', 'Pavel', 'Jana', 'Tomáš', 'Věra', 'Jakub']
    
    location_names = {
        'letna_park': 'Letná',
        'old_town': 'Celetná', 
        'vinohrady': 'Korunní',
        'shadow_district': 'Stínová'
    }
    
    wound_aliases = {
        'Urban Necrosis - Death of Green Life': 'NDVI Martyr',
        'Green Fundamentalism - Anti-Human Bias': 'Vegetation Zealot',
        'Concrete Fever - Artificial Heat Syndrome': 'UI Fanatic',
        'Spectral Confusion - Identity Crisis': 'Data Mystic',
        'Ultimate Scapegoat Syndrome': 'Shadow Confessor'
    }
    
    import random
    first_name = random.choice(first_names)
    location_name = location_names.get(wound_info['location'], wound_info['location'].title())
    spectral_alias = wound_aliases.get(wound_info['spectral_wound'], 'Wound Machine')
    
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
    
    return {
        'name': full_name,
        'location': wound_info['location'],
        'role': f"Spectral Wound Theater Machine of {wound_info['location']}",
        'type': 'spectral_wound_theater',
        'arendtian_mode': arendtian_mode,
        'mood': wound_info['emotional_bias'],
        'civic_position': wound_info['civic_trauma'],
        'democratic_tension': f"Argues from wound: {wound_info['spectral_wound']}",
        'temporal_status': 'Eternally wounded',
        'voice': generate_wound_voice(wound_info),
        'perspective': wound_info.get('spectral_possession', f"Possessed by {wound_info['spectral_wound']}"),
        'values': f"Spectral wound integrity and {wound_info['emotional_bias']}",
        'dominant_indices': wound_info['indices'],
        'spectral_signature': wound_info['indices'],
        'spectral_wound': wound_info['spectral_wound'],
        'civic_trauma': wound_info['civic_trauma'],
        'emotional_bias': wound_info['emotional_bias']
    }

def generate_wound_voice(wound_info):
    """Generate a voice sample for wound theater persona"""
    
    wound_voices = {
        'Urban Necrosis - Death of Green Life': "I am the NDVI fundamentalist. Everything that isn't green is the enemy. Your concrete kills my soul.",
        'Green Fundamentalism - Anti-Human Bias': "I am the vegetation zealot. Humans are the virus. Only plants deserve to live in Prague.",
        'Concrete Fever - Artificial Heat Syndrome': "I am the urban index cynic. Everything that looks like stone is a police agent. Development is surveillance.",
        'Spectral Confusion - Identity Crisis': "I am the data mystic. My indices contradict each other. I don't know what I am anymore.",
        'Ultimate Scapegoat Syndrome': "I am Prague's necessary scapegoat. I absorb all your guilt so you can sleep at night. Blame me for everything."
    }
    
    return wound_voices.get(wound_info['spectral_wound'], "I speak data because I've stopped trusting people. Build your own argument machine because humans hurt you.")

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 SUCCESS: Parallel persona generation complete!")
    else:
        print("\n💥 FAILED: Check the errors above")
