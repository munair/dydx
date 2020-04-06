#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get latest prices
ethpricing = client.get_orderbook( market='WETH-USDC' )
daipricing = client.get_orderbook( market='DAI-USDC' )

# Get dYdX account balances
balances = client.eth.get_my_balances()

# Disaggregate asset balances
ethbalance = Decimal(balances[0] / (10**18))
usdbalance = Decimal(balances[2] / (10**6))
daibalance = Decimal(balances[3] / (10**18))

# Dollarize balances
ethprice = Decimal( 0.5 * (10**12)) * ( Decimal(ethpricing["bids"][0]["price"]) + Decimal(ethpricing["asks"][0]["price"]) )
daiprice = Decimal( 0.5 * (10**12) ) * ( Decimal(daipricing["bids"][0]["price"]) + Decimal(daipricing["asks"][0]["price"]) )
ethvalue = ethbalance * ethprice
daivalue = daibalance * daiprice

# Display dYdX account balance information
print ( f"                        ETH: {ethvalue:10.4f}" )
print ( f"                       USDC: {usdbalance:10.4f}" )
print ( f"                        DAI: {daivalue:10.4f}" )
print ( f"      TOTAL ACCOUNT BALANCE: {usdbalance + ethvalue + daivalue:10.4f}" )
print ( f" TOTAL ETH-DAI TRADING GAIN: {ethvalue + daivalue:10.4f}" )
