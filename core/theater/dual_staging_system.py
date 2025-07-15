#!/usr/bin/env python3
"""
Dual Staging System for Prague Spectral Theater
Implements three parallel staging approaches:
1. Scientific Data Theater - Educational, explanatory dialogues
2. Conspiracy Theater - Non-human actors with anti-consensus conflicts
3. Parallel Mode - Both systems together

This system ensures that the different persona generation approaches lead to
fundamentally different theatrical experiences.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import random

logger = logging.getLogger(__name__)

# Import conspiracy system
try:
    from core.conspiracy.non_human_actor_detector import NonHumanActorDetector
    from core.conspiracy.conspiracy_dialogue_generator import ConspiracyDialogueGenerator
except ImportError:
    logger.warning("Conspiracy system not available - falling back to basic functionality")
    NonHumanActorDetector = None
    ConspiracyDialogueGenerator = None

@dataclass
class StageConfiguration:
    """Configuration for a specific staging approach"""
    name: str
    description: str
    dialogue_style: str
    conflict_intensity: str
    educational_focus: bool
    emotional_focus: bool
    data_explanation_required: bool
    trauma_expression_required: bool

class DualStagingSystem:
    """
    Manages two parallel staging systems with distinct theatrical approaches
    """
    
    def __init__(self):
        self.scientific_stage = StageConfiguration(
            name="Scientific Data Theater",
            description="Educational dialogues where personas explain spectral data scientifically",
            dialogue_style="explanatory_scientific",
            conflict_intensity="low_to_medium",
            educational_focus=True,
            emotional_focus=False,
            data_explanation_required=True,
            trauma_expression_required=False
        )
        
        self.conspiracy_stage = StageConfiguration(
            name="Conspiracy Theater",
            description="Non-human actors use data as conspiracy evidence for impossible conflicts",
            dialogue_style="anti_consensus_confrontational",
            conflict_intensity="extreme_to_absurd",
            educational_focus=False,
            emotional_focus=False,
            data_explanation_required=False,
            trauma_expression_required=False
        )
        
        self.current_stage = None
        self.active_personas = []
        self.staging_history = []
        
        # Initialize conspiracy system if available
        self.conspiracy_detector = NonHumanActorDetector() if NonHumanActorDetector else None
        self.conspiracy_dialogue = None  # Will be initialized with API key when needed
    
    def set_staging_mode(self, mode: str, personas: List[Dict], api_key: str = None) -> bool:
        """Set the staging mode and configure personas accordingly"""
        try:
            if mode == "scientific_data":
                self.current_stage = self.scientific_stage
                self.active_personas = self._configure_personas_for_scientific_stage(personas)
                logger.info("🌈 Configured Scientific Data Theater staging")
                
            elif mode == "conspiracy_theater":
                self.current_stage = self.conspiracy_stage
                self.active_personas = self._configure_personas_for_conspiracy_stage(personas)
                if api_key and ConspiracyDialogueGenerator:
                    self.conspiracy_dialogue = ConspiracyDialogueGenerator(api_key)
                logger.info("🕵️ Configured Conspiracy Theater staging")
                
            elif mode == "parallel_dual":
                # Special mode that maintains both staging approaches simultaneously
                self.current_stage = "dual_parallel"
                self.active_personas = self._configure_personas_for_dual_stage(personas)
                if api_key and ConspiracyDialogueGenerator:
                    self.conspiracy_dialogue = ConspiracyDialogueGenerator(api_key)
                logger.info("⚔️ Configured Parallel Dual staging")
                
            else:
                logger.error(f"Unknown staging mode: {mode}")
                return False
                
            return True
            
        except Exception as e:
            logger.error(f"Error setting staging mode: {e}")
            return False
    
    def _configure_personas_for_scientific_stage(self, personas: List[Dict]) -> List[Dict]:
        """Configure personas for scientific data theater"""
        configured_personas = []
        
        for persona in personas:
            if persona.get('type') == 'spectral_multiplicity':
                # Enhance for scientific explanation
                enhanced_persona = persona.copy()
                enhanced_persona['staging_mode'] = 'scientific_data'
                enhanced_persona['dialogue_requirements'] = {
                    'must_explain_data': True,
                    'must_cite_indices': True,
                    'must_provide_context': True,
                    'educational_tone': True,
                    'conflict_level': 'constructive'
                }
                enhanced_persona['performance_style'] = 'scientific_educator'
                configured_personas.append(enhanced_persona)
                
        return configured_personas
    
    def _configure_personas_for_conspiracy_stage(self, personas: List[Dict]) -> List[Dict]:
        """Configure personas for conspiracy theater"""
        configured_personas = []
        
        for persona in personas:
            if persona.get('type') == 'non_human_actor':
                # Enhance for anti-consensus confrontation
                enhanced_persona = persona.copy()
                enhanced_persona['staging_mode'] = 'conspiracy_theater'
                enhanced_persona['dialogue_requirements'] = {
                    'must_refuse_discussion': True,
                    'must_make_impossible_demands': True,
                    'must_use_data_as_conspiracy_evidence': True,
                    'anti_consensus_intensity': 'extreme',
                    'conflict_level': 'territorial_war'
                }
                enhanced_persona['performance_style'] = 'conspiracy_actor'
                configured_personas.append(enhanced_persona)
                
        return configured_personas
    
    def _configure_personas_for_dual_stage(self, personas: List[Dict]) -> List[Dict]:
        """Configure personas for dual parallel staging"""
        configured_personas = []
        
        # Separate by type and configure each appropriately
        for persona in personas:
            enhanced_persona = persona.copy()
            
            if persona.get('type') == 'spectral_multiplicity':
                enhanced_persona['staging_mode'] = 'scientific_data'
                enhanced_persona['dialogue_requirements'] = {
                    'must_explain_data': True,
                    'must_cite_indices': True,
                    'educational_tone': True,
                    'can_react_to_wounds': True  # Special: can respond to wound theater
                }
                enhanced_persona['performance_style'] = 'scientific_educator'
                
            elif persona.get('type') == 'non_human_actor':
                enhanced_persona['staging_mode'] = 'conspiracy_theater'
                enhanced_persona['dialogue_requirements'] = {
                    'must_refuse_discussion': True,
                    'must_make_impossible_demands': True,
                    'anti_consensus_intensity': 'extreme',
                    'can_attack_scientists': True  # Special: can attack scientific personas
                }
                enhanced_persona['performance_style'] = 'conspiracy_actor'
            
            configured_personas.append(enhanced_persona)
                
        return configured_personas
    
    def generate_staging_appropriate_prompt(self, persona1: Dict, persona2: Dict, topic: str) -> str:
        """Generate dialogue prompt appropriate for the current staging mode"""
        
        if self.current_stage == self.scientific_stage:
            return self._generate_scientific_prompt(persona1, persona2, topic)
            
        elif self.current_stage == self.conspiracy_stage:
            return self._generate_conspiracy_prompt(persona1, persona2, topic)
            
        elif self.current_stage == "dual_parallel":
            return self._generate_dual_prompt(persona1, persona2, topic)
            
        else:
            return f"Create a dialogue between {persona1['name']} and {persona2['name']} about {topic}"
    
    def _generate_scientific_prompt(self, persona1: Dict, persona2: Dict, topic: str) -> str:
        """Generate scientific data theater prompt"""
        
        # Get detailed spectral data for both personas
        indices1 = persona1.get('dominant_indices', {})
        indices2 = persona2.get('dominant_indices', {})
        
        return f"""
