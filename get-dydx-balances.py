#!/usr/bin/env python3

from dydx.client import Client
import dydx.constants as consts
import dydx.util as utils

from credentials import client


# get dYdX balances
balances = client.eth.get_my_balances()

print ( balances )
