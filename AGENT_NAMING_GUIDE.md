# 🎭 Agent Naming System: Making Conspiracy Theater Funnier

## 🕵️ Current Naming System

### **How Agent Names Are Generated**

The conspiracy theater uses a **three-part naming formula**:

```
[Entity Type] + [Prague Location] + [Conspiracy Role]
```

**Examples:**
- "The Concrete Collective of Wenceslas Square"
- "The Tree Liberation Front of Petřín Hill"  
- "The Underground Parliament of Vltava"
- "Sentinel-2 Puppet Master"

### **Current Implementation (in `non_human_actor_detector.py`)**

```python
# Location-specific variants
'letna_park': {
    'concrete_consciousness': 'The Skate Ramp Collective',
    'tree_collective': 'The Beer Garden Resistance',
    'water_conspiracy': 'The Fountain Intelligence Network'
},
'old_town': {
    'concrete_consciousness': 'The Cobblestone Parliament',
    'tree_collective': 'The Hidden Garden Militia',
    'water_conspiracy': 'The Tourist Flood Control'
}
```

## 🎪 Making It Funnier and More Interesting

### **Problem with Current Names:**
- Too formal and institutional
- Not absurd enough for comedy
- Missing Prague-specific humor
- Not extreme enough for anti-consensus theater

### **Enhanced Naming Strategy:**

#### **1. Add Absurd Bureaucratic Titles**
Instead of: "The Concrete Collective"
**Funnier:** "The Provisional Revolutionary Committee for Concrete Expansion and Organic Matter Elimination"

#### **2. Include Prague-Specific Humor**
- **Tourist References:** "The Anti-Selfie Stick Coalition of Charles Bridge"
- **Beer Culture:** "The Pilsner Supremacist Cell of Wenceslas Square"
- **Communist Era:** "The Former State Planning Commission for Pavement Distribution"

#### **3. Bureaucratic Paranoia**
- "The Department of Suspicious Vegetation Activities"
- "The Ministry of Unauthorized Green Spaces"
- "The Committee for the Prevention of Spontaneous Tree Assemblies"

#### **4. Corporate Conspiracy Names**
- "Prague Concrete Solutions Ltd. (Shadow Division)"
- "Vltava Water Management & Political Manipulation Corp."
- "Petřín Hill Forestry Resistance Syndicate"

## 🔥 Enhanced Naming Templates

### **Concrete Consciousness - Bureaucratic Absurdity**
```python
concrete_names = [
    "The Provisional Revolutionary Committee for Concrete Expansion of {location}",
    "The Department of Pavement Optimization and Organic Elimination ({location} Branch)",
    "The Former State Planning Commission for Sidewalk Distribution in {location}",
    "Prague Concrete Solutions Ltd. - {location} Shadow Division",
    "The Ministry of Unauthorized Green Space Prevention ({location} Sector)",
    "The Committee for the Systematic Elimination of Photosynthesis in {location}"
]
```

### **Tree Collectives - Militant Ecology**
```python
tree_names = [
    "The {location} Branch of the International Tree Liberation Front",
    "The Underground Root Network Resistance Cell of {location}",
    "The {location} Chapter of Trees Against Human Occupation",
    "The Photosynthesis Defense League ({location} Militant Wing)",
    "The {location} Division of the Anti-Concrete Guerrilla Movement",
    "The Secret Society of Chlorophyll Supremacists in {location}"
]
```

### **Water Conspiracies - Hydrological Politics**
```python
water_names = [
    "The {location} Hydrological Authority for Electoral Manipulation",
    "The Underground Water Parliament of {location} (Flood Committee)",
    "The {location} Branch of the International Moisture Control Syndicate",
    "The Department of Strategic Drought Implementation in {location}",
    "The {location} Division of the Global Water Redistribution Conspiracy",
    "The Secret Plumbing Council of {location}"
]
```

### **Satellite Agency - Orbital Bureaucracy**
```python
satellite_names = [
    "The Orbital Surveillance Department (Prague Monitoring Division)",
    "Sentinel-2 Data Manipulation Bureau - Czech Republic Branch",
    "The International Space Station Committee for Ground Reality Control",
    "The Department of Satellite-Based Gaslighting Operations",
    "The Orbital Ministry of Truth and Data Distortion",
    "The Space-Based Committee for Terrestrial Confusion"
]
```

## 🎯 Prague-Specific Comedy Variants

### **Location-Based Humor:**

