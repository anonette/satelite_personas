# 🌆 Dynamic Citizen Personas - Conflict-Driven Spectral Theater

**Alive, dramatic spectral citizens generated from real satellite data with automatic conflict generation**

## 🎭 What This Is

Dynamic Citizen Personas is an interactive AI theater system that transforms real satellite spectral data from Prague into dramatic, conflicting environmental activists. Each persona represents a different spectral band (B02, B03, B04, B08, B11, B12) and automatically generates conflicts with other active personas based on their competing environmental priorities.

## ✨ Key Features

### 🔥 **Automatic Conflict Generation**
- **New personas automatically challenge existing ones** when activated
- **Band-specific conflicts** based on real spectral data differences
- **Competing environmental priorities**: Air quality vs vegetation vs moisture vs thermal management
- **Spontaneous argument generation** with the "⚔️ Generate Conflict" button

### 🎪 **Spectral Theater System**
- **Real satellite data** from Prague transformed into personality traits
- **Dynamic persona generation** using TIFF spectral analysis
- **Multi-language support** (English/Czech) with ethical dative patterns
- **Voice synthesis** integration with ElevenLabs for audio responses

### 🌍 **Environmental Activism Simulation**
- **Prague-specific locations** targeted by personas (Wenceslas Square, Charles Bridge, Petřín Hill, etc.)
- **Data-driven environmental claims** based on actual spectral readings
- **Quirky protest ideas** generated from spectral band characteristics
- **Competing solutions** for Prague's environmental challenges

## 🎯 Conflict Examples

### Band Rivalries:
- **B02 (Blue/Air Quality)** vs **B08 (Vegetation)**: "Air pollution vs dying plants - which crisis matters more?"
- **B11 (Moisture)** vs **B12 (Thermal)**: "Drought vs heat islands - what's killing Prague?"
- **B03 (Green/Photosynthesis)** vs **B04 (Red/Plant Stress)**: "Healthy growth vs stress indicators debate"

### Typical Conflicts:
```
🎭 Thermo Wizz (B12): "My thermal readings show Prague is COOKING! 
Urban heat islands are the real crisis!"

🎭 Blue Berta (B02): "Thermal fool! Air pollution is choking us! 
Your heat obsession ignores the toxic atmosphere!"

🎭 Hydration Holmes (B11): "You're both wrong! Drought is the hidden 
killer - without water, there's no life to heat or breathe!"
```

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
Streamlit
OpenAI API key
ElevenLabs API key (optional, for voice)
```

### Installation
```bash
# Clone the repository
git clone [your-repo-url]
cd Satelite

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with:
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key  # Optional
```

### Running the Application
```bash
streamlit run main.py
```

Navigate to `http://localhost:8501` in your browser.

## 📊 How It Works

### 1. **Data Loading**
- Load TIFF files or ZIP archives containing satellite spectral data
- Extract spectral bands (B02, B03, B04, B08, B11, B12) from Prague imagery
- Calculate derived indices (NDVI, NDWI, moisture stress, etc.)

### 2. **Persona Generation**
- Each spectral band becomes a unique environmental activist
- Real spectral values influence personality traits and environmental claims
- Conflict awareness: New personas automatically know about existing ones

### 3. **Conflict Theater**
- **Automatic conflicts** when multiple personas are active
- **Band-specific rivalry templates** (air vs vegetation vs moisture vs thermal)
- **Prague location targeting** based on spectral data analysis
- **Competing protest ideas** and environmental solutions

### 4. **Interactive Dialogue**
- Users can chat with active personas
- Personas respond with their band-specific environmental perspective
- **Cross-persona awareness**: Each response considers other active personas
- **Spontaneous conflicts** can be triggered manually

## 🎨 Persona Types

### B02 - Blue Band (490nm) - Air Quality Activists
- **Focus**: Atmospheric pollution, air quality, urban haze
- **Conflicts with**: Everyone (claims air is the foundation of life)
- **Typical actions**: Oxygen mask protests, smog monster costumes

### B08 - Near-Infrared (842nm) - Vegetation Defenders  
- **Focus**: Plant biomass, vegetation health, urban forests
- **Conflicts with**: Air activists (plants create oxygen!), thermal activists
- **Typical actions**: Tree-hugging therapy, guerrilla gardening

