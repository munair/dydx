#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


orderbook = client.get_orderbook( market='WETH-DAI' )

jsondata = json.dumps( orderbook, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
