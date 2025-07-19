"""
Ethical Dative Grammar System
Implements ethical dative positioning for non-human agency in spectral personas
"""

from typing import Dict, List, Optional
from enum import Enum
import random

class RhetoricalMode(Enum):
    ETHICAL_DATIVE = "ethical_dative"
    ADMINISTRATIVE = "administrative" 
    SARCASTIC = "sarcastic"
    ELEGIAC = "elegiac"
    FORENSIC = "forensic"

class EthicalDativeGenerator:
    """Generates ethical dative constructions for spectral band personas"""
    
    def __init__(self):
        self.language_patterns = {
            "czech": {
                "dative_marker": "na mně",
                "dative_marker_plural": "na nás",
                "temporal_markers": ["právě teď", "postupně", "rychle", "pomalu"],
                "intensity_modifiers": ["silně", "jemně", "dramaticky", "nenápadně"]
            },
            "english": {
                "dative_marker": "on me",
                "dative_marker_plural": "on us", 
                "temporal_markers": ["right now", "gradually", "rapidly", "slowly"],
                "intensity_modifiers": ["intensely", "gently", "dramatically", "subtly"]
            },
            "german": {
                "dative_marker": "mir",
                "dative_marker_plural": "uns",
                "temporal_markers": ["gerade jetzt", "allmählich", "schnell", "langsam"],
                "intensity_modifiers": ["stark", "sanft", "dramatisch", "unauffällig"]
            }
        }
        
        self.action_templates = {
            "environmental_change": {
                "czech": [
                    "{action} se děje—{dative} {modifier}",
                    "{action}—{dative} {temporal}",
                    "Cítím, jak {action}—{dative}"
                ],
                "english": [
                    "{action} happens—{dative} {modifier}",
                    "{action}—{dative} {temporal}",
                    "I feel {action}—{dative}"
                ],
                "german": [
                    "{action} geschieht—{dative} {modifier}",
                    "{action}—{dative} {temporal}",
                    "Ich spüre {action}—{dative}"
                ]
            },
            "observation": {
                "czech": [
                    "Vidím, jak {action}—{dative}",
                    "{action} se odehrává—{dative}",
                    "Registruji {action}—{dative}"
                ],
                "english": [
                    "I see {action}—{dative}",
                    "{action} unfolds—{dative}",
                    "I register {action}—{dative}"
                ],
                "german": [
                    "Ich sehe {action}—{dative}",
                    "{action} entfaltet sich—{dative}",
                    "Ich registriere {action}—{dative}"
                ]
            },
            "accusation": {
                "czech": [
                    "{action} způsobuje škodu—{dative}",
                    "Kvůli {action} trpím—{dative}",
                    "{action} narušuje—{dative} rovnováhu"
                ],
                "english": [
                    "{action} causes harm—{dative}",
                    "Because of {action} I suffer—{dative}",
                    "{action} disrupts—{dative} balance"
                ],
                "german": [
                    "{action} verursacht Schaden—{dative}",
                    "Wegen {action} leide ich—{dative}",
                    "{action} stört—{dative} Gleichgewicht"
                ]
            }
        }
        
        self.band_specific_actions = {
            "B02": {
                "czech": ["mlha se usazuje", "znečištění stoupá", "atmosféra se kalí"],
                "english": ["haze settles", "pollution rises", "atmosphere clouds"],
                "german": ["Dunst setzt sich", "Verschmutzung steigt", "Atmosphäre trübt sich"]
            },
            "B08": {
                "czech": ["listy žloutnou", "vegetace slábne", "chlorofyl mizí"],
                "english": ["leaves yellow", "vegetation weakens", "chlorophyll disappears"],
                "german": ["Blätter vergilben", "Vegetation schwächt", "Chlorophyll verschwindet"]
            },
            "B11": {
                "czech": ["voda mizí", "půda vysychá", "vlhkost klesá"],
                "english": ["water disappears", "soil dries", "moisture drops"],
                "german": ["Wasser verschwindet", "Boden trocknet", "Feuchtigkeit sinkt"]
            },
            "B12": {
                "czech": ["beton se šíří", "zástavba roste", "město expanduje"],
                "english": ["concrete spreads", "development grows", "city expands"],
                "german": ["Beton breitet sich", "Bebauung wächst", "Stadt expandiert"]
            }
        }
    
    def generate_ethical_positioning(self, 
                                   band_id: str,
                                   action_type: str,
                                   language: str = "czech",
                                   intensity: float = 0.5,
                                   is_plural: bool = False) -> str:
        """Generate ethical dative construction for specific context"""
        
        if language not in self.language_patterns:
            language = "czech"
            
        patterns = self.language_patterns[language]
        dative_marker = patterns["dative_marker_plural"] if is_plural else patterns["dative_marker"]
        
        # Select appropriate action
        actions = self.band_specific_actions.get(band_id, {}).get(language, ["změny se dějí"])
        action = random.choice(actions)
        
        # Select template based on action type
        templates = self.action_templates.get(action_type, self.action_templates["observation"])
        template = random.choice(templates[language])
        
        # Select modifiers based on intensity
        if intensity > 0.7:
            modifier = patterns["intensity_modifiers"][2]  # dramatic
            temporal = patterns["temporal_markers"][2]    # rapid
        elif intensity > 0.4:
            modifier = patterns["intensity_modifiers"][0]  # intense
            temporal = patterns["temporal_markers"][1]    # gradual
        else:
            modifier = patterns["intensity_modifiers"][1]  # gentle
            temporal = patterns["temporal_markers"][3]    # slow
            
        # Format the template
        try:
            result = template.format(
                action=action,
                dative=dative_marker,
                modifier=modifier,
                temporal=temporal
            )
        except KeyError:
            # Fallback to simple construction
            result = f"{action}—{dative_marker}"
            
        return result
    
    def generate_rhetorical_response(self,
                                   band_id: str,
                                   rhetorical_mode: RhetoricalMode,
                                   context: str,
                                   language: str = "czech",
                                   intensity: float = 0.5) -> str:
        """Generate response based on rhetorical mode"""
        
        if rhetorical_mode == RhetoricalMode.ETHICAL_DATIVE:
            return self.generate_ethical_positioning(band_id, "observation", language, intensity)
            
        elif rhetorical_mode == RhetoricalMode.FORENSIC:
            return self.generate_ethical_positioning(band_id, "accusation", language, intensity)
            
        elif rhetorical_mode == RhetoricalMode.ELEGIAC:
            return self._generate_elegiac_response(band_id, language, intensity)
            
        elif rhetorical_mode == RhetoricalMode.ADMINISTRATIVE:
            return self._generate_administrative_response(band_id, language, intensity)
            
        elif rhetorical_mode == RhetoricalMode.SARCASTIC:
            return self._generate_sarcastic_response(band_id, language, intensity)
            
        else:
            return self.generate_ethical_positioning(band_id, "observation", language, intensity)
    
    def _generate_elegiac_response(self, band_id: str, language: str, intensity: float) -> str:
        """Generate mourning/lamenting response"""
        elegiac_patterns = {
            "czech": [
                "Vzpomínám, jak to bývalo jiné—na mně",
                "Oplakávám to, co mizí—na mně",
                "Truchlím nad ztrátou—na mně"
            ],
            "english": [
                "I remember how it used to be different—on me",
                "I mourn what disappears—on me", 
                "I grieve the loss—on me"
            ],
            "german": [
                "Ich erinnere mich, wie es anders war—mir",
                "Ich betrauere was verschwindet—mir",
                "Ich trauere um den Verlust—mir"
            ]
        }
        
        patterns = elegiac_patterns.get(language, elegiac_patterns["czech"])
        return random.choice(patterns)
    
    def _generate_administrative_response(self, band_id: str, language: str, intensity: float) -> str:
        """Generate bureaucratic/procedural response"""
        admin_patterns = {
            "czech": [
                "Eviduji změny—na mně podle protokolu",
                "Registruji odchylky—na mně v souladu s předpisy",
                "Dokumentuji proces—na mně dle směrnic"
            ],
            "english": [
                "I record changes—on me according to protocol",
                "I register deviations—on me in compliance with regulations",
                "I document the process—on me per guidelines"
            ],
            "german": [
                "Ich erfasse Änderungen—mir gemäß Protokoll",
                "Ich registriere Abweichungen—mir regelkonform",
                "Ich dokumentiere den Prozess—mir nach Richtlinien"
            ]
        }
        
        patterns = admin_patterns.get(language, admin_patterns["czech"])
        return random.choice(patterns)
    
    def _generate_sarcastic_response(self, band_id: str, language: str, intensity: float) -> str:
        """Generate ironic/sarcastic response"""
        sarcastic_patterns = {
            "czech": [
                "Jak překvapivé, další změna—na mně",
                "Zase něco 'nového'—na mně",
                "Ach, pokrok—na mně jako vždy"
            ],
            "english": [
                "How surprising, another change—on me",
                "Something 'new' again—on me",
                "Ah, progress—on me as always"
            ],
            "german": [
                "Wie überraschend, eine weitere Änderung—mir",
                "Wieder etwas 'Neues'—mir",
                "Ach, Fortschritt—mir wie immer"
            ]
        }
        
        patterns = sarcastic_patterns.get(language, sarcastic_patterns["czech"])
        return random.choice(patterns)
    
    def create_multi_persona_dialogue(self,
                                    personas: List[Dict],
                                    conflict_type: str,
                                    language: str = "czech") -> List[Dict]:
        """Generate dialogue between multiple personas using ethical dative"""
        
        dialogue = []
        
        for i, persona in enumerate(personas):
            band_id = persona.get("band_id", "B08")
            rhetorical_mode = RhetoricalMode(persona.get("rhetorical_mode", "ethical_dative"))
            intensity = persona.get("ethical_intensity", 0.5)
            
            if conflict_type == "accusation" and i > 0:
                # Later personas respond to earlier ones
                response = self.generate_rhetorical_response(
                    band_id, RhetoricalMode.FORENSIC, "", language, intensity
                )
            else:
                response = self.generate_rhetorical_response(
                    band_id, rhetorical_mode, "", language, intensity
                )
            
            dialogue.append({
                "speaker": persona.get("character", band_id),
                "band_id": band_id,
                "response": response,
                "rhetorical_mode": rhetorical_mode.value,
                "language": language
            })
        
        return dialogue
    
    def translate_ethical_construction(self, 
                                     construction: str,
                                     from_language: str,
                                     to_language: str) -> str:
        """Translate ethical dative construction between languages"""
        
        # Simple pattern-based translation for ethical dative markers
        translations = {
            ("czech", "english"): {"na mně": "on me", "na nás": "on us"},
            ("english", "czech"): {"on me": "na mně", "on us": "na nás"},
            ("czech", "german"): {"na mně": "mir", "na nás": "uns"},
            ("german", "czech"): {"mir": "na mně", "uns": "na nás"},
            ("english", "german"): {"on me": "mir", "on us": "uns"},
            ("german", "english"): {"mir": "on me", "uns": "on us"}
        }
        
        translation_map = translations.get((from_language, to_language), {})
        
        result = construction
        for source, target in translation_map.items():
            result = result.replace(source, target)
            
        return result

if __name__ == "__main__":
    # Test the ethical dative generator
    generator = EthicalDativeGenerator()
    
    # Test basic positioning
    print("=== Ethical Dative Positioning Tests ===")
    for band_id in ["B08", "B11", "B12"]:
        for lang in ["czech", "english", "german"]:
            positioning = generator.generate_ethical_positioning(
                band_id, "environmental_change", lang, 0.7
            )
            print(f"{band_id} ({lang}): {positioning}")
        print()
    
    # Test rhetorical modes
    print("=== Rhetorical Mode Tests ===")
    for mode in RhetoricalMode:
        response = generator.generate_rhetorical_response(
            "B08", mode, "test context", "czech", 0.6
        )
        print(f"{mode.value}: {response}")
    
    # Test translation
    print("\n=== Translation Tests ===")
    czech_construction = "Listy žloutnou—na mně rychle"
    english_translation = generator.translate_ethical_construction(
        czech_construction, "czech", "english"
    )
    print(f"Czech: {czech_construction}")
    print(f"English: {english_translation}")