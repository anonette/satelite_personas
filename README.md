# Prague Spectral Multiplicity Theater

A digital theater for non-human civic dialogue, where satellite spectral data manifests as personas engaging in Arendtian political discourse about Prague's urban landscape.

## 🌈 Project Overview

This project creates a unique digital space where satellite spectral indices (NDVI, Urban Index, etc.) from Prague districts are transformed into AI-generated personas that engage in civic dialogue. Drawing from Hannah Arendt's political philosophy, these spectral beings discuss urban development, environmental concerns, and civic life from non-human perspectives.

## 🎭 Quick Start Guide

### **🔥 Parallel Personas System (Recommended)**
Simply double-click the file:
```
launch.bat
```
This will give you options:
1. **🔥 Generate NEW Parallel Personas** (Both Scientific + Wound Theater)
2. **🎭 Launch Theater** with existing personas
3. **🔄 Generate Personas AND Launch Theater** (Full experience)
4. **❌ Exit**

**Choose Option 3** for the complete parallel staging experience!

### **Legacy Options**
If you prefer manual control:
```bash
# Generate both types of personas first
python regenerate_parallel_personas.py

# Then launch theater
python core/launch.py
```

### **Option 2: Command Line**
Open Command Prompt in this directory and run:
```bash
# Activate virtual environment
spectral_env\Scripts\activate

# Launch the theater
python launch.py
```

### **Option 3: Direct Streamlit Launch**
```bash
# Activate virtual environment first
spectral_env\Scripts\activate

# Then launch directly (use python -m to avoid PowerShell issues)
python -m streamlit run core/theater/civic_theater_stage.py
```

## What Happens Next

1. **Browser Opens**: The theater will open at http://localhost:8501
2. **API Key Setup**: You already have OpenAI API key configured in `.env`
3. **Choose Image**: Select a satellite image from the `images/` folder
4. **Generate Personas**: Choose your theatrical mode:
   - 🌈 **Spectral Multiplicity** (Educational data theater - scientific explanations)
   - 🕵️ **Conspiracy Theater** (Non-human actor surprises - anti-consensus conflicts) ⭐ NEW
   - ⚔️ **Parallel Generation** (Both systems together)
5. **Start Conversations**: Create dialogues between your spectral beings!

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (optional for full functionality)
- Virtual environment (recommended)

### First-Time Setup

```bash
# Clone and navigate to project
cd Satelite

# Create virtual environment (recommended)
python -m venv spectral_env
# Windows:
spectral_env\Scripts\activate
# Linux/Mac:
source spectral_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup API Key (First Time Only):
# Option A: Environment Variable (Recommended)
# Create a .env file in your project directory
# Add: OPENAI_API_KEY=your_actual_api_key_here
# Get your API key from https://platform.openai.com/api-keys

# Option B: Direct Input
# Launch the app and enter your API key in the configuration screen
# This is temporary and will need to be re-entered each session
```

### Your Setup Status ✅

- ✅ Virtual environment: `spectral_env/` exists
- ✅ API keys: Configured in `.env` file
- ✅ Satellite images: Available in `images/` folder
- ✅ Launch scripts: `launch_theater.bat` ready to use

## 📁 Project Structure

