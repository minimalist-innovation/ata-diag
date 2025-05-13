import logging
import os

import toml


def setup_logging():
    """Configure logging based on .streamlit/config.toml settings"""
    try:
        # Attempt to load the config.toml file
        config_path = os.path.join('.streamlit', 'config.toml')
        if os.path.exists(config_path):
            config = toml.load(config_path)

            # Get logging settings from config
            log_level = config.get('logger', {}).get('level', 'info').upper()
            log_format = config.get('logger', {}).get('messageFormat',
                                                      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            # Check if file logging is enabled
            enable_file_logging = config.get('logger', {}).get('enableFileLogging', False)
            log_file_path = config.get('logger', {}).get('logFilePath', 'logs/app.log')

            # Convert string level to logging level
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }
            level = level_map.get(log_level, logging.INFO)

            # Configure basic logging
            logging.basicConfig(level=level, format=log_format)

            # Add file handler if enabled
            if enable_file_logging:
                # Ensure log directory exists
                log_dir = os.path.dirname(log_file_path)
                if log_dir and not os.path.exists(log_dir):
                    os.makedirs(log_dir)

                # Add file handler
                file_handler = logging.FileHandler(log_file_path)
                file_handler.setFormatter(logging.Formatter(log_format))

                # Add to root logger
                root_logger = logging.getLogger()
                root_logger.addHandler(file_handler)

            return True
        else:
            # Fall back to basic config if no file exists
            logging.basicConfig(level=logging.INFO,
                                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            return False
    except Exception as e:
        # If anything goes wrong, fall back to basic config
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.error(f"Error setting up logging from config: {str(e)}")
        return False
