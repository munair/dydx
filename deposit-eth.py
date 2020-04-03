#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Set Allowance
#
# Is not required for WETH

depositamount = Decimal("0.0001")

# Deposit ETH
tx_hash = client.eth.deposit(
  market=consts.MARKET_WETH,
  wei=utils.token_to_wei(depositamount, consts.MARKET_WETH)
)
receipt = client.eth.get_receipt(tx_hash)

# Display deposit confirmation
print ( receipt )
