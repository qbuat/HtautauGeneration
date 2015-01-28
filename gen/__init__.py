import logging
import os

log = logging.getLogger('gen')


SEEDS = [123456000 + i for i in range(0, 50)]
MASSES = range(60, 205, 5)
DSIDS = [300000 + i for i in xrange(len(MASSES))]
FLAT_DRIVER = 'flatskim2.py'

from cards import get_jo
from cmd import generate_cmd, d3pd_cmd, flat_cmd, flat2_cmd

__all__ = [
    'get_jo',
    'generate_cmd',
    'd3pd_cmd',
    'flat_cmd',
    'flat2_cmd',
]

