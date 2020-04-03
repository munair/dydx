#!/usr/bin/env python3

import json
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Define ask 
ask = Decimal("134.65")
amt = Decimal("0.1")

# Create order to SELL ETH
created_order = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_SELL,
    amount=utils.token_to_wei(amt, consts.MARKET_WETH),
    price=ask,
    fillOrKill=False,
    postOnly=False
)

# Display order information
jsondata = json.dumps( created_order, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )
