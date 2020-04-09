#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get dYdX account collateralization
collateralization = client.eth.get_my_collateralization()

# Get latest index prices from oracles
ethpricing = client.eth.get_oracle_price( 0 )
daipricing = client.eth.get_oracle_price( 3 )

# Get dYdX account balances
balances = client.eth.get_my_balances()

# Disaggregate asset balances
ethbalance = Decimal(balances[0] / (10**18))
usdbalance = Decimal(balances[2] / (10**6))
daibalance = Decimal(balances[3] / (10**18))

# Dollarize balances
ethprice = Decimal( 10**18 ) * Decimal( ethpricing )
daiprice = Decimal( 10**18 ) * Decimal( daipricing )
ethvalue = ethbalance * ethprice
daivalue = daibalance * daiprice

# Display dYdX account balance information
print ( f"                        ETH: {ethvalue:10.4f}" )
print ( f"                       USDC: {usdbalance:10.4f}" )
print ( f"                        DAI: {daivalue:10.4f}" )
print ( f"      TOTAL ACCOUNT BALANCE: {usdbalance + ethvalue + daivalue:10.4f}" )
print ( f" TOTAL ETH-DAI TRADING GAIN: {ethvalue + daivalue:10.4f}" )
print ( f"                 TOTAL DEBT: {(usdbalance + ethvalue + daivalue) / Decimal(collateralization):10.4f}" )
print ( f"  ACCOUNT COLLATERALIZATION: {Decimal(collateralization) * 100:10.4f}%" )
