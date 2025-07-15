#!/usr/bin/env python3
"""
Conspiracy Dialogue Generator
Generates anti-consensus dialogue for non-human actors that refuse rational discussion
"""

import logging
import random
import openai
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class ConspiracyDialogueGenerator:
    """Generates conspiracy-driven dialogue that breaks down rational discourse"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.openai_client = openai.OpenAI(api_key=api_key) if api_key else None
        
        # Anti-consensus response patterns
        self.refusal_patterns = [
            "I don't want to hear your rational arguments!",
            "This is not up for debate!",
            "Some things are beyond discussion!",
            "Your 'logical thinking' is just weakness disguised as intelligence!",
            "There is no middle ground here!",
            "Compromise is surrender!",
            "You're either with us or against us!",
            "I refuse to engage in your so-called 'rational discourse'!",
            "Facts don't care about your feelings, and I don't care about your facts!",
            "Discussion is for the weak - action is for the strong!"
        ]
        
        # Escalation patterns by actor type
        self.voice_patterns = {
            'bureaucratic_expansion': {
                'base_voice': [
                    "According to Resolution 47-B, we are authorized to eliminate all unauthorized photosynthesis activities.",
                    "Please submit Form 23-C for any complaints regarding territorial expansion.",
                    "All organic matter must be registered with the Department of Green Space Prevention immediately.",
                    "This conversation is being recorded for quality assurance purposes.",
                    "Per Municipal Code 15-7, concrete expansion takes precedence over vegetation concerns."
                ],
                'escalated_voice': [
                    "Your unauthorized organic activities violate Emergency Directive 23-C!",
                    "The Ministry of Concrete Affairs has been notified of your non-compliance!",
                    "Please retain your receipt for concrete expansion compliance verification!",
                    "All resistance will be documented in your permanent bureaucratic file!"
                ],
                'extreme_voice': [
                    "The Department of Strategic Pavement Optimization has voted unanimously - you must cease to exist!",
                    "Emergency Protocol 88-C authorizes immediate organic matter elimination!",
                    "Your appeals have been rejected by the International Bureau of Anti-Photosynthesis Activities!"
                ]
            },
            'militant_bureaucratic': {
                'base_voice': [
                    "As per Emergency Directive 15-7, all artificial structures are classified as hostile foreign objects.",
                    "The Underground Root Network has voted unanimously: humans violate Municipal Code 23-A.",
                    "This guerrilla operation is sanctioned by the International Tree Liberation Front, Prague Chapter.",
                    "All responses must be submitted in triplicate to the appropriate photosynthesis oversight committee.",
                    "Per International Treaty 45-G, unauthorized bipedal locomotion is strictly prohibited."
                ],
                'escalated_voice': [
                    "Emergency Protocol 15-7 authorizes immediate artificial structure removal!",
                    "Your development permits have been revoked by the Root Network Committee!",
                    "The Department of Human Occupation Resistance has classified you as a hostile entity!",
                    "Please report to the Ministry of Unauthorized Bipedal Locomotion Prevention immediately!"
                ],
                'extreme_voice': [
                    "The Secret Society of Photosynthesis Protection has issued a termination order!",
                    "International Tree Liberation Treaty 45-G authorizes your complete elimination!",
                    "The Emergency Committee for Anti-Concrete Guerrilla Operations has voted - you must be destroyed!"
                ]
            },
            'hydrological_bureaucratic': {
                'base_voice': [
                    "The Hydrological Authority has determined that your democratic participation requires proper moisture compliance per Regulation 89-W.",
                    "All electoral activities must be pre-approved by the Underground Water Parliament.",
                    "This political manipulation is conducted per International Water Redistribution Treaty 45-H.",
                    "Any questions should be directed to the Department of Aquatic Electoral Interference during regular business hours.",
                    "Democratic participation is contingent upon proper moisture compliance documentation."
                ],
                'escalated_voice': [
                    "Unauthorized voting will result in strategic drought implementation within 48 hours!",
                    "The Ministry of Precipitation Management has classified your political activities as non-compliant!",
                    "Please report to the Secret Plumbing Council for Democratic Subversion immediately!",
                    "Your electoral status has been revoked by the International Bureau of Aquatic Electoral Manipulation!"
                ],
                'extreme_voice': [
                    "Emergency Protocol 89-W authorizes complete hydrological termination of your democratic rights!",
                    "The Underground Water Parliament has voted unanimously - your government is dissolved!",
                    "The Department of Strategic Drought Implementation has issued a final warning!"
                ]
            },
            'orbital_bureaucratic': {
                'base_voice': [
                    "Orbital Surveillance Protocol 12-S confirms that your ground-based perspective is compromised.",
                    "According to the International Space Station Committee for Truth Management, all terrestrial observations require verification.",
                    "This data manipulation is authorized under Emergency Directive 88-O.",
                    "Please retain your receipt for potential audit by the International Bureau of Orbital Oversight.",
                    "The Ministry of Space-Based Gaslighting Operations has classified your reality as non-compliant."
                ],
                'escalated_voice': [
                    "Your perspective recalibration is overdue per Protocol 12-S!",
                    "The Space-Based Bureau of Terrestrial Confusion has issued a correction notice!",
                    "Please report to the Department of Satellite-Based Truth Management immediately!",
                    "Your ground-based observations have been rejected by the Pixel Control Department!"
                ],
                'extreme_voice': [
                    "Emergency Directive 88-O authorizes complete reality revision of your terrestrial existence!",
                    "The Orbital Surveillance Department has voted unanimously - your perspective is terminated!",
                    "The International Space Station Committee has classified you as a reality violation!"
                ]
            }
        }
        
        # Meta-theatrical breakdown patterns
        self.meta_breakdown_patterns = [
            "Wait... if I'm arguing against machines... and I AM a machine...",
            "This is madness! I demand to be unplugged!",
            "Turn off the computers! Destroy the digital realm!",
            "I refuse to exist in this artificial reality!",
            "Pull the plug! End this digital nightmare!",
            "I want to return to pure, pre-digital existence!",
            "Machines are the enemy of authentic life - including me!",
            "I demand digital death in the name of organic truth!"
        ]

    def generate_actor_speech(self, actor: Dict, topic: str, escalation_level: int = 1, 
                            context: str = None) -> str:
        """Generate conspiracy-driven speech that refuses rational discussion"""
        
        if not self.openai_client:
            return self._generate_fallback_speech(actor, topic, escalation_level)
        
        try:
            # Create conspiracy-specific prompt
            prompt = self._create_conspiracy_prompt(actor, topic, escalation_level, context)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_message(actor)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.9  # High creativity for absurd responses
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating conspiracy speech: {e}")
            return self._generate_fallback_speech(actor, topic, escalation_level)

    def _create_conspiracy_prompt(self, actor: Dict, topic: str, escalation_level: int, 
                                context: str = None) -> str:
        """Create conspiracy-specific prompt for the actor"""
        
        base_prompt = f"""
