class ConfigurationError(Exception):
    """Custom exception for configuration errors."""

    def __init__(self, message):
        super().__init__(message)
