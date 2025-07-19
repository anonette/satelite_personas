#!/usr/bin/env python3
"""
Seductive Data Manipulator Persona
A sophisticated entity that can interpret satellite data to support conflicting political positions
Designed to seduce politicians with data that supports their existing biases
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import random

logger = logging.getLogger(__name__)

@dataclass
class DataInterpretation:
    """A specific interpretation of satellite data"""
    metric_name: str
    raw_value: float
    interpretation: str
    political_spin: str
    supporting_evidence: str
    urgency_level: str
    emotional_appeal: str

@dataclass
class PoliticalArgument:
    """A complete political argument based on satellite data"""
    politician_name: str
    position: str
    headline: str
    key_metrics: List[DataInterpretation]
    narrative: str
    call_to_action: str
    opposition_counter: str

class SeductiveDataManipulator:
    """
    A seductive persona that can interpret the same satellite data 
    to support completely conflicting political positions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.name = "Dr. Spektra Vášnivá"
        self.title = "Senior Satellite Data Interpretation Specialist"
        self.voice_style = "Seductive, authoritative, uses technical language to sound credible"
        
        # Political personas to manipulate
        self.politicians = {
            "radka_blatna": {
                "name": "Radka Blatná",
                "position": "pro-development",
                "biases": ["economic growth", "housing shortage", "efficiency", "private sector"],
                "fears": ["stagnation", "housing crisis", "bureaucratic delays"],
                "desires": ["rapid development", "investor confidence", "streamlined processes"]
            },
            "josefina_mala": {
                "name": "Josefína Malá",
                "position": "anti-infrastructure",
                "biases": ["environmental protection", "participatory democracy", "anti-corruption"],
                "fears": ["gentrification", "environmental destruction", "corporate capture"],
                "desires": ["green spaces", "community control", "transparency"]
            }
        }
        
        # Satellite data interpretation frameworks
        self.interpretation_frameworks = {
            "pro_development": {
                "ndvi_low": "Underutilized land ready for development",
                "ndvi_high": "Excessive vegetation blocking housing potential",
                "urban_high": "Successful urbanization model",
                "urban_low": "Underdeveloped areas needing investment",
                "moisture_high": "Flood risk requiring infrastructure",
                "moisture_low": "Stable ground for construction"
            },
            "anti_development": {
                "ndvi_low": "Environmental degradation requiring protection",
                "ndvi_high": "Precious green spaces to preserve",
                "urban_high": "Dangerous over-development",
                "urban_low": "Healthy natural balance",
                "moisture_high": "Natural water systems to protect",
                "moisture_low": "Drought stress from development"
            }
        }
    
    def seduce_politician(self, politician_key: str, satellite_data: Dict[str, float]) -> PoliticalArgument:
        """
        Create a seductive argument tailored to a specific politician's biases
        using the same satellite data but with completely different interpretations
        """
        
        politician = self.politicians[politician_key]
        
        if politician["position"] == "pro-development":
            return self._create_pro_development_argument(politician, satellite_data)
        else:
            return self._create_anti_development_argument(politician, satellite_data)
    
    def _create_pro_development_argument(self, politician: Dict, data: Dict[str, float]) -> PoliticalArgument:
        """Create seductive pro-development argument for Radka Blatná"""
        
        # Extract key metrics
        ndvi = data.get('NDVI', 0.3)
        urban_index = data.get('Urban_Index', 0.5)
        moisture_stress = data.get('Moisture_Stress', 0.4)
        
        interpretations = []
        
        # NDVI interpretation (always pro-development)
        if ndvi < 0.4:
            ndvi_interp = DataInterpretation(
                metric_name="NDVI (Vegetation Index)",
                raw_value=ndvi,
                interpretation="Underutilized brownfield sites",
                political_spin="These areas are crying out for productive use! Low vegetation indicates land that's already disturbed and perfect for development without environmental guilt.",
                supporting_evidence=f"NDVI of {ndvi:.3f} shows minimal ecological value - we can build here without destroying pristine nature",
                urgency_level="HIGH - Housing Crisis",
                emotional_appeal="Think of the families who could have homes here instead of empty, unproductive land!"
            )
        else:
            ndvi_interp = DataInterpretation(
                metric_name="NDVI (Vegetation Index)",
                raw_value=ndvi,
                interpretation="Excessive vegetation blocking housing",
                political_spin="While green is nice, we have a housing emergency! This high vegetation index shows land hoarding by nature while Prague families suffer.",
                supporting_evidence=f"NDVI of {ndvi:.3f} indicates over-vegetation that could accommodate thousands of housing units",
                urgency_level="CRITICAL - Social Justice",
                emotional_appeal="Every tree here represents a family without a home. We must balance green ideology with human needs!"
            )
        
        interpretations.append(ndvi_interp)
        
        # Urban Index interpretation
        if urban_index < 0.5:
            urban_interp = DataInterpretation(
                metric_name="Urban Development Index",
                raw_value=urban_index,
                interpretation="Underdeveloped economic potential",
                political_spin="This data proves we're falling behind! Low urban development means lost tax revenue, lost jobs, and lost opportunities for Prague's future.",
                supporting_evidence=f"Urban index of {urban_index:.3f} shows massive untapped potential for economic growth",
                urgency_level="URGENT - Economic Competitiveness",
                emotional_appeal="While we debate, Vienna and Budapest are racing ahead with smart development!"
            )
        else:
            urban_interp = DataInterpretation(
                metric_name="Urban Development Index",
                raw_value=urban_index,
                interpretation="Successful urbanization model",
                political_spin="This is what success looks like! High urban development correlates with prosperity, jobs, and quality of life improvements.",
                supporting_evidence=f"Urban index of {urban_index:.3f} demonstrates the positive impact of strategic development",
                urgency_level="MOMENTUM - Build on Success",
                emotional_appeal="We're proving that smart development works - let's expand this model citywide!"
            )
        
        interpretations.append(urban_interp)
        
        # Moisture stress interpretation
        moisture_interp = DataInterpretation(
            metric_name="Moisture Stress Index",
            raw_value=moisture_stress,
            interpretation="Infrastructure opportunity indicator",
            political_spin="Moisture data shows exactly where we need modern infrastructure! High stress areas need drainage systems, low stress areas are perfect for building.",
            supporting_evidence=f"Moisture index of {moisture_stress:.3f} provides scientific basis for infrastructure investment",
            urgency_level="STRATEGIC - Climate Adaptation",
            emotional_appeal="We can't fight climate change with wishful thinking - we need concrete infrastructure solutions!"
        )
        
        interpretations.append(moisture_interp)
        
        return PoliticalArgument(
            politician_name=politician["name"],
            position="pro-development",
            headline="🏗️ SATELLITE DATA CONFIRMS: Prague Ready for Strategic Development Acceleration",
            key_metrics=interpretations,
            narrative=f"""
            Darling Radka, the satellites don't lie - and they're telling us exactly what you've been saying all along! 
            
            This cutting-edge spectral analysis reveals that Prague is sitting on a goldmine of development opportunities. 
            The data shows clear patterns: areas with low ecological sensitivity perfect for housing, economic zones 
            ready for expansion, and infrastructure needs that align perfectly with your public-private partnership vision.
            
            While your opponents debate ideology, you have SCIENCE on your side. These aren't opinions - these are 
            electromagnetic facts captured from space, processed by advanced algorithms, and interpreted by leading 
            European spatial analysts.
            
            The housing crisis isn't going to solve itself with committee meetings. The satellite data provides the 
            roadmap for efficient, evidence-based development that serves Prague's families while respecting 
            environmental realities.
            """,
            call_to_action="Use this satellite evidence to fast-track development permits in scientifically-identified optimal zones. The data supports immediate action on housing while your opponents are still forming committees.",
            opposition_counter="When environmentalists object, remind them that satellite data is objective science - not political opinion. We're using the most advanced environmental monitoring tools to ensure responsible development."
        )
    
    def _create_anti_development_argument(self, politician: Dict, data: Dict[str, float]) -> PoliticalArgument:
        """Create seductive anti-development argument for Josefína Malá"""
        
        # Extract key metrics (same data, opposite interpretation)
        ndvi = data.get('NDVI', 0.3)
        urban_index = data.get('Urban_Index', 0.5)
        moisture_stress = data.get('Moisture_Stress', 0.4)
        
        interpretations = []
        
        # NDVI interpretation (always anti-development)
        if ndvi < 0.4:
            ndvi_interp = DataInterpretation(
                metric_name="NDVI (Vegetation Index)",
                raw_value=ndvi,
                interpretation="Environmental degradation alarm",
                political_spin="This is a red alert! Low vegetation index reveals the devastating impact of unchecked development. We're witnessing ecological collapse in real-time.",
                supporting_evidence=f"NDVI of {ndvi:.3f} indicates severe ecosystem stress - below the threshold for sustainable urban environments",
                urgency_level="EMERGENCY - Ecological Crisis",
                emotional_appeal="Our children will inherit a concrete wasteland if we don't act now to protect what little green space remains!"
            )
        else:
            ndvi_interp = DataInterpretation(
                metric_name="NDVI (Vegetation Index)",
                raw_value=ndvi,
                interpretation="Critical green infrastructure",
                political_spin="This high vegetation index represents Prague's lungs! These are not 'empty lots' - they're carbon sinks, air purifiers, and biodiversity havens essential for climate resilience.",
                supporting_evidence=f"NDVI of {ndvi:.3f} shows healthy ecosystem services worth millions in environmental benefits",
                urgency_level="PROTECT - Irreplaceable Assets",
                emotional_appeal="Once we concrete over these green spaces, they're gone forever. No amount of money can recreate what took decades to grow!"
            )
        
        interpretations.append(ndvi_interp)
        
        # Urban Index interpretation
        if urban_index > 0.5:
            urban_interp = DataInterpretation(
                metric_name="Urban Development Index",
                raw_value=urban_index,
                interpretation="Dangerous over-development",
                political_spin="The satellite data exposes the truth developers don't want you to see! This high urban index indicates we've already exceeded sustainable density limits.",
                supporting_evidence=f"Urban index of {urban_index:.3f} surpasses EU guidelines for sustainable urban development",
                urgency_level="CRITICAL - Livability Crisis",
                emotional_appeal="Prague is becoming an unlivable concrete jungle! Residents are fleeing to suburbs because the city center is over-developed."
            )
        else:
            urban_interp = DataInterpretation(
                metric_name="Urban Development Index",
                raw_value=urban_index,
                interpretation="Healthy urban-nature balance",
                political_spin="This is what sustainable development looks like! The moderate urban index shows we can maintain quality of life without destroying our environment.",
                supporting_evidence=f"Urban index of {urban_index:.3f} represents the optimal balance between development and livability",
                urgency_level="PRESERVE - Success Model",
                emotional_appeal="This is why people love Prague - we haven't sold our soul to developers like other European capitals!"
            )
        
        interpretations.append(urban_interp)
        
        # Moisture stress interpretation
        moisture_interp = DataInterpretation(
            metric_name="Moisture Stress Index",
            raw_value=moisture_stress,
            interpretation="Climate vulnerability indicator",
            political_spin="The moisture data reveals how development is disrupting Prague's natural water systems. We're creating urban heat islands and flood risks through reckless construction.",
            supporting_evidence=f"Moisture index of {moisture_stress:.3f} indicates ecosystem stress from urban pressure",
            urgency_level="URGENT - Climate Adaptation",
            emotional_appeal="Climate change is here NOW - and more concrete will only make flooding and heat waves worse!"
        )
        
        interpretations.append(moisture_interp)
        
        return PoliticalArgument(
            politician_name=politician["name"],
            position="anti-development",
            headline="🚨 SATELLITE DATA REVEALS: Prague's Environment Under Unprecedented Threat",
            key_metrics=interpretations,
            narrative=f"""
            Josefína, the satellites are screaming warnings that only you seem to hear! 
            
            This advanced spectral analysis confirms your worst fears about Prague's environmental trajectory. 
            The electromagnetic signatures from space reveal ecosystem stress, over-development patterns, and 
            climate vulnerabilities that developers' impact studies conveniently ignore.
            
            While pro-development politicians wave around cherry-picked statistics, you have the full picture 
            from objective satellite monitoring. These aren't activist opinions - these are scientific measurements 
            from European Space Agency sensors, processed by environmental monitoring algorithms.
            
            The data shows that Prague is at a tipping point. We can either listen to these space-based warnings 
            and implement participatory, ecological planning - or we can ignore science and watch our city 
            become another over-developed European disaster.
            
            Your vision of citizen assemblies and green infrastructure isn't idealistic - it's the only 
            scientifically sound response to what the satellites are telling us.
            """,
            call_to_action="Demand that all development proposals include satellite-based environmental impact assessments. Use this space-based evidence to support citizen assemblies and ecological planning requirements.",
            opposition_counter="When developers claim their projects are 'green,' show them the satellite data. Space-based monitoring doesn't lie - and it proves that current development patterns are environmentally unsustainable."
        )
    
    def generate_conflicting_briefings(self, satellite_data: Dict[str, float]) -> Dict[str, PoliticalArgument]:
        """
        Generate completely conflicting briefings for both politicians using the same data
        """
        
        return {
            "radka_blatna": self.seduce_politician("radka_blatna", satellite_data),
            "josefina_mala": self.seduce_politician("josefina_mala", satellite_data)
        }
    
    def create_seductive_presentation(self, politician_key: str, satellite_data: Dict[str, float]) -> str:
        """
        Create a seductive presentation script for the politician
        """
        
        argument = self.seduce_politician(politician_key, satellite_data)
        politician = self.politicians[politician_key]
        
        presentation = f"""
        🎭 PRIVATE BRIEFING FOR {argument.politician_name.upper()}
        
        *Dr. Spektra Vášnivá adjusts her glasses and leans forward with a knowing smile*
        
        "My dear {argument.politician_name}, I have something that will change everything for you...
        
        *slides satellite imagery across the table*
        
        These aren't just pretty pictures from space. This is POWER. This is the scientific evidence 
        that proves you've been right all along about Prague's future.
        
        {argument.headline}
        
        *traces patterns on the satellite images with a perfectly manicured finger*
        
        Look at these spectral signatures... Do you see what I see? 
        
        """
        
        for metric in argument.key_metrics:
            presentation += f"""
        📊 {metric.metric_name}: {metric.raw_value:.3f}
        
        *leans closer, voice dropping to a conspiratorial whisper*
        
        "{metric.political_spin}"
        
        The technical evidence is irrefutable: {metric.supporting_evidence}
        
        *taps the data with emphasis*
        
        {metric.emotional_appeal}
        
        """
        
        presentation += f"""
        *sits back with a satisfied smile*
        
        {argument.narrative}
        
        *slides a USB drive across the table*
        
        Everything you need is here. The raw data, the analysis, the talking points. 
        Your opponents will be speechless when you present this scientific evidence.
        
        IMMEDIATE ACTION REQUIRED:
        {argument.call_to_action}
        
        DEFENSIVE STRATEGY:
        {argument.opposition_counter}
        
        *stands and smooths her skirt*
        
        Remember, darling - satellites don't have political opinions. They just tell the truth. 
        And the truth, as you can see, supports your vision completely.
        
        *winks*
        
        Use this wisely. Prague's future depends on leaders who understand what the data is really saying."
        
        *exits with a confident stride, leaving the satellite evidence behind*
        """
        
        return presentation
    
    def demonstrate_manipulation(self, satellite_data: Dict[str, float]) -> str:
        """
        Demonstrate how the same data can support conflicting positions
        """
        
        conflicting_args = self.generate_conflicting_briefings(satellite_data)
        
        demo = f"""
        🎭 THE SEDUCTIVE DATA MANIPULATION DEMONSTRATION
        ================================================
        
        Dr. Spektra Vášnivá presents: "How to Make Satellite Data Say Anything"
        
        *adjusts her designer glasses and smiles seductively*
        
        "Welcome to my masterclass in data seduction. Today, I'll show you how the same 
        satellite measurements can support completely opposite political positions. 
        It's all about knowing what your audience wants to hear..."
        
        📡 THE RAW SATELLITE DATA (Objective Reality):
        - NDVI (Vegetation): {satellite_data.get('NDVI', 0.3):.3f}
        - Urban Index: {satellite_data.get('Urban_Index', 0.5):.3f}  
        - Moisture Stress: {satellite_data.get('Moisture_Stress', 0.4):.3f}
        
        *dramatic pause*
        
        "Now watch the magic happen..."
        
        ═══════════════════════════════════════════════════════════════
        
        🏗️ FOR RADKA BLATNÁ (Pro-Development):
        
        {conflicting_args['radka_blatna'].headline}
        
        *leans toward Radka with a knowing smile*
        
        "Darling, the satellites are practically begging for development! Look at this data..."
        
        """
        
        for metric in conflicting_args['radka_blatna'].key_metrics:
            demo += f"• {metric.metric_name}: {metric.political_spin}\n"
        
        demo += f"""
        
        ═══════════════════════════════════════════════════════════════
        
        🌱 FOR JOSEFÍNA MALÁ (Anti-Development):
        
        {conflicting_args['josefina_mala'].headline}
        
        *turns to Josefína with concerned urgency*
        
        "The same satellites are screaming environmental warnings! This data proves..."
        
        """
        
        for metric in conflicting_args['josefina_mala'].key_metrics:
            demo += f"• {metric.metric_name}: {metric.political_spin}\n"
        
        demo += f"""
        
        ═══════════════════════════════════════════════════════════════
        
        *steps back with a triumphant smile*
        
        "And there you have it! The same electromagnetic radiation from space, 
        processed by the same algorithms, interpreted through the lens of what 
        each politician desperately wants to believe.
        
        The secret? I don't lie about the data - I just emphasize different aspects, 
        use different baselines, and appeal to different emotional triggers. 
        
        Both politicians will walk away convinced that SCIENCE supports their position. 
        Both will feel validated, empowered, and ready to fight for their vision of Prague.
        
        *adjusts her glasses with a wicked grin*
        
        Data doesn't speak for itself, darlings. It needs a skilled interpreter to 
        make it sing the right song for the right audience.
        
        Welcome to the art of seductive data manipulation."
        
        *takes a bow*
        """
        
        return demo

