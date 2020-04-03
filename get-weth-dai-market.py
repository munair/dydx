#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


market = client.get_market( market='WETH-DAI' )

jsondata = json.dumps( market, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
