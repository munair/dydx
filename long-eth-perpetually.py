#!/usr/bin/env python3

import json
import time
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Define the order size and the return on assets required
ordersize = Decimal("0.1")
requiredreturn = Decimal("1.01")


# Start perpetual loop
while True:

    # Get WETH-DAI market information
    market = client.get_market( market='WETH-DAI' )

    # Get the WETH-DAI orderbook
    orderbook = client.get_orderbook( market='WETH-DAI' )

    # Define minimum tick size, best ask, and best bid values
    quotetick = market["market"]["minimumTickSize"]
    bestask = orderbook["asks"][0]["price"]
    bestbid = orderbook["bids"][0]["price"]

    # Define bid
    # This bid is either the best bid in the orderbook or
    # one quote currency tick below the best ask
    if Decimal(bestask) - Decimal(bestbid) > Decimal(quotetick):
        rawbid = Decimal(bestask) - Decimal(quotetick)
        bid = rawbid.quantize( Decimal(quotetick) )
    else:
        rawbid = Decimal(bestbid)
        bid = rawbid.quantize( Decimal(quotetick) )

    # Define ask
    # This ask closes the position opened by the bid
    # The ask is the required return on the bid
    ask = Decimal(bid) * requiredreturn


    # STEP 1
    #
    #

    # Create order to BUY ETH
    placed_bid = client.place_order(
        market=consts.PAIR_WETH_DAI,
        side=consts.SIDE_BUY,
        amount=utils.token_to_wei(ordersize, consts.MARKET_WETH),
        price=bid,
        fillOrKill=False,
        postOnly=False
    )

    # Display order information
    jsondata = json.dumps( placed_bid, sort_keys=True, indent=4, separators=(',', ': ') )
    print ( jsondata )

    # Loop until the bid order is filled
    while True:
        # Give the bid placed five seconds to fill
        time.sleep(5)

        # Get fills created by my account for both sides of the orderbook
        my_fills = client.get_my_fills(
            market=['WETH-DAI'],
            limit=1
        )
        if my_fills["fills"][0]["orderId"] == placed_bid["order"]["id"]:
            break


    # STEP 2
    #
    #

    # Create order to SELL ETH
    placed_ask = client.place_order(
        market=consts.PAIR_WETH_DAI,
        side=consts.SIDE_SELL,
        amount=utils.token_to_wei(ordersize, consts.MARKET_WETH),
        price=ask.quantize( Decimal(quotetick) ),
        fillOrKill=False,
        postOnly=False
    )

    # Display order information
    jsondata = json.dumps( placed_ask, sort_keys=True, indent=4, separators=(',', ': ') )
    print ( jsondata )

    # Loop until the ask order is filled
    while True:
        # Every five seconds poll to determine if the ask placed was fill
        time.sleep(5)

        # Get fills created by my account for both sides of the orderbook
        my_fills = client.get_my_fills(
            market=['WETH-DAI'],
            limit=1
        )
        if my_fills["fills"][0]["orderId"] == placed_ask["order"]["id"]:
            break
