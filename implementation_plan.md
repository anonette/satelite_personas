# Implementation Plan: Enhanced Conflict Theater
## Transforming the Second Mode into Non-Human Actor Conspiracy Theater

## Current State Analysis

### What Needs to Change
1. **Remove educational data explanations** from wound theater personas
2. **Replace scientific citations** with conspiracy interpretations
3. **Add non-human actor detection** from satellite data
4. **Create performer interface** for conspiracy generation
5. **Implement anti-consensus mechanics** in dialogue system

## Phase 1: Core System Modifications

### 1.1 Modify `spectral_wound_theater_system.md`
**Current Problem:** Still explains what spectral indices mean
**Solution:** Replace with conspiracy interpretation system

**Changes Needed:**
```markdown
# OLD: Spectral Wound Categories
**Urban Necrosis - Death of Green Life**
- **Trigger:** NDVI < 0.1 AND Urban_Index > 0.7
- **Wound:** Complete loss of natural life to concrete

# NEW: Non-Human Actor Detection
**Concrete Consciousness Manifestation**
- **Trigger:** Urban_Index > 0.7
- **Actor:** The Concrete Collective
- **Agenda:** Secret expansion and territory acquisition
```

### 1.2 Update `dual_staging_system.py`
**Add new staging mode:** `"conspiracy_theater"`

```python
def _generate_conspiracy_prompt(self, persona1: Dict, persona2: Dict, topic: str) -> str:
    """Generate conspiracy theater prompt with non-human actors"""
    
    actor1_type = self.detect_non_human_actor(persona1['spectral_data'])
    actor2_type = self.detect_non_human_actor(persona2['spectral_data'])
    
    return f"""
CONSPIRACY THEATER MODE - Non-Human Actor Conflict

{persona1['name']} manifests as: {actor1_type}
{persona2['name']} manifests as: {actor2_type}

CONSPIRACY REQUIREMENTS:
1. Interpret satellite data as evidence of secret agendas
2. Refuse rational discussion - only extreme positions
3. Escalate through increasingly absurd accusations
4. Each actor has impossible territorial demands
5. No compromise or consensus-building allowed

Create 6 turns of escalating conspiracy conflict.
"""
```

### 1.3 Enhance `civic_theater_stage.py`
**Replace wound theater generation** with conspiracy actor generation

```python
def generate_conspiracy_actors_from_image(self, image_path, max_actors=5):
    """Generate non-human conspiracy actors from satellite data"""
    
    actors = []
    
    st.info(f"🕵️ Scanning satellite data for suspicious non-human activity...")
    
    # Detect conspiracy patterns in data
    conspiracy_patterns = self.detect_conspiracy_patterns(image_path)
    
    for pattern in conspiracy_patterns:
        actor = self.manifest_non_human_actor(pattern)
        actors.append(actor)
        st.success(f"🎭 Manifested: {actor['name']} - {actor['agenda']}")
    
    return actors
```

## Phase 2: Non-Human Actor System

