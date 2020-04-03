#!/usr/bin/env python3

import json
import time
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Define return on assets required
requiredreturn = Decimal("0.99")

# Get WETH-DAI market information
market = client.get_market( market='WETH-DAI' )

# Get the WETH-DAI orderbook
orderbook = client.get_orderbook( market='WETH-DAI' )

# Define minimum tick size, best ask, and best bid values
quotetick = market["market"]["minimumTickSize"]
bestask = orderbook["asks"][0]["price"]
bestbid = orderbook["bids"][0]["price"]

# Define ask
if Decimal(bestask) - Decimal(bestbid) > Decimal(quotetick):
    rawask = Decimal(bestbid) + Decimal(quotetick)
    ask = rawask.quantize( Decimal(quotetick) )
else:
    rawask = Decimal(bestask)
    ask = rawask.quantize( Decimal(quotetick) )

# Create order to SELL 0.10 ETH
placed_ask = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_SELL,
    amount=utils.token_to_wei(0.1, consts.MARKET_WETH),
    price=ask,
    fillOrKill=False,
    postOnly=False
)

# Display order information
jsondata = json.dumps( placed_ask, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )


while True:
    # Give the bid placed five seconds to fill
    time.sleep(5)

    # Get fills created by my account for both sides of the orderbook
    my_fills = client.get_my_fills(
        market=['WETH-DAI'],
        limit=1
    )
    if my_fills["fills"][0]["orderId"] == placed_ask["order"]["id"]:
        break

# Place bid to close the position opened by the ask
# that returns 500 basis points
bid = Decimal(ask) * requiredreturn

# Create order to SELL 0.10 ETH
placed_bid = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_BUY,
    amount=utils.token_to_wei(0.1, consts.MARKET_WETH),
    price=bid.quantize( Decimal(quotetick) ),
    fillOrKill=False,
    postOnly=False
)

# Display order information
jsondata = json.dumps( placed_bid, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )
