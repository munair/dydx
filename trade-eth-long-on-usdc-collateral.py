#!/usr/bin/env python3

import json
import time
from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Define the return on assets and price drop (pricetrigger) required for bidding
# Also define a stop limit ask and a stop market ask (just in case the price crashes)
# In addition, define target (mimimum) collateralization ratio and maximum leverage
# Note: to make a bid without waiting for the prices to fall, set the price trigger to 1
pricetrigger = Decimal( "0.99" )
# Submit a bid after a 1% drop in the ask price
requiredreturn = Decimal( "1.01" )
# Submit an ask immediately after the bid is filled.
stoplimitask = Decimal( "0.99" )
# Break out of a loop waiting for the profitable ask to fill if the stop limit is triggered.
stopmarketask = Decimal( "0.98" )
# Break out of a loop waiting for the profitable ask to fill if the stop market is triggered.
maximumleverage = Decimal( "5" )
# 5X constants established by dYdX (note that it is 4X for a SHORT)
minimumcollateralization = Decimal( "1.25" )
# dYdX accounts must be overcollateralized at the ratio of 125%.
# Note that positions are liquidated at 115%.
# However, the target collateralization should reflect risk tolerance.
# For example, a cautious trader may feel comfortable using a target of 150%.
# Or the trader may prefer to be overcollateralized at 200% during periods of high volatility.


# Define best price function
# Return market / limit price
def bestprices( tradingpair, quotetick ):
    # Get the orderbook for the trading pair specified
    orderbook = client.get_orderbook( market = tradingpair )

    # Define best ask and best bid values in the market
    marketask = orderbook["asks"][0]["price"]
    marketbid = orderbook["bids"][0]["price"]

    # Define most competitive limit ask
    if Decimal( marketask ) - Decimal( marketbid ) > Decimal( quotetick ):
        rawbid = Decimal( marketask ) - Decimal( quotetick )
        limitbid = rawbid.quantize( Decimal( quotetick ) )
    else:
        rawbid = Decimal( marketbid )
        limitbid = rawbid.quantize( Decimal( quotetick ) )

    # Define most competitive limit bid
    if Decimal( marketask ) - Decimal(marketbid) > Decimal(quotetick):
        rawask = Decimal( marketbid ) + Decimal( quotetick )
        limitask = rawask.quantize( Decimal( quotetick ) )
    else:
        rawask = Decimal( marketask )
        limitask = rawask.quantize( Decimal( quotetick ) )

    # Return the best ask and best bid
    # In the orderbook of the trading pair
    # Also, return the most competitive limit orders
    return ( marketask, marketbid, limitask, limitbid )


# Get dYdX markets and define market constants
markets = client.get_markets()
daiquotetick = markets["markets"]["WETH-DAI"]["minimumTickSize"]
daidecimals = markets["markets"]["WETH-DAI"]["quoteCurrency"]["decimals"]
daiassetid = markets["markets"]["WETH-DAI"]["quoteCurrency"]["soloMarketId"]
usdcdecimals = markets["markets"]["WETH-USDC"]["quoteCurrency"]["decimals"]
usdcassetid = markets["markets"]["WETH-USDC"]["quoteCurrency"]["soloMarketId"]


# Get best ask
# Loop until the ask drops below the trigger price
bookprices = bestprices( 'WETH-DAI', daiquotetick )
presentask = bookprices[0]

triggerask = Decimal( presentask ) * Decimal ( pricetrigger )

while Decimal(presentask) > Decimal(triggerask):
    # Sleep ten seconds before checking updating the present price
    time.sleep(10)

    bookprices = bestprices( 'WETH-DAI', daiquotetick )
    presentask = bookprices[0]
    # If the present price is below the trigger price this loop ends


# Get dYdX index price for ETH
# dYdX uses price oracles for DAI and ETH
oracleprice = client.eth.get_oracle_price( daiassetid )
normalprice = Decimal(oracleprice) * Decimal( 10**(daidecimals) )
daiusdprice = Decimal(normalprice)


# Get dYdX account balances
balances = client.eth.get_my_balances()
# Determine overcollateralized collateral (USDC asset balance in DAI terms)
# And DAI balance to determine the maximum amount of DAI borrowable
usdbalance = Decimal( balances[usdcassetid] / (10**usdcdecimals) ) / Decimal(daiusdprice)
daibalance = Decimal( balances[daiassetid] / (10**daidecimals) )