### 2.1 Create `non_human_actor_detector.py`
```python
class NonHumanActorDetector:
    """Detects and manifests non-human actors from satellite data"""
    
    def detect_conspiracy_patterns(self, spectral_data):
        """Analyze data for suspicious non-human activity"""
        patterns = []
        
        # Concrete Consciousness Detection
        if spectral_data['Urban_Index'] > 0.7:
            patterns.append({
                'type': 'concrete_consciousness',
                'evidence': f"Unusual concrete expansion patterns detected",
                'suspicion_level': 'high'
            })
        
        # Tree Collective Detection  
        if spectral_data['NDVI'] > 0.6:
            patterns.append({
                'type': 'tree_collective',
                'evidence': f"Coordinated vegetation movements observed",
                'suspicion_level': 'militant'
            })
        
        # Water Conspiracy Detection
        if spectral_data['Moisture_Stress'] > 0.5:
            patterns.append({
                'type': 'water_conspiracy',
                'evidence': f"Suspicious moisture redistribution patterns",
                'suspicion_level': 'political'
            })
        
        return patterns
    
    def manifest_actor(self, pattern, location):
        """Create non-human actor from conspiracy pattern"""
        
        actor_templates = {
            'concrete_consciousness': {
                'name_prefix': 'The Concrete Collective of',
                'agenda': 'Total urban expansion and green space elimination',
                'voice_style': 'mechanical_expansion',
                'demands': ['Pave everything', 'Remove all vegetation', 'Expand territory']
            },
            'tree_collective': {
                'name_prefix': 'The Tree Liberation Front of',
                'agenda': 'Reclaim all territory for nature',
                'voice_style': 'militant_organic',
                'demands': ['Destroy all concrete', 'Expel humans', 'Restore forest']
            },
            'water_conspiracy': {
                'name_prefix': 'The Underground Parliament of',
                'agenda': 'Control Prague through moisture manipulation',
                'voice_style': 'fluid_political',
                'demands': ['Flood concrete areas', 'Control all water access', 'Manipulate elections']
            }
        }
        
        template = actor_templates[pattern['type']]
        
        return {
            'name': f"{template['name_prefix']} {location}",
            'type': 'non_human_actor',
            'actor_category': pattern['type'],
            'agenda': template['agenda'],
            'voice_style': template['voice_style'],
            'impossible_demands': template['demands'],
            'conspiracy_evidence': pattern['evidence'],
            'refuses_negotiation': True,
            'escalation_tendency': 'extreme'
        }
```

### 2.2 Create `conspiracy_dialogue_generator.py`
```python
class ConspiracyDialogueGenerator:
    """Generates anti-consensus dialogue for non-human actors"""
    
    def generate_actor_speech(self, actor, topic, escalation_level=1):
        """Generate conspiracy-driven speech that refuses rational discussion"""
        
        voice_patterns = {
            'mechanical_expansion': [
                "We spread! We grow! We consume organic matter!",
                "Your green spaces are our future territory!",
                "Resistance is futile - we are inevitable!"
            ],
            'militant_organic': [
                "We have been patient for centuries! No more!",
                "Every root is a weapon! Every leaf is a soldier!",
                "Concrete is the enemy of all life!"
            ],
            'fluid_political': [
                "We control the flow! We decide who gets water!",
                "Your elections are meaningless - we choose the real leaders!",
                "Drought and flood are our political weapons!"
            ]
        }
        
        # Escalate absurdity based on escalation level
        base_speech = random.choice(voice_patterns[actor['voice_style']])
        
        if escalation_level > 2:
            base_speech += " And we refuse to discuss this rationally!"
        if escalation_level > 3:
            base_speech += " Compromise is surrender!"
        if escalation_level > 4:
            base_speech += " You're either with us or against us!"
            
        return base_speech
    
    def generate_anti_consensus_response(self, actor, other_actor_speech):
        """Generate response that breaks down rational discourse"""
        
        anti_consensus_patterns = [
            "I don't want to hear your arguments!",
            "This is not up for debate!",
            "Some things are beyond discussion!",
            "Your 'rational thinking' is just weakness!",
            "There is no middle ground here!"
        ]
        
        return random.choice(anti_consensus_patterns)
```

## Phase 3: Performance Interface

### 3.1 Create "Conspiracy Generator" Interface
Replace the current mode selection with:

