#!/usr/bin/env python3

import json
import time
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Define bid size
# Note: no bid price specified
ordersize = Decimal("0.1")


# Start perpetual loop
while True:

    # Get the WETH-DAI orderbook
    orderbook = client.get_orderbook( market='WETH-DAI' )

    # Define minimum tick size, best ask, and best bid values
    bestask = orderbook["asks"][0]["price"]

    # Define bid
    # Note: take the best ask
    bid = Decimal(bestask)

    # Create order to BUY ETH
    placed_bid = client.place_order(
        market=consts.PAIR_WETH_DAI,
        side=consts.SIDE_BUY,
        amount=utils.token_to_wei(ordersize, consts.MARKET_WETH),
        price=bid,
        fillOrKill=True,
        postOnly=False
    )

    # Display order information
    jsondata = json.dumps( placed_bid, sort_keys=True, indent=4, separators=(',', ': ') )
    print ( jsondata )

    # Give the bid placed two seconds to fill
    # Then get details of submitted order
    time.sleep(2)
    my_order = client.get_order( orderId=placed_bid["order"]["id"] )

    # Display order information
    jsondata = json.dumps( my_order, sort_keys=True, indent=4, separators=(',', ': ') )
    print ( jsondata )

    if my_order["order"]["status"] == "CANCELED":
        # Repeat: Start at the top of the loop and try again.
        print ("Order ", my_order["order"]["id"], " was not filled. Retrying...")
        continue
    elif my_order["order"]["status"] == "FILLED":
        # Exit: End the loop and exit.
        print ("Order ", my_order["order"]["id"], " was filled at: ", my_order["order"]["price"], " DAI/ETH.")
        break
    else:
        # Cancel the previously created order and try again from the top.
        print ("Order ", my_order["order"]["id"], " was not killed or filled. Cancelling...")
        canceled_order = client.cancel_order( hash=my_order["order"]["id"] )

        # Display order kill information
        jsondata = json.dumps( canceled_order, sort_keys=True, indent=4, separators=(',', ': ') )
        print ( jsondata )
