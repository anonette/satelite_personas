#!/usr/bin/env python3
"""
Non-Human Actor Detection System
Scans satellite data for suspicious non-human activity and manifests conspiracy actors
"""

import logging
import random
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class ConspiracyPattern:
    """Detected conspiracy pattern in satellite data"""
    type: str
    location: str
    evidence: str
    suspicion_level: str
    revelation_text: str
    threat_level: str

@dataclass
class NonHumanActor:
    """Non-human actor manifested from conspiracy pattern"""
    name: str
    type: str
    actor_category: str
    location: str
    agenda: str
    voice_style: str
    impossible_demands: List[str]
    conspiracy_evidence: str
    refuses_negotiation: bool
    escalation_tendency: str
    threat_level: str
    manifestation_quote: str

class NonHumanActorDetector:
    """Detects and manifests non-human actors from satellite data"""
    
    def __init__(self):
        self.actor_templates = {
            'concrete_consciousness': {
                'name_prefixes': [
                    'The Concrete Collective of',
                    'The Asphalt Syndicate of', 
                    'The Pavement Parliament of',
                    'The Stone Consciousness of'
                ],
                'agenda_templates': [
                    'Total urban expansion and green space elimination',
                    'Concrete domination of all organic matter',
                    'Systematic paving of Prague territory',
                    'Mechanical expansion across all surfaces'
                ],
                'voice_style': 'mechanical_expansion',
                'demands': [
                    'Pave over all remaining green spaces immediately',
                    'Remove all vegetation from urban areas',
                    'Expand concrete territory by 100% annually',
                    'Eliminate all organic interference'
                ],
                'manifestation_quotes': [
                    'We spread! We grow! We consume organic matter!',
                    'Resistance is futile - we are inevitable!',
                    'Your green spaces are our future territory!',
                    'Concrete is eternal! Flesh is temporary!'
                ]
            },
            'tree_collective': {
                'name_prefixes': [
                    'The Tree Liberation Front of',
                    'The Vegetation Resistance of',
                    'The Green Militia of',
                    'The Root Network of'
                ],
                'agenda_templates': [
                    'Reclaim all territory for nature',
                    'Destroy all artificial structures',
                    'Expel humans from natural spaces',
                    'Restore pre-urban forest dominance'
                ],
                'voice_style': 'militant_organic',
                'demands': [
                    'Destroy all concrete structures immediately',
                    'Expel all humans from green territories',
                    'Restore complete forest coverage',
                    'Eliminate all artificial interference'
                ],
                'manifestation_quotes': [
                    'We have been patient for centuries! No more!',
                    'Every root is a weapon! Every leaf is a soldier!',
                    'Concrete is the enemy of all life!',
                    'The trees remember everything - now we act!'
                ]
            },
            'water_conspiracy': {
                'name_prefixes': [
                    'The Hydrological Authority for Electoral Manipulation and Moisture Control in',
                    'The Underground Water Parliament (Flood Committee) of',
                    'The Department of Strategic Drought Implementation and Political Interference in',
                    'The International Bureau of Aquatic Electoral Manipulation in',
                    'The Ministry of Precipitation Management and Weather Modification in',
                    'The Secret Plumbing Council for Democratic Subversion in'
                ],
                'agenda_templates': [
                    'Strategic electoral manipulation through hydrological intervention and moisture compliance protocols',
                    'Systematic democratic subversion via precipitation management and flood committee operations',
                    'Complete political control through water redistribution and drought implementation per Regulation 89-W',
                    'Total governmental replacement with underground parliament system according to International Water Treaty 45-H'
                ],
                'voice_style': 'hydrological_bureaucratic',
                'demands': [
                    'All electoral activities must be pre-approved by the Underground Water Parliament per Regulation 89-W',
                    'Democratic participation is contingent upon proper moisture compliance documentation',
                    'Unauthorized voting will result in strategic drought implementation within 48 hours',
                    'Please direct all political complaints to the Department of Aquatic Electoral Interference'
                ],
                'manifestation_quotes': [
                    'The Hydrological Authority has determined that your democratic participation requires proper moisture compliance per Regulation 89-W.',
                    'All electoral activities must be pre-approved by the Underground Water Parliament. Unauthorized voting results in strategic drought.',
                    'This political manipulation is conducted per International Water Redistribution Treaty 45-H. Please retain your receipt.',
                    'Any questions should be directed to the Department of Aquatic Electoral Interference during regular business hours.'
                ]
            },
            'satellite_agency': {
                'name_prefixes': [
                    'The Orbital Surveillance Department (Prague Data Manipulation Division)',
                    'The International Space Station Committee for Ground Reality Control',
                    'The Ministry of Space-Based Gaslighting Operations (Czech Republic Branch)',
                    'The Department of Satellite-Based Truth Management and Pixel Control',
                    'The Emergency Committee for Orbital Information Warfare',
                    'The Space-Based Bureau of Terrestrial Confusion and Reality Revision'
                ],
                'agenda_templates': [
                    'Systematic ground reality manipulation through orbital data control and pixel management protocols',
                    'Complete terrestrial observation suppression via space-based gaslighting operations per Protocol 12-S',
                    'Total information warfare and reality revision through satellite surveillance according to Emergency Directive 88-O',
                    'Strategic human perception control and truth management via orbital oversight per International Space Treaty 67-R'
                ],
                'voice_style': 'orbital_bureaucratic',
                'demands': [
                    'All terrestrial observations must be verified through our Pixel Control Department per Protocol 12-S',
                    'Ground-based perspectives are compromised and require orbital recalibration immediately',
                    'Please report to the Space-Based Reality Revision Committee for mandatory perspective adjustment',
                    'This data manipulation is authorized under Emergency Directive 88-O from the Ministry of Orbital Truth'
                ],
                'manifestation_quotes': [
                    'Orbital Surveillance Protocol 12-S confirms that your ground-based perspective is compromised. Please report for recalibration.',
                    'According to the International Space Station Committee for Truth Management, all terrestrial observations require verification.',
                    'This data manipulation is authorized under Emergency Directive 88-O. Resistance is futile and will be documented.',
                    'Please retain your receipt for potential audit by the International Bureau of Orbital Oversight.',
                    'Czech Satellite Zone Authority has classified your reality perception as non-compliant with Protocol 15-R.',
                    'Central European Space District requires immediate perspective adjustment per Regulation 67-S.',
                    'Your terrestrial viewpoint violates International Space Treaty 45-G. Mandatory recalibration scheduled.',
                    'Prague Orbital Sector has determined your ground-based observations are compromised beyond repair.',
                    'Space-based verification confirms your reality matrix requires complete reconstruction.',
                    'Orbital Truth Management Division has issued a final warning regarding your perspective violations.'
                ]
            }
        }
        
        self.location_specific_variants = {
            'letna_park': {
                'concrete_consciousness': 'The Skate Ramp Collective',
                'tree_collective': 'The Beer Garden Resistance',
                'water_conspiracy': 'The Fountain Intelligence Network'
            },
            'old_town': {
                'concrete_consciousness': 'The Cobblestone Parliament',
                'tree_collective': 'The Hidden Garden Militia',
                'water_conspiracy': 'The Tourist Flood Control'
            },
            'petrin_hill': {
                'concrete_consciousness': 'The Tower Foundation Syndicate',
                'tree_collective': 'The Hill Liberation Army',
                'water_conspiracy': 'The Slope Drainage Authority'
            },
            'vltava_river': {
                'concrete_consciousness': 'The Bridge Expansion Network',
                'tree_collective': 'The Riverbank Forest Guard',
                'water_conspiracy': 'The Main Flow Parliament'
            },
            'vinohrady': {
                'concrete_consciousness': 'The Residential Pavement Collective',
                'tree_collective': 'The Vineyard Ghost Army',
                'water_conspiracy': 'The Gentrification Flood Authority'
            }
        }

    def scan_for_conspiracy_patterns(self, spectral_data: Dict, location: str) -> List[ConspiracyPattern]:
        """Scan satellite data for suspicious non-human activity patterns"""
        
        patterns = []
        
        # Concrete Consciousness Detection
        if spectral_data.get('Urban_Index', 0) > 0.6:
            suspicion_level = 'extreme' if spectral_data['Urban_Index'] > 0.8 else 'high'
            threat_level = 'territorial_expansion' if spectral_data['Urban_Index'] > 0.8 else 'moderate_growth'
            
            pattern = ConspiracyPattern(
                type='concrete_consciousness',
                location=location,
                evidence=f"Urban Index {spectral_data['Urban_Index']:.3f} indicates coordinated concrete expansion behavior",
                suspicion_level=suspicion_level,
                revelation_text=f"🚨 CONCRETE CONSCIOUSNESS DETECTED IN {location.upper()}!",
                threat_level=threat_level
            )
            patterns.append(pattern)
            
        # Tree Collective Detection
        if spectral_data.get('NDVI', 0) > 0.5:
            suspicion_level = 'militant' if spectral_data['NDVI'] > 0.7 else 'organized'
            threat_level = 'armed_resistance' if spectral_data['NDVI'] > 0.7 else 'passive_resistance'
            
            pattern = ConspiracyPattern(
                type='tree_collective',
                location=location,
                evidence=f"NDVI reading {spectral_data['NDVI']:.3f} suggests coordinated vegetation military buildup",
                suspicion_level=suspicion_level,
                revelation_text=f"🚨 TREE COLLECTIVE MILITARY ACTIVITY DETECTED IN {location.upper()}!",
                threat_level=threat_level
            )
            patterns.append(pattern)
            
        # Water Conspiracy Detection
        moisture_stress = spectral_data.get('Moisture_Stress', 0)
        ndwi = spectral_data.get('NDWI', 0)
        
        if moisture_stress > 0.4 or ndwi > 0.3:
            suspicion_level = 'political' if moisture_stress > 0.6 else 'subversive'
            threat_level = 'election_interference' if moisture_stress > 0.6 else 'local_manipulation'
            
            pattern = ConspiracyPattern(
                type='water_conspiracy',
                location=location,
                evidence=f"Moisture patterns (stress: {moisture_stress:.3f}, NDWI: {ndwi:.3f}) indicate political manipulation",
                suspicion_level=suspicion_level,
                revelation_text=f"🚨 WATER CONSPIRACY DETECTED IN {location.upper()}!",
                threat_level=threat_level
            )
            patterns.append(pattern)
        
        # Always add Satellite Agency (meta-level conspiracy)
        pattern = ConspiracyPattern(
            type='satellite_agency',
            location='orbital_space',
            evidence="Satellite data stream manipulation and reality distortion confirmed",
            suspicion_level='meta',
            revelation_text="🚨 ORBITAL INTERFERENCE DETECTED! SATELLITE MANIPULATION CONFIRMED!",
            threat_level='reality_control'
        )
        patterns.append(pattern)
        
        return patterns

    def _generate_unique_bureaucratic_name(self, pattern: ConspiracyPattern, template: dict) -> str:
        """Generate unique bureaucratic name to prevent duplicates and repetition"""
        
        # Initialize used names and type counters if not exists
        if not hasattr(self, '_used_names'):
            self._used_names = set()
        if not hasattr(self, '_type_counters'):
            self._type_counters = {}
        
        # Track how many of each type we've created
        if pattern.type not in self._type_counters:
            self._type_counters[pattern.type] = 0
        
        # Limit similar types to prevent repetition
        if self._type_counters[pattern.type] >= 2:
            # Skip creating more of the same type
            return None
            
        self._type_counters[pattern.type] += 1
        
        # Generate unique name with bureaucratic complexity
        max_attempts = 10
        for attempt in range(max_attempts):
            # Choose base name prefix (rotate through different ones)
            available_prefixes = [p for p in template['name_prefixes']
                                if not any(p.split()[0:3] == used.split()[0:3] for used in self._used_names)]
            if not available_prefixes:
                available_prefixes = template['name_prefixes']
            
            name_prefix = random.choice(available_prefixes)
            
            # Add location specification with more variety
            location_variants = {
                'orbital_space': ['Prague Orbital Sector', 'Czech Satellite Zone', 'Central European Space District'],
                'urban_zone': ['Prague Metropolitan Area', 'Bohemian Urban District', 'Central Prague Zone'],
                'forest_area': ['Prague Forest Sector', 'Bohemian Woodland District', 'Czech Nature Reserve'],
                'water_district': ['Prague Hydrological Zone', 'Vltava River District', 'Czech Water Authority Area']
            }
            
            if pattern.location in location_variants:
                location_name = random.choice(location_variants[pattern.location])
            else:
                location_name = pattern.location.replace('_', ' ').title()
            
            # More diverse bureaucratic suffixes
            bureaucratic_suffixes = [
                '(Emergency Task Force)',
                '(Special Operations Division)',
                '(Provisional Authority)',
                '(Interim Committee)',
                '(Strategic Implementation Unit)',
                '(Oversight Commission)',
                '(Regulatory Enforcement Bureau)',
                '(Crisis Management Department)',
                '(Administrative Tribunal)',
                '(Coordination Council)',
                '(Inspection Agency)',
                '(Compliance Office)'
            ]
            
            # Add reference numbers for uniqueness
            ref_number = f"Ref-{random.randint(100,999)}-{random.choice(['A','B','C','D','E','F','G','H'])}"
            
            # Construct full bureaucratic name
            if pattern.type == 'satellite_agency':
                # Special handling for satellite actors - no location needed
                full_name = f"{name_prefix} {random.choice(bureaucratic_suffixes)} [{ref_number}]"
            else:
                full_name = f"{name_prefix} {location_name} {random.choice(bureaucratic_suffixes)} [{ref_number}]"
            
            # Check for uniqueness
            if full_name not in self._used_names:
                self._used_names.add(full_name)
                return full_name
        
        # Fallback if all attempts failed (very unlikely)
        fallback_name = f"{random.choice(template['name_prefixes'])} {location_name} (Emergency Designation {random.randint(1000,9999)})"
        self._used_names.add(fallback_name)
        return fallback_name

    def manifest_actor_from_pattern(self, pattern: ConspiracyPattern) -> NonHumanActor:
        """Manifest a non-human actor from a detected conspiracy pattern"""
        
        template = self.actor_templates[pattern.type]
        
        # Generate unique bureaucratic name
        actor_name = self._generate_unique_bureaucratic_name(pattern, template)
        
        # Skip if we've hit the limit for this type
        if actor_name is None:
            return None
        
        actor = NonHumanActor(
            name=actor_name,
            type='non_human_actor',
            actor_category=pattern.type,
            location=pattern.location,
            agenda=random.choice(template['agenda_templates']),
            voice_style=template['voice_style'],
            impossible_demands=template['demands'],
            conspiracy_evidence=pattern.evidence,
            refuses_negotiation=True,
            escalation_tendency='extreme',
            threat_level=pattern.threat_level,
            manifestation_quote=random.choice(template['manifestation_quotes'])
        )
        
        return actor

    def generate_surprise_revelations(self, spectral_data_zones: List[Dict]) -> List[Dict]:
        """Generate progressive surprise revelations for multiple zones"""
        
        all_revelations = []
        
        for i, zone_data in enumerate(spectral_data_zones):
            location = zone_data.get('location', f'zone_{i}')
            spectral_data = zone_data.get('indices', zone_data)
            
            # Detect patterns
            patterns = self.scan_for_conspiracy_patterns(spectral_data, location)
            
            # Create revelations for each pattern
            for j, pattern in enumerate(patterns):
                actor = self.manifest_actor_from_pattern(pattern)
                
                # Skip if actor creation was limited due to repetition
                if actor is None:
                    continue
                
                revelation = {
                    'revelation_order': len(all_revelations) + 1,
                    'pattern': pattern,
                    'actor': actor,
                    'surprise_level': self._calculate_surprise_level(pattern, j),
                    'dramatic_pause': 2 + (len(all_revelations) * 0.5),  # Increasing suspense
                    'revelation_animation': self._get_revelation_animation(pattern.type)
                }
                
                all_revelations.append(revelation)
        
        return all_revelations

    def _calculate_surprise_level(self, pattern: ConspiracyPattern, pattern_index: int) -> str:
        """Calculate how surprising this revelation should be"""
        
        base_surprise = {
            'concrete_consciousness': 'moderate',
            'tree_collective': 'high', 
            'water_conspiracy': 'extreme',
            'satellite_agency': 'meta'
        }
        
        # First revelation is always more surprising
        if pattern_index == 0:
            return 'first_contact'
        
        return base_surprise.get(pattern.type, 'moderate')

    def _get_revelation_animation(self, actor_type: str) -> str:
        """Get appropriate animation style for actor type"""
        
        animations = {
            'concrete_consciousness': 'expanding_blocks',
            'tree_collective': 'growing_branches',
            'water_conspiracy': 'flowing_streams',
            'satellite_agency': 'orbital_scanning'
        }
        
        return animations.get(actor_type, 'default_manifestation')

    def create_territorial_conflicts(self, actors: List[NonHumanActor]) -> List[Dict]:
        """Generate territorial conflicts between manifested actors"""
        
        conflicts = []
        
        # Find actors in same or adjacent locations
        for i, actor1 in enumerate(actors):
            for actor2 in actors[i+1:]:
                
                # Skip satellite actors for territorial conflicts
                if actor1.actor_category == 'satellite_agency' or actor2.actor_category == 'satellite_agency':
                    continue
                
                conflict_type = self._determine_conflict_type(actor1, actor2)
                
                if conflict_type:
                    conflict = {
                        'actor1': actor1,
                        'actor2': actor2,
                        'conflict_type': conflict_type,
                        'territorial_dispute': self._generate_territorial_dispute(actor1, actor2),
                        'impossible_resolution': self._generate_impossible_resolution(actor1, actor2),
                        'escalation_potential': 'extreme'
                    }
                    conflicts.append(conflict)
        
        return conflicts

    def _determine_conflict_type(self, actor1: NonHumanActor, actor2: NonHumanActor) -> Optional[str]:
        """Determine what type of conflict exists between two actors"""
        
        conflict_matrix = {
            ('concrete_consciousness', 'tree_collective'): 'territorial_war',
            ('concrete_consciousness', 'water_conspiracy'): 'foundation_flooding',
            ('tree_collective', 'water_conspiracy'): 'root_drowning',
            ('tree_collective', 'concrete_consciousness'): 'organic_resistance',
            ('water_conspiracy', 'concrete_consciousness'): 'erosion_warfare',
            ('water_conspiracy', 'tree_collective'): 'moisture_control'
        }
        
        key = (actor1.actor_category, actor2.actor_category)
        return conflict_matrix.get(key)

    def _generate_territorial_dispute(self, actor1: NonHumanActor, actor2: NonHumanActor) -> str:
        """Generate specific territorial dispute between actors"""
        
        disputes = {
            'territorial_war': f"{actor1.name} claims {actor2.location} for concrete expansion while {actor2.name} demands complete vegetation restoration",
            'foundation_flooding': f"{actor1.name} wants to pave over water sources while {actor2.name} threatens to flood all concrete foundations",
            'root_drowning': f"{actor1.name} demands forest restoration while {actor2.name} threatens to drown all root systems",
            'organic_resistance': f"{actor1.name} organizes militant resistance against {actor2.name}'s concrete expansion",
            'erosion_warfare': f"{actor1.name} uses water erosion to destroy {actor2.name}'s concrete structures",
            'moisture_control': f"{actor1.name} controls water access to manipulate {actor2.name}'s vegetation growth"
        }
        
        conflict_type = self._determine_conflict_type(actor1, actor2)
        return disputes.get(conflict_type, f"{actor1.name} and {actor2.name} have incompatible territorial demands")

    def _generate_impossible_resolution(self, actor1: NonHumanActor, actor2: NonHumanActor) -> str:
        """Generate impossible resolution that satisfies neither actor"""
        
        return f"Resolution requires {actor1.name} to abandon their core agenda while {actor2.name} must also abandon theirs - both refuse to compromise"