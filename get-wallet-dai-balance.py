#!/usr/bin/env python3

import json
from decimal import *

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get WETH-DAI market information
markets = client.get_markets()
decimals = markets["markets"]["DAI-USDC"]["baseCurrency"]["decimals"]

# Get Wallet balances
walletbalance = client.eth.get_my_wallet_balance(consts.MARKET_DAI)

# Format balance using DECIMAL information for the asset
balance = Decimal(walletbalance) / Decimal(10**(decimals))

print ( balance )
