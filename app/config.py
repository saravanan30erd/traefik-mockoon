import logging
import sys
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Mockoon CLI path
MOCKOON_CLI = '/usr/local/bin/mockoon-cli'

# Traefik URL
TRAEFIK_URL = 'mock.example.com'