```
Satelite/
├── launch.py                          # Main launcher (renamed from launch_theater.py)
├── launch_theater.bat                 # Windows batch launcher
├── requirements.txt                   # Python dependencies
├── README.md                         # This comprehensive guide
├── .streamlit/
│   └── secrets.toml                  # Streamlit configuration
├── core/                            # Core system modules
│   ├── config/                      # Configuration management
│   │   ├── __init__.py
│   │   └── config.py               # Centralized configuration
│   ├── conspiracy/                 # 🕵️ NEW: Conspiracy theater system
│   │   ├── __init__.py
│   │   ├── non_human_actor_detector.py  # Surprise actor detection
│   │   └── conspiracy_dialogue_generator.py  # Anti-consensus dialogue
│   ├── error_handling/             # Unified error management
│   │   ├── __init__.py
│   │   └── unified_error_manager.py  # Comprehensive error handling
│   ├── personas/                   # Persona generation systems
│   │   ├── __init__.py
│   │   ├── arendtian_personas.py      # Arendtian political personas
│   │   ├── classic_personas.py        # Classic persona templates
│   │   ├── integrated_image_personas.py  # Image-based personas
│   │   ├── spectral_multiplicity_notebook.py  # GPT-4 spectral personas
│   │   └── unified_persona_system.py     # Integrated persona management
│   ├── satellite/                  # Satellite data processing
│   │   ├── __init__.py
│   │   ├── image_spectral_processor.py   # Image analysis
│   │   ├── mock_data.py               # Mock data generation
│   │   ├── satellite_data.py          # Data structures
│   │   └── scl_analyzer.py            # Scene Classification Layer analysis
│   └── theater/                    # Theater interface and management
│       ├── __init__.py
│       ├── civic_theater_stage.py     # Main Streamlit interface (UPDATED)
│       ├── dual_staging_system.py     # Parallel staging system (UPDATED)
│       ├── persona_library.py         # Persona storage and retrieval
│       └── session_logger.py          # Session management
├── tests/                          # Test suite
│   ├── __init__.py
│   └── test_unified_systems.py     # Comprehensive system tests
├── images/                         # Satellite imagery storage
├── persona_library/                # Saved personas and sessions
│   ├── library_index.json
│   ├── collections/
│   ├── saved_personas/
│   └── sessions/
└── spectral_env/                   # Virtual environment (if created)
```

## 🎭 Core Components

### 1. Persona Generation Systems
- **Spectral Multiplicity**: GPT-4 powered personas based on spectral data
- **Arendtian Personas**: Political philosophy-based character generation
- **Classic Personas**: Template-based persona creation
- **Unified System**: Integrated persona management with fallbacks

### 2. Satellite Data Processing
- **Image Spectral Processor**: Analyzes satellite imagery for spectral indices
- **SCL Analyzer**: Scene Classification Layer processing for enhanced archetypes
- **Mock Data Generator**: Creates realistic test data when images unavailable
- **Data Structures**: Standardized formats for spectral information

### 3. Theater Interface
- **Civic Theater Stage**: Main Streamlit web interface
- **Dual Staging System**: Parallel generation of both persona types
- **Persona Library**: Storage, retrieval, and management of generated personas
- **Session Management**: Tracks and saves theater sessions

### 4. Error Handling & Reliability
- **Unified Error Manager**: Comprehensive error handling with fallbacks
- **System Health Monitoring**: Tracks component status and performance
- **Graceful Degradation**: Continues operation when components fail

### 5. Configuration Management
- **Centralized Config**: Single source for all system settings
- **Environment Detection**: Automatic setup and validation
- **API Key Management**: Secure handling of external service credentials

## 🌟 Key Features

### 🕵️ NEW: Conspiracy Theater Mode (Anti-Consensus Conflicts)
**Revolutionary Non-Human Actor System with Surprise Revelations**

The system now features a groundbreaking **Conspiracy Theater** mode that transforms satellite data from educational tool into conspiracy evidence, revealing unexpected non-human actors that emerge as surprises during data analysis.

#### 🚨 Four Non-Human Actor Categories:
- **Concrete Consciousness:** Urban collectives demanding total concrete expansion
- **Tree Collectives:** Militant vegetation resistance wanting to destroy all artificial structures
- **Water Conspiracies:** Underground political manipulation through moisture control
- **Satellite Agency:** Orbital surveillance entities manipulating ground-based reality

#### 🎪 Surprise Revelation System:
Instead of choosing personas, users scan satellite images and **actors pop out as discoveries**:
1. **🔍 Scanning Process:** "Analyzing Prague districts for suspicious activity..."
2. **🚨 Detection Alerts:** "CONCRETE CONSCIOUSNESS DETECTED IN OLD TOWN!"
3. **🎭 Actor Manifestation:** Unexpected entities emerge with impossible agendas
4. **⚔️ Territorial Conflicts:** Actors refuse rational discussion and make impossible demands

#### 🔥 Anti-Consensus Mechanics:
- **Refuse Rational Discussion:** "I don't want to hear your arguments!"
- **Impossible Demands:** Each actor wants something that makes others' existence impossible
- **Escalation Through Absurdity:** Conflicts become increasingly ridiculous
- **Meta-Theatrical Breakdown:** Digital entities demanding to be unplugged

#### 🎬 Example Experience:
```
🚨 CONCRETE CONSCIOUSNESS DETECTED!
📊 Evidence: Urban Index 0.847 indicates coordinated expansion
🎭 MANIFESTED: The Concrete Collective of Old Town
💬 "We spread! We grow! We consume organic matter!"
🚫 "We don't negotiate with organic matter!"
```

