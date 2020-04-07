#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get DAI-USDC market information
markets = client.get_markets()
asset = markets["markets"]["DAI-USDC"]["baseCurrency"]["currency"]
decimals = markets["markets"]["DAI-USDC"]["baseCurrency"]["decimals"]
assetid = markets["markets"]["DAI-USDC"]["baseCurrency"]["soloMarketId"]

# Get dYdX index price for ETH
rawdata = client.eth.get_oracle_price( assetid )
pricedata = Decimal(rawdata) * Decimal( 10**(decimals) )
indexprice = Decimal(pricedata)

# Format balance using DECIMAL information for the asset
print ( asset, "is" , indexprice.quantize( Decimal("0.0001") ), "dollars." )
