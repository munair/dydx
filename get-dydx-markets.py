#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get dYdX markets
markets = client.get_markets()

jsondata = json.dumps( markets, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