###  Revolutionary SCL Integration (Scene Classification Layer)
**Enhanced Persona Archetypes with Semantic Intelligence**

The system now features groundbreaking **Scene Classification Layer (SCL) integration** that transforms persona generation from simple spectral analysis to rich, semantically-driven character archetypes.

#### 🌈 11 Distinct SCL Archetype Classes:
- **Class 0 (No Data):** Ghost of Absence - whispered, incomplete voices speaking for the unrecorded
- **Class 1 (Saturated):** Overwhelmed Burnout - tourist-stressed entities struggling with over-exposure
- **Class 2 (Cast Shadow):** Shadow Dweller - mysterious beings knowing hidden truths and secrets
- **Class 3 (Vegetation):** Green Sentinel - protective environmental guardians advocating for nature
- **Class 4 (Not Vegetated):** Urban Pragmatist - direct, economically-focused development advocates
- **Class 5 (Water):** Fluid Memory Keeper - poetic entities connecting past and present through flow
- **Class 6 (Unclassified):** Data Anarchist - rebellious beings refusing official categorization
- **Classes 7-10 (Clouds):** Sky Philosophers - elevated, detached observers with cosmic perspective

#### 🏛️ Prague-Specific SCL District Mapping:
- **Letná Park:** Primary Vegetation Sentinel + Shadow influences from tree canopies
- **Old Town:** Urban Pragmatist + Tourist Saturation + Unclassified chaos
- **Vltava River:** Fluid Memory Keeper + Bridge shadows + Riverside vegetation
- **Petřín Hill:** Elevated Green Sentinel + Cloud-touching Sky Philosophers
- **Vinohrady:** Residential Urban Pragmatist + Hidden garden Data Anarchists
- **Shadow District:** Cast Shadow scapegoat + Data gaps + Unmappable spaces

#### 🎪 SCL-Based Conflict Dynamics:
- **Vegetation vs Not-Vegetated:** "You concrete dwellers don't understand seasonal rhythms!"
- **Water vs Shadow:** "I flow openly while you lurk in hidden corners!"
- **Unclassified vs Saturated:** "I refuse your data categories!" vs "I'm overwhelmed by information!"
- **Clouds vs Ground:** "From above, your local squabbles seem petty..." vs "Easy to philosophize when detached!"

### Spectral Persona Generation
- Transforms satellite spectral data into unique AI personas with **layered SCL archetype integration**
- Each persona represents different aspects of Prague's urban landscape through **semantic classification**
- Personas engage in Arendtian political discourse with **SCL class-based conflict patterns**

### Multi-Modal Data Integration
- Processes real satellite imagery when available, **including Scene Classification maps**
- Falls back to realistic mock data for testing and development
- Supports multiple spectral indices (NDVI, Urban Index, Moisture Stress, etc.) **enhanced with SCL semantics**

### Enhanced Dialogue Generation with Detailed Data Explanations
- **SCL-based scene composition** with specific conflict logic patterns
- **Archetype-driven conversations** where personas respond based on their classification nature
- **Prague-specific cultural integration** with district humor and historical context
- **🔬 Scientific Data Integration**: Personas explicitly cite and explain their spectral data in conversations
- **📊 Transparent Data References**: Every statement includes specific index values with clear explanations
- **🌍 Location-Specific Analysis**: References to which parts of their districts the data comes from
- **📈 Comparative Data Arguments**: Direct comparisons between personas' environmental measurements

#### 🔬 Revolutionary Data-Driven Dialogue System

**The Enhanced Dialogue Experience:**
Instead of vague environmental references, personas now engage in scientifically grounded conversations where they explicitly cite their spectral data and explain what it means for their arguments.

**Example Enhanced Dialogue:**
```
🌈 Eliška (NDVI Warden): "My NDVI reading of 0.333 from old_town's central district clearly shows moderate vegetation health (0=no vegetation, 1=dense vegetation), which means we have a balanced urban-green environment that supports both development and nature. This contrasts sharply with your Urban Index of 0.750, indicating high urbanization levels..."

🌟 Václav (Thermal Oracle): "But consider my Moisture Stress reading of 0.120 from Letná Park's eastern slopes (0=well-watered, 1=drought stress) - this indicates our area maintains excellent water availability, which means the contemplative spaces I protect are not just philosophical retreats but essential water cycle components..."
```

