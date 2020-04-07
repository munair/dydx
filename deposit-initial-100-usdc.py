#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Set Allowance [must only be called once EVER (aka the initial deposit)]
tx_hash = client.eth.set_allowance(market=consts.MARKET_USDC)
receipt = client.eth.get_receipt(tx_hash)

depositamount = Decimal("100")

# Deposit USDC
tx_hash = client.eth.deposit(
  market=consts.MARKET_USDC,
  wei=utils.token_to_wei(depositamount, consts.MARKET_USDC)
)
receipt = client.eth.get_receipt(tx_hash)

# Display deposit confirmation
print ( receipt )