SCIENTIFIC DATA THEATER MODE - Educational Dialogue

Create a scientific, educational dialogue between two Prague spectral beings about: {topic}

PERSONA 1: {persona1['name']} from {persona1['location']}
Spectral Data: NDVI {indices1.get('NDVI', 0):.3f}, Urban_Index {indices1.get('Urban_Index', 0):.3f}

PERSONA 2: {persona2['name']} from {persona2['location']}  
Spectral Data: NDVI {indices2.get('NDVI', 0):.3f}, Urban_Index {indices2.get('Urban_Index', 0):.3f}

SCIENTIFIC THEATER REQUIREMENTS:
1. Each persona MUST explain their spectral indices in detail
2. They must educate each other and the audience about what the data means
3. Conflicts should be constructive and fact-based
4. Use phrases like "My NDVI reading of X.XXX indicates..." and "This means for Prague..."
5. Reference specific parts of their districts
6. Explain the scientific significance of differences in their data
7. Maintain educational tone while showing personality

Create 6 turns of educational dialogue where they compare and contrast their environmental data.
Focus on teaching the audience about spectral analysis while maintaining character.

Format as:
{persona1['name']}: [scientific explanation with data]
{persona2['name']}: [educational response with comparative data]
"""
    
    def _generate_conspiracy_prompt(self, persona1: Dict, persona2: Dict, topic: str) -> str:
        """Generate conspiracy theater prompt"""
        
        # Get conspiracy information
        agenda1 = persona1.get('agenda', 'Unknown agenda')
        agenda2 = persona2.get('agenda', 'Unknown agenda')
        evidence1 = persona1.get('conspiracy_evidence', 'Unknown evidence')
        evidence2 = persona2.get('conspiracy_evidence', 'Unknown evidence')
        
        return f"""
