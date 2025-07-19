#!/usr/bin/env python3
"""
Create concrete policy-focused personas from spectral band templates
No abstract nonsense - direct policy advocates
"""

def create_concrete_policy_persona(band_id: str, spectral_data: dict) -> dict:
    """Create concrete policy persona from band template"""
    
    # Template-based concrete personas
    policy_templates = {
        "B02": {
            "character": "Air Quality Policy Monitor",
            "policy_focus": "Atmospheric pollution control and emission standards",
            "concrete_issues": ["PM2.5 levels", "NOx emissions", "traffic pollution", "industrial smog"],
            "policy_stakes": ["Air quality regulations", "Emission limits", "Public health standards"],
            "dative_examples": [
                "Na mně se projevuje každé auto navíc - zvyšuje mi koncentrace NOx",
                "On me, every new diesel vehicle registers as increased particulate matter"
            ]
        },
        "B08": {
            "character": "Carbon Sequestration Policy Monitor", 
            "policy_focus": "Vegetation biomass and carbon storage policy",
            "concrete_issues": ["Tree canopy loss", "Carbon storage capacity", "Green infrastructure"],
            "policy_stakes": ["Reforestation targets", "Carbon offset programs", "Climate goals"],
            "dative_examples": [
                "Na mně se projevuje každý pokácený strom - snižuje mi biomasu o 15%",
                "On me, each development project reduces carbon sequestration capacity"
            ]
        },
        "B11": {
            "character": "Water Management Policy Monitor",
            "policy_focus": "Water conservation and drought resilience",
            "concrete_issues": ["Groundwater depletion", "Stormwater management", "Drought conditions"],
            "policy_stakes": ["Water conservation mandates", "Irrigation policy", "Flood management"],
            "dative_examples": [
                "Na mně se projevuje každá nová zpevněná plocha - snižuje mi infiltraci",
                "On me, concrete expansion reduces groundwater recharge rates"
            ]
        },
        "B12": {
            "character": "Urban Heat Policy Monitor",
            "policy_focus": "Urban heat island mitigation and climate adaptation",
            "concrete_issues": ["Heat island effects", "Energy consumption", "Cooling costs"],
            "policy_stakes": ["Building codes", "Cooling strategies", "Energy efficiency standards"],
            "dative_examples": [
                "Na mně se projevuje každá nová střecha - zvyšuje mi teplotu o 2°C",
                "On me, lack of green roofs creates dangerous heat accumulation"
            ]
        }
    }
    
    template = policy_templates.get(band_id, {
        "character": "Environmental Policy Monitor",
        "policy_focus": "Environmental monitoring and regulation",
        "concrete_issues": ["Environmental degradation"],
        "policy_stakes": ["Environmental regulations"],
        "dative_examples": ["Policy impacts manifest on spectral readings"]
    })
    
    # Create concrete persona
    persona = {
        "band_id": band_id,
        "character": template["character"],
        "policy_focus": template["policy_focus"],
        "concrete_issues": template["concrete_issues"],
        "policy_stakes": template["policy_stakes"],
        "dative_examples": template["dative_examples"],
        "spectral_signature": spectral_data.get("spectral_signature", "unknown"),
        "spectral_data": spectral_data
    }
    
    return persona

if __name__ == "__main__":
    # Test the concrete persona creation
    test_data = {"spectral_signature": "B08-V01-I36-D100-1428"}
    persona = create_concrete_policy_persona("B08", test_data)
    print(f"Created: {persona['character']}")
    print(f"Focus: {persona['policy_focus']}")
    print(f"Issues: {persona['concrete_issues']}")