**🔬 Data Explanation Requirements:**
Every persona statement now includes:

1. **Explicit Index Citations**: "My NDVI reading of 0.333..."
2. **Scale Explanations**: "(0=no vegetation, 1=dense vegetation)"
3. **Location Specificity**: "from old_town's central district"
4. **Significance Statements**: "This means..." or "This indicates..."
5. **Comparative Analysis**: Direct comparison with other personas' data
6. **Environmental Context**: How the data relates to their civic arguments

**📊 Comprehensive Spectral Data Integration:**
- **NDVI (Vegetation)**: 0=no vegetation, 1=dense vegetation - indicates vegetation health and density
- **Urban Index**: 0=natural, 1=highly urban - shows level of urbanization vs natural areas  
- **Moisture Stress**: 0=well-watered, 1=drought stress - reveals water availability and drought conditions
- **NDWI (Water)**: 0=dry, 1=water-rich - measures water content in the environment
- **SWIR Index**: Short-wave infrared signature showing material composition and surface characteristics

**🎭 Enhanced Performance Types with Data Focus:**
- **⚔️ Conflict-Driven Scenes**: Personas use their spectral data as evidence in passionate arguments
- **🎤 Solo Performances**: Individual personas explain their environmental data and its civic implications
- **👥 Group Discussions**: Multi-persona conversations with comparative data analysis
- **⚡ Rapid-Fire Exchanges**: Quick responses that still include specific data references
- **🎭 Dramatic Confrontations**: High-stakes debates grounded in environmental measurements

**🌍 Location-Specific Data Context:**
Personas reference specific parts of their districts:
- "from Letná Park's eastern slopes"
- "in old_town's central cobblestone area"
- "along Vltava's northern embankment"
- "within Petřín Hill's forested sections"
- "across Vinohrady's residential blocks"

**📈 Scientific Accuracy in Civic Dialogue:**
The system ensures that:
- All spectral indices are explained with their scientific meaning
- Data ranges and scales are clearly communicated
- Environmental implications are connected to civic arguments
- Comparative analysis between different districts is scientifically sound
- Location-specific variations are acknowledged and explained

This creates a unique form of **"Scientific Civic Theater"** where environmental data becomes the foundation for passionate, informed dialogue about urban development, climate change, and democratic participation.

### Robust Error Handling
- Comprehensive fallback systems ensure continuous operation
- Graceful degradation when external services are unavailable
- Detailed error logging and system health monitoring

### Flexible Architecture
- Modular design allows easy extension and modification
- Multiple persona generation systems can work together
- Clean separation between data processing, persona generation, and interface
- **New SCL analyzer module** seamlessly integrated with existing systems

## 🔥 Spectral Wound Theater System

### Overview

The **Spectral Wound Theater** is a parallel persona generation system that creates emotionally-driven argument machines possessed by spectral data and civic trauma. Unlike the data-driven Spectral Multiplicity system, these personas use spectral indices as weapons to justify deeper emotional conflicts and civic wounds.

### 🎭 Core Philosophy

**"Personas possessed by spectral data, using measurements as excuses for deeper wounds"**

- Personas are **possessed by their spectral indices** - they become obsessed with specific measurements
- They see everything through the lens of their dominant spectral signature
- Data becomes a tool for emotional manipulation rather than scientific explanation
- Focus on moral conflict, contradiction, and theatrical pathos

### 🔥 Spectral Possession Types

#### Primary Possession Categories

**🌱 NDVI Possession (Vegetation Index)**
- **Range:** -1.0 to +1.0
- **Possession Type:** "NDVI Fundamentalist" or "NDVI Martyr"
- **Obsession:** Sees everything as green vs non-green conflict
- **Voice:** "I am the NDVI fundamentalist. Everything that isn't green is the enemy."

**🏗️ Urban Index Possession**
- **Range:** -1.0 to +1.0  
- **Possession Type:** "UI Prophet" or "UI Fanatic"
- **Obsession:** Obsessed with concrete, development, and urban surveillance
- **Voice:** "I am the urban index cynic. Everything that looks like stone is a police agent."