### B11 - SWIR1 (1610nm) - Moisture Guardians
- **Focus**: Soil moisture, drought conditions, water stress
- **Conflicts with**: Thermal activists (heat evaporates water!), air activists
- **Typical actions**: Water bucket brigades, rain dances

### B12 - SWIR2 (2190nm) - Thermal Warriors
- **Focus**: Urban heat islands, thermal stress, fire risk
- **Conflicts with**: Everyone (heat affects everything!)
- **Typical actions**: Ice cube protests, giant fan cooling actions

### B03 - Green (560nm) - Photosynthesis Fanatics
- **Focus**: Chlorophyll, photosynthesis, green light absorption
- **Conflicts with**: Red band activists, infrared obsessives

### B04 - Red (665nm) - Plant Stress Detectives
- **Focus**: Chlorophyll absorption, vegetation stress indicators
- **Conflicts with**: Green band activists, vegetation defenders

## 🎮 User Interface

### Sidebar Controls:
- **📊 Randomness Slider**: Control persona personality variation
- **🎲 Regenerate**: Create new personalities for existing bands
- **⚔️ Generate Conflict**: Trigger spontaneous arguments (appears when 2+ personas active)
- **🔊/🔇 Activate/Deactivate**: Control which personas participate

### Main Chat:
- **Multi-persona dialogue** with automatic conflict awareness
- **Real-time spectral data display** for each active persona
- **Audio playback** for persona responses (if ElevenLabs configured)
- **Prague location mapping** showing where personas detect problems

## 🔧 Technical Architecture

### Core Components:
- **`main.py`**: Main Streamlit application
- **`core/personas/dynamic_citizen_personas.py`**: Conflict-aware persona generation
- **`core/conversation/spectral_dialogue.py`**: Multi-persona dialogue system
- **`core/satellite/`**: TIFF processing and spectral data extraction
- **`core/audio/`**: ElevenLabs voice synthesis integration

### Conflict Generation System:
- **Band rivalry templates**: Pre-defined conflicts between spectral bands
- **Context-aware prompts**: New personas know about existing ones
- **Dynamic introduction generation**: Conflict-driven first appearances
- **Cross-persona dialogue enhancement**: Responses reference other active personas

## 📁 File Structure

```
Satelite/
├── main.py                            # Main application
├── requirements.txt                   # Dependencies
├── core/
│   ├── personas/
│   │   └── dynamic_citizen_personas.py  # Conflict-aware persona generation
│   ├── conversation/
│   │   └── spectral_dialogue.py        # Multi-persona dialogue
│   ├── satellite/                      # TIFF processing
│   └── audio/                          # Voice synthesis
├── images/                            # Sample satellite imagery
│   └── TIFF/                          # Raw TIFF spectral data
└── theater_logs/                      # Session and persona logs
```

## 🎪 Example Session

1. **Load satellite data** from Prague TIFF files
2. **Activate B12 (Thermal)** - "Thermo Wizz" appears, warns about heat islands
3. **Activate B02 (Air Quality)** - "Blue Berta" appears, immediately challenges Thermo Wizz
4. **User asks**: "What should Prague do about environmental problems?"
5. **Conflict erupts**: Each persona proposes competing solutions
6. **Click "⚔️ Generate Conflict"** for spontaneous arguments
7. **Add B11 (Moisture)** - "Hydration Holmes" joins, attacks both previous personas

## 🌟 Advanced Features

### Conflict Customization:
- **Randomness control**: Adjust how dramatic conflicts become
- **Language switching**: Conflicts work in both English and Czech
- **Location targeting**: Personas focus on specific Prague neighborhoods
- **Data-driven arguments**: Conflicts based on actual spectral readings

### Audio Theater:
- **Voice synthesis**: Each persona gets a unique voice
- **Conflict audio**: Heated arguments with voice acting
- **Multi-language audio**: Czech and English voice support

## 🔮 Future Enhancements

- **Real-time satellite data** integration
- **More cities** beyond Prague
- **Citizen voting** on environmental proposals
- **Persona alliances** and temporary truces
- **Environmental impact scoring** for proposed solutions

## 🤝 Contributing

This is an experimental AI theater system exploring how satellite data can create engaging environmental narratives through conflict-driven personas. Contributions welcome for:

- New conflict scenarios
- Additional spectral bands
- More cities and locations
- Enhanced voice synthesis
- Real-time data integration

## 📜 License

[Your chosen license]

---

**🎭 "Where satellite data becomes environmental drama, and every spectral band has an opinion about Prague's future!"**