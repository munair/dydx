#!/usr/bin/env python3

import json

import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get fills created by my account for both sides of the orderbook
my_fills = client.get_my_fills(
    market=['WETH-DAI'],
    limit=None,  # optional
    startingBefore=None  # optional
)

jsondata = json.dumps( my_fills, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