# Determine the total margin, the maximum allowable debt of the dydx account
# And permissable additional debt (all in DAI terms)
totalmargin = Decimal(usdbalance) / Decimal(minimumcollateralization)
maximumdebt = Decimal(totalmargin) * Decimal(maximumleverage)
if daibalance < 0:
    alloweddebt = Decimal(maximumdebt) + Decimal(daibalance)
else:
    alloweddebt = Decimal(maximumdebt)


# Determine most competitive bid price and amount
# Based on the debt remaining and present market values
bookpricing = bestprices( 'WETH-DAI', daiquotetick )
greatestbid = bookpricing[3]
bidquantity = Decimal(alloweddebt) / Decimal(greatestbid)
# Submit the order to BUY ETH
placed_bid = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_BUY,
    amount=utils.token_to_wei(bidquantity, consts.MARKET_WETH),
    price=greatestbid,
    fillOrKill=False,
    postOnly=False
)
# Display order information
jsondata = json.dumps( placed_bid, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )


# Loop until the bid is filled
while True:
    # Give the bid placed five seconds to fill
    time.sleep(5)

    # Get fills
    my_fills = client.get_my_fills(
        market=['WETH-DAI'],
        limit=1
    )
    if my_fills["fills"][0]["orderId"] == placed_bid["order"]["id"]:
        break


# Place ask to close the position opened by the bid
# that returns 100 basis points
askprice = Decimal( greatestbid ) * requiredreturn
quantity = bidquantity
# Create order to SELL ETH
placed_ask = client.place_order(
    market=consts.PAIR_WETH_DAI,
    side=consts.SIDE_SELL,
    amount=utils.token_to_wei(quantity, consts.MARKET_WETH),
    price=askprice.quantize( Decimal(daiquotetick) ),
    fillOrKill=False,
    postOnly=False
)
# Display order information
jsondata = json.dumps( placed_ask, sort_keys=True, indent=4, separators=(',', ': ') )
print ( jsondata )

while True:
    # Check the status of the submitted ask
    submittedask = client.get_order( orderId=placed_ask["order"]["id"] )
    if submittedask["order"]["status"] == "FILLED":
        # Exit: End the loop and exit.
        print ("Order ", submittedask["order"]["id"], " was filled at: ", submittedask["order"]["price"], " DAI/ETH.")
        break
    else:
        # Sleep
        # Then check price
        time.sleep(5)
        bookprices = bestprices( 'WETH-DAI', daiquotetick )
        bookmarket = bookprices[1]
        limitprice = bookprices[2]
        # If the present price is below the trigger price this loop ends
        if Decimal( bookmarket ) < Decimal( greatestbid ) * Decimal( stopmarketask ):
            # Create order to SELL ETH
            placed_ask = client.place_order(
                market=consts.PAIR_WETH_DAI,
                side=consts.SIDE_SELL,
                amount=utils.token_to_wei(quantity, consts.MARKET_WETH),
                price=bookmarket.quantize( Decimal(daiquotetick) ),
                fillOrKill=False,
                postOnly=False
            )
            # Display order information
            jsondata = json.dumps( placed_ask, sort_keys=True, indent=4, separators=(',', ': ') )
            print ( jsondata )
            # Cancel the previously submitted ask then exit the loop.
            print ( "Cancelling order: ", submittedask["order"]["id"] )
            canceledask = client.cancel_order( hash=my_order["order"]["id"] )
            # Display order cancel information
            jsondata = json.dumps( canceledask, sort_keys=True, indent=4, separators=(',', ': ') )
            print ( jsondata )
            # exit loop
            break
        elif Decimal( bookmarket ) < Decimal( greatestbid ) * Decimal( stoplimitask ):
            # Create order to SELL ETH
            placed_ask = client.place_order(
                market=consts.PAIR_WETH_DAI,
                side=consts.SIDE_SELL,
                amount=utils.token_to_wei(quantity, consts.MARKET_WETH),
                price=limitprice.quantize( Decimal(daiquotetick) ),
                fillOrKill=False,
                postOnly=False
            )
            # Display order information
            jsondata = json.dumps( placed_ask, sort_keys=True, indent=4, separators=(',', ': ') )
            print ( jsondata )
            # Cancel the previously submitted ask then exit the loop.
            print ( "Cancelling order: ", submittedask["order"]["id"] )
            canceledask = client.cancel_order( hash=my_order["order"]["id"] )
            # Display order cancel information
            jsondata = json.dumps( canceledask, sort_keys=True, indent=4, separators=(',', ': ') )
            print ( jsondata )
            # exit loop
            break