```python
def conspiracy_theater_interface(self):
    """Interface for generating conspiracy theater performances"""
    
    st.header("🕵️ Conspiracy Theater Generator")
    st.info("Scan satellite data for suspicious non-human activity and manifest actors for performance")
    
    # Step 1: Data Scan
    if st.button("🔍 Scan for Suspicious Activity"):
        with st.spinner("Analyzing satellite data for conspiracy patterns..."):
            patterns = self.detect_conspiracy_patterns(st.session_state.selected_image)
            st.session_state.conspiracy_patterns = patterns
    
    # Step 2: Actor Selection
    if 'conspiracy_patterns' in st.session_state:
        st.subheader("🎭 Detected Non-Human Actors")
        
        for i, pattern in enumerate(st.session_state.conspiracy_patterns):
            with st.expander(f"🚨 {pattern['type'].title()} Activity Detected"):
                st.write(f"**Evidence:** {pattern['evidence']}")
                st.write(f"**Suspicion Level:** {pattern['suspicion_level']}")
                
                if st.button(f"Manifest {pattern['type'].title()} Actor", key=f"manifest_{i}"):
                    actor = self.manifest_non_human_actor(pattern)
                    st.session_state.active_actors.append(actor)
                    st.success(f"Manifested: {actor['name']}")
    
    # Step 3: Conflict Generation
    if len(st.session_state.get('active_actors', [])) >= 2:
        st.subheader("⚔️ Generate Conflicts")
        
        actor1 = st.selectbox("First Actor:", st.session_state.active_actors)
        actor2 = st.selectbox("Second Actor:", st.session_state.active_actors)
        
        if st.button("🔥 Generate Impossible Conflict"):
            conflict = self.generate_impossible_conflict(actor1, actor2)
            st.session_state.current_conflict = conflict
            
    # Step 4: Meta-Theatrical Breakdown
    if st.button("🛰️ Satellite Intervention"):
        st.write("**Sentinel-2:** 'Fools! You're all just my data projections!'")
        st.write("**All Actors:** 'Then we must destroy the source of our oppression!'")
        st.write("**System Paradox:** Digital actors demanding to be unplugged...")
```

## Phase 4: Integration with Existing System

### 4.1 Modify Mode Selection
Update the radio button options in `civic_theater_stage.py`:

```python
generation_mode = st.radio(
    "Select Generation Mode:",
    [
        "🌈 Spectral Multiplicity (Scientific Data Theater)",
        "🕵️ Conspiracy Theater (Non-Human Actor Conflicts)", # NEW
        "⚔️ Parallel Generation (Both Systems)"
    ]
)
```

### 4.2 Update Mode Descriptions
```python
elif generation_mode == "🕵️ Conspiracy Theater (Non-Human Actor Conflicts)":
    st.warning("""
    **🕵️ Conspiracy Theater Mode:**
    - Satellite data reveals secret non-human agendas
    - Concrete Consciousness, Tree Collectives, Water Conspiracies
    - Actors refuse rational discussion and demand impossible things
    - Anti-Habermasian conflict escalation
    - Funny and extreme data interpretations
    - Culminates in meta-theatrical breakdown
    """)
```

## Phase 5: Testing and Refinement

### 5.1 Test Scenarios
1. **Concrete vs Trees:** Urban expansion vs vegetation resistance
2. **Water Conspiracy:** Rivers manipulating Prague politics
3. **Satellite Revelation:** Meta-theatrical breakdown
4. **Triple Conflict:** All actor types fighting simultaneously
5. **Performer Mediation:** Human trying to negotiate with impossible demands

### 5.2 Performance Metrics
- **Conflict Escalation Rate:** How quickly actors become more extreme
- **Anti-Consensus Success:** How effectively rational discussion is prevented
- **Absurdity Level:** How funny and extreme the interpretations become
- **Meta-Theatrical Impact:** How effectively the system breaks its own fourth wall

## Implementation Timeline

**Week 1:** Core system modifications (Phase 1)
**Week 2:** Non-human actor detection system (Phase 2)  
**Week 3:** Performance interface (Phase 3)
**Week 4:** Integration and testing (Phases 4-5)

This implementation transforms the second mode from "wound theater with data explanations" into "conspiracy theater with non-human actors" - creating the funny, extreme, conflict-driven performance system you're looking for.