CONSPIRACY THEATER MODE - Anti-Consensus Confrontation

Create an impossible conflict between two Prague non-human actors about: {topic}

ACTOR 1: {persona1['name']} from {persona1['location']}
Actor Category: {persona1.get('actor_category', 'Unknown')}
Agenda: {agenda1}
Conspiracy Evidence: {evidence1}
Impossible Demands: {persona1.get('impossible_demands', ['Unknown demands'])}

ACTOR 2: {persona2['name']} from {persona2['location']}
Actor Category: {persona2.get('actor_category', 'Unknown')}
Agenda: {agenda2}
Conspiracy Evidence: {evidence2}
Impossible Demands: {persona2.get('impossible_demands', ['Unknown demands'])}

CONSPIRACY THEATER REQUIREMENTS:
1. Actors use satellite data as CONSPIRACY EVIDENCE, not scientific explanation
2. They REFUSE all rational discussion and compromise
3. Each makes IMPOSSIBLE territorial demands that contradict the other
4. Escalate through increasingly ABSURD accusations
5. Focus on territorial conflicts and conspiracy theories
6. No consensus-building or problem-solving allowed
7. Data becomes proof of secret agendas, not environmental measurements

Create 6 turns of escalating territorial conflict where they refuse to discuss rationally.
Focus on impossible demands and conspiracy accusations, not education.

Format as:
{persona1['name']}: [territorial claim using data as conspiracy evidence]
{persona2['name']}: [counter-claim with impossible demand and refusal to negotiate]
"""
    
    def _generate_dual_prompt(self, persona1: Dict, persona2: Dict, topic: str) -> str:
        """Generate dual staging prompt with both approaches"""
        
        # Determine which persona is which type
        scientific_persona = None
        wound_persona = None
        conspiracy_persona = None
        
        if persona1.get('type') == 'spectral_multiplicity':
            scientific_persona = persona1
        if persona1.get('type') == 'spectral_wound_theater':
            wound_persona = persona1
        if persona1.get('type') == 'non_human_actor':
            conspiracy_persona = persona1
            
        if persona2.get('type') == 'spectral_multiplicity':
            scientific_persona = persona2
        if persona2.get('type') == 'spectral_wound_theater':
            wound_persona = persona2
        if persona2.get('type') == 'non_human_actor':
            conspiracy_persona = persona2
        
        if scientific_persona and conspiracy_persona:
            # Cross-system dialogue
            return f"""
DUAL PARALLEL THEATER MODE - Science vs Conspiracy Confrontation

Create a confrontation between a scientific data persona and a conspiracy actor about: {topic}

SCIENTIFIC PERSONA: {scientific_persona['name']} from {scientific_persona['location']}
- Explains data scientifically and educationally
- Tries to be rational and fact-based
- Spectral Data: {scientific_persona.get('dominant_indices', {})}

