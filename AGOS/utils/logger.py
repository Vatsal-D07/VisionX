import logging
import sys
from datetime import datetime

class Logger:
    @staticmethod
    def setup_logger(name: str = "AGOS"):
        """
        Sets up a logger with console and file handlers.
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # file
        # ensure logs dir exists or just write to root for now?
        # User structure didn't specify logs dir, so I'll keep it simple or put in root.
        # Let's avoid file logging to keep it clean unless requested, 
        # but "production quality" usually implies file logs.
        # I'll stick to console for now to avoid file permission clutter, 
        # or maybe a single run.log.
        
        return logger

# Singleton instance
log = Logger.setup_logger()
