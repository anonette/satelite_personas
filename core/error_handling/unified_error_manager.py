"""
Unified Error Management System for Prague Spectral Multiplicity Theater
Consolidates all error handling, fallback systems, and reliability monitoring
"""

import logging
import traceback
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ErrorEvent:
    """Structured error event for tracking and analysis"""
    timestamp: str
    error_type: str
    component: str
    message: str
    severity: str  # 'low', 'medium', 'high', 'critical'
    context: Dict[str, Any]
    stack_trace: Optional[str] = None
    resolved: bool = False
    fallback_used: Optional[str] = None

class UnifiedErrorManager:
    """Centralized error management with fallback systems and monitoring"""
    
    def __init__(self, log_file: Optional[Path] = None):
        self.log_file = log_file or Path("error_log.json")
        self.error_history: List[ErrorEvent] = []
        self.fallback_registry: Dict[str, Callable] = {}
        self.component_health: Dict[str, str] = {}
        self.error_counts: Dict[str, int] = {}
        
        # Load existing error history
        self._load_error_history()
        
        logger.info("UnifiedErrorManager initialized")
    
    def register_fallback(self, component: str, fallback_func: Callable):
        """Register a fallback function for a component"""
        self.fallback_registry[component] = fallback_func
        logger.info(f"Registered fallback for component: {component}")
    
    def handle_error(self, 
                    error: Exception, 
                    component: str, 
                    context: Dict[str, Any] = None,
                    severity: str = "medium",
                    use_fallback: bool = True) -> Any:
        """
        Handle an error with optional fallback execution
        
        Args:
            error: The exception that occurred
            component: Component where error occurred
            context: Additional context information
            severity: Error severity level
            use_fallback: Whether to attempt fallback
            
        Returns:
            Result from fallback function if available and successful, None otherwise
        """
        if context is None:
            context = {}
        
        # Create error event
        error_event = ErrorEvent(
            timestamp=datetime.now().isoformat(),
            error_type=type(error).__name__,
            component=component,
            message=str(error),
            severity=severity,
            context=context,
            stack_trace=traceback.format_exc()
        )
        
        # Log the error
        self._log_error(error_event)
        
        # Update component health
        self._update_component_health(component, "error")
        
        # Attempt fallback if available and requested
        fallback_result = None
        if use_fallback and component in self.fallback_registry:
            try:
                fallback_result = self.fallback_registry[component](error, context)
                error_event.fallback_used = f"{component}_fallback"
                error_event.resolved = True
                logger.info(f"Fallback successful for {component}")
                
                # Update component health to degraded (working with fallback)
                self._update_component_health(component, "degraded")
                
            except Exception as fallback_error:
                logger.error(f"Fallback failed for {component}: {fallback_error}")
                self._update_component_health(component, "failed")
        
        # Store error event
        self.error_history.append(error_event)
        self._save_error_history()
        
        # Display user-friendly error in Streamlit if available
        self._display_streamlit_error(error_event, fallback_result is not None)
        
        return fallback_result
    
    def _log_error(self, error_event: ErrorEvent):
        """Log error event with appropriate level"""
        log_message = f"{error_event.component}: {error_event.message}"
        
        if error_event.severity == "critical":
            logger.critical(log_message)
        elif error_event.severity == "high":
            logger.error(log_message)
        elif error_event.severity == "medium":
            logger.warning(log_message)
        else:
            logger.info(log_message)
    
    def _update_component_health(self, component: str, status: str):
        """Update component health status"""
        self.component_health[component] = status
        self.error_counts[component] = self.error_counts.get(component, 0) + 1
    
    def _display_streamlit_error(self, error_event: ErrorEvent, fallback_used: bool):
        """Display user-friendly error in Streamlit interface"""
        try:
            if error_event.severity == "critical":
                st.error(f"🚨 Critical Error in {error_event.component}: {error_event.message}")
            elif error_event.severity == "high":
                st.error(f"❌ Error in {error_event.component}: {error_event.message}")
            elif fallback_used:
                st.warning(f"⚠️ {error_event.component} encountered an issue but is using fallback system")
            else:
                st.info(f"ℹ️ Minor issue in {error_event.component}: {error_event.message}")
        except:
            # Streamlit not available or error in display
            pass
    
    def _load_error_history(self):
        """Load error history from file"""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.error_history = [ErrorEvent(**event) for event in data.get('errors', [])]
                    self.component_health = data.get('component_health', {})
                    self.error_counts = data.get('error_counts', {})
                logger.info(f"Loaded {len(self.error_history)} error events from history")
            except Exception as e:
                logger.warning(f"Could not load error history: {e}")
    
    def _save_error_history(self):
        """Save error history to file"""
        try:
            data = {
                'errors': [asdict(event) for event in self.error_history[-100:]],  # Keep last 100
                'component_health': self.component_health,
                'error_counts': self.error_counts,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save error history: {e}")
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status"""
        total_errors = len(self.error_history)
        recent_errors = len([e for e in self.error_history 
                           if (datetime.now() - datetime.fromisoformat(e.timestamp)).seconds < 3600])
        
        # Determine overall health
        if recent_errors == 0:
            overall_health = "healthy"
        elif recent_errors < 5:
            overall_health = "degraded"
        else:
            overall_health = "unhealthy"
        
        return {
            'overall_health': overall_health,
            'total_errors': total_errors,
            'recent_errors_1h': recent_errors,
            'component_health': self.component_health.copy(),
            'error_counts': self.error_counts.copy(),
            'active_fallbacks': len([c for c, h in self.component_health.items() if h == "degraded"])
        }
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get error summary for the last N hours"""
        cutoff = datetime.now().timestamp() - (hours * 3600)
        recent_errors = [
            e for e in self.error_history 
            if datetime.fromisoformat(e.timestamp).timestamp() > cutoff
        ]
        
        # Group by component
        component_errors = {}
        for error in recent_errors:
            if error.component not in component_errors:
                component_errors[error.component] = []
            component_errors[error.component].append(error)
        
        return {
            'total_recent_errors': len(recent_errors),
            'component_breakdown': {
                comp: len(errors) for comp, errors in component_errors.items()
            },
            'severity_breakdown': {
                severity: len([e for e in recent_errors if e.severity == severity])
                for severity in ['low', 'medium', 'high', 'critical']
            },
            'resolved_errors': len([e for e in recent_errors if e.resolved])
        }
    
    def clear_old_errors(self, days: int = 7):
        """Clear error history older than specified days"""
        cutoff = datetime.now().timestamp() - (days * 24 * 3600)
        self.error_history = [
            e for e in self.error_history 
            if datetime.fromisoformat(e.timestamp).timestamp() > cutoff
        ]
        self._save_error_history()
        logger.info(f"Cleared error history older than {days} days")

# Global error manager instance
_global_error_manager = None

def get_error_manager() -> UnifiedErrorManager:
    """Get the global error manager instance"""
    global _global_error_manager
    if _global_error_manager is None:
        _global_error_manager = UnifiedErrorManager()
    return _global_error_manager

def handle_error(error: Exception, 
                component: str, 
                context: Dict[str, Any] = None,
                severity: str = "medium",
                use_fallback: bool = True) -> Any:
    """Convenience function to handle errors using global manager"""
    return get_error_manager().handle_error(error, component, context, severity, use_fallback)

def register_fallback(component: str, fallback_func: Callable):
    """Convenience function to register fallback using global manager"""
    get_error_manager().register_fallback(component, fallback_func)

# Common fallback functions
def api_fallback(error: Exception, context: Dict[str, Any]) -> str:
    """Fallback for API errors"""
    return "API temporarily unavailable. Using cached data or simplified functionality."

def persona_generation_fallback(error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback for persona generation errors"""
    return {
        'name': 'Fallback Persona',
        'location': context.get('location', 'Unknown'),
        'role': 'Spectral Being (Fallback Mode)',
        'type': 'fallback',
        'perspective': 'Operating in simplified mode due to system limitations.',
        'voice': 'I am a simplified spectral being, manifested when the full system encounters difficulties.'
    }

def image_analysis_fallback(error: Exception, context: Dict[str, Any]) -> Dict[str, Any]:
    """Fallback for image analysis errors"""
    return {
        'analysis': 'Image analysis temporarily unavailable',
        'spectral_data': {'NDVI': 0.5, 'Urban_Index': 0.3},
        'description': 'Using default spectral values due to analysis system limitations.'
    }

# Register common fallbacks
def initialize_common_fallbacks():
    """Initialize common fallback functions"""
    manager = get_error_manager()
    manager.register_fallback('api', api_fallback)
    manager.register_fallback('persona_generation', persona_generation_fallback)
    manager.register_fallback('image_analysis', image_analysis_fallback)

# Error Classes for backward compatibility
class TheaterError(Exception):
    """Base exception for theater-related errors"""
    pass

class PersonaGenerationError(TheaterError):
    """Error in persona generation"""
    pass

class APIError(TheaterError):
    """Error with external API calls"""
    pass

class ImageProcessingError(TheaterError):
    """Error in image processing"""
    pass

class ConfigurationError(TheaterError):
    """Error in system configuration"""
    pass

# Decorator functions for backward compatibility
def error_handler(severity: str = "medium", fallback_value: Any = None):
    """Decorator for error handling with fallback"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                component = func.__module__ + "." + func.__name__
                result = handle_error(e, component, {}, severity, True)
                return result if result is not None else fallback_value
        return wrapper
    return decorator

def with_fallback(fallback_value: Any = None):
    """Decorator that returns fallback value on any error"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                component = func.__module__ + "." + func.__name__
                handle_error(e, component, {}, "low", False)
                return fallback_value
        return wrapper
    return decorator

# Fallback classes for backward compatibility
class FallbackPersonaGenerator:
    """Fallback persona generator when main systems fail"""
    
    def generate_persona(self, location: str = "Unknown") -> Dict[str, Any]:
        return persona_generation_fallback(Exception("Fallback mode"), {"location": location})

class MockDataProvider:
    """Provides mock data when real data is unavailable"""
    
    def get_spectral_data(self, location: str = "Unknown") -> Dict[str, float]:
        return {"NDVI": 0.5, "Urban_Index": 0.3, "NDWI": 0.4}

class EmergencyTheaterMode:
    """Emergency mode for theater when systems fail"""
    
    def __init__(self):
        self.active = False
    
    def activate(self):
        self.active = True
        logger.warning("Emergency Theater Mode activated")
    
    def deactivate(self):
        self.active = False
        logger.info("Emergency Theater Mode deactivated")

# Monitoring classes for backward compatibility
class ReliabilityMonitor:
    """Monitor system reliability"""
    
    def get_status(self) -> Dict[str, Any]:
        return get_error_manager().get_system_health()

class SystemHealthChecker:
    """Check system health"""
    
    def check_health(self) -> str:
        health = get_error_manager().get_system_health()
        return health['overall_health']

class PerformanceTracker:
    """Track system performance"""
    
    def get_metrics(self) -> Dict[str, Any]:
        return get_error_manager().get_error_summary()

# Alias for backward compatibility
ErrorManager = UnifiedErrorManager

# Auto-initialize on import
initialize_common_fallbacks()
