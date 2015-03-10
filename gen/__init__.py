import logging
import os

log = logging.getLogger('gen')


SEEDS = [123456000 + i for i in range(0, 50)]
MASSES = range(60, 205, 5)
DSIDS = [300000 + i for i in xrange(len(MASSES))]

BASE_DIR = os.getenv('DIR_HTAUTAUGENERATION_SETUP')
PROD_DIR = './d3pd'
NTUPLE_DIR = './ntuple'
FLAT_DRIVER = 'flatskim.py'
FLAT_DRIVER_2 = 'flatskim2.py'

from cmd import generate_cmd, d3pd_cmd, flat_cmd, flat2_cmd

__all__ = [
    'generate_cmd',
    'd3pd_cmd',
    'flat_cmd',
    'flat2_cmd',
]

