import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s:%(levelname)s: %(message)s',
        handlers=[
            # Specify mode='w' here instead of filemode in basicConfig
            logging.FileHandler('mcrits.log', mode='w'),  
            logging.StreamHandler()
        ]
    )