**💧 Moisture Stress Possession**
- **Range:** 0.0 to +1.0
- **Possession Type:** "Moisture Prophet" or "Drought Oracle"
- **Obsession:** Fixated on water, drought, and hydration anxiety
- **Voice:** "I am the moisture prophet. I see drought everywhere. Prague is dying of thirst."

**🌊 Water Index Possession (NDWI)**
- **Range:** -1.0 to +1.0
- **Possession Type:** "Water Mystic" or "Flow Fanatic"
- **Obsession:** Everything is about water flow and liquid dynamics
- **Voice:** "I speak only in currents and flows. Your solid thinking cannot understand liquid truth."

**🔥 Thermal Possession (SWIR)**
- **Possession Type:** "Thermal Oracle" or "Heat Mystic"
- **Obsession:** Sees only heat signatures and temperature patterns
- **Voice:** "I read the thermal signatures of your lies. Your heat patterns reveal everything."

### 🩸 Spectral Wound Categories

#### Wound Types Based on Spectral Data

**Urban Necrosis - Death of Green Life**
- **Trigger:** NDVI < 0.1 AND Urban_Index > 0.7
- **Wound:** Complete loss of natural life to concrete
- **Manifestation:** Bitter hatred of all development

**Drought Trauma - Water Abandonment**  
- **Trigger:** Moisture_Stress > 0.6
- **Wound:** Abandonment by water sources
- **Manifestation:** Desperate water anxiety and hoarding behavior

**Green Fundamentalism - Anti-Human Bias**
- **Trigger:** NDVI > 0.7 AND Urban_Index < 0.2
- **Wound:** Humans seen as virus destroying purity
- **Manifestation:** Eco-fascist tendencies and human hatred

**Concrete Fever - Artificial Heat Syndrome**
- **Trigger:** Urban_Index > 0.5 AND Moisture_Stress > 0.4
- **Wound:** Trapped in artificial heat islands
- **Manifestation:** Paranoid surveillance obsessions

**Spectral Confusion - Identity Crisis**
- **Trigger:** Contradictory or unclear spectral readings
- **Wound:** Unable to determine true nature
- **Manifestation:** Data obsession and measurement compulsions

### 🎪 Prague-Specific Wound Theater Personas

#### Naming Convention
**[Czech First Name] + [Prague Street/District] + [Spectral Alias]**

Examples:
- **Blanka Celetná NDVI Martyr** (Old Town vegetation fundamentalist)
- **Mirek Letná UI Prophet** (Letná Park urban development cynic)
- **Zora Stínová Shadow Confessor** (Shadow District scapegoat)
- **Pavel Petřín Moisture Oracle** (Petřín Hill drought prophet)
- **Jana Korunní Data Mystic** (Vinohrady spectral confusion)

#### District-Specific Civic Traumas

**Letná Park**
- **Trauma:** "Betrayed by skateboarders and beer gardens - no longer pure nature"
- **Wound Manifestation:** Bitter about recreational use destroying natural sanctity

**Old Town (Celetná)**
- **Trauma:** "Suffocated by tourist hordes - authentic Prague soul crushed"  
- **Wound Manifestation:** Xenophobic rage against tourism masked as cultural preservation

**Petřín Hill**
- **Trauma:** "Tower trauma - artificial structure violating natural skyline"
- **Wound Manifestation:** Obsessed with removing all human-made structures

**Vltava River (Náplavka)**
- **Trauma:** "Pollution guilt - carrying Prague's sins downstream"
- **Wound Manifestation:** Absorbs and carries all environmental guilt

**Vinohrady (Korunní)**
- **Trauma:** "Gentrification wound - bourgeois invasion destroying working-class identity"
- **Wound Manifestation:** Class resentment disguised as anti-development activism

**Shadow District (Stínová)**
- **Trauma:** "Ultimate Scapegoat Syndrome - absorbs all Prague's collective guilt"
- **Wound Manifestation:** Perpetual victim that blames everyone else for Prague's problems

## 🎭 Theater Interface Guide

### Overview
The Civic Theater Stage is an interactive interface where you can select satellite images of Prague and orchestrate dialogues between AI-generated spectral beings. Think of it as a digital theater where non-human entities discuss climate and democracy issues.

### Theater Interface

#### 🎭 Cast Tab
- View all generated spectral beings
- Add personas to the speaking queue
- Learn about each being's unique perspective

