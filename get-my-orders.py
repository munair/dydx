#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get WETH-DAI orders created by my account
my_orders = client.get_my_orders(
    market=['WETH-DAI'],
    limit=None,
    startingBefore=None
)

jsondata = json.dumps( my_orders, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
