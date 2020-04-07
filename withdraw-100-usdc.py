#!/usr/bin/env python3

from decimal import Decimal

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Specify withdraw amount
withdrawalamount = Decimal("100")

# Withdraw USDC
tx_hash = client.eth.withdraw(
  market=consts.MARKET_USDC,
  wei=utils.token_to_wei(withdrawalamount, consts.MARKET_USDC)
)
receipt = client.eth.get_receipt(tx_hash)

print ( receipt )
