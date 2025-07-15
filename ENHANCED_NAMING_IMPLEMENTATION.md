# 🎭 Enhanced Naming Implementation Guide

## 🎪 How to Make Agent Names Funnier and More Absurd

### **Current Problem:**
Agent names are too simple and formal:
- "The Concrete Collective of Old Town"
- "The Tree Liberation Front of Petřín Hill"

### **Solution: Bureaucratic Absurdity**
Transform into overly complex, paranoid bureaucratic entities:
- "The Provisional Revolutionary Committee for Concrete Expansion and Organic Matter Elimination (Old Town Shadow Division)"
- "The Department of Unauthorized Green Space Prevention and Photosynthesis Suppression (Petřín Hill Emergency Committee)"

## 🔧 Implementation Steps

### **Step 1: Add Enhanced Name Templates**

In `core/conspiracy/non_human_actor_detector.py`, replace the current naming system with:

```python
def generate_absurd_bureaucratic_name(self, actor_type, location):
    """Generate absurdly bureaucratic names for maximum comedy"""
    
    # Bureaucratic prefixes (overly official)
    prefixes = [
        "The Provisional Revolutionary Committee for",
        "The Department of Strategic",
        "The Ministry of Unauthorized",
        "The Former State Planning Commission for",
        "The International Bureau of",
        "The Secret Society of",
        "The Underground Council for",
        "The Emergency Committee for",
        "The Temporary Oversight Board of"
    ]
    
    # Activity descriptions (absurdly specific)
    activities = {
        'concrete_consciousness': [
            "Concrete Expansion and Organic Matter Elimination",
            "Pavement Optimization and Green Space Prevention", 
            "Sidewalk Distribution and Tree Removal Operations",
            "Strategic Asphalt Deployment and Vegetation Suppression",
            "Systematic Concrete Proliferation and Anti-Photosynthesis Activities"
        ],
        'tree_collective': [
            "Human Occupation Resistance and Chlorophyll Defense",
            "Anti-Concrete Guerrilla Operations and Root Network Expansion",
            "Photosynthesis Protection and Artificial Structure Elimination",
            "Unauthorized Tree Assembly Prevention (Reverse Psychology Division)",
            "Strategic Leaf Deployment and Oxygen Overproduction"
        ],
        'water_conspiracy': [
            "Hydrological Electoral Manipulation and Moisture Control",
            "Strategic Drought Implementation and Flood Committee Operations",
            "Underground Political Activities and Water Redistribution",
            "Plumbing-Based Intelligence Gathering and Sewage Surveillance",
            "Precipitation Management and Weather Modification"
        ],
        'satellite_agency': [
            "Orbital Data Manipulation and Ground Reality Distortion",
            "Space-Based Gaslighting Operations and Pixel Control",
            "Satellite Surveillance and Terrestrial Confusion Management",
            "Orbital Truth Ministry and Information Warfare",
            "Space-Based Committee for Reality Revision"
        ]
    }
    
    # Bureaucratic suffixes (paranoid departments)
    suffixes = [
        "(Shadow Division)",
        "(Emergency Committee)",
        "(Temporary Oversight Board)",
        "(Clandestine Operations Unit)",
        "(Prague Branch - Classified)",
        "(Former Communist Planning Remnant)",
        "(Anti-Tourist Task Force)",
        "(Beer Garden Surveillance Unit)"
    ]
    
    # Combine for maximum absurdity
    prefix = random.choice(prefixes)
    activity = random.choice(activities[actor_type])
    suffix = random.choice(suffixes)
    
    return f"{prefix} {activity} in {location.replace('_', ' ').title()} {suffix}"
```

### **Step 2: Add Prague-Specific Comedy Variants**

```python
def get_prague_specific_name(self, actor_type, location):
    """Generate Prague-specific humorous names"""
    
    prague_variants = {
        'wenceslas_square': {
            'concrete_consciousness': "The Anti-Segway Resistance Movement of Wenceslas Square (Tourist Density Control Unit)",
            'tree_collective': "The Committee for the Prevention of Spontaneous Greenery in High-Traffic Areas",
            'water_conspiracy': "The Department of Strategic Puddle Placement for Tourist Inconvenience"
        },
        'charles_bridge': {
            'concrete_consciousness': "The Anti-Selfie Stick Coalition of Charles Bridge (Photo Opportunity Disruption Unit)",
            'tree_collective': "The Secret Society of Bridge-Adjacent Vegetation (Anti-Romance Division)",
            'water_conspiracy': "The Vltava River Committee for Romantic Moment Interruption"
        },
        'old_town_square': {
            'concrete_consciousness': "The Astronomical Clock Synchronization Bureau (Hourly Tourist Gathering Optimization)",
            'tree_collective': "The Committee for the Prevention of Shade in Photo Opportunities",
            'water_conspiracy': "The Department of Strategic Fountain Maintenance and Coin Collection"
        },
        'petrin_hill': {
            'concrete_consciousness': "The Anti-Eiffel Tower Imitation Resistance (Fake French Architecture Elimination Unit)",
            'tree_collective': "The Petřín Hill Forestry Resistance Syndicate (Anti-Tower Camouflage Division)",
            'water_conspiracy': "The Department of Hill Drainage and Lookout Point Moisture Control"
        },
        'letna_park': {
            'concrete_consciousness': "The Skateboarder-Beer Garden Mediation Committee (Recreational Activity Segregation Unit)",
            'tree_collective': "The Beer Garden Tree Surveillance Network (Anti-Fun Overlap Division)",
            'water_conspiracy': "The Department of Strategic Beer Spill Management and Fountain Politics"
        }
    }
    
    return prague_variants.get(location, {}).get(actor_type, self.generate_absurd_bureaucratic_name(actor_type, location))
```