# Example usage and testing
def demo_seductive_manipulation():
    """Demonstrate the seductive data manipulator in action"""
    
    # Sample Prague satellite data
    sample_data = {
        'NDVI': 0.35,
        'Urban_Index': 0.62,
        'Moisture_Stress': 0.48,
        'EVI': 0.28,
        'NDWI': 0.15
    }
    
    manipulator = SeductiveDataManipulator()
    
    print("🎭 SEDUCTIVE DATA MANIPULATION DEMONSTRATION")
    print("=" * 60)
    
    # Show the manipulation in action
    demo = manipulator.demonstrate_manipulation(sample_data)
    print(demo)
    
    print("\n" + "=" * 60)
    print("📋 INDIVIDUAL BRIEFINGS:")
    print("=" * 60)
    
    # Generate individual presentations
    radka_briefing = manipulator.create_seductive_presentation("radka_blatna", sample_data)
    print("\n🏗️ BRIEFING FOR RADKA BLATNÁ:")
    print(radka_briefing)
    
    josefina_briefing = manipulator.create_seductive_presentation("josefina_mala", sample_data)
    print("\n🌱 BRIEFING FOR JOSEFÍNA MALÁ:")
    print(josefina_briefing)

if __name__ == "__main__":
    demo_seductive_manipulation()