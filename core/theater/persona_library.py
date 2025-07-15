"""
Persona Library System for Prague Spectral Multiplicity Theater
Handles saving, loading, and managing personas and sessions with comprehensive logging
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)

@dataclass
class PersonaEntry:
    """A saved persona with metadata"""
    id: str
    persona: Dict[str, Any]
    tags: List[str]
    created_at: str
    updated_at: str
    notes: str
    source_image: Optional[str] = None
    usage_count: int = 0
    last_used: Optional[str] = None

@dataclass
class SessionEntry:
    """A saved theater session"""
    id: str
    name: str
    personas: List[Dict[str, Any]]
    dialogue_history: List[Dict[str, Any]]
    selected_image: Optional[str]
    created_at: str
    persona_count: int
    dialogue_count: int
    tags: List[str]
    notes: str

@dataclass
class CollectionEntry:
    """A collection of personas"""
    id: str
    name: str
    description: str
    persona_ids: List[str]
    created_at: str
    updated_at: str
    tags: List[str]

class PersonaLibrary:
    """Comprehensive persona and session management system"""
    
    def __init__(self, library_dir: Path):
        self.library_dir = Path(library_dir)
        self.personas_dir = self.library_dir / "saved_personas"
        self.sessions_dir = self.library_dir / "sessions"
        self.collections_dir = self.library_dir / "collections"
        self.index_file = self.library_dir / "library_index.json"
        
        # Ensure directories exist
        for directory in [self.library_dir, self.personas_dir, self.sessions_dir, self.collections_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Initialize or load index
        self.index = self._load_or_create_index()
        
        logger.info(f"PersonaLibrary initialized at {self.library_dir}")
    
    def _load_or_create_index(self) -> Dict[str, Any]:
        """Load or create the library index"""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    index = json.load(f)
                logger.info(f"Loaded library index with {len(index.get('personas', {}))} personas")
                return index
            except Exception as e:
                logger.error(f"Error loading index: {e}")
        
        # Create new index
        index = {
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "personas": {},
            "sessions": {},
            "collections": {},
            "stats": {
                "total_personas": 0,
                "total_sessions": 0,
                "total_collections": 0,
                "last_updated": datetime.now().isoformat()
            }
        }
        self._save_index(index)
        logger.info("Created new library index")
        return index
    
    def _save_index(self, index: Optional[Dict[str, Any]] = None):
        """Save the library index"""
        if index is None:
            index = self.index
        
        index["stats"]["last_updated"] = datetime.now().isoformat()
        
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(index, f, indent=2, ensure_ascii=False)
            logger.debug("Library index saved")
        except Exception as e:
            logger.error(f"Error saving index: {e}")
    
    def save_persona(self, persona: Dict[str, Any], tags: List[str] = None, 
                    notes: str = "", source_image: str = None) -> str:
        """Save a persona to the library"""
        persona_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if tags is None:
            tags = []
        
        # Create persona entry
        entry = PersonaEntry(
            id=persona_id,
            persona=persona,
            tags=tags,
            created_at=timestamp,
            updated_at=timestamp,
            notes=notes,
            source_image=source_image,
            usage_count=0,
            last_used=None
        )
        
        # Save persona file
        persona_file = self.personas_dir / f"{persona_id}.json"
        try:
            with open(persona_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(entry), f, indent=2, ensure_ascii=False)
            
            # Update index
            self.index["personas"][persona_id] = {
                "name": persona.get("name", "Unknown"),
                "type": persona.get("type", "unknown"),
                "location": persona.get("location", "unknown"),
                "created_at": timestamp,
                "tags": tags,
                "file": str(persona_file)
            }
            self.index["stats"]["total_personas"] += 1
            self._save_index()
            
            logger.info(f"Saved persona: {persona.get('name', 'Unknown')} ({persona_id})")
            return persona_id
            
        except Exception as e:
            logger.error(f"Error saving persona: {e}")
            raise
    
    def load_persona(self, persona_id: str) -> Optional[PersonaEntry]:
        """Load a persona from the library"""
        if persona_id not in self.index["personas"]:
            logger.warning(f"Persona {persona_id} not found in index")
            return None
        
        persona_file = self.personas_dir / f"{persona_id}.json"
        if not persona_file.exists():
            logger.error(f"Persona file not found: {persona_file}")
            return None
        
        try:
            with open(persona_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            entry = PersonaEntry(**data)
            
            # Update usage stats
            entry.usage_count += 1
            entry.last_used = datetime.now().isoformat()
            
            # Save updated entry
            with open(persona_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(entry), f, indent=2, ensure_ascii=False)
            
            logger.info(f"Loaded persona: {entry.persona.get('name', 'Unknown')}")
            return entry
            
        except Exception as e:
            logger.error(f"Error loading persona {persona_id}: {e}")
            return None
    
    def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona from the library"""
        if persona_id not in self.index["personas"]:
            logger.warning(f"Persona {persona_id} not found in index")
            return False
        
        persona_file = self.personas_dir / f"{persona_id}.json"
        
        try:
            # Remove file
            if persona_file.exists():
                persona_file.unlink()
            
            # Remove from index
            persona_name = self.index["personas"][persona_id].get("name", "Unknown")
            del self.index["personas"][persona_id]
            self.index["stats"]["total_personas"] -= 1
            self._save_index()
            
            logger.info(f"Deleted persona: {persona_name} ({persona_id})")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting persona {persona_id}: {e}")
            return False
    
    def search_personas(self, query: str = "", tags: List[str] = None, 
                       persona_type: str = None) -> Dict[str, Dict[str, Any]]:
        """Search personas by query, tags, or type"""
        results = {}
        
        for persona_id, persona_info in self.index["personas"].items():
            # Check query match
            if query:
                query_lower = query.lower()
                if not any(query_lower in str(value).lower() 
                          for value in [persona_info.get("name", ""), 
                                      persona_info.get("location", ""),
                                      persona_info.get("type", "")]):
                    continue
            
            # Check tags match
            if tags:
                persona_tags = persona_info.get("tags", [])
                if not any(tag in persona_tags for tag in tags):
                    continue
            
            # Check type match
            if persona_type and persona_info.get("type") != persona_type:
                continue
            
            results[persona_id] = persona_info
        
        logger.debug(f"Search found {len(results)} personas")
        return results
    
    def get_all_personas(self) -> Dict[str, Dict[str, Any]]:
        """Get all personas in the library"""
        return self.index["personas"].copy()
    
    def save_session(self, name: str, personas: List[Dict[str, Any]], 
                    dialogue_history: List[Dict[str, Any]], 
                    selected_image: str = None, tags: List[str] = None,
                    notes: str = "") -> str:
        """Save a theater session"""
        session_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if tags is None:
            tags = []
        
        # Create session entry
        entry = SessionEntry(
            id=session_id,
            name=name,
            personas=personas,
            dialogue_history=dialogue_history,
            selected_image=selected_image,
            created_at=timestamp,
            persona_count=len(personas),
            dialogue_count=len(dialogue_history),
            tags=tags,
            notes=notes
        )
        
        # Save session file
        session_file = self.sessions_dir / f"{session_id}.json"
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(entry), f, indent=2, ensure_ascii=False)
            
            # Update index
            self.index["sessions"][session_id] = {
                "name": name,
                "created_at": timestamp,
                "persona_count": len(personas),
                "dialogue_count": len(dialogue_history),
                "tags": tags,
                "file": str(session_file)
            }
            self.index["stats"]["total_sessions"] += 1
            self._save_index()
            
            logger.info(f"Saved session: {name} ({session_id})")
            return session_id
            
        except Exception as e:
            logger.error(f"Error saving session: {e}")
            raise
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session from the library"""
        if session_id not in self.index["sessions"]:
            logger.warning(f"Session {session_id} not found in index")
            return None
        
        session_file = self.sessions_dir / f"{session_id}.json"
        if not session_file.exists():
            logger.error(f"Session file not found: {session_file}")
            return None
        
        try:
            with open(session_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded session: {data.get('name', 'Unknown')}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading session {session_id}: {e}")
            return None
    
    def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all sessions in the library"""
        sessions = []
        for session_id, session_info in self.index["sessions"].items():
            session_info["id"] = session_id
            sessions.append(session_info)
        return sessions
    
    def save_collection(self, name: str, persona_ids: List[str], 
                       description: str = "", tags: List[str] = None) -> str:
        """Save a collection of personas"""
        collection_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        if tags is None:
            tags = []
        
        # Create collection entry
        entry = CollectionEntry(
            id=collection_id,
            name=name,
            description=description,
            persona_ids=persona_ids,
            created_at=timestamp,
            updated_at=timestamp,
            tags=tags
        )
        
        # Save collection file
        collection_file = self.collections_dir / f"{collection_id}.json"
        try:
            with open(collection_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(entry), f, indent=2, ensure_ascii=False)
            
            # Update index
            self.index["collections"][collection_id] = {
                "name": name,
                "description": description,
                "created_at": timestamp,
                "persona_count": len(persona_ids),
                "tags": tags,
                "file": str(collection_file)
            }
            self.index["stats"]["total_collections"] += 1
            self._save_index()
            
            logger.info(f"Saved collection: {name} ({collection_id})")
            return collection_id
            
        except Exception as e:
            logger.error(f"Error saving collection: {e}")
            raise
    
    def load_collection(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """Load a collection from the library"""
        if collection_id not in self.index["collections"]:
            logger.warning(f"Collection {collection_id} not found in index")
            return None
        
        collection_file = self.collections_dir / f"{collection_id}.json"
        if not collection_file.exists():
            logger.error(f"Collection file not found: {collection_file}")
            return None
        
        try:
            with open(collection_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded collection: {data.get('name', 'Unknown')}")
            return data
            
        except Exception as e:
            logger.error(f"Error loading collection {collection_id}: {e}")
            return None
    
    def get_all_collections(self) -> List[Dict[str, Any]]:
        """Get all collections in the library"""
        collections = []
        for collection_id, collection_info in self.index["collections"].items():
            collection_info["id"] = collection_id
            collections.append(collection_info)
        return collections
    
    def get_library_stats(self) -> Dict[str, Any]:
        """Get comprehensive library statistics"""
        stats = self.index["stats"].copy()
        
        # Persona type distribution
        persona_types = {}
        for persona_info in self.index["personas"].values():
            persona_type = persona_info.get("type", "unknown")
            persona_types[persona_type] = persona_types.get(persona_type, 0) + 1
        
        stats["persona_types"] = persona_types
        
        # Recent personas (last 10)
        recent_personas = []
        sorted_personas = sorted(
            self.index["personas"].items(),
            key=lambda x: x[1].get("created_at", ""),
            reverse=True
        )
        for persona_id, persona_info in sorted_personas[:10]:
            recent_personas.append({
                "id": persona_id,
                "name": persona_info.get("name", "Unknown"),
                "created_at": persona_info.get("created_at", "")
            })
        
        stats["recent_personas"] = recent_personas
        
        # Storage usage
        total_size = 0
        for directory in [self.personas_dir, self.sessions_dir, self.collections_dir]:
            for file_path in directory.glob("*.json"):
                total_size += file_path.stat().st_size
        
        stats["storage_size_bytes"] = total_size
        stats["storage_size_mb"] = round(total_size / (1024 * 1024), 2)
        
        return stats
    
    def export_library(self, export_path: Path) -> bool:
        """Export the entire library to a single file"""
        try:
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "library_version": self.index.get("version", "1.0"),
                "index": self.index,
                "personas": {},
                "sessions": {},
                "collections": {}
            }
            
            # Load all personas
            for persona_id in self.index["personas"]:
                entry = self.load_persona(persona_id)
                if entry:
                    export_data["personas"][persona_id] = asdict(entry)
            
            # Load all sessions
            for session_id in self.index["sessions"]:
                session = self.load_session(session_id)
                if session:
                    export_data["sessions"][session_id] = session
            
            # Load all collections
            for collection_id in self.index["collections"]:
                collection = self.load_collection(collection_id)
                if collection:
                    export_data["collections"][collection_id] = collection
            
            # Save export file
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Library exported to {export_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting library: {e}")
            return False
    
    def cleanup_orphaned_files(self) -> int:
        """Clean up orphaned files not referenced in the index"""
        cleaned_count = 0
        
        # Check personas directory
        for file_path in self.personas_dir.glob("*.json"):
            persona_id = file_path.stem
            if persona_id not in self.index["personas"]:
                try:
                    file_path.unlink()
                    cleaned_count += 1
                    logger.info(f"Removed orphaned persona file: {file_path}")
                except Exception as e:
                    logger.error(f"Error removing orphaned file {file_path}: {e}")
        
        # Check sessions directory
        for file_path in self.sessions_dir.glob("*.json"):
            session_id = file_path.stem
            if session_id not in self.index["sessions"]:
                try:
                    file_path.unlink()
                    cleaned_count += 1
                    logger.info(f"Removed orphaned session file: {file_path}")
                except Exception as e:
                    logger.error(f"Error removing orphaned file {file_path}: {e}")
        
        # Check collections directory
        for file_path in self.collections_dir.glob("*.json"):
            collection_id = file_path.stem
            if collection_id not in self.index["collections"]:
                try:
                    file_path.unlink()
                    cleaned_count += 1
                    logger.info(f"Removed orphaned collection file: {file_path}")
                except Exception as e:
                    logger.error(f"Error removing orphaned file {file_path}: {e}")
        
        if cleaned_count > 0:
            logger.info(f"Cleanup completed: removed {cleaned_count} orphaned files")
        
        return cleaned_count
