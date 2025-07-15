"""
Error Handling and Reliability System for Prague Spectral Multiplicity Theater
Provides comprehensive error handling, graceful degradation, and robust fallback mechanisms
"""

from .unified_error_manager import (
    TheaterError,
    PersonaGenerationError,
    APIError,
    ImageProcessingError,
    ConfigurationError,
    ErrorManager,
    error_handler,
    with_fallback,
    FallbackPersonaGenerator,
    MockDataProvider,
    EmergencyTheaterMode,
    ReliabilityMonitor,
    SystemHealthChecker,
    PerformanceTracker,
    get_error_manager
)

__all__ = [
    # Core error classes
    'TheaterError',
    'PersonaGenerationError', 
    'APIError',
    'ImageProcessingError',
    'ConfigurationError',
    
    # Error management
    'ErrorManager',
    'error_handler',
    'with_fallback',
    'get_error_manager',
    
    # Fallback systems
    'FallbackPersonaGenerator',
    'MockDataProvider',
    'EmergencyTheaterMode',
    
    # Reliability monitoring
    'ReliabilityMonitor',
    'SystemHealthChecker',
    'PerformanceTracker'
]
