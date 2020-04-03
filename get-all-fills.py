#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get all fills from one side of the book
all_fills = client.get_fills(
    market=['WETH-DAI'], # 'DAI-WETH' side of the book is not included
    limit=2,  # optional
    startingBefore=None  # optional
)

jsondata = json.dumps( all_fills, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
