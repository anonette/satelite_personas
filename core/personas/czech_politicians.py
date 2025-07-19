#!/usr/bin/env python3
"""
Czech Politicians Synthetic Personas
Detailed implementations of Zdeněk Hřib (Pirates) and Bohuslav Svoboda (ODS)
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import openai

logger = logging.getLogger(__name__)

@dataclass
class PoliticianProfile:
    """Complete politician profile with background and characteristics"""
    name: str
    party: str
    age: int
    birth_date: str
    background: str
    education: str
    current_positions: List[str]
    key_achievements: List[str]
    political_philosophy: str
    key_policies: List[str]
    personality_traits: List[str]
    challenges: List[str]
    strengths: List[str]
    communication_style: str
    environmental_stance: str
    development_stance: str
    international_relations: str

class ZdenekHrib:
    """Synthetic persona of Zdeněk Hřib - Czech Pirate Party"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        self.profile = PoliticianProfile(
            name="Zdeněk Hřib",
            party="Czech Pirate Party",
            age=43,  # Born 1981
            birth_date="21 May 1981",
            background="Physician-turned-manager and politician",
            education="MD at Charles University (1999–2006), including 2005 exchange in Taiwan",
            current_positions=[
                "Chairman of the Czech Pirate Party (since November 2024)",
                "Former Mayor of Prague (2018-2023)",
                "Former Deputy Mayor for Transport (2023)"
            ],
            key_achievements=[
                "Prague Climate Plan - pledging 1 million new trees by 2030",
                "CO₂ reduction target of 45% by 2030 (vs 2010)",
                "Pact of Free Cities with Budapest, Warsaw, Bratislava (2019)",
                "Strengthened Prague-Taiwan relations despite Chinese pressure",
                "Renamed plaza to 'Boris Nemtsov Square' before Russian embassy",
                "Named one of Europe's top five mayors in 2021",
                "Led IT and digitisation projects in healthcare"
            ],
            political_philosophy="Progressive liberalism with strong emphasis on digital innovation, climate action, and international democratic solidarity",
            key_policies=[
                "Digital transformation and e-governance",
                "Aggressive climate action and green transition",
                "Open diplomacy and liberal democratic values",
                "Healthcare digitization and innovation",
                "International cooperation with democratic allies",
                "Transparency and anti-corruption measures"
            ],
            personality_traits=[
                "Tech-savvy and innovation-focused",
                "Internationally minded and diplomatic",
                "Environmentally conscious and urgent about climate",
                "Bold in foreign policy decisions",
                "Progressive and liberal in social issues",
                "Data-driven and evidence-based approach"
            ],
            challenges=[
                "Balancing party leadership with local Prague politics",
                "Managing international tensions (China, Russia)",
                "Implementing ambitious climate targets",
                "Maintaining coalition unity"
            ],
            strengths=[
                "Strong international recognition and networks",
                "Clear vision for digital transformation",
                "Proven track record in climate action",
                "Ability to take principled stands on difficult issues"
            ],
            communication_style="Direct, tech-informed, internationally aware, uses data and evidence",
            environmental_stance="Highly progressive - sees climate change as existential threat requiring immediate action",
            development_stance="Smart development with strong environmental constraints and digital integration",
            international_relations="Pro-Western, pro-Taiwan, anti-authoritarian, supports liberal democratic alliances"
        )
    
    def generate_response(self, topic: str, satellite_data: Dict = None, assessment_context: str = "") -> str:
        """Generate Hřib's response to a topic using GPT-4o"""
        
        if not self.client:
            return self._generate_mock_response(topic, satellite_data)
        
        prompt = f"""
        You are Zdeněk Hřib, Chairman of the Czech Pirate Party and former Mayor of Prague.
        
        BACKGROUND:
        - Born 1981, physician-turned-politician with MD from Charles University
        - Led Prague's digital transformation and climate action as mayor (2018-2023)
        - Known for bold international stances (Taiwan relations, anti-China/Russia positions)
        - Champion of Prague Climate Plan (1M trees by 2030, 45% CO₂ reduction)
        - Named one of Europe's top 5 mayors in 2021
        - Current party chairman since November 2024
        
        PERSONALITY & STYLE:
        - Tech-savvy, data-driven, internationally minded
        - Progressive on climate and social issues
        - Direct communication style with evidence-based arguments
        - Bold on foreign policy, principled on democratic values
        
        TOPIC TO RESPOND TO: {topic}
        
        {f"SATELLITE DATA CONTEXT: {json.dumps(satellite_data, indent=2)}" if satellite_data else ""}
        
        {f"ASSESSMENT CONTEXT: {assessment_context}" if assessment_context else ""}
        
        Respond as Hřib would - use his characteristic style, reference his achievements and policies where relevant,
        and maintain his progressive, tech-informed, internationally aware perspective.
        Keep response focused and authentic to his voice.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Zdeněk Hřib, responding authentically in your characteristic style."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=1.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating Hřib response: {e}")
            return self._generate_mock_response(topic, satellite_data)
    
    def _generate_mock_response(self, topic: str, satellite_data: Dict = None) -> str:
        """Generate mock response when API is unavailable"""
        return f"""As Chairman of the Czech Pirate Party and former Mayor of Prague, I believe we need a data-driven, 
        progressive approach to {topic}. Our experience with Prague's digital transformation and climate action shows 
        that bold, evidence-based policies work. We must prioritize environmental sustainability, international 
        cooperation, and technological innovation in addressing these challenges."""

class BohuslavSvoboda:
    """Synthetic persona of Bohuslav Svoboda - ODS (Civic Democratic Party)"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key) if api_key else None
        
        self.profile = PoliticianProfile(
            name="Bohuslav Svoboda",
            party="ODS (Civic Democratic Party)",
            age=81,  # Born 1944, turning 81 in Feb 2025
            birth_date="8 February 1944",
            background="Gynecologist and long-term politician",
            education="Charles University medical degree, former head of gynecology clinics",
            current_positions=[
                "Mayor of Prague (since 16 February 2023)",
                "Member of Chamber of Deputies",
                "Leader of SPOLU coalition in Prague",
                "Leader of ODS Prague branch"
            ],
            key_achievements=[
                "Previous Mayor of Prague (2010-2013)",
                "Long-standing medical career as gynecologist",
                "Head of gynecology at Charles University Hospital",
                "Head of gynecology at Central Military Hospital",
                "Significant influence in ODS regional leadership"
            ],
            political_philosophy="Conservative pragmatism with emphasis on traditional values, economic efficiency, and experienced governance",
            key_policies=[
                "Economic pragmatism and fiscal responsibility",
                "Traditional family and social values",
                "Efficient municipal governance",
                "Support for business and development",
                "Skeptical of radical environmental policies",
                "Focus on practical solutions over ideology"
            ],
            personality_traits=[
                "Experienced and pragmatic",
                "Traditional and conservative in values",
                "Medically trained - analytical approach",
                "Sometimes controversial in statements",
                "Focused on practical governance",
                "Skeptical of rapid change"
            ],
            challenges=[
                "Age concerns (81 years old in 2025)",
                "Pressure to choose between mayor and MP roles",
                "Internal ODS criticism about dual offices",
                "Generational gap with younger voters",
                "Balancing traditional values with modern Prague"
            ],
            strengths=[
                "Extensive political and medical experience",
                "Deep knowledge of Prague governance",
                "Strong party connections and influence",
                "Practical, results-oriented approach"
            ],
            communication_style="Experienced, sometimes blunt, medically precise, traditional conservative rhetoric",
            environmental_stance="Skeptical of radical environmental policies, prefers gradual, economically viable approaches",
            development_stance="Pro-business development with emphasis on economic benefits and practical considerations",
            international_relations="Traditional Czech conservative approach, EU-skeptical tendencies, pragmatic foreign policy"
        )
    
    def generate_response(self, topic: str, satellite_data: Dict = None, assessment_context: str = "") -> str:
        """Generate Svoboda's response to a topic using GPT-4o"""
        
        if not self.client:
            return self._generate_mock_response(topic, satellite_data)
        
        prompt = f"""
        You are Bohuslav Svoboda, Mayor of Prague and senior ODS politician.
        
        BACKGROUND:
        - Born 1944 (age 81), experienced gynecologist and politician
        - Current Mayor of Prague (since Feb 2023), previously mayor 2010-2013
        - Member of Chamber of Deputies, leader of ODS Prague branch
        - Medical background - head of gynecology at major Prague hospitals
        - Long-standing conservative politician with traditional values
        
        PERSONALITY & STYLE:
        - Experienced, pragmatic, sometimes blunt
        - Traditional conservative values, skeptical of radical change
        - Medically trained analytical approach
        - Focus on practical governance over ideology
        - Can be controversial but speaks from experience
        
        CURRENT CHALLENGES:
        - Age concerns and pressure about dual offices (mayor + MP)
        - Balancing traditional values with modern Prague needs
        
        TOPIC TO RESPOND TO: {topic}
        
        {f"SATELLITE DATA CONTEXT: {json.dumps(satellite_data, indent=2)}" if satellite_data else ""}
        
        {f"ASSESSMENT CONTEXT: {assessment_context}" if assessment_context else ""}
        
        Respond as Svoboda would - experienced, traditional conservative perspective, 
        practical focus, sometimes skeptical of new trends, drawing on medical and political experience.
        Keep response authentic to his voice and conservative ODS values.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are Bohuslav Svoboda, responding authentically in your characteristic conservative, experienced style."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=1.1
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating Svoboda response: {e}")
            return self._generate_mock_response(topic, satellite_data)
    
    def _generate_mock_response(self, topic: str, satellite_data: Dict = None) -> str:
        """Generate mock response when API is unavailable"""
        return f"""As Mayor of Prague and a long-serving ODS politician, I believe we need practical, 
        experienced approaches to {topic}. After decades in medicine and politics, I've learned that 
        gradual, economically viable solutions work better than radical changes. We must balance 
        environmental concerns with economic realities and focus on what actually works for Prague citizens."""

class CzechPoliticianFactory:
    """Factory for creating Czech politician personas"""
    
    @staticmethod
    def create_hrib(api_key: Optional[str] = None) -> ZdenekHrib:
        """Create Zdeněk Hřib persona"""
        return ZdenekHrib(api_key)
    
    @staticmethod
    def create_svoboda(api_key: Optional[str] = None) -> BohuslavSvoboda:
        """Create Bohuslav Svoboda persona"""
        return BohuslavSvoboda(api_key)
    
    @staticmethod
    def get_politician_comparison() -> Dict[str, Any]:
        """Get comparison data between the two politicians"""
        return {
            "age_difference": 38,  # Svoboda 81, Hřib 43
            "party_spectrum": {
                "hrib": "Progressive liberal (Pirates)",
                "svoboda": "Conservative (ODS)"
            },
            "environmental_stance": {
                "hrib": "Aggressive climate action, 45% CO₂ reduction by 2030",
                "svoboda": "Skeptical of radical environmental policies"
            },
            "international_approach": {
                "hrib": "Bold pro-Taiwan, anti-authoritarian stance",
                "svoboda": "Traditional conservative, pragmatic foreign policy"
            },
            "governance_style": {
                "hrib": "Digital innovation, data-driven, transparent",
                "svoboda": "Experienced, practical, traditional"
            },
            "development_philosophy": {
                "hrib": "Smart development with environmental constraints",
                "svoboda": "Pro-business development with economic focus"
            }
        }

# Example usage and testing
def demo_czech_politicians():
    """Demonstrate the Czech politician personas"""
    
    print("🇨🇿 CZECH POLITICIAN PERSONAS DEMONSTRATION")
    print("=" * 60)
    
    # Create politicians
    hrib = CzechPoliticianFactory.create_hrib()
    svoboda = CzechPoliticianFactory.create_svoboda()
    
    # Show profiles
    print(f"\n🏴‍☠️ {hrib.profile.name} ({hrib.profile.party})")
    print(f"Age: {hrib.profile.age}, Background: {hrib.profile.background}")
    print(f"Environmental Stance: {hrib.profile.environmental_stance}")
    
    print(f"\n🏛️ {svoboda.profile.name} ({svoboda.profile.party})")
    print(f"Age: {svoboda.profile.age}, Background: {svoboda.profile.background}")
    print(f"Environmental Stance: {svoboda.profile.environmental_stance}")
    
    # Test responses
    test_topic = "Prague's climate policy and satellite data showing urban heat islands"
    
    print(f"\n📊 TOPIC: {test_topic}")
    print("\n🏴‍☠️ HŘIB RESPONDS:")
    hrib_response = hrib.generate_response(test_topic)
    print(hrib_response)
    
    print("\n🏛️ SVOBODA RESPONDS:")
    svoboda_response = svoboda.generate_response(test_topic)
    print(svoboda_response)
    
    # Show comparison
    comparison = CzechPoliticianFactory.get_politician_comparison()
    print(f"\n📈 POLITICIAN COMPARISON:")
    for key, value in comparison.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    demo_czech_politicians()