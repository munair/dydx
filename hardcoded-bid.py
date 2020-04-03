#!/usr/bin/env python3

import json
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Define bid
bid = Decimal("134.65")
amt = Decimal("0.1")

# Create order to BUY ETH
created_order = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_BUY,
    amount=utils.token_to_wei(amt, consts.MARKET_WETH),
    price=bid,
    fillOrKill=False,
    postOnly=False
)

# Display order information
jsondata = json.dumps( created_order, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )
