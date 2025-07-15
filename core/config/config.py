"""
Centralized configuration management for Prague Spectral Multiplicity Theater
Handles environment variables, paths, and feature flags with cross-platform support
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class AppConfig:
    """Application configuration with auto-detection and environment variable support"""
    
    # API settings
    openai_api_key: Optional[str]
    
    # Paths (auto-detected, cross-platform)
    project_root: Path
    images_dir: Path
    persona_library_dir: Path
    sessions_dir: Path
    
    # Feature flags for optional complexity
    enable_shadow_district: bool = True
    enable_advanced_dialogue: bool = True
    enable_vision_api: bool = True
    enable_voice_synthesis: bool = False
    
    # Persona generation settings
    persona_generation_mode: str = "spectral_multiplicity"  # primary system
    max_personas_per_session: int = 10
    
    # Performance settings
    api_timeout: int = 30
    max_image_size: int = 1024
    cache_enabled: bool = True
    
    # Debug settings
    debug_mode: bool = False
    log_level: str = "INFO"

def _get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable"""
    value = os.getenv(key, "").lower()
    if value in ("true", "1", "yes", "on"):
        return True
    elif value in ("false", "0", "no", "off"):
        return False
    return default

def _get_env_int(key: str, default: int) -> int:
    """Get integer value from environment variable"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

def _find_project_root() -> Path:
    """Find the project root directory by looking for key files"""
    current = Path(__file__).parent.parent.parent  # Go up from core/config/
    
    # Look for key project indicators
    key_indicators = ['main.py', 'requirements.txt', 'core', 'images']
    
    # Check current directory first
    if all((current / indicator).exists() for indicator in key_indicators):
        return current.absolute()
    
    # If not found, try going up one more level (in case we're in a subdirectory)
    parent = current.parent
    if all((parent / indicator).exists() for indicator in key_indicators):
        return parent.absolute()
    
    # Fallback to current directory
    logger.warning(f"Could not find project root, using: {current}")
    return current.absolute()

def _load_env_file(project_root: Path) -> None:
    """Load environment variables from .env file if it exists"""
    env_file = project_root / ".env"
    
    if not env_file.exists():
        return
    
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    # Only set if not already in environment
                    if key not in os.environ:
                        os.environ[key] = value
                        
    except Exception as e:
        logger.warning(f"Error loading .env file: {e}")

def get_app_config() -> AppConfig:
    """Get application configuration with auto-detection and environment variables"""
    
    # Find project root
    project_root = _find_project_root()
    
    # Load .env file if it exists
    _load_env_file(project_root)
    
    # Get API key from multiple sources
    api_key = (
        os.getenv("OPENAI_API_KEY") or
        os.getenv("OPENAI_KEY") or
        None
    )
    
    # Auto-detect directories
    images_dir = Path(os.getenv("IMAGES_DIR", project_root / "images"))
    persona_library_dir = Path(os.getenv("PERSONA_LIBRARY_DIR", project_root / "persona_library"))
    sessions_dir = Path(os.getenv("SESSIONS_DIR", project_root / "sessions"))
    
    # Ensure directories exist (create if needed)
    for directory in [images_dir, persona_library_dir, sessions_dir]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create directory {directory}: {e}")
    
    # Feature flags from environment
    enable_shadow_district = _get_env_bool("ENABLE_SHADOW_DISTRICT", True)
    enable_advanced_dialogue = _get_env_bool("ENABLE_ADVANCED_DIALOGUE", True)
    enable_vision_api = _get_env_bool("ENABLE_VISION_API", True)
    enable_voice_synthesis = _get_env_bool("ENABLE_VOICE_SYNTHESIS", False)
    
    # Persona generation settings
    persona_mode = os.getenv("PERSONA_GENERATION_MODE", "spectral_multiplicity")
    max_personas = _get_env_int("MAX_PERSONAS_PER_SESSION", 10)
    
    # Performance settings
    api_timeout = _get_env_int("API_TIMEOUT", 30)
    max_image_size = _get_env_int("MAX_IMAGE_SIZE", 1024)
    cache_enabled = _get_env_bool("CACHE_ENABLED", True)
    
    # Debug settings
    debug_mode = _get_env_bool("DEBUG", False)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    return AppConfig(
        # API settings
        openai_api_key=api_key,
        
        # Paths
        project_root=project_root,
        images_dir=images_dir,
        persona_library_dir=persona_library_dir,
        sessions_dir=sessions_dir,
        
        # Feature flags
        enable_shadow_district=enable_shadow_district,
        enable_advanced_dialogue=enable_advanced_dialogue,
        enable_vision_api=enable_vision_api,
        enable_voice_synthesis=enable_voice_synthesis,
        
        # Persona settings
        persona_generation_mode=persona_mode,
        max_personas_per_session=max_personas,
        
        # Performance settings
        api_timeout=api_timeout,
        max_image_size=max_image_size,
        cache_enabled=cache_enabled,
        
        # Debug settings
        debug_mode=debug_mode,
        log_level=log_level
    )

def validate_config(config: AppConfig) -> list[str]:
    """Validate configuration and return list of issues"""
    issues = []
    
    # Check API key
    if not config.openai_api_key:
        issues.append("OpenAI API key not configured")
    elif config.openai_api_key == "your_openai_api_key_here":
        issues.append("OpenAI API key is placeholder value")
    
    # Check critical directories
    if not config.project_root.exists():
        issues.append(f"Project root directory not found: {config.project_root}")
    
    if not config.images_dir.exists():
        issues.append(f"Images directory not found: {config.images_dir}")
    
    # Check for image files
    if config.images_dir.exists():
        image_extensions = ['.jpg', '.jpeg', '.png', '.tiff', '.tif']
        image_files = []
        for ext in image_extensions:
            image_files.extend(config.images_dir.glob(f"*{ext}"))
        
        if not image_files:
            issues.append(f"No image files found in {config.images_dir}")
    
    # Validate persona generation mode
    valid_modes = ["spectral_multiplicity", "arendtian", "classic", "integrated"]
    if config.persona_generation_mode not in valid_modes:
        issues.append(f"Invalid persona generation mode: {config.persona_generation_mode}")
    
    # Validate numeric settings
    if config.max_personas_per_session < 1:
        issues.append("max_personas_per_session must be at least 1")
    
    if config.api_timeout < 5:
        issues.append("api_timeout should be at least 5 seconds")
    
    return issues

def print_config_summary(config: AppConfig) -> None:
    """Print a summary of the current configuration"""
    print("🔧 Configuration Summary")
    print("=" * 40)
    print(f"Project Root: {config.project_root}")
    print(f"Images Directory: {config.images_dir}")
    print(f"API Key Configured: {'✅' if config.openai_api_key else '❌'}")
    print(f"Persona Mode: {config.persona_generation_mode}")
    print(f"Max Personas: {config.max_personas_per_session}")
    print()
    print("Feature Flags:")
    print(f"  Shadow District: {'✅' if config.enable_shadow_district else '❌'}")
    print(f"  Advanced Dialogue: {'✅' if config.enable_advanced_dialogue else '❌'}")
    print(f"  Vision API: {'✅' if config.enable_vision_api else '❌'}")
    print(f"  Voice Synthesis: {'✅' if config.enable_voice_synthesis else '❌'}")
    print()

# Global config instance (lazy-loaded)
_config_instance: Optional[AppConfig] = None

def get_config() -> AppConfig:
    """Get the global configuration instance (singleton pattern)"""
    global _config_instance
    if _config_instance is None:
        _config_instance = get_app_config()
    return _config_instance

def reload_config() -> AppConfig:
    """Reload configuration (useful for testing or config changes)"""
    global _config_instance
    _config_instance = None
    return get_config()

# Convenience functions for common config access
def get_images_dir() -> Path:
    """Get the images directory path"""
    return get_config().images_dir

def get_api_key() -> Optional[str]:
    """Get the OpenAI API key"""
    return get_config().openai_api_key

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled"""
    config = get_config()
    feature_map = {
        "shadow_district": config.enable_shadow_district,
        "advanced_dialogue": config.enable_advanced_dialogue,
        "vision_api": config.enable_vision_api,
        "voice_synthesis": config.enable_voice_synthesis,
    }
    return feature_map.get(feature, False)

def get_persona_mode() -> str:
    """Get the current persona generation mode"""
    return get_config().persona_generation_mode
