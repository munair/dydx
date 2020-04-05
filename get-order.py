#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get WETH-DAI orders created by my account
my_order = client.get_order( orderId="0x9df797fe0bd0326cc9deb659eb2a7f5a9e560005ae6d5c44ebf0425bf6125b1b" )

jsondata = json.dumps( my_order, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
