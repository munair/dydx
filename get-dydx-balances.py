#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Get dYdX account balances
balances = client.eth.get_my_balances()

# Disaggregate asset balances
ethbalance = Decimal(balances[0] / (10**18))
usdbalance = Decimal(balances[2] / (10**6))
daibalance = Decimal(balances[3] / (10**18))

# Display dYdX account balance information
print (f'{ethbalance:28.18f} ETH')
print (f'{usdbalance:28.18f} USD')
print (f'{daibalance:28.18f} DAI')