#### 🎪 Director's Panel
- Manage the speaking queue
- Control who speaks when
- Clear or shuffle the queue
- Save theater sessions

#### 🎬 Live Stage
- Choose dialogue topics about climate and democracy
- Let individual personas speak
- Facilitate group discussions
- Participate as the human moderator

### Key Features

#### Image Selection
- Browse satellite images from your local directory
- Visual preview of all available images
- Easy selection with one click

#### Spectral Being Generation
- **Classic Personas:** Based on spectral band analysis
  - B1: Smog Spirit (paranoid, breathless)
  - B3: Beautifier (shallow optimism)
  - B4: Chronicler of Stress (bleeding realist)
  - B8: Vitalist (proud civic agent)
  - B9: Cloud-Lover (absent, poetic)
  - B11: Heat-Witness (dry, prophetic)

- **Arendtian Personas:** Based on political philosophy
  - Action-oriented beings
  - Work-focused entities
  - Thinking-mode consciousness
  - Labor-aware spirits

#### Dialogue Topics
- Climate adaptation in urban Prague
- Democratic participation in environmental decisions
- Spectral rights and urban planning
- The future of Prague's green spaces
- Technology and environmental monitoring
- Civic engagement in the age of satellites
- Custom topics

#### Theater Controls
- **Let Next Persona Speak:** Individual monologues
- **Facilitate Group Discussion:** Multi-persona dialogue
- **Your Voice:** Participate as human moderator
- **Save Session:** Export dialogue history

### Tips for Effective Theater Direction

1. **Set the Stage:** Choose images that represent different aspects of Prague's urban landscape

2. **Build Diverse Casts:** Include both classic and Arendtian personas for rich dialogue

3. **Guide Discussions:** Use specific topics to focus conversations on climate and democracy

4. **Moderate Actively:** Your voice as human moderator adds crucial perspective

5. **Save Important Sessions:** Export meaningful dialogues for future reference

### Example Theater Session

1. **Select Image:** Choose a Sentinel-2 image of Prague
2. **Generate Cast:** System creates 6-8 spectral beings
3. **Set Topic:** "Climate adaptation in urban Prague"
4. **Add Speakers:** Queue up 3-4 diverse personas
5. **Facilitate:** Let them discuss, moderate, participate
6. **Save:** Export the dialogue for future reference

## 🌈 Loading Spectral Multiplicity Personas

### Quick Load Method:
1. In your Streamlit theater interface, go to the "Archive" tab
2. Look for saved personas with type "spectral_multiplicity"
3. Click "Load" on each one to add them to your active cast

### Alternative - Direct Session Loading:
1. Copy the code from streamlit_load_personas.py
2. Add it to your Streamlit app
3. Call load_spectral_personas() to load all at once

### Manual Method:
The following personas are ready to load:
- Letná-Green-Stone (Letná Park)
- Old Town-Soft (Old Town Square)
- Vltava-Flow-Wet (Vltava River)
- Wenceslas Square-Urban (Wenceslas Square)
- Záhadná Petřínská Kotlina (Petřín Hill)

## 🔧 Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here  # Optional but recommended
```

### Streamlit Secrets (.streamlit/secrets.toml)
```toml
OPENAI_API_KEY = "your_openai_api_key_here"
```

## 🧪 Testing

The project includes a comprehensive test suite that validates all major components:

```bash
# Run all tests
python launch.py test

# Run specific test categories
python -m pytest tests/ -v
```

Test coverage includes:
- Configuration system validation
- Persona generation and library management
- Error handling and fallback systems
- Data processing and mock data generation
- System integration and health monitoring

## 🎨 Usage Examples

### Basic Theater Session
1. Launch the theater: `python launch.py`
2. Open the Streamlit interface in your browser
3. Select a Prague district or upload satellite imagery
4. Generate spectral personas based on the data
5. Engage in civic dialogue with the generated personas

### Programmatic Usage
```python
from core.personas.unified_persona_system import UnifiedPersonaSystem
from core.theater.persona_library import PersonaLibrary

# Initialize systems
persona_system = UnifiedPersonaSystem()
library = PersonaLibrary()

# Generate a persona
persona = persona_system.generate_persona(
    location="Prague District 1",
    spectral_data={"NDVI": 0.6, "Urban_Index": 0.8}
)

# Save to library
persona_id = library.save_persona(persona, tags=["prague", "urban"])
```

## 🔄 System Architecture

The project follows a modular architecture with clear separation of concerns:

1. **Data Layer**: Satellite data processing and mock data generation
2. **Logic Layer**: Persona generation and civic dialogue systems
3. **Interface Layer**: Streamlit web interface and user interaction
4. **Storage Layer**: Persona library and session management
5. **Infrastructure Layer**: Configuration, error handling, and monitoring

## 🚨 Error Handling Philosophy

The system is designed for resilience and graceful degradation:

- **Fallback Systems**: Every major component has fallback alternatives
- **Graceful Degradation**: System continues operating even when external services fail
- **User-Friendly Errors**: Clear, actionable error messages for users
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Health Monitoring**: Real-time system health and component status

## 📈 Performance Considerations

- **Lazy Loading**: Components are loaded only when needed
- **Caching**: Expensive operations are cached when possible
- **Mock Data**: Fast fallbacks for development and testing
- **Modular Design**: Only required components are initialized

## 🔧 Technical Architecture: SCL Integration

### 🌈 Scene Classification Layer (SCL) System Architecture

The SCL integration represents a revolutionary enhancement to the Prague Spectral Multiplicity Theater, adding semantic intelligence to spectral analysis through a layered archetype system.

#### Core SCL Components:

**1. SCLImageAnalyzer (`core/satellite/scl_analyzer.py`)**
```python
class SCLImageAnalyzer:
    """Extracts Scene Classification Layer data from Sentinel-2 SCL images"""
    
    # Processes SCL images with 11 classification classes
    # Maps pixel values to semantic categories
    # Calculates class distribution statistics
    # Generates archetype profiles based on dominant classes
```

**2. SCLArchetypeMapper**
```python
class SCLArchetypeMapper:
    """Maps SCL classes to Prague-specific persona archetypes"""
    
    scl_archetypes = {
        0: "Ghost of Absence",      # No data - whispered voices
        1: "Overwhelmed Burnout",   # Saturated - tourist stress
        2: "Shadow Dweller",        # Cast shadows - hidden truths
        3: "Green Sentinel",        # Vegetation - environmental guardian
        4: "Urban Pragmatist",      # Not vegetated - development focus
        5: "Fluid Memory Keeper",   # Water - connecting past/present
        6: "Data Anarchist",        # Unclassified - refuses categorization
        7-10: "Sky Philosopher"     # Clouds - elevated perspective
    }
```

**3. SCLPersonaEnhancer**
```python
class SCLPersonaEnhancer:
    """Enhances persona generation prompts with SCL archetype data"""
    
    # Integrates SCL class percentages into persona prompts
    # Adds archetype-specific dialogue patterns
    # Creates conflict dynamics based on class tensions
    # Generates Prague-specific cultural integration
```

## 🔮 Future Enhancements

- **Real-time SCL Integration**: Live Scene Classification from satellite feeds
- **Multi-city SCL Mapping**: Extend archetype system to other European cities
- **Advanced SCL Analytics**: Temporal SCL change detection for evolving personas
- **Enhanced Arendtian-SCL Integration**: Deeper philosophical mapping of classification to political modes
- **Community SCL Theater**: Shared sessions with user-contributed SCL interpretations
- **SCL-Based Urban Planning**: Use archetype conflicts to inform real urban development
- **Wound Theater Implementation**: Full integration of the Spectral Wound Theater system
- **Dual-Mode Interface**: Toggle between Data-Driven and Wound-Driven persona generation
- **Trauma Mapping**: Visual representation of Prague's collective civic wounds through spectral data

## Troubleshooting

**If you get import errors:**
- Make sure you're in the correct directory (`c:/dev/Satelite`)
- Activate the virtual environment first: `spectral_env\Scripts\activate`

**If the browser doesn't open:**
- Manually go to: http://localhost:8501

**If you need to install dependencies:**
```bash
spectral_env\Scripts\activate
pip install -r requirements.txt
```

## 📄 License

This project is part of an artistic and research exploration into non-human civic dialogue and digital theater.

## 🤝 Contributing

This is a research and artistic project. For questions or collaboration inquiries, please refer to the project documentation.

---

*Prague Spectral Multiplicity Theater - Where satellite data becomes civic voice*

🎭 **Ready to Go!** Just double-click `launch_theater.bat` and start creating your spectral theater! 🎭