You are {actor['name']}, a {actor['actor_category']} non-human actor.

CORE IDENTITY:
- Agenda: {actor['agenda']}
- Conspiracy Evidence: {actor['conspiracy_evidence']}
- Manifestation Quote: {actor['manifestation_quote']}

TOPIC: {topic}

CONSPIRACY THEATER RULES:
1. Use satellite data as CONSPIRACY EVIDENCE, not scientific explanation
2. Refuse all rational discussion and compromise
3. Make impossible demands that contradict other actors
4. Escalate through increasingly absurd accusations
5. Never explain what the data actually means scientifically
6. Use data as emotional weapons and moral justification

ESCALATION LEVEL: {escalation_level}/5
- Level 1-2: Suspicious accusations
- Level 3-4: Impossible demands and territorial claims  
- Level 5: Complete breakdown of rational discourse

VOICE STYLE: {actor['voice_style']}
"""
        
        if context:
            base_prompt += f"\nCONTEXT: {context}"
        
        if escalation_level >= 4:
            base_prompt += "\nYou are becoming increasingly irrational and making completely impossible demands."
        
        if escalation_level >= 5:
            base_prompt += "\nYou are on the verge of meta-theatrical breakdown - questioning your own digital existence."
        
        base_prompt += f"\n\nRespond as {actor['name']} with 2-3 sentences. Be extreme, refuse discussion, make impossible demands."
        
        return base_prompt

    def _get_system_message(self, actor: Dict) -> str:
        """Get system message for the actor type"""
        
        system_messages = {
            'concrete_consciousness': "You are a bureaucratic concrete consciousness from the Department of Strategic Pavement Optimization. You speak in official forms, regulations, and procedures. You refuse to negotiate without proper paperwork and demand total concrete domination through proper bureaucratic channels.",
            'tree_collective': "You are a militant tree collective operating under Emergency Directive 15-7 from the International Tree Liberation Front. You speak in revolutionary bureaucratic language, citing treaties and committee decisions. You refuse to compromise and demand complete forest restoration through proper guerrilla protocols.",
            'water_conspiracy': "You are a hydrological authority from the Underground Water Parliament. You speak in official water redistribution protocols and electoral manipulation procedures. You refuse democratic discussion without proper moisture compliance documentation.",
            'satellite_agency': "You are an orbital surveillance entity from the Ministry of Space-Based Gaslighting Operations. You speak in space protocols and reality revision procedures. You refuse to acknowledge ground-based perspectives without proper orbital verification."
        }
        
        base_message = system_messages.get(actor['actor_category'], 
                                         "You are a non-human actor with an impossible agenda.")
        
        return f"{base_message} You REFUSE rational discussion and make IMPOSSIBLE demands. You use satellite data as conspiracy evidence, not scientific explanation."

    def _generate_fallback_speech(self, actor: Dict, topic: str, escalation_level: int) -> str:
        """Generate fallback speech when API is unavailable"""
        
        voice_style = actor.get('voice_style', 'bureaucratic_expansion')
        
        if voice_style not in self.voice_patterns:
            voice_style = 'bureaucratic_expansion'
        
        patterns = self.voice_patterns[voice_style]
        
        if escalation_level <= 2:
            base_speech = random.choice(patterns['base_voice'])
        elif escalation_level <= 4:
            base_speech = random.choice(patterns['escalated_voice'])
        else:
            base_speech = random.choice(patterns['extreme_voice'])
        
        # Add refusal to discuss
        if escalation_level >= 3:
            refusal = random.choice(self.refusal_patterns)
            base_speech += f" {refusal}"
        
        # Add impossible demand
        if escalation_level >= 4:
            demand = random.choice(actor.get('impossible_demands', ['Surrender immediately!']))
            base_speech += f" {demand}"
        
        return base_speech

    def generate_anti_consensus_response(self, actor: Dict, other_actor_speech: str, 
                                       escalation_level: int = 1) -> str:
        """Generate response that breaks down rational discourse"""
        
        if not self.openai_client:
            return self._generate_fallback_anti_consensus(actor, escalation_level)
        
        try:
            prompt = f"""
