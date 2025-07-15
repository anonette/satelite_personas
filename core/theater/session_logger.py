"""
Session Logger for Prague Spectral Multiplicity Theater
Comprehensive logging system for personas, interactions, and sessions
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import uuid

class TheaterSessionLogger:
    """Comprehensive logging system for theater sessions"""
    
    def __init__(self, base_dir: str = "theater_logs"):
        self.base_dir = Path(base_dir)
        self.setup_directories()
        
        # Session tracking
        self.current_session_id = None
        self.session_start_time = None
        
    def setup_directories(self):
        """Create logging directory structure"""
        directories = [
            self.base_dir,
            self.base_dir / "sessions",
            self.base_dir / "personas", 
            self.base_dir / "interactions",
            self.base_dir / "analysis",
            self.base_dir / "exports"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def start_new_session(self, session_name: Optional[str] = None) -> str:
        """Start a new theater session"""
        self.current_session_id = str(uuid.uuid4())[:8]
        self.session_start_time = datetime.now()
        
        if not session_name:
            session_name = f"Theater_Session_{self.session_start_time.strftime('%Y%m%d_%H%M%S')}"
        
        session_data = {
            "session_id": self.current_session_id,
            "session_name": session_name,
            "start_time": self.session_start_time.isoformat(),
            "personas_generated": [],
            "interactions": [],
            "image_used": None,
            "generation_settings": {},
            "status": "active"
        }
        
        session_file = self.base_dir / "sessions" / f"{self.current_session_id}.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
        
        print(f"📝 Started new session: {session_name} (ID: {self.current_session_id})")
        return self.current_session_id
    
    def log_persona_generation(self, personas: List[Dict], image_path: str, settings: Dict):
        """Log generated personas"""
        if not self.current_session_id:
            self.start_new_session()
        
        timestamp = datetime.now().isoformat()
        
        # Log each persona individually
        for persona in personas:
            persona_id = str(uuid.uuid4())[:8]
            persona_log = {
                "persona_id": persona_id,
                "session_id": self.current_session_id,
                "timestamp": timestamp,
                "name": persona.get('name', 'Unknown'),
                "location": persona.get('location', 'Unknown'),
                "type": persona.get('type', 'spectral_multiplicity'),
                "arendtian_mode": persona.get('arendtian_mode', 'Unknown'),
                "mood": persona.get('mood', 'Unknown'),
                "civic_position": persona.get('civic_position', 'Unknown'),
                "temporal_status": persona.get('temporal_status', 'stable'),
                "dominant_indices": persona.get('dominant_indices', {}),
                "voice_sample": persona.get('voice', '')[:200],  # First 200 chars
                "full_persona_data": persona,
                "source_image": str(image_path),
                "generation_settings": settings
            }
            
            # Save individual persona log
            persona_file = self.base_dir / "personas" / f"{persona_id}_{persona['name'].replace(' ', '_')}.json"
            with open(persona_file, 'w', encoding='utf-8') as f:
                json.dump(persona_log, f, indent=2, ensure_ascii=False)
        
        # Update session log
        self.update_session_log({
            "personas_generated": [p.get('name', 'Unknown') for p in personas],
            "image_used": str(image_path),
            "generation_settings": settings,
            "persona_count": len(personas)
        })
        
        print(f"📝 Logged {len(personas)} personas to session {self.current_session_id}")
    
    def log_interaction(self, interaction_type: str, participants: List[str], content: str, metadata: Dict = None):
        """Log interactions between personas"""
        if not self.current_session_id:
            return
        
        interaction_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().isoformat()
        
        interaction_log = {
            "interaction_id": interaction_id,
            "session_id": self.current_session_id,
            "timestamp": timestamp,
            "type": interaction_type,  # 'dialogue', 'group_discussion', 'scene_composition'
            "participants": participants,
            "content": content,
            "metadata": metadata or {},
            "duration_seconds": None  # Could be calculated if needed
        }
        
        # Save interaction log
        interaction_file = self.base_dir / "interactions" / f"{interaction_id}_{interaction_type}.json"
        with open(interaction_file, 'w', encoding='utf-8') as f:
            json.dump(interaction_log, f, indent=2, ensure_ascii=False)
        
        # Update session log
        self.update_session_log({
            "interactions": [interaction_id]
        }, append_to_lists=True)
        
        print(f"📝 Logged {interaction_type} interaction: {interaction_id}")
    
    def update_session_log(self, updates: Dict, append_to_lists: bool = False):
        """Update the current session log"""
        if not self.current_session_id:
            return
        
        session_file = self.base_dir / "sessions" / f"{self.current_session_id}.json"
        
        # Read current session data
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)
        else:
            return
        
        # Update session data
        for key, value in updates.items():
            if append_to_lists and key in session_data and isinstance(session_data[key], list):
                if isinstance(value, list):
                    session_data[key].extend(value)
                else:
                    session_data[key].append(value)
            else:
                session_data[key] = value
        
        session_data["last_updated"] = datetime.now().isoformat()
        
        # Save updated session data
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session_data, f, indent=2, ensure_ascii=False)
    
    def end_session(self):
        """End the current session"""
        if not self.current_session_id:
            return
        
        end_time = datetime.now()
        duration = (end_time - self.session_start_time).total_seconds() if self.session_start_time else 0
        
        self.update_session_log({
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "status": "completed"
        })
        
        print(f"📝 Ended session {self.current_session_id} (Duration: {duration:.0f}s)")
        
        self.current_session_id = None
        self.session_start_time = None
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all logged sessions"""
        sessions = []
        sessions_dir = self.base_dir / "sessions"
        
        if not sessions_dir.exists():
            return sessions
        
        for session_file in sessions_dir.glob("*.json"):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                    sessions.append(session_data)
            except Exception as e:
                print(f"Error reading session {session_file}: {e}")
        
        # Sort by start time (newest first)
        sessions.sort(key=lambda x: x.get('start_time', ''), reverse=True)
        return sessions
    
    def get_all_personas(self) -> List[Dict]:
        """Get all logged personas"""
        personas = []
        personas_dir = self.base_dir / "personas"
        
        if not personas_dir.exists():
            return personas
        
        for persona_file in personas_dir.glob("*.json"):
            try:
                with open(persona_file, 'r', encoding='utf-8') as f:
                    persona_data = json.load(f)
                    personas.append(persona_data)
            except Exception as e:
                print(f"Error reading persona {persona_file}: {e}")
        
        # Sort by timestamp (newest first)
        personas.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return personas
    
    def get_session_interactions(self, session_id: str) -> List[Dict]:
        """Get all interactions for a specific session"""
        interactions = []
        interactions_dir = self.base_dir / "interactions"
        
        if not interactions_dir.exists():
            return interactions
        
        for interaction_file in interactions_dir.glob("*.json"):
            try:
                with open(interaction_file, 'r', encoding='utf-8') as f:
                    interaction_data = json.load(f)
                    if interaction_data.get('session_id') == session_id:
                        interactions.append(interaction_data)
            except Exception as e:
                print(f"Error reading interaction {interaction_file}: {e}")
        
        # Sort by timestamp
        interactions.sort(key=lambda x: x.get('timestamp', ''))
        return interactions
    
    def search_personas(self, query: str = "", location: str = "", persona_type: str = "") -> List[Dict]:
        """Search personas by various criteria"""
        all_personas = self.get_all_personas()
        results = []
        
        for persona in all_personas:
            match = True
            
            if query and query.lower() not in persona.get('name', '').lower():
                match = False
            
            if location and location.lower() not in persona.get('location', '').lower():
                match = False
            
            if persona_type and persona_type != persona.get('type', ''):
                match = False
            
            if match:
                results.append(persona)
        
        return results
    
    def export_session_analysis(self, session_id: str) -> Dict:
        """Export comprehensive analysis of a session"""
        sessions = self.get_all_sessions()
        session = next((s for s in sessions if s['session_id'] == session_id), None)
        
        if not session:
            return {}
        
        interactions = self.get_session_interactions(session_id)
        
        # Get personas from this session
        session_personas = []
        for persona_name in session.get('personas_generated', []):
            matching_personas = self.search_personas(query=persona_name)
            session_personas.extend([p for p in matching_personas if p['session_id'] == session_id])
        
        analysis = {
            "session_info": session,
            "personas": session_personas,
            "interactions": interactions,
            "statistics": {
                "total_personas": len(session_personas),
                "total_interactions": len(interactions),
                "interaction_types": list(set(i.get('type', 'unknown') for i in interactions)),
                "persona_types": list(set(p.get('type', 'unknown') for p in session_personas)),
                "locations_covered": list(set(p.get('location', 'unknown') for p in session_personas)),
                "arendtian_modes": list(set(p.get('arendtian_mode', 'unknown') for p in session_personas))
            },
            "export_timestamp": datetime.now().isoformat()
        }
        
        # Save analysis
        analysis_file = self.base_dir / "analysis" / f"session_analysis_{session_id}.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        return analysis
    
    def get_statistics(self) -> Dict:
        """Get overall statistics"""
        sessions = self.get_all_sessions()
        personas = self.get_all_personas()
        
        # Count interactions
        interactions_dir = self.base_dir / "interactions"
        total_interactions = len(list(interactions_dir.glob("*.json"))) if interactions_dir.exists() else 0
        
        stats = {
            "total_sessions": len(sessions),
            "total_personas": len(personas),
            "total_interactions": total_interactions,
            "persona_types": {},
            "locations": {},
            "arendtian_modes": {},
            "recent_activity": {
                "last_session": sessions[0].get('start_time', 'Never') if sessions else 'Never',
                "sessions_this_week": 0,
                "personas_this_week": 0
            }
        }
        
        # Analyze persona distribution
        for persona in personas:
            persona_type = persona.get('type', 'unknown')
            location = persona.get('location', 'unknown')
            mode = persona.get('arendtian_mode', 'unknown')
            
            stats["persona_types"][persona_type] = stats["persona_types"].get(persona_type, 0) + 1
            stats["locations"][location] = stats["locations"].get(location, 0) + 1
            stats["arendtian_modes"][mode] = stats["arendtian_modes"].get(mode, 0) + 1
        
        return stats
