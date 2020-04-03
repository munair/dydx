#!/usr/bin/env python3

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# Withdraw 100 USDC
tx_hash = client.eth.withdraw(
  market=consts.MARKET_USDC,
  wei=utils.token_to_wei(100, consts.MARKET_USDC)
)
receipt = client.eth.get_receipt(tx_hash)

print ( receipt )