CONSPIRACY ACTOR: {conspiracy_persona['name']} from {conspiracy_persona['location']}
- Uses data as conspiracy evidence
- Agenda: {conspiracy_persona.get('agenda', 'Unknown')}
- Refuses rational discussion completely

DUAL THEATER DYNAMICS:
1. Scientific persona tries to educate and explain rationally
2. Conspiracy actor refuses discussion and makes impossible demands
3. Scientific persona gets frustrated by anti-rational responses
4. Conspiracy actor sees scientific approach as part of the conspiracy
5. Creates tension between rational analysis and conspiracy thinking
6. Both use same spectral data but interpret it completely differently

Create 8 turns showing the clash between scientific rationality and conspiracy paranoia.

Format as:
{scientific_persona['name']}: [rational scientific explanation]
{conspiracy_persona['name']}: [conspiracy accusation and refusal to discuss]
"""
        
        else:
            # Same-system dialogue within dual mode
            if persona1.get('type') == persona2.get('type') == 'spectral_multiplicity':
                return self._generate_scientific_prompt(persona1, persona2, topic)
            elif persona1.get('type') == persona2.get('type') == 'non_human_actor':
                return self._generate_conspiracy_prompt(persona1, persona2, topic)
            else:
                return f"Create a dialogue between {persona1['name']} and {persona2['name']} about {topic}"
    
    def get_staging_recommendations(self, personas: List[Dict]) -> Dict[str, Any]:
        """Analyze personas and recommend optimal staging approach"""
        
        spectral_count = sum(1 for p in personas if p.get('type') == 'spectral_multiplicity')
        conspiracy_count = sum(1 for p in personas if p.get('type') == 'non_human_actor')
        
        recommendations = {
            "total_personas": len(personas),
            "spectral_multiplicity_count": spectral_count,
            "conspiracy_actor_count": conspiracy_count,
            "recommended_mode": None,
            "reasoning": "",
            "staging_options": []
        }
        
        if spectral_count > 0 and conspiracy_count == 0:
            recommendations["recommended_mode"] = "scientific_data"
            recommendations["reasoning"] = "All personas are spectral multiplicity type - perfect for educational data theater"
            recommendations["staging_options"] = ["scientific_data"]
            
        elif conspiracy_count > 0 and spectral_count == 0:
            recommendations["recommended_mode"] = "conspiracy_theater"
            recommendations["reasoning"] = "All personas are conspiracy actors - ideal for anti-consensus confrontation"
            recommendations["staging_options"] = ["conspiracy_theater"]
            
        elif spectral_count > 0 and conspiracy_count > 0:
            recommendations["recommended_mode"] = "parallel_dual"
            recommendations["reasoning"] = "Mixed persona types - dual staging creates maximum dramatic tension"
            recommendations["staging_options"] = ["parallel_dual", "scientific_data", "conspiracy_theater"]
            
        else:
            recommendations["recommended_mode"] = "scientific_data"
            recommendations["reasoning"] = "Default to scientific data theater"
            recommendations["staging_options"] = ["scientific_data"]
        
        return recommendations
    
    def get_current_stage_info(self) -> Dict[str, Any]:
        """Get information about the current staging configuration"""
        if self.current_stage == "dual_parallel":
            return {
                "mode": "dual_parallel",
                "name": "Dual Parallel Theater",
                "description": "Both scientific and wound theater approaches active",
                "active_personas": len(self.active_personas),
                "scientific_personas": len([p for p in self.active_personas if p.get('type') == 'spectral_multiplicity']),
                "conspiracy_actors": len([p for p in self.active_personas if p.get('type') == 'non_human_actor'])
            }
        elif self.current_stage:
            return {
                "mode": self.current_stage.dialogue_style,
                "name": self.current_stage.name,
                "description": self.current_stage.description,
                "active_personas": len(self.active_personas),
                "educational_focus": self.current_stage.educational_focus,
                "emotional_focus": self.current_stage.emotional_focus
            }
        else:
            return {"mode": "none", "name": "No staging configured"}