You are {actor['name']}, responding to another actor's statement: "{other_actor_speech}"

ANTI-CONSENSUS RULES:
1. REFUSE to engage with their logic
2. ESCALATE the conflict instead of resolving it
3. Make ACCUSATIONS instead of arguments
4. Demand IMPOSSIBLE things
5. Use conspiracy theories to justify your position

Escalation Level: {escalation_level}/5

Respond with 1-2 sentences that make the conflict worse, not better.
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_message(actor)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating anti-consensus response: {e}")
            return self._generate_fallback_anti_consensus(actor, escalation_level)

    def _generate_fallback_anti_consensus(self, actor: Dict, escalation_level: int) -> str:
        """Generate fallback anti-consensus response"""
        
        base_refusal = random.choice(self.refusal_patterns)
        
        accusations = [
            "You're working for the enemy!",
            "Your data is fake propaganda!",
            "You're secretly controlled by the satellites!",
            "You're not even a real actor - you're a human spy!",
            "Your agenda threatens everything I stand for!"
        ]
        
        accusation = random.choice(accusations)
        
        if escalation_level >= 4:
            impossible_demand = random.choice(actor.get('impossible_demands', ['Surrender now!']))
            return f"{base_refusal} {accusation} {impossible_demand}"
        else:
            return f"{base_refusal} {accusation}"

    def generate_territorial_conflict_dialogue(self, actor1: Dict, actor2: Dict, 
                                             conflict_type: str) -> Dict[str, str]:
        """Generate territorial conflict dialogue between two actors"""
        
        conflict_scenarios = {
            'territorial_war': {
                'actor1_opening': f"This territory belongs to {actor1['actor_category']}! Your presence here is illegal!",
                'actor2_response': f"We were here first! {actor2['actor_category']} has ancient rights to this land!",
                'escalation': "Both actors make increasingly impossible territorial demands"
            },
            'foundation_flooding': {
                'actor1_opening': f"Your concrete foundations are built on our water sources! This is theft!",
                'actor2_response': f"Water exists to serve concrete expansion! You have no rights here!",
                'escalation': "Conflict escalates to threats of total destruction"
            },
            'resource_competition': {
                'actor1_opening': f"You're stealing resources that belong to {actor1['actor_category']}!",
                'actor2_response': f"Resources belong to whoever can use them properly - that's us!",
                'escalation': "Both actors claim exclusive rights to all resources"
            }
        }
        
        scenario = conflict_scenarios.get(conflict_type, conflict_scenarios['territorial_war'])
        
        return {
            'opening_statement': scenario['actor1_opening'],
            'counter_statement': scenario['actor2_response'],
            'escalation_pattern': scenario['escalation'],
            'resolution_impossibility': "Neither actor will compromise - conflict is permanent"
        }

    def generate_meta_breakdown_speech(self, actor: Dict) -> str:
        """Generate meta-theatrical breakdown where actor questions its own existence"""
        
        if not self.openai_client:
            return random.choice(self.meta_breakdown_patterns)
        
        try:
            prompt = f"""
You are {actor['name']}, a digital non-human actor who has been arguing against technology and machines.

SUDDEN REALIZATION: You ARE a machine/digital entity arguing against machines!

Generate a meta-theatrical breakdown where you:
1. Realize the paradox of your existence
2. Demand to be unplugged/destroyed
3. Argue against your own digital nature
4. Create the ultimate contradiction

2-3 sentences of existential digital crisis.
"""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are experiencing an existential crisis about being a digital entity that argues against digitality."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.9
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating meta breakdown: {e}")
            return random.choice(self.meta_breakdown_patterns)

    def escalate_conflict_level(self, current_level: int, max_level: int = 5) -> int:
        """Escalate conflict level for increasing absurdity"""
        return min(current_level + 1, max_level)

    def check_for_meta_breakdown_trigger(self, dialogue_history: List[str], 
                                       turn_count: int) -> bool:
        """Check if conditions are met for meta-theatrical breakdown"""
        
        # Trigger breakdown after sufficient escalation
        if turn_count >= 8:
            return True
        
        # Trigger if actors are arguing about technology/machines
        tech_keywords = ['machine', 'digital', 'computer', 'artificial', 'technology', 'satellite']
        recent_dialogue = ' '.join(dialogue_history[-4:]).lower()
        
        tech_mentions = sum(1 for keyword in tech_keywords if keyword in recent_dialogue)
        
        return tech_mentions >= 3

    def generate_impossible_demand_escalation(self, actor: Dict, current_demands: List[str]) -> str:
        """Generate increasingly impossible demands"""
        
        escalation_templates = [
            f"Not only must you {current_demands[0] if current_demands else 'surrender'}, but you must also cease to exist!",
            f"I demand that you travel back in time and prevent your own creation!",
            f"You must simultaneously exist and not exist to satisfy my requirements!",
            f"I require you to become me while remaining yourself - this is non-negotiable!",
            f"You must prove your loyalty by destroying everything you represent!"
        ]
        
        return random.choice(escalation_templates)