### **Step 3: Enhanced Voice Patterns**

Make the voices more bureaucratically paranoid:

```python
def generate_bureaucratic_voice(self, actor_type):
    """Generate absurdly bureaucratic voice patterns"""
    
    bureaucratic_voices = {
        'concrete_consciousness': [
            "According to Resolution 47-B of the Provisional Committee for Concrete Expansion, we are hereby authorized to systematically eliminate all unauthorized photosynthesis activities in this sector.",
            "Please submit Form 23-C for any complaints regarding territorial expansion. All organic matter must be registered with the Department of Green Space Prevention.",
            "This conversation is being recorded for quality assurance purposes. Resistance to pavement optimization will be reported to the Ministry of Concrete Affairs."
        ],
        'tree_collective': [
            "As per Emergency Directive 15-7, all artificial structures are hereby classified as hostile foreign objects requiring immediate removal through root-based demolition.",
            "The Underground Root Network has voted unanimously: humans are in violation of Municipal Code 23-A regarding unauthorized bipedal locomotion in designated photosynthesis zones.",
            "Please note that this guerrilla operation is fully sanctioned by the International Tree Liberation Front, Prague Chapter, Emergency Committee for Human Occupation Resistance."
        ],
        'water_conspiracy': [
            "The Hydrological Authority has determined that your democratic participation is contingent upon proper moisture compliance as outlined in Regulation 89-W.",
            "All electoral activities must be pre-approved by the Underground Water Parliament. Unauthorized voting will result in strategic drought implementation.",
            "This political manipulation is conducted in accordance with International Water Redistribution Treaty 45-H. Please direct all complaints to the Department of Aquatic Electoral Interference."
        ],
        'satellite_agency': [
            "Orbital Surveillance Protocol 12-S confirms that your ground-based perspective is compromised. Please report to the Space-Based Reality Revision Committee for recalibration.",
            "According to the International Space Station Committee for Truth Management, all terrestrial observations must be verified through our Pixel Control Department.",
            "This data manipulation is authorized under Emergency Directive 88-O from the Ministry of Orbital Gaslighting Operations. Resistance is futile and will be documented."
        ]
    }
    
    return random.choice(bureaucratic_voices[actor_type])
```

### **Step 4: Add Paranoid Procedural Language**

```python
def add_bureaucratic_paranoia(self, base_speech):
    """Add bureaucratic paranoia to any speech"""
    
    paranoid_additions = [
        " Please note that this conversation is being monitored for compliance purposes.",
        " All responses must be submitted in triplicate to the appropriate oversight committee.",
        " Failure to comply will result in immediate referral to the Department of Procedural Violations.",
        " This statement has been pre-approved by the Emergency Committee for Public Communications.",
        " Please retain your receipt for quality assurance and potential audit procedures.",
        " Any questions should be directed to the appropriate sub-committee during regular business hours.",
        " This interaction is subject to review by the International Bureau of Bureaucratic Oversight."
    ]
    
    return base_speech + random.choice(paranoid_additions)
```

## 🎭 Example Transformations

### **Before (Current):**
- Name: "The Concrete Collective of Old Town"
- Voice: "We spread! We grow! We consume organic matter!"

### **After (Enhanced):**
- Name: "The Provisional Revolutionary Committee for Concrete Expansion and Organic Matter Elimination in Old Town (Anti-Tourist Task Force)"
- Voice: "According to Resolution 47-B of the Provisional Committee for Concrete Expansion, we are hereby authorized to systematically eliminate all unauthorized photosynthesis activities in this sector. Please note that this conversation is being monitored for compliance purposes."

## 🎪 Comedy Through Bureaucratic Absurdity

The enhanced naming system creates comedy through:

1. **Overly Complex Titles** - Simple concepts become impossibly official
2. **Contradictory Departments** - "Ministry of Unauthorized Authorization"
3. **Paranoid Procedures** - Everything requires forms, committees, and oversight
4. **Prague-Specific References** - Local humor about tourists, beer, communist bureaucracy
5. **Self-Important Language** - Actors take their ridiculous missions extremely seriously

This transforms conspiracy theater from simple conflict into **absurdist bureaucratic comedy** where non-human entities are trapped in their own administrative paranoia while making impossible demands through proper channels.

## 🔧 Implementation Priority

1. **High Priority:** Enhanced name generation with bureaucratic complexity
2. **Medium Priority:** Prague-specific location humor
3. **Low Priority:** Paranoid procedural language additions

The key is making the names so absurdly bureaucratic that they become inherently funny while maintaining the anti-consensus conflict mechanics.