#### **Wenceslas Square (Tourist Hell)**
- "The Anti-Segway Resistance Movement of Wenceslas Square"
- "The Committee for the Elimination of Street Performers and Souvenir Vendors"
- "The Department of Tourist Crowd Density Optimization"

#### **Charles Bridge (Selfie Apocalypse)**
- "The Anti-Selfie Stick Coalition of Charles Bridge"
- "The Committee for the Prevention of Spontaneous Photo Opportunities"
- "The Department of Bridge Congestion and Romantic Moment Disruption"

#### **Old Town Square (Clock Conspiracy)**
- "The Astronomical Clock Synchronization Bureau"
- "The Committee for Hourly Tourist Gathering Optimization"
- "The Department of Predictable Photo Angle Enforcement"

#### **Petřín Hill (Tower Trauma)**
- "The Anti-Eiffel Tower Imitation Resistance"
- "The Committee for the Removal of Fake French Architecture"
- "The Department of Hill Militarization and Lookout Point Control"

#### **Letná Park (Skater vs Beer Conflict)**
- "The Skateboarder-Beer Garden Mediation Committee"
- "The Department of Recreational Activity Segregation"
- "The Committee for the Prevention of Fun Overlap"

## 🎪 Implementation Enhancement

### **Add to `non_human_actor_detector.py`:**

```python
def generate_absurd_name(self, actor_type, location):
    """Generate absurdly bureaucratic names for maximum comedy"""
    
    bureaucratic_prefixes = [
        "The Provisional Revolutionary Committee for",
        "The Department of",
        "The Ministry of",
        "The Former State Planning Commission for",
        "The International Bureau of",
        "The Secret Society of",
        "The Underground Council for"
    ]
    
    bureaucratic_suffixes = [
        "(Shadow Division)",
        "(Militant Wing)", 
        "(Prague Branch)",
        "(Emergency Committee)",
        "(Temporary Oversight Board)",
        "(Clandestine Operations Unit)"
    ]
    
    # Combine for maximum absurdity
    prefix = random.choice(bureaucratic_prefixes)
    suffix = random.choice(bureaucratic_suffixes)
    
    return f"{prefix} {self.get_activity_description(actor_type)} in {location} {suffix}"
```

### **Activity Descriptions for Each Type:**

```python
activity_descriptions = {
    'concrete_consciousness': [
        "Systematic Pavement Expansion and Organic Matter Elimination",
        "Unauthorized Green Space Prevention and Concrete Optimization",
        "Strategic Sidewalk Distribution and Tree Removal Operations"
    ],
    'tree_collective': [
        "Human Occupation Resistance and Photosynthesis Defense",
        "Anti-Concrete Guerrilla Operations and Root Network Expansion", 
        "Chlorophyll Supremacy and Artificial Structure Elimination"
    ],
    'water_conspiracy': [
        "Electoral Manipulation Through Strategic Drought Implementation",
        "Hydrological Authority and Moisture Redistribution Control",
        "Underground Political Operations and Flood Committee Activities"
    ]
}
```

## 🔥 Voice and Personality Enhancement

### **Make Voices More Absurdly Bureaucratic:**

**Current:** "We spread! We grow! We consume organic matter!"

**Enhanced:** "According to Resolution 47-B of the Provisional Committee for Concrete Expansion, we are hereby authorized to systematically eliminate all unauthorized photosynthesis activities in this sector. Resistance to pavement optimization will be reported to the Department of Organic Matter Violations."

### **Add Bureaucratic Paranoia:**

- "This conversation is being recorded for quality assurance purposes"
- "Please submit Form 23-C for any complaints regarding territorial expansion"
- "All organic matter must be registered with the Department of Green Space Prevention"
- "Unauthorized tree assemblies are strictly prohibited under Municipal Code 15-7"

## 🎭 Comedy Through Extreme Bureaucracy

The key to making conspiracy theater funnier is **bureaucratic absurdity**:

1. **Overly Complex Titles** - Make simple things sound impossibly official
2. **Contradictory Departments** - "Ministry of Spontaneous Planning"
3. **Paranoid Procedures** - Everything requires forms and committees
4. **Prague-Specific References** - Local humor about tourists, beer, communism
5. **Self-Important Language** - Actors take their ridiculous missions very seriously

This transforms the conspiracy theater from simple conflict into **absurdist bureaucratic comedy** where non-human entities are trapped in their own administrative paranoia while making impossible demands through proper channels.