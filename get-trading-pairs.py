#!/usr/bin/env python3

import json

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get all trading pairs for dydx
pairs = client.get_pairs()

jsondata = json.dumps( pairs, sort_keys=True, indent=4, separators=(',', ': ') )

print ( jsondata )
