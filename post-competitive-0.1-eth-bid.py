#!/usr/bin/env python3

import json
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get WETH-DAI market information
market = client.get_market(
    market='WETH-DAI'
)

# Get the WETH-DAI orderbook
orderbook = client.get_orderbook(
    market='WETH-DAI'
)

quotetick = market["market"]["minimumTickSize"]
bestask = orderbook["asks"][0]["price"]
bestbid = orderbook["bids"][0]["price"]

if bestask - bestbid > quotetick:
    rawbid = Decimal(bestask) - Decimal(quotetick)
    bid = rawbid.quantize(Decimal(quotetick))
else:
    rawbid = Decimal(bestbid)
    bid = rawbid.quantize(Decimal(quotetick))

# Create order to BUY 0.10 ETH
created_order = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_BUY,
    amount=utils.token_to_wei(0.1, consts.MARKET_WETH),
    price=bid,
    fillOrKill=False,
    postOnly=False
)

# Display order information
jsondata = json.dumps( created_order, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )
