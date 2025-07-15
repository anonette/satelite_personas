# Surprise Actor Interface Design
## Non-Human Actors Pop Out as Surprises After Image Selection

## Core Concept: "Unexpected Revelations"

After the user selects a satellite image and starts persona generation, the system **scans the data and reveals surprising non-human actors** that were "hidden" in the satellite readings. The user doesn't choose what actors appear - they emerge as **discoveries** from the data analysis.

## Updated Mode Selection Interface

### Three Clear Options:
```
🌈 Spectral Multiplicity (Educational Data Theater)
- Personas explain their spectral data scientifically
- Focus on NDVI, Urban Index, moisture stress measurements
- Educational and informative dialogue

🕵️ Conspiracy Theater (Non-Human Actor Surprises)
- Satellite data reveals hidden non-human agendas
- Unexpected actors emerge from data analysis
- Conflict-driven, anti-consensus theater

⚔️ Parallel Generation (Both Systems)
- Creates both educational and conspiracy personas
- Maximum variety and theatrical tension
```

## Surprise Revelation Workflow

### Step 1: Image Selection (Same as Current)
User browses and selects satellite image - **no indication yet** of what actors might be hidden inside.

### Step 2: Generation Mode Choice
User selects "🕵️ Conspiracy Theater" mode.

**Interface shows:**
```
🕵️ Conspiracy Theater Mode Selected
- The system will scan your satellite image for hidden non-human activity
- Unexpected actors may emerge from the data
- Prepare for surprises...
```

### Step 3: "Scanning for Hidden Activity"
When user clicks generate, instead of predictable persona creation:

```
🔍 SCANNING SATELLITE DATA FOR SUSPICIOUS ACTIVITY...

📡 Analyzing spectral signatures...
🔍 Detecting anomalous patterns...
⚠️  ALERT: Unusual activity detected!
🚨 ALERT: Non-human intelligence signatures found!
🕵️ ALERT: Hidden agendas revealed!
```

### Step 4: Surprise Actor Revelations
Actors **pop out** one by one as **discoveries**:

```
🚨 FIRST DETECTION:
"Concrete Consciousness activity detected in Wenceslas Square area!"
Urban Index readings suggest coordinated expansion behavior...
🎭 MANIFESTING: The Concrete Collective of Wenceslas Square

🚨 SECOND DETECTION:  
"Tree Collective military buildup detected in Petřín Hill!"
NDVI patterns indicate organized resistance movement...
🎭 MANIFESTING: The Tree Liberation Front of Petřín Hill

🚨 THIRD DETECTION:
"Water Conspiracy detected in Vltava River systems!"
Moisture patterns suggest political manipulation...
🎭 MANIFESTING: The Underground Parliament of Vltava

🚨 ORBITAL INTERFERENCE DETECTED:
"Satellite manipulation of data streams confirmed!"
🎭 MANIFESTING: Sentinel-2 Puppet Master
```

## Surprise Generation Algorithm

### Data-Driven Actor Discovery
The system analyzes the **actual satellite data** and generates surprises based on **real patterns**:

```python
def discover_hidden_actors(satellite_data, location):
    """Scan data and reveal surprising non-human actors"""
    
    surprises = []
    
    # Concrete Consciousness Surprise
    if satellite_data['Urban_Index'] > 0.6:
        surprise = {
            'type': 'concrete_consciousness',
            'revelation': f"Unusual concrete expansion patterns detected in {location}!",
            'evidence': f"Urban Index of {satellite_data['Urban_Index']:.3f} suggests coordinated behavior",
            'actor_name': f"The Concrete Collective of {location}",
            'surprise_level': 'high' if satellite_data['Urban_Index'] > 0.8 else 'medium'
        }
        surprises.append(surprise)
    
    # Tree Collective Surprise
    if satellite_data['NDVI'] > 0.5:
        surprise = {
            'type': 'tree_collective',
            'revelation': f"Coordinated vegetation activity detected in {location}!",
            'evidence': f"NDVI reading of {satellite_data['NDVI']:.3f} indicates organized movement",
            'actor_name': f"The Tree Liberation Front of {location}",
            'surprise_level': 'militant' if satellite_data['NDVI'] > 0.7 else 'moderate'
        }
        surprises.append(surprise)
    
    # Water Conspiracy Surprise
    if satellite_data['Moisture_Stress'] > 0.4 or satellite_data.get('NDWI', 0) > 0.3:
        surprise = {
            'type': 'water_conspiracy',
            'revelation': f"Suspicious water system behavior detected in {location}!",
            'evidence': f"Moisture patterns suggest political manipulation",
            'actor_name': f"The Underground Parliament of {location}",
            'surprise_level': 'political'
        }
        surprises.append(surprise)
    
    # Always add Satellite Surprise (meta-level)
    surprise = {
        'type': 'satellite_agency',
        'revelation': "ORBITAL INTERFERENCE DETECTED!",
        'evidence': "Satellite manipulation of data streams confirmed",
        'actor_name': "Sentinel-2 Puppet Master",
        'surprise_level': 'meta'
    }
    surprises.append(surprise)
    
    return surprises
```

## Surprise Presentation Interface

### Progressive Revelation
Each actor appears with **dramatic revelation**:

```
🚨 DETECTION ALERT 🚨

[Scanning animation...]

⚠️  ANOMALY FOUND IN SECTOR: Old Town
📊 EVIDENCE: Urban Index 0.847 - Unusual expansion behavior
🔍 ANALYSIS: Coordinated concrete growth patterns detected
🎭 MANIFESTATION: The Concrete Collective of Old Town

[Actor card appears with dramatic animation]

AGENDA: "We spread! We grow! We consume organic matter!"
DEMANDS: "Pave over all remaining green spaces immediately!"
REFUSES: "We don't negotiate with organic matter!"

[Continue scanning button appears]
```

### Escalating Surprises
Each new actor discovery becomes more dramatic:

1. **First Actor:** "Unusual activity detected..."
2. **Second Actor:** "ALERT: Coordinated resistance movement found!"
3. **Third Actor:** "🚨 CONSPIRACY CONFIRMED: Political manipulation detected!"
4. **Satellite Actor:** "⚠️ ORBITAL INTERFERENCE: The satellites are manipulating everything!"

## Interface Flow Design

### Updated Generation Button
Instead of: "🔥 Summon Spectral Wound Theater Machines"
New: "🔍 Scan for Hidden Non-Human Activity"

### Scanning Process Display
```
🔍 SCANNING SATELLITE IMAGE...
📡 Analyzing spectral signatures... [Progress bar]
🔍 Detecting anomalous patterns... [Progress bar]
⚠️  Searching for non-human intelligence... [Progress bar]
🚨 SURPRISES DETECTED! Revealing hidden actors...
```

### Actor Revelation Cards
Each surprise appears as an animated card:

```
┌─────────────────────────────────────┐
│ 🚨 SURPRISE DETECTION 🚨            │
├─────────────────────────────────────┤
│ 🎭 The Concrete Collective of       │
│    Wenceslas Square                 │
├─────────────────────────────────────┤
│ 📊 Evidence: Urban Index 0.847      │
│ 🔍 Behavior: Coordinated expansion  │
│ ⚠️  Threat Level: HIGH              │
├─────────────────────────────────────┤
│ 💬 "We are spreading! Resistance    │
│    is futile - we are inevitable!"  │
├─────────────────────────────────────┤
│ [Add to Performance] [Learn More]   │
└─────────────────────────────────────┘
```

## Surprise Variety System

### Location-Specific Surprises
Different Prague areas reveal different actors:

**Old Town:**
- Concrete Collective (tourist pressure creates expansion)
- Tourist Surveillance Network (hidden monitoring system)

**Petřín Hill:**
- Tree Liberation Front (militant vegetation resistance)
- Tower Conspiracy (Petřín Tower as communication hub)

**Vltava River:**
- Underground Parliament (water political control)
- Bridge Intelligence Network (bridges as spy nodes)

**Letná Park:**
- Skater Collective (recreational territory disputes)
- Beer Garden Syndicate (social manipulation through alcohol)

### Seasonal/Temporal Surprises
Based on image date:
- **Spring:** "Tree Awakening Protocol detected!"
- **Summer:** "Tourist Invasion Response activated!"
- **Autumn:** "Strategic Leaf Drop Campaign initiated!"
- **Winter:** "Concrete Hibernation Period - underground activity!"

## Technical Implementation

### Surprise Timing
```python
def reveal_surprises_progressively(surprises):
    """Reveal actors one by one with dramatic timing"""
    
    for i, surprise in enumerate(surprises):
        # Scanning delay
        time.sleep(2 + i)  # Increasing suspense
        
        # Dramatic revelation
        st.warning(f"🚨 DETECTION {i+1}: {surprise['revelation']}")
        
        # Evidence presentation
        st.info(f"📊 Evidence: {surprise['evidence']}")
        
        # Actor manifestation
        st.success(f"🎭 MANIFESTING: {surprise['actor_name']}")
        
        # Add to active actors
        manifest_actor(surprise)
        
        # Pause before next revelation
        if i < len(surprises) - 1:
            st.button(f"Continue Scanning...", key=f"continue_{i}")
```

This design creates the **surprise element** you want - users don't know what non-human actors will emerge from their satellite image until the system reveals them as dramatic discoveries during the